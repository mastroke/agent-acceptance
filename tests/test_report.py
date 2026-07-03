from __future__ import annotations

from agent_acceptance.models import BehavioralBlock, CombinedReport, MemoryBlock
from agent_acceptance.report import render_report


def test_render_pass_includes_both_sections():
    r = CombinedReport(
        project="demo",
        behavioral=BehavioralBlock(
            ran=True, project="demo", verdict="PASS",
            scenarios=[{"name": "tool-schema-drift", "passed": True}],
        ),
        memory=MemoryBlock(ran=True, mgs=0.91, utility=0.95, access_control=0.02, active_forgetting=0.0, n_checkpoints=6),
    )
    md = render_report(r)
    assert "ACCEPTED" in md
    assert "tool-schema-drift" in md
    assert "0.910" in md
    assert "GateMem" in md


def test_render_behavioral_only_marked_conditional():
    r = CombinedReport(
        project="demo",
        behavioral=BehavioralBlock(ran=True, project="demo", verdict="PASS", scenarios=[{"name": "x", "passed": True}]),
        memory=MemoryBlock(ran=False, error="not requested"),
    )
    md = render_report(r)
    assert "CONDITIONAL" in md
    assert "Not assessed" in md


def test_render_behavioral_not_run():
    r = CombinedReport(
        project="demo",
        behavioral=BehavioralBlock(ran=False, project="", verdict="", error="agent-handoff CLI not found"),
        memory=MemoryBlock(ran=False, error="not requested"),
    )
    md = render_report(r)
    assert "Not run" in md
    assert "agent-handoff CLI not found" in md
