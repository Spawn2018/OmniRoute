from app.domain.errors import InvalidMoney, InvalidOrganizationSetting
from app.domain.money import Currency

ALLOWED_SETTING_KEYS = frozenset(
    {
        "default_currency",
        "quotation_number_prefix",
        "quotation_print_template",
        "inquiry_default_n",
        "lane_scorecard_window_days",
        "fx_rate_basis",
        "fx_rate_offset_days",
        "fx_rate_table",
    },
)
ALLOWED_PRINT_TEMPLATES = frozenset({"plain", "letter"})
_FX_BASIS = frozenset({"etd", "loading_date", "unloading_date", "invoice_date"})
_FX_OFFSET = frozenset({"0", "-1"})
_FX_TABLE = frozenset({"nbp_a", "nbp_b"})
_PREFIX_CHARS = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-")
_SECRET_MARKERS = ("secret", "password", "token", "api_key")


def normalize_setting_key(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidOrganizationSetting("klucz ustawienia musi być tekstem")
    token = raw.strip().lower()
    if token == "":
        raise InvalidOrganizationSetting("klucz ustawienia jest obowiązkowy")
    if any(marker in token for marker in _SECRET_MARKERS):
        raise InvalidOrganizationSetting("sekret tenanta nie wchodzi do organization_setting")
    if token not in ALLOWED_SETTING_KEYS:
        raise InvalidOrganizationSetting("klucz poza allowlistą")
    return token


def normalize_quotation_number_prefix(raw: str) -> str:
    token = raw.strip().upper()
    if not (1 <= len(token) <= 16) or any(char not in _PREFIX_CHARS for char in token):
        raise InvalidOrganizationSetting("prefiks numeru: 1–16 znaków A–Z 0–9 . _ -")
    return token


def normalize_quotation_print_template(raw: str) -> str:
    token = raw.strip().lower()
    if token not in ALLOWED_PRINT_TEMPLATES:
        raise InvalidOrganizationSetting("szablon oferty: plain albo letter")
    return token


def normalize_default_currency(raw: str) -> str:
    try:
        return Currency(raw.strip().upper()).code
    except InvalidMoney as exc:
        raise InvalidOrganizationSetting("waluta ISO 4217 — CHAR(3)") from exc


def normalize_inquiry_default_n(raw: str) -> str:
    token = raw.strip()
    if not token.isdigit():
        raise InvalidOrganizationSetting("inquiry_default_n: liczba 1–20")
    value = int(token)
    if value < 1 or value > 20:
        raise InvalidOrganizationSetting("inquiry_default_n: liczba 1–20")
    return token


def normalize_lane_scorecard_window_days(raw: str) -> str:
    token = raw.strip()
    if not token.isdigit():
        raise InvalidOrganizationSetting("lane_scorecard_window_days: liczba 1–365")
    value = int(token)
    if value < 1 or value > 365:
        raise InvalidOrganizationSetting("lane_scorecard_window_days: liczba 1–365")
    return token


def normalize_fx_rate_basis(raw: str) -> str:
    token = raw.strip().lower()
    if token not in _FX_BASIS:
        raise InvalidOrganizationSetting("kurs: data spoza zbioru")
    return token


def normalize_fx_rate_offset_days(raw: str) -> str:
    token = raw.strip()
    if token not in _FX_OFFSET:
        raise InvalidOrganizationSetting("dni: tylko 0 albo -1")
    return token


def normalize_fx_rate_table(raw: str) -> str:
    token = raw.strip().lower()
    if token not in _FX_TABLE:
        raise InvalidOrganizationSetting("kurs: tabela spoza zbioru")
    return token


_VALUE_PARSERS = {
    "default_currency": normalize_default_currency,
    "quotation_number_prefix": normalize_quotation_number_prefix,
    "quotation_print_template": normalize_quotation_print_template,
    "inquiry_default_n": normalize_inquiry_default_n,
    "lane_scorecard_window_days": normalize_lane_scorecard_window_days,
    "fx_rate_basis": normalize_fx_rate_basis,
    "fx_rate_offset_days": normalize_fx_rate_offset_days,
    "fx_rate_table": normalize_fx_rate_table,
}


def normalize_setting_value(setting_key: str, raw: object) -> str:
    if type(raw) is not str:
        raise InvalidOrganizationSetting("wartość ustawienia musi być tekstem")
    parser = _VALUE_PARSERS.get(setting_key)
    if parser is None:
        raise InvalidOrganizationSetting("klucz poza allowlistą")
    return parser(raw)
