from app.domain.errors import InvalidExecutiveMark

_KINDS = (
    "loss",
    "lane",
    "risk",
    "cash",
    "other",
)
_FIXTURE = "fixture://executive-mark/"
_MANUAL = "tenant:manual"


def require_question_kind(raw: object) -> str:
    match raw:
        case str() as text:
            token = text.strip().lower()
            if token in _KINDS:
                return token
            raise InvalidExecutiveMark("pytanie: allowlista HITL")
        case _:
            raise InvalidExecutiveMark("pytanie musi być tekstem")


def require_brief_source_ref(raw: object) -> str:
    if not isinstance(raw, str):
        raise InvalidExecutiveMark("source_ref musi być tekstem")
    origin = raw.strip()
    if origin == _MANUAL or origin.startswith(_FIXTURE):
        if len(origin) > 256:
            raise InvalidExecutiveMark("wskazanie zapisu pytania zarządu za długie")
        return origin
    if origin == "":
        raise InvalidExecutiveMark("wskazanie zapisu pytania zarządu")
    raise InvalidExecutiveMark("obce wskazanie zapisu pytania zarządu")
