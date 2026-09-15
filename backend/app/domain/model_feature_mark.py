import re

from app.domain.errors import InvalidModelFeatureMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"numeric", "categorical", "derived", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://model-feature-mark/"
_REF_CAP = 256


def parse_model_feature_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidModelFeatureMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidModelFeatureMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidModelFeatureMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidModelFeatureMark(
            "rodzaj: numeric, categorical, derived albo other",
        )
    if type(origin) is not str:
        raise InvalidModelFeatureMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidModelFeatureMark(
            "obce wskazanie zapisu cechy modelu",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidModelFeatureMark(
            "obce wskazanie zapisu cechy modelu za dlugie",
        )
    return slug, token, pointer
