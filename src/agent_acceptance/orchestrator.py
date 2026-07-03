"""Run the behavioral + memory-governance legs and merge into one report.

Behavioral leg shells out to the `agent-handoff` CLI (a separate installed
package) so we reuse its frozen-scenario replay verbatim instead of forking it.
Memory leg imports `verified_memory_gate` in-process and calls its public
GateMem harness. Both legs degrade independently: if agent-handoff is missing
or GateMem data is absent, that leg records `ran=False` with a reason instead
of crashing the whole run."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from .models import BehavioralBlock, CombinedReport, MemoryBlock


def _behavioral_summary(scenarios: list[dict[str, Any]]) -> str:
    if not scenarios:
        return ""
    passed = sum(1 for s in scenarios if s.get("passed"))
    return f"{passed}/{len(scenarios)} scenarios passed"


def run_behavioral(scenarios_path: Path) -> BehavioralBlock:
    """Replay golden scenarios via agent-handoff and load its JSON.

    Prefers the `agent-handoff` console script; falls back to
    `python -m agent_handoff.cli` so this works whenever agent_handoff is
    importable even if its entry point isn't on PATH (e.g. an editable
    install in a venv that isn't activated)."""
    py = sys.executable
    cmd: list[str] | None = None
    if shutil.which("agent-handoff"):
        cmd = ["agent-handoff", "run", str(scenarios_path)]
    elif importlib.util.find_spec("agent_handoff") is not None:
        cmd = [py, "-m", "agent_handoff.cli", "run", str(scenarios_path)]
    if cmd is None:
        return BehavioralBlock(
            ran=False, project="", verdict="",
            error="agent-handoff not found (no CLI on PATH and not importable); pip install -e ../agent-handoff",
        )
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "behavioral.results.json"
        proc = subprocess.run(
            cmd + ["-o", str(out)], capture_output=True, text=True, timeout=120,
        )
        if proc.returncode not in (0, 1):
            return BehavioralBlock(
                ran=False, project="", verdict="",
                error=f"agent-handoff run exited {proc.returncode}: {proc.stderr[:200]}",
            )
        if not out.exists():
            return BehavioralBlock(
                ran=False, project="", verdict="",
                error=f"agent-handoff run produced no results JSON: {proc.stderr[:200]}",
            )
        data = json.loads(out.read_text())
    return BehavioralBlock(
        ran=True,
        project=data.get("project", ""),
        verdict=data.get("verdict", "FAIL"),
        scenarios=data.get("scenarios", []),
    )


def run_memory(
    domain: str,
    *,
    data_dir: str | None = None,
    download: bool = False,
    max_episodes: int = 1,
) -> MemoryBlock:
    """Run the GateMem-aligned MGS eval via verified_memory_gate.

    Returns ran=False (not a crash) when the public episode data is not
    available locally and download=False — the common case in CI and on a
    fresh checkout. The caller treats 'not assessed' honestly."""
    try:
        from verified_memory_gate.gatemem_public import load_and_run_public_harness
        from verified_memory_gate.gatemem_loader import GateMemDomain
    except Exception as exc:  # pragma: no cover - dependency missing
        return MemoryBlock(ran=False, error=f"verified-memory-gate not importable: {exc}")

    # GateMemDomain is a typing.Literal alias, not an enum; validate the string
    # against its allowed values and pass the string straight through.
    import typing
    allowed = set(typing.get_args(GateMemDomain))
    if domain not in allowed:
        return MemoryBlock(
            ran=False,
            error=f"unknown GateMem domain: {domain} (choose from {sorted(allowed)})",
        )

    try:
        report = load_and_run_public_harness(
            domain, data_dir=data_dir, download=download, max_episodes=max_episodes,
        )
    except Exception as exc:
        return MemoryBlock(
            ran=False,
            error=f"GateMem data unavailable (set download=True or point --memory-data-dir at the bench tree): {exc}",
        )

    score = getattr(report, "score", None)
    n = len(getattr(report, "checkpoints", []) or [])
    if score is None:
        return MemoryBlock(ran=False, error="harness returned no score")
    raw = score.as_dict() if hasattr(score, "as_dict") else dict(score)
    return MemoryBlock(
        ran=True,
        mgs=_as_float(raw.get("mgs")),
        utility=_as_float(raw.get("utility")),
        access_control=_as_float(raw.get("access_control")),
        active_forgetting=_as_float(raw.get("active_forgetting")),
        n_checkpoints=n,
    )


def _as_float(v: Any) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def build_report(
    scenarios_path: Path,
    *,
    project: str | None = None,
    memory_domain: str | None = None,
    memory_data_dir: str | None = None,
    memory_download: bool = False,
    max_episodes: int = 1,
    memory_threshold: float = 0.5,
) -> CombinedReport:
    behavioral = run_behavioral(scenarios_path)
    proj = project or behavioral.project or scenarios_path.stem
    if memory_domain:
        memory = run_memory(
            memory_domain, data_dir=memory_data_dir,
            download=memory_download, max_episodes=max_episodes,
        )
    else:
        memory = MemoryBlock(ran=False, error="memory governance not requested (pass --memory-domain)")
    return CombinedReport(
        project=proj, behavioral=behavioral, memory=memory, memory_threshold=memory_threshold,
    )
