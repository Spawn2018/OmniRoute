import re

from app.domain.errors import InvalidFreightAuditMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"expected_vs_invoice", "expected_vs_charge"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://freight-audit-mark/"
_REF_CAP = 256


def parse_freight_audit_mark_row(
    code: object, kind: object, origin: object
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidFreightAuditMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidFreightAuditMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidFreightAuditMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidFreightAuditMark("rodzaj: expected_vs_invoice albo expected_vs_charge")
    if type(origin) is not str:
        raise InvalidFreightAuditMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_PREFIX):
        raise InvalidFreightAuditMark("obce wskazanie zapisu znacznika audytu frachtu")
    if len(pointer) > _REF_CAP:
        raise InvalidFreightAuditMark("obce wskazanie zapisu znacznika audytu frachtu za długie")
    return slug, token, pointer
