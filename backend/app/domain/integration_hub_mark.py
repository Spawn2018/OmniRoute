import re

from app.domain.errors import InvalidIntegrationHubMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"rest", "soap", "edi", "sftp", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://integration-hub-mark/"
_REF_CAP = 256


def parse_integration_hub_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidIntegrationHubMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidIntegrationHubMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidIntegrationHubMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidIntegrationHubMark(
            "rodzaj: rest, soap, edi, sftp albo other",
        )
    if type(origin) is not str:
        raise InvalidIntegrationHubMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidIntegrationHubMark("obce wskazanie zapisu znacznika Integration Hub")
    if len(pointer) > _REF_CAP:
        raise InvalidIntegrationHubMark(
            "obce wskazanie zapisu znacznika Integration Hub za długie",
        )
    return slug, token, pointer
