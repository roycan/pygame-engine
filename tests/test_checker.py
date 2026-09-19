"""T4.3 gate: check_my_class.py -- friendly diagnostics, no tracebacks."""

import sys
from pathlib import Path

from check_my_class import format_findings, inspect_classes

FIXTURES_DIR = Path(__file__).parent / "fixtures"
sys.path.insert(0, str(FIXTURES_DIR))


def test_good_file_passes():
    findings = inspect_classes("checker_good")
    assert findings, "a healthy file should still earn [PASS] lines"
    assert all(f.level != "FAIL" for f in findings)
    assert any(f.level == "PASS" for f in findings)


def test_missing_act_is_a_fail_with_hint():
    findings = inspect_classes("checker_no_act")
    fails = [f for f in findings if f.level == "FAIL"]
    assert fails
    assert any("act()" in f.title for f in fails)
    assert any("WaitAction" in (f.detail or "") for f in fails)


def test_none_return_is_a_warn_with_fix():
    findings = inspect_classes("checker_returns_none")
    warns = [f for f in findings if f.level == "WARN"]
    assert warns
    assert any("instead of an Action" in w.title for w in warns)


def test_syntax_error_becomes_single_friendly_fail():
    findings = inspect_classes("checker_syntax_error")
    assert len(findings) == 1
    assert findings[0].level == "FAIL"
    assert "syntax" in findings[0].title.lower()
    # The whole point: humanized output, never a raw traceback.
    rendered = format_findings(findings)
    assert "Traceback" not in rendered


def test_format_findings_uses_the_three_icons():
    findings = (
        inspect_classes("checker_good")
        + inspect_classes("checker_returns_none")
        + inspect_classes("checker_no_act")
    )
    rendered = format_findings(findings)
    assert "[PASS]" in rendered
    assert "[WARN]" in rendered
    assert "[FAIL]" in rendered
    assert "Summary:" in rendered


def test_unimportable_module_is_a_fail():
    findings = inspect_classes("definitely_not_a_real_module_xyz")
    assert findings[0].level == "FAIL"
