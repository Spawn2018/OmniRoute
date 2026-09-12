import re

from app.domain.errors import InvalidWebhookOutboxMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"webhook", "retry", "dead", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://webhook-outbox-mark/"
_REF_CAP = 256


def parse_webhook_outbox_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidWebhookOutboxMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidWebhookOutboxMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidWebhookOutboxMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidWebhookOutboxMark(
            "rodzaj: webhook, retry, dead albo other",
        )
    if type(origin) is not str:
        raise InvalidWebhookOutboxMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidWebhookOutboxMark("obce wskazanie zapisu znacznika webhook outbox")
    if len(pointer) > _REF_CAP:
        raise InvalidWebhookOutboxMark(
            "obce wskazanie zapisu znacznika webhook outbox za długie",
        )
    return slug, token, pointer
