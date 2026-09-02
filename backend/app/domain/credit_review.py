from datetime import date

from app.domain.errors import InvalidCreditReview

_DECISIONS = frozenset({"ok", "hold", "refuse"})
_NOTE_MAX = 512


def normalize_review_decision(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCreditReview("decyzja recenzji musi być tekstem")
    token = raw.strip().lower()
    if token not in _DECISIONS:
        raise InvalidCreditReview("decyzja recenzji: ok, hold albo refuse")
    return token


def normalize_review_note(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidCreditReview("notatka recenzji musi być tekstem")
    note = raw.strip()
    if note == "":
        return None
    if len(note) > _NOTE_MAX:
        raise InvalidCreditReview("notatka recenzji za długa")
    return note


def normalize_review_date(raw: object) -> date:
    if type(raw) is date:
        return raw
    raise InvalidCreditReview("data recenzji musi być dniem")
