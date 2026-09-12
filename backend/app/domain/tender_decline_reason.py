import re

from app.domain.errors import InvalidTenderDeclineReason

_CODE_RE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_ALLOWED_KINDS = frozenset({"decline", "no_bid", "withdraw", "other"})
_MANUAL_REF = "tenant:manual"
_FIXTURE_PREFIX = "fixture://tender-decline-reason/"
_MAX_REF = 256


def parse_tender_decline_reason_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidTenderDeclineReason("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE_RE.fullmatch(slug) is None:
        raise InvalidTenderDeclineReason("oznaczenie: snake 2–32")

    if type(kind) is not str:
        raise InvalidTenderDeclineReason("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _ALLOWED_KINDS:
        raise InvalidTenderDeclineReason(
            "rodzaj: decline, no_bid, withdraw albo other",
        )

    if type(origin) is not str:
        raise InvalidTenderDeclineReason("obce source_ref")
    pointer = origin.strip()
    accepted = pointer == _MANUAL_REF or pointer.startswith(_FIXTURE_PREFIX)
    if not accepted:
        raise InvalidTenderDeclineReason("obce wskazanie zapisu powodu decline")
    if len(pointer) > _MAX_REF:
        raise InvalidTenderDeclineReason("obce wskazanie zapisu powodu decline za długie")
    return slug, token, pointer
