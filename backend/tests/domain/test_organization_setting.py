import pytest

from app.domain.errors import InvalidOrganizationSetting
from app.domain.organization_setting import normalize_setting_key, normalize_setting_value


def test_normalize_setting_key_accepts_default_currency() -> None:
    assert normalize_setting_key(" Default_Currency ") == "default_currency"


def test_normalize_setting_key_rejects_secret() -> None:
    with pytest.raises(InvalidOrganizationSetting, match="sekret"):
        normalize_setting_key("openai_api_key")


def test_normalize_setting_value_uppercases_currency() -> None:
    assert normalize_setting_value("default_currency", "eur") == "EUR"
