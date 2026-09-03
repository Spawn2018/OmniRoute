from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "016_quotation_port_party.py"


def test_migration_016_adds_pol_pod_party_fks_check_and_downgrade() -> None:
    assert _MIGRATION.is_file()
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "016_quotation_port_party"' in source
    assert 'down_revision: str | None = "015_party_rls"' in source
    assert "origin_port_id" in source
    assert "destination_port_id" in source
    assert "party_id" in source
    assert "fk_quotation_origin_port" in source
    assert "fk_quotation_destination_port" in source
    assert "fk_quotation_party" in source
    assert "ck_quotation_lane_party_complete" in source
    assert "ix_quotation_org_party_id" in source
    assert "ix_quotation_org_origin_port_id" in source
    assert "ix_quotation_org_destination_port_id" in source
    assert "def downgrade" in source
    downgrade = source.split("def downgrade")[1]
    assert "origin_port_id" in downgrade
    assert "ck_quotation_lane_party_complete" in downgrade


_NEGOTIATED = _ROOT / "backend" / "alembic" / "versions" / "044_quotation_negotiated_channel.py"


def test_migration_044_adds_negotiated_channel_pointer() -> None:
    assert _NEGOTIATED.is_file()
    source = _NEGOTIATED.read_text(encoding="utf-8")
    assert 'revision: str = "044_quotation_negotiated_channel"' in source
    assert 'down_revision: str | None = "043_carrier_inquiry_rls"' in source
    assert "negotiated_channel_quote_id" in source
    assert "ix_quotation_org_negotiated_channel" in source
    assert "Numeric" not in source
    assert "amount" not in source
    assert "def downgrade" in source
    downgrade = source.split("def downgrade")[1]
    assert "negotiated_channel_quote_id" in downgrade


def test_generated_api_types_include_quotation_lane_party() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "origin_port_id" in source
    assert "destination_port_id" in source
    assert "QuotationCreate" in source or "QuotationResponse" in source


def test_generated_api_types_include_negotiated_channel() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "negotiated_channel_quote_id" in source
    assert "QuotationNegotiate" in source
