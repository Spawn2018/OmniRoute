from pathlib import Path

from app.domain.errors import InvalidOrganizationSetting
from app.domain.organization_setting import (
    normalize_fx_rate_basis,
    optional_fx_token,
)

_ROOT = Path(__file__).resolve().parents[3]


def test_migration_490_adds_charge_fx_columns() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "490_charge_fx_rate.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "490_charge_fx_rate"' in source
    assert 'down_revision: str | None = "489_shipment_tree_margin"' in source
    assert "fx_rate_basis" in source
    assert "fx_rate_offset_days" in source
    assert "fx_rate_table" in source
    assert "create_table" not in source
    assert "httpx" not in source


def test_charge_service_does_not_import_nbp_or_settings_service() -> None:
    source = (
        _ROOT / "backend" / "app" / "services" / "charges" / "charge_service.py"
    ).read_text(encoding="utf-8")
    assert "app.services.nbp_rates" not in source
    assert "app.services.organization_settings" not in source
    assert "optional_fx_token" in source


def test_optional_fx_token_blank_is_none() -> None:
    assert optional_fx_token(None, normalize_fx_rate_basis) is None
    assert optional_fx_token("  ", normalize_fx_rate_basis) is None
    assert optional_fx_token("etd", normalize_fx_rate_basis) == "etd"


def test_optional_fx_token_rejects_unknown_basis() -> None:
    try:
        optional_fx_token("tomorrow", normalize_fx_rate_basis)
    except InvalidOrganizationSetting as exc:
        assert "kurs" in str(exc)
    else:
        raise AssertionError("expected InvalidOrganizationSetting")
