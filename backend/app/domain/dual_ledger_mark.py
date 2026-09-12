import re

from app.domain.errors import InvalidDualLedgerMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_LEDGER_KINDS = frozenset({"ops", "finance", "tax", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://dual-ledger-mark/"


def parse_dual_ledger_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidDualLedgerMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidDualLedgerMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidDualLedgerMark("rodzaj ledgera musi być tekstem")
    token = kind.strip().lower()
    if token not in _LEDGER_KINDS:
        raise InvalidDualLedgerMark(
            "rodzaj ledgera: ops, finance, tax albo other",
        )
    if type(origin) is not str:
        raise InvalidDualLedgerMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidDualLedgerMark(
            "obce wskazanie zapisu znacznika dual ledger",
        )
    if len(pointer) > 256:
        raise InvalidDualLedgerMark(
            "obce wskazanie zapisu znacznika dual ledger za długie",
        )
    return slug, token, pointer
