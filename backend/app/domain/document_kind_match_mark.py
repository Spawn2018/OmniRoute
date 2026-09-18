import re

from app.domain.errors import InvalidDocumentKindMatchMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"exact", "alias", "missing", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://document-kind-match-mark/"
_REF_CAP = 256


def parse_document_kind_match_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidDocumentKindMatchMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidDocumentKindMatchMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidDocumentKindMatchMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidDocumentKindMatchMark(
            "dopasowanie: exact, alias, missing albo other",
        )
    if type(origin) is not str:
        raise InvalidDocumentKindMatchMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidDocumentKindMatchMark(
            "obce wskazanie zapisu znacznika dopasowania rodzaju dokumentu",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidDocumentKindMatchMark(
            "obce wskazanie zapisu znacznika dopasowania rodzaju dokumentu za długie",
        )
    return slug, token, pointer
