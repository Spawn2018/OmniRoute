from app.domain.errors import InvalidMoney, InvalidOrganizationSetting
from app.domain.money import Currency

ALLOWED_SETTING_KEYS = frozenset({"default_currency"})
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


def normalize_setting_value(setting_key: str, raw: object) -> str:
    if type(raw) is not str:
        raise InvalidOrganizationSetting("wartość ustawienia musi być tekstem")
    if setting_key == "default_currency":
        try:
            return Currency(raw.strip().upper()).code
        except InvalidMoney as exc:
            raise InvalidOrganizationSetting("waluta ISO 4217 — CHAR(3)") from exc
    raise InvalidOrganizationSetting("klucz poza allowlistą")
