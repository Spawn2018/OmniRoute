from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_THREAT = _ROOT / "docs" / "ops" / "threat-model-tenant-hitl.md"
_CODEQL = _ROOT / ".github" / "workflows" / "codeql.yml"
_GATE = _ROOT / ".github" / "workflows" / "gate.yml"
_JUSTFILE = _ROOT / "justfile"


def test_threat_model_covers_tenant_rls_and_hitl_accept() -> None:
    text = _THREAT.read_text(encoding="utf-8")
    assert "organization_id" in text
    assert "RLS" in text
    assert "HITL" in text or "human" in text.casefold()
    assert "ExtractionService" in text or "extract" in text.casefold()
    assert "rate_line" in text


def test_codeql_workflow_scans_python_and_javascript_outside_gate() -> None:
    workflow = _CODEQL.read_text(encoding="utf-8")
    assert "python" in workflow
    assert "javascript-typescript" in workflow
    gate = _GATE.read_text(encoding="utf-8")
    assert "codeql" not in gate.casefold()
    justfile = _JUSTFILE.read_text(encoding="utf-8")
    assert "codeql" not in justfile.casefold()
