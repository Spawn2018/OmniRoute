from app.domain.errors import InvalidSourceRef

_SOURCE_REF_MAX = 512


def require_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidSourceRef("source_ref musi być tekstem")
    origin = raw.strip()
    if origin == "":
        raise InvalidSourceRef("source_ref jest obowiązkowy")
    if len(origin) > _SOURCE_REF_MAX:
        raise InvalidSourceRef("source_ref: max 512 znaków")
    return origin
