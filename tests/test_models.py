from __future__ import annotations

from agent_acceptance.models import BehavioralBlock, CombinedReport, MemoryBlock, OverallVerdict


def _rep(beh_passed: bool, mem=None) -> CombinedReport:
    return CombinedReport(
        project="p",
        behavioral=BehavioralBlock(ran=True, project="p", verdict="PASS" if beh_passed else "FAIL"),
        memory=mem or MemoryBlock(ran=False, error="not requested"),
    )


def test_pass_requires_both_gates():
    both = _rep(True, MemoryBlock(ran=True, mgs=0.9, utility=0.95, access_control=0.0, active_forgetting=0.0))
    assert both.verdict is OverallVerdict.PASS


def test_behavioral_fail_overrides_memory():
    fail = _rep(False, MemoryBlock(ran=True, mgs=0.9))
    assert fail.verdict is OverallVerdict.FAIL


def test_memory_below_threshold_fails():
    low = _rep(True, MemoryBlock(ran=True, mgs=0.2))
    assert low.verdict is OverallVerdict.FAIL


def test_memory_not_run_is_behavioral_only():
    cond = _rep(True, MemoryBlock(ran=False, error="not requested"))
    assert cond.verdict is OverallVerdict.BEHAVIORAL_ONLY


def test_as_dict_roundtrip_shape():
    r = _rep(True, MemoryBlock(ran=True, mgs=0.8, n_checkpoints=4))
    d = r.as_dict()
    assert d["verdict"] == "PASS"
    assert d["memory"]["mgs"] == 0.8
    assert d["behavioral"]["verdict"] == "PASS"
