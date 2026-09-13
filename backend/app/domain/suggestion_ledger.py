import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from uuid import UUID

from app.domain.errors import InvalidSuggestionLedger

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"eta", "rate", "route", "other"})
_REACTIONS = frozenset({"accept", "modify", "reject"})
_MANUAL = "tenant:manual"
_FIX = "fixture://suggestion-ledger/"
_FOUR = Decimal("0.0001")
_NONE = "none"


@dataclass(frozen=True)
class SuggestionLedgerDraft:
    target_bc: str
    entity_id: UUID
    suggestion_kind: str
    interval_low: Decimal
    interval_high: Decimal
    model_version: str
    prompt_version: str
    reaction: str
    changed_to: str
    source_ref: str


def _snake(raw: object, label: str) -> str:
    if type(raw) is not str:
        raise InvalidSuggestionLedger(f"{label} musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE.fullmatch(token) is None:
        raise InvalidSuggestionLedger(f"{label}: snake 2–32")
    return token


def _interval_bound(raw: object) -> Decimal:
    if isinstance(raw, float) or isinstance(raw, bool):
        raise InvalidSuggestionLedger("przedział nie może być float")
    if not isinstance(raw, Decimal | str | int):
        raise InvalidSuggestionLedger("przedział musi być liczbą dziesiętną")
    token = raw.strip() if isinstance(raw, str) else raw
    if token == "":
        raise InvalidSuggestionLedger("przedział: brak")
    try:
        parsed = token if isinstance(token, Decimal) else Decimal(str(token))
    except InvalidOperation as exc:
        raise InvalidSuggestionLedger("przedział musi być liczbą dziesiętną") from exc
    return parsed.quantize(_FOUR)


def _entity_id(raw: object) -> UUID:
    if type(raw) is not str:
        raise InvalidSuggestionLedger("encja musi być UUID")
    try:
        return UUID(raw.strip())
    except ValueError as exc:
        raise InvalidSuggestionLedger("encja musi być UUID") from exc


def _reaction_change(reaction: str, raw: object) -> str:
    if type(raw) is not str:
        raise InvalidSuggestionLedger("zmiana musi być tekstem")
    token = raw.strip()
    if reaction == "modify":
        if token == "" or token == _NONE or len(token) > 256:
            raise InvalidSuggestionLedger("zmiana: na co zmienił, nie none")
        return token
    if token != _NONE:
        raise InvalidSuggestionLedger("zmiana: none przy accept albo reject")
    return token


def _source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidSuggestionLedger("obce source_ref")
    pointer = raw.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidSuggestionLedger("obce wskazanie zapisu ledgeru podpowiedzi")
    if len(pointer) > 256:
        raise InvalidSuggestionLedger("obce wskazanie zapisu ledgeru podpowiedzi za długie")
    return pointer


def parse_suggestion_ledger_row(
    target_bc: object,
    entity_id: object,
    suggestion_kind: object,
    interval_low: object,
    interval_high: object,
    model_version: object,
    prompt_version: object,
    reaction: object,
    changed_to: object,
    source_ref: object,
) -> SuggestionLedgerDraft:
    kind = _snake(suggestion_kind, "rodzaj")
    if kind not in _KINDS:
        raise InvalidSuggestionLedger("rodzaj: eta, rate, route albo other")
    verdict = _snake(reaction, "reakcja")
    if verdict not in _REACTIONS:
        raise InvalidSuggestionLedger("reakcja: accept, modify albo reject")
    low = _interval_bound(interval_low)
    high = _interval_bound(interval_high)
    if high < low:
        raise InvalidSuggestionLedger("przedział: high poniżej low")
    return SuggestionLedgerDraft(
        target_bc=_snake(target_bc, "kontekst"),
        entity_id=_entity_id(entity_id),
        suggestion_kind=kind,
        interval_low=low,
        interval_high=high,
        model_version=_snake(model_version, "model"),
        prompt_version=_snake(prompt_version, "prompt"),
        reaction=verdict,
        changed_to=_reaction_change(verdict, changed_to),
        source_ref=_source_ref(source_ref),
    )
