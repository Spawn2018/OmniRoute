from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_ARCHITECTURE = _ROOT / "docs" / "ARCHITECTURE.md"
_KONTRAHENT = _ROOT / "docs" / "operator" / "kontrahent.md"
_KATALOGI = _ROOT / "docs" / "operator" / "katalogi.md"


def test_kontrahent_howto_says_lookup_does_not_write_party() -> None:
    text = _KONTRAHENT.read_text(encoding="utf-8")
    assert "nie zapisuje" in text
    assert "tax_id" in text or "NIP" in text
    assert "party" in text


def test_catalog_howto_is_not_seventy_stubs() -> None:
    text = _KATALOGI.read_text(encoding="utf-8")
    assert "zapisują" in text or "INSERT" in text
    assert "70" in text
    assert "source_ref" in text
    assert len(text.splitlines()) <= 40


def test_architecture_has_c4_context_and_container() -> None:
    text = _ARCHITECTURE.read_text(encoding="utf-8")
    assert "```mermaid" in text
    assert "C4Context" in text
    assert "C4Container" in text
    assert "Operator" in text
    assert "FastAPI" in text
