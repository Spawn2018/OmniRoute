import re

from app.domain.errors import InvalidRelationDocumentRequirement

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"domestic", "international", "waste", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://relation-document-requirement/"
_REF_CAP = 256


def parse_relation_document_requirement_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidRelationDocumentRequirement("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidRelationDocumentRequirement("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidRelationDocumentRequirement("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidRelationDocumentRequirement(
            "relacja: domestic, international, waste albo other",
        )
    if type(origin) is not str:
        raise InvalidRelationDocumentRequirement("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidRelationDocumentRequirement(
            "obce wskazanie zapisu znacznika wymogu dokumentow relacji",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidRelationDocumentRequirement(
            "obce wskazanie zapisu wymogu dokumentow relacji za długie",
        )
    return slug, token, pointer
