import re

from app.domain.errors import InvalidClauseNotice

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MANUAL = "tenant:manual"
_PREFIX = "fixture://clause-notice/"
_REF_CAP = 256
_LABEL_CAP = 128


def parse_clause_notice_row(
    code: object, clause_label: object, origin: object
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidClauseNotice("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidClauseNotice("oznaczenie: snake 2–32")
    if type(clause_label) is not str:
        raise InvalidClauseNotice("etykieta musi być tekstem")
    label = clause_label.strip()
    if not label or len(label) > _LABEL_CAP:
        raise InvalidClauseNotice("etykieta: tekst 1–128")
    if type(origin) is not str:
        raise InvalidClauseNotice("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidClauseNotice("obce wskazanie zapisu powiadomienia o klauzuli")
    if len(pointer) > _REF_CAP:
        raise InvalidClauseNotice("obce wskazanie zapisu powiadomienia o klauzuli za długie")
    return slug, label, pointer
