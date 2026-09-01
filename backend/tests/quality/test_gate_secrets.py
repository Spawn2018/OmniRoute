import re
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_GATE = _ROOT / ".github" / "workflows" / "gate.yml"
_USES = re.compile(r"uses:\s+(\S+)")
_SHA = re.compile(r"^[0-9a-f]{40}$")


def test_gate_workflow_reads_jwt_secret_from_github_secrets() -> None:
    text = _GATE.read_text(encoding="utf-8")
    assert "secrets.JWT_SECRET" in text
    assert "ci-gate-jwt-secret" not in text
    assert "change-me-local-only" not in text


def test_github_actions_are_sha_pinned() -> None:
    workflows = (_ROOT / ".github" / "workflows").glob("*.yml")
    pinned = 0
    for path in workflows:
        for match in _USES.finditer(path.read_text(encoding="utf-8")):
            ref = match.group(1)
            if ref.startswith("./"):
                continue
            assert "@" in ref, f"{path}: {ref}"
            digest = ref.rsplit("@", 1)[1]
            assert _SHA.fullmatch(digest), f"{path}: unpinned {ref}"
            pinned += 1
    assert pinned >= 6


def test_just_audit_is_not_echo_stub() -> None:
    justfile = (_ROOT / "justfile").read_text(encoding="utf-8")
    assert "python -m pip_audit" in justfile
    assert "--skip-editable" in justfile
    assert '@echo "audit: stub, nie DoD (pip-audit)"' not in justfile
    assert "just audit" in _GATE.read_text(encoding="utf-8")

