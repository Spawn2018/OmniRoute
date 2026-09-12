import re

from app.domain.errors import InvalidDemandSnapshotMark

_CODE_RE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_ALLOWED_KINDS = frozenset({"forecast", "booking", "actual", "other"})
_MANUAL_REF = "tenant:manual"
_FIXTURE_PREFIX = "fixture://demand-snapshot-mark/"
_MAX_REF = 256


def parse_demand_snapshot_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidDemandSnapshotMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE_RE.fullmatch(slug) is None:
        raise InvalidDemandSnapshotMark("oznaczenie: snake 2–32")

    if type(kind) is not str:
        raise InvalidDemandSnapshotMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _ALLOWED_KINDS:
        raise InvalidDemandSnapshotMark(
            "rodzaj: forecast, booking, actual albo other",
        )

    if type(origin) is not str:
        raise InvalidDemandSnapshotMark("obce source_ref")
    pointer = origin.strip()
    accepted = pointer == _MANUAL_REF or pointer.startswith(_FIXTURE_PREFIX)
    if not accepted:
        raise InvalidDemandSnapshotMark("obce wskazanie zapisu powodu decline")
    if len(pointer) > _MAX_REF:
        raise InvalidDemandSnapshotMark("obce wskazanie zapisu powodu decline za długie")
    return slug, token, pointer
