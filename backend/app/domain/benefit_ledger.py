import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from app.domain.errors import InvalidBenefitLedger, InvalidMoney
from app.domain.money import Money

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MANUAL = "tenant:manual"
_FIX = "fixture://benefit-ledger/"
_FOUR = Decimal("0.0001")


@dataclass(frozen=True)
class BenefitLedgerDraft:
    benefit_code: str
    method_label: str
    hours_saved: Decimal
    saved_amount: Decimal
    saved_currency: str
    source_ref: str


def _snake(raw: object, label: str) -> str:
    if type(raw) is not str:
        raise InvalidBenefitLedger(f"{label} musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE.fullmatch(token) is None:
        raise InvalidBenefitLedger(f"{label}: snake 2–32")
    return token


def _label(raw: object, name: str) -> str:
    if type(raw) is not str:
        raise InvalidBenefitLedger(f"{name} musi być tekstem")
    token = raw.strip()
    if token == "" or len(token) > 256:
        raise InvalidBenefitLedger(f"{name}: 1–256")
    return token


def _hours_saved(raw: object) -> Decimal:
    if isinstance(raw, float) or isinstance(raw, bool):
        raise InvalidBenefitLedger("godziny nie mogą być float")
    if not isinstance(raw, Decimal | str | int):
        raise InvalidBenefitLedger("godziny muszą być liczbą dziesiętną")
    token = raw.strip() if isinstance(raw, str) else raw
    if token == "":
        raise InvalidBenefitLedger("godziny: brak")
    try:
        parsed = token if isinstance(token, Decimal) else Decimal(str(token))
    except InvalidOperation as exc:
        raise InvalidBenefitLedger("godziny muszą być liczbą dziesiętną") from exc
    return parsed.quantize(_FOUR)


def _saved_money(amount: object, currency: object) -> Money:
    try:
        return Money.of(amount, currency)
    except InvalidMoney as exc:
        raise InvalidBenefitLedger(str(exc)) from exc


def _source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidBenefitLedger("obce source_ref")
    pointer = raw.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidBenefitLedger("obce wskazanie zapisu ledgeru oszczędności")
    if len(pointer) > 256:
        raise InvalidBenefitLedger("obce wskazanie zapisu ledgeru oszczędności za długie")
    return pointer


def parse_benefit_ledger_row(
    benefit_code: object,
    method_label: object,
    hours_saved: object,
    saved_amount: object,
    saved_currency: object,
    source_ref: object,
) -> BenefitLedgerDraft:
    money = _saved_money(saved_amount, saved_currency)
    return BenefitLedgerDraft(
        benefit_code=_snake(benefit_code, "kod"),
        method_label=_label(method_label, "metoda"),
        hours_saved=_hours_saved(hours_saved),
        saved_amount=money.amount,
        saved_currency=money.currency.code,
        source_ref=_source_ref(source_ref),
    )
