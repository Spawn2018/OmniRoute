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


def test_normalize_setting_key_accepts_prefix_and_template() -> None:
    assert normalize_setting_key("Quotation_Number_Prefix") == "quotation_number_prefix"
    assert normalize_setting_key("quotation_print_template") == "quotation_print_template"


def test_normalize_prefix_and_template_values() -> None:
    assert normalize_setting_value("quotation_number_prefix", " or-q. ") == "OR-Q."
    assert normalize_setting_value("quotation_print_template", " Letter ") == "letter"


def test_normalize_prefix_rejects_spaces_and_long_token() -> None:
    with pytest.raises(InvalidOrganizationSetting, match="prefiks"):
        normalize_setting_value("quotation_number_prefix", "OR Q")
    with pytest.raises(InvalidOrganizationSetting, match="prefiks"):
        normalize_setting_value("quotation_number_prefix", "A" * 17)


def test_normalize_template_rejects_unknown_token() -> None:
    with pytest.raises(InvalidOrganizationSetting, match="szablon"):
        normalize_setting_value("quotation_print_template", "fancy")
