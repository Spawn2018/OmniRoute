from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]


def test_migration_468_creates_resource_document() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "468_resource_document.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "468_resource_document"' in source
    assert 'down_revision: str | None = "467_resource_capacity_m3"' in source
    assert "resource_document" in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "resource_document_tenant_isolation" in source
    assert "fk_resource_document_resource" in source
    assert "party_document" not in source
    assert "drop_table" in source.split("def downgrade")[1]
