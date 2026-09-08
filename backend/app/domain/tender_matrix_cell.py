import re
from decimal import Decimal, InvalidOperation
from uuid import UUID

from app.domain.errors import InvalidTenderMatrixCell

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_CCY = re.compile(r"^[A-Z]{3}$")
_MAX_REF = 256
_FIXTURE = "fixture://tender-matrix-cell/"
_MANUAL = "tenant:manual"
_FOUR = Decimal("0.0001")


def require_board_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidTenderMatrixCell("tender_id musi być UUID")
    return raw


def require_cell_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderMatrixCell("komórka musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE.fullmatch(token) is None:
        raise InvalidTenderMatrixCell("komórka: snake 2–32")
    return token


def require_cell_amount(raw: object) -> Decimal:
    if type(raw) is float or type(raw) is bool:
        raise InvalidTenderMatrixCell("kwota nie może być float")
    if type(raw) is not Decimal and type(raw) is not str and type(raw) is not int:
        raise InvalidTenderMatrixCell("kwota musi być liczbą dziesiętną")
    try:
        parsed = raw if type(raw) is Decimal else Decimal(str(raw))
    except InvalidOperation as exc:
        raise InvalidTenderMatrixCell("kwota musi być liczbą dziesiętną") from exc
    if parsed <= 0:
        raise InvalidTenderMatrixCell("kwota musi być dodatnia")
    return parsed.quantize(_FOUR)


def require_cell_currency(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderMatrixCell("waluta komórki musi być tekstem")
    token = raw.strip().upper()
    if _CCY.fullmatch(token) is None:
        raise InvalidTenderMatrixCell("kwota wymaga waluty ISO")
    return token


def require_cell_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderMatrixCell("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTenderMatrixCell("wskazanie zapisu komórki matrycy")
    if len(token) > _MAX_REF:
        raise InvalidTenderMatrixCell("wskazanie zapisu komórki matrycy za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTenderMatrixCell("obce wskazanie zapisu komórki matrycy")
    return token
