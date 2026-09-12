import re

from app.domain.errors import InvalidImpersonateGuardMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_GUARD_KINDS = frozenset({"impersonate", "unwrap_denied", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://impersonate-guard-mark/"


def parse_impersonate_guard_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidImpersonateGuardMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidImpersonateGuardMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidImpersonateGuardMark("rodzaj guardu musi być tekstem")
    token = kind.strip().lower()
    if token not in _GUARD_KINDS:
        raise InvalidImpersonateGuardMark(
            "rodzaj guardu: impersonate, unwrap_denied albo other",
        )
    if type(origin) is not str:
        raise InvalidImpersonateGuardMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidImpersonateGuardMark(
            "obce wskazanie zapisu znacznika impersonate guard",
        )
    if len(pointer) > 256:
        raise InvalidImpersonateGuardMark(
            "obce wskazanie zapisu znacznika impersonate guard za długie",
        )
    return slug, token, pointer
