from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "069_cargo_claim_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_069_creates_cargo_claim_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "069_cargo_claim_rls"' in source
    assert 'down_revision: str | None = "068_shipment_leg_ocean_lcl_kind"' in source
    assert '"cargo_claim"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "cargo_claim_tenant_isolation" in source
    assert "fk_cargo_claim_shipment" in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_cargo_claim_service_does_not_import_parents() -> None:
    service = (_SERVICES / "cargo_claims" / "cargo_claim_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.shipments" not in service
    assert "app.services.quotations" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service
    assert "timedelta" not in service


def test_importlinter_lists_cargo_claims_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.cargo_claims" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.cargo_claims" in forbidden
    assert "app.models.cargo_claim" in forbidden


def test_migration_131_adds_cmr_clocks_without_timedelta() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "131_cargo_claim_cmr.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "131_cargo_claim_cmr"' in source
    assert 'down_revision: str | None = "130_carbon_method"' in source
    assert "damage_code" in source
    assert "notice_due_at" in source
    assert "suit_due_at" in source
    assert "cmr_notice_window" in source
    assert "timedelta" not in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source


def test_migration_517_adds_evidence_bools_without_gps() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "517_cargo_claim_evidence.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "517_cargo_claim_evidence"' in source
    assert 'down_revision: str | None = "516_dg_limited_quantity"' in source
    assert "evidence_gps" in source
    assert "evidence_temp" in source
    assert "evidence_photo" in source
    assert "timedelta" not in source
    assert "lat" not in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source


def test_generated_api_types_include_cargo_claim() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "CargoClaimResponse" in source
    assert "CargoClaimCreate" in source
    assert "damage_code" in source
    assert "notice_due_at" in source
    assert "evidence_gps" in source
    assert "evidence_temp" in source
    assert "evidence_photo" in source
