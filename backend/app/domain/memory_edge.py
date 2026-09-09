from app.domain.errors import InvalidMemoryEdge

_KINDS = (
    "recalls",
    "follows",
    "blocks",
    "cites",
    "other",
)
_FIXTURE = "fixture://memory-edge/"
_MANUAL = "tenant:manual"


def require_edge_kind(raw: object) -> str:
    match raw:
        case str() as text:
            token = text.strip().lower()
            if token in _KINDS:
                return token
            raise InvalidMemoryEdge("krawędź: allowlista HITL")
        case _:
            raise InvalidMemoryEdge("krawędź musi być tekstem")


def require_edge_source_ref(raw: object) -> str:
    if not isinstance(raw, str):
        raise InvalidMemoryEdge("source_ref musi być tekstem")
    origin = raw.strip()
    from_catalog = origin == _MANUAL or origin.startswith(_FIXTURE)
    if from_catalog:
        if len(origin) > 256:
            raise InvalidMemoryEdge("wskazanie zapisu krawędzi pamięci za długie")
        return origin
    if origin == "":
        raise InvalidMemoryEdge("wskazanie zapisu krawędzi pamięci")
    raise InvalidMemoryEdge("obce wskazanie zapisu krawędzi pamięci")
