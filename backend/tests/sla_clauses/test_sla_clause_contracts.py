from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "225_sla_clause.py"
_SERVICE = (
    _ROOT / "backend" / "app" / "services" / "sla_clauses" / "sla_clause_service.py"
)
_API = _ROOT / "backend" / "app" / "api" / "sla_clauses.py"
_BANNED = (
    "httpx",
    "float(",
    "shipment_id",
    "penalty_ciphertext",
    "app.services.charges",
    "app.services.customer_contracts",
    "app.services.extraction",
)


def test_migration_225_creates_sla_clause_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "225_sla_clause"' in source
    assert 'down_revision: str | None = "224_visibility_connector_vendors"' in source
    assert '"sla_clause"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "sla_clause_tenant_isolation" in source
    assert "uq_sla_clause_org_source_ref" in source
    assert "fk_sla_clause_customer_contract" in source
    for banned in ("shipment_id", "penalty_ciphertext", "httpx", "float(", "currency"):
        assert banned not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_sla_clause_service_is_catalog_and_isolated() -> None:
    source = _SERVICE.read_text(encoding="utf-8")
    for banned in _BANNED:
        assert banned not in source
    assert "UPDATE" not in source
    assert "DELETE" not in source


def test_importlinter_lists_sla_clause_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.sla_clauses" in forbidden
    assert "app.models.sla_clause" in forbidden


def test_create_schema_forbids_penalty_and_amount_fields() -> None:
    source = _API.read_text(encoding="utf-8")
    assert "extra=\"forbid\"" in source or "extra='forbid'" in source
    assert "penalty_ciphertext" not in source
    assert "amount" not in source
    assert "obligation_ciphertext" not in source


def test_generated_api_types_include_sla_clause() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "SlaClauseResponse" in source
    assert "SlaClauseCreate" in source


def test_extraction_service_does_not_import_sla_clause() -> None:
    extraction = _ROOT / "backend" / "app" / "services" / "extraction"
    for path in extraction.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert "sla_clause" not in source
