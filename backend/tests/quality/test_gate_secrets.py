from pathlib import Path

_GATE = Path(".github/workflows/gate.yml")


def test_gate_workflow_reads_jwt_secret_from_github_secrets() -> None:
    text = _GATE.read_text(encoding="utf-8")
    assert "secrets.JWT_SECRET" in text
    assert "ci-gate-jwt-secret" not in text
    assert "change-me-local-only" not in text
