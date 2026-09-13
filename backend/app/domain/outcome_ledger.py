import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from uuid import UUID

from app.domain.errors import InvalidOutcomeLedger

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MANUAL = "tenant:manual"
_FIX = "fixture://outcome-ledger/"
_FOUR = Decimal("0.0001")


@dataclass(frozen=True)
class OutcomeLedgerDraft:
    target_bc: str
    entity_id: UUID
    suggestion_id: UUID
    outcome_kind: str
    actual_value: Decimal
    source_ref: str


def _snake(raw: object, label: str) -> str:
    if type(raw) is not str:
        raise InvalidOutcomeLedger(f"{label} musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE.fullmatch(token) is None:
        raise InvalidOutcomeLedger(f"{label}: snake 2–32")
    return token


def _actual_value(raw: object) -> Decimal:
    if isinstance(raw, float) or isinstance(raw, bool):
        raise InvalidOutcomeLedger("fakt nie może być float")
    if not isinstance(raw, Decimal | str | int):
        raise InvalidOutcomeLedger("fakt musi być liczbą dziesiętną")
    token = raw.strip() if isinstance(raw, str) else raw
    if token == "":
        raise InvalidOutcomeLedger("fakt: brak")
    try:
        parsed = token if isinstance(token, Decimal) else Decimal(str(token))
    except InvalidOperation as exc:
        raise InvalidOutcomeLedger("fakt musi być liczbą dziesiętną") from exc
    return parsed.quantize(_FOUR)


def _uuid_field(raw: object, label: str) -> UUID:
    if type(raw) is not str:
        raise InvalidOutcomeLedger(f"{label} musi być UUID")
    try:
        return UUID(raw.strip())
    except ValueError as exc:
        raise InvalidOutcomeLedger(f"{label} musi być UUID") from exc


def _source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidOutcomeLedger("obce source_ref")
    pointer = raw.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidOutcomeLedger("obce wskazanie zapisu ledgeru wyniku")
    if len(pointer) > 256:
        raise InvalidOutcomeLedger("obce wskazanie zapisu ledgeru wyniku za długie")
    return pointer


def parse_outcome_ledger_row(
    target_bc: object,
    entity_id: object,
    suggestion_id: object,
    outcome_kind: object,
    actual_value: object,
    source_ref: object,
) -> OutcomeLedgerDraft:
    kind = _snake(outcome_kind, "rodzaj")
    return OutcomeLedgerDraft(
        target_bc=_snake(target_bc, "kontekst"),
        entity_id=_uuid_field(entity_id, "encja"),
        suggestion_id=_uuid_field(suggestion_id, "podpowiedź"),
        outcome_kind=kind,
        actual_value=_actual_value(actual_value),
        source_ref=_source_ref(source_ref),
    )
