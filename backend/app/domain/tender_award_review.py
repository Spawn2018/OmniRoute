from uuid import UUID

from app.domain.errors import InvalidTenderAwardReview

_REVIEWS = frozenset({"countersign", "challenge"})
_MAX_REF = 256
_FIXTURE = "fixture://tender-award-review/"
_MANUAL = "tenant:manual"


def require_board_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidTenderAwardReview("tender_id musi być UUID")
    return raw


def require_review_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderAwardReview("przegląd musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if token not in _REVIEWS:
        raise InvalidTenderAwardReview("przegląd: countersign albo challenge")
    return token


def require_review_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderAwardReview("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTenderAwardReview("wskazanie zapisu przeglądu nagrody")
    if len(token) > _MAX_REF:
        raise InvalidTenderAwardReview("wskazanie zapisu przeglądu nagrody za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTenderAwardReview("obce wskazanie zapisu przeglądu nagrody")
    return token
