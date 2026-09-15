import re

from app.domain.errors import InvalidArticle50Mark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"generated", "exempt", "human", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://article50-mark/"
_REF_CAP = 256


def parse_article50_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidArticle50Mark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidArticle50Mark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidArticle50Mark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidArticle50Mark(
            "rodzaj: generated, exempt, human albo other",
        )
    if type(origin) is not str:
        raise InvalidArticle50Mark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidArticle50Mark(
            "obce wskazanie zapisu mitygacji art. 50",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidArticle50Mark(
            "obce wskazanie zapisu mitygacji art. 50 za dlugie",
        )
    return slug, token, pointer
