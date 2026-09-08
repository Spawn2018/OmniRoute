from app.domain.errors import InvalidMoney, InvalidOrganizationSetting
from app.domain.money import Currency

ALLOWED_SETTING_KEYS = frozenset(
    {
        "default_currency",
        "quotation_number_prefix",
        "quotation_print_template",
        "inquiry_default_n",
    },
)
ALLOWED_PRINT_TEMPLATES = frozenset({"plain", "letter"})
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


def normalize_setting_value(setting_key: str, raw: object) -> str:
    if type(raw) is not str:
        raise InvalidOrganizationSetting("wartość ustawienia musi być tekstem")
    if setting_key == "default_currency":
        try:
            return Currency(raw.strip().upper()).code
        except InvalidMoney as exc:
            raise InvalidOrganizationSetting("waluta ISO 4217 — CHAR(3)") from exc
    if setting_key == "quotation_number_prefix":
        return normalize_quotation_number_prefix(raw)
    if setting_key == "quotation_print_template":
        return normalize_quotation_print_template(raw)
    if setting_key == "inquiry_default_n":
        return normalize_inquiry_default_n(raw)
    raise InvalidOrganizationSetting("klucz poza allowlistą")


def normalize_inquiry_default_n(raw: str) -> str:
    token = raw.strip()
    if not token.isdigit():
        raise InvalidOrganizationSetting("inquiry_default_n: liczba 1–20")
    value = int(token)
    if value < 1 or value > 20:
        raise InvalidOrganizationSetting("inquiry_default_n: liczba 1–20")
    return token
