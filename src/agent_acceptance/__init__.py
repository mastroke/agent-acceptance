"""agent-acceptance: one acceptance report for agentic AI.

Combines two shipped portfolio products into a single sign-off artifact an AI
agency hands to a client at delivery, proving the agent is BOTH behaviorally
correct across layers AND memory-governed:

  - behavioral: agent-handoff's cross-layer (prompt/tool/memory/retrieval)
    golden-scenario replay -> a PASS/FAIL verdict.
  - memory governance: verified-memory-gate's GateMem-aligned MGS eval
    (MGS = U * (1 - A) * (1 - F); utility / access-control / active-forgetting).

The combined verdict is the AND of the two. Memory is optional: when the
GateMem episode data is not present locally the report records "not assessed"
and the verdict falls back to behavioral-only, so the CLI always works.
"""

from __future__ import annotations

from .models import CombinedReport, OverallVerdict

__all__ = ["CombinedReport", "OverallVerdict", "__version__"]
__version__ = "0.1.0"
