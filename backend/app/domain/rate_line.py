from decimal import Decimal, InvalidOperation

from app.domain.errors import InvalidRateLine, InvalidSourceRef

_SOURCE_REF_MAX = 512
_FOUR = Decimal("0.0001")
_MAX_ABS = Decimal("10000000000")


def require_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidSourceRef("source_ref musi być tekstem")
    origin = raw.strip()
    if origin == "":
        raise InvalidSourceRef("source_ref jest obowiązkowy")
    if len(origin) > _SOURCE_REF_MAX:
        raise InvalidSourceRef("source_ref: max 512 znaków")
    return origin


def require_allotment_teu(raw: object) -> Decimal | None:
    if raw is None:
        return None
    if type(raw) is str and raw.strip() == "":
        return None
    if isinstance(raw, float) or isinstance(raw, bool):
        raise InvalidRateLine("allotment teu nie może być float")
    if not isinstance(raw, Decimal | str | int):
        raise InvalidRateLine("allotment teu musi być liczbą dziesiętną")
    try:
        parsed = raw if isinstance(raw, Decimal) else Decimal(str(raw))
    except InvalidOperation as exc:
        raise InvalidRateLine("allotment teu musi być liczbą dziesiętną") from exc
    if not parsed.is_finite():
        raise InvalidRateLine("allotment teu musi być skończona")
    if parsed < 0:
        raise InvalidRateLine("allotment teu nie może być ujemne")
    quantized = parsed.quantize(_FOUR)
    if quantized >= _MAX_ABS:
        raise InvalidRateLine("allotment teu: precyzja Numeric(14,4)")
    return quantized


def require_spot_or_contract(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidRateLine("spot_or_contract musi być tekstem")
    token = raw.strip().lower()
    if token == "":
        return None
    if token not in {"spot", "contract", "other"}:
        raise InvalidRateLine("spot_or_contract: spot|contract|other")
    return token
