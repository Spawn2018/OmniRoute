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


def test_normalize_inquiry_default_n_accepts_range() -> None:
    assert normalize_setting_key(" Inquiry_Default_N ") == "inquiry_default_n"
    assert normalize_setting_value("inquiry_default_n", " 3 ") == "3"


def test_normalize_inquiry_default_n_rejects_zero() -> None:
    with pytest.raises(InvalidOrganizationSetting, match="1–20"):
        normalize_setting_value("inquiry_default_n", "0")


def test_normalize_lane_window_accepts_range() -> None:
    assert normalize_setting_key(" Lane_Scorecard_Window_Days ") == "lane_scorecard_window_days"
    assert normalize_setting_value("lane_scorecard_window_days", " 90 ") == "90"


def test_normalize_lane_window_rejects_zero() -> None:
    with pytest.raises(InvalidOrganizationSetting, match="1–365"):
        normalize_setting_value("lane_scorecard_window_days", "0")


def test_normalize_fx_rate_keys() -> None:
    assert normalize_setting_key(" Fx_Rate_Basis ") == "fx_rate_basis"
    assert normalize_setting_value("fx_rate_basis", " ETD ") == "etd"
    assert normalize_setting_value("fx_rate_offset_days", " -1 ") == "-1"
    assert normalize_setting_value("fx_rate_table", " NBP_A ") == "nbp_a"


def test_normalize_fx_rate_rejects_unknown() -> None:
    with pytest.raises(InvalidOrganizationSetting, match="kurs"):
        normalize_setting_value("fx_rate_basis", "margin")
    with pytest.raises(InvalidOrganizationSetting, match="dni"):
        normalize_setting_value("fx_rate_offset_days", "2")
    with pytest.raises(InvalidOrganizationSetting, match="kurs"):
        normalize_setting_value("fx_rate_table", "nbp_c")
