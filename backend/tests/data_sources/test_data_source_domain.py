import pytest

from app.domain.data_source import parse_data_source_row
from app.domain.errors import InvalidDataSource


def test_parse_data_source_row_accepts_manual() -> None:
    code, license_label, rights, origin = parse_data_source_row(
        "ds_openmeteo_01",
        "CC-BY-4.0",
        "weather read-only",
        "tenant:manual",
    )
    assert (code, license_label, rights, origin) == (
        "ds_openmeteo_01",
        "CC-BY-4.0",
        "weather read-only",
        "tenant:manual",
    )


def test_parse_data_source_row_rejects_short_license() -> None:
    with pytest.raises(InvalidDataSource, match="licencja"):
        parse_data_source_row(
            "ds_openmeteo_01",
            "x",
            "weather read-only",
            "tenant:manual",
        )
