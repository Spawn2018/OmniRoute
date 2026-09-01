from decimal import Decimal

from app.domain.errors import InvalidMoney, InvalidPartyData
from app.domain.money import Money

ALLOWED_ROLES: tuple[str, ...] = (
    "customer",
    "vendor",
    "agent",
    "carrier",
    "shipper",
    "consignee",
    "notify",
)
_NIP_WEIGHTS = (6, 5, 7, 2, 3, 4, 5, 6, 7)
_MANUAL_SOURCE = "tenant:manual"


def normalize_country_code(raw: str) -> str:
    if type(raw) is not str:
        raise InvalidPartyData("country_code musi być tekstem")
    code = raw.strip().upper()
    if len(code) != 2 or not code.isalpha():
        raise InvalidPartyData("country_code: ISO 3166-1 alpha-2")
    return code


def normalize_legal_name(raw: str) -> str:
    if type(raw) is not str:
        raise InvalidPartyData("legal_name musi być tekstem")
    label = " ".join(raw.split())
    if label == "":
        raise InvalidPartyData("legal_name jest wymagane")
    return label


def normalize_tax_id(country_code: str, tax_id: str) -> str:
    country = normalize_country_code(country_code)
    if type(tax_id) is not str:
        raise InvalidPartyData("tax_id musi być tekstem")
    if country == "PL":
        return _normalize_nip(tax_id)
    token = "".join(tax_id.split()).upper()
    if token == "":
        raise InvalidPartyData("tax_id nie może być puste")
    return token


def _normalize_nip(raw: str) -> str:
    digits = "".join(ch for ch in raw if ch.isdigit())
    if len(digits) != 10:
        raise InvalidPartyData("NIP: 10 cyfr")
    body = digits[:9]
    total = sum(int(digit) * weight for digit, weight in zip(body, _NIP_WEIGHTS, strict=True))
    checksum = total % 10
    if digits[9] != str(checksum):
        raise InvalidPartyData("NIP: suma kontrolna")
    return digits


def normalize_roles(raw: list[str]) -> list[str]:
    if type(raw) is not list:
        raise InvalidPartyData("roles muszą być listą")
    unique: list[str] = []
    for item in raw:
        if type(item) is not str:
            raise InvalidPartyData("rola musi być tekstem")
        role = item.strip().lower()
        if role == "":
            continue
        if role not in ALLOWED_ROLES:
            raise InvalidPartyData(f"role spoza allowlisty: {role}")
        if role not in unique:
            unique.append(role)
    if len(unique) == 0:
        raise InvalidPartyData("roles: co najmniej jedna rola")
    return unique


def normalize_email_domain(raw: str) -> str:
    if type(raw) is not str:
        raise InvalidPartyData("domena musi być tekstem")
    folded = raw.strip().lower()
    if folded == "" or "." not in folded:
        raise InvalidPartyData("domena mailowa jest wymagana")
    return folded


def email_domain_from_address(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPartyData("adres mailowy musi być tekstem")
    folded = raw.strip().lower()
    if folded.count("@") != 1:
        raise InvalidPartyData("adres mailowy wymaga dokładnie jednego @")
    local, domain = folded.split("@", 1)
    if local == "":
        raise InvalidPartyData("adres mailowy: pusta część lokalna")
    return normalize_email_domain(domain)


def normalize_credit_pair(
    limit: object | None,
    currency: str | None,
) -> tuple[Decimal | None, str | None]:
    if isinstance(limit, float) or isinstance(limit, bool):
        raise InvalidPartyData("kwota kredytu nie może być float")
    if limit is None and currency is None:
        return None, None
    if limit is None or currency is None:
        raise InvalidPartyData("credit_limit i credit_currency to para")
    try:
        money = Money.of(limit, currency)
    except InvalidMoney as exc:
        raise InvalidPartyData(f"credit: {exc}") from exc
    return money.amount, money.currency.code


def manual_source_ref() -> str:
    return _MANUAL_SOURCE


def lookup_source_ref(source: str) -> str:
    token = source.strip().lower()
    if token == "":
        raise InvalidPartyData("źródło lookupu jest wymagane")
    return f"tenant:lookup:{token}"
