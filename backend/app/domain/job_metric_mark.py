import re

from app.domain.errors import InvalidJobMetricMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_METRIC_KINDS = frozenset({"time_to_fix", "touches", "rework", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://job-metric-mark/"


def parse_job_metric_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidJobMetricMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidJobMetricMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidJobMetricMark("metryka musi być tekstem")
    token = kind.strip().lower()
    if token not in _METRIC_KINDS:
        raise InvalidJobMetricMark("metryka: time_to_fix, touches, rework albo other")
    if type(origin) is not str:
        raise InvalidJobMetricMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidJobMetricMark("obce wskazanie zapisu znacznika metryki jobu")
    if len(pointer) > 256:
        raise InvalidJobMetricMark("obce wskazanie zapisu znacznika metryki jobu za długie")
    return slug, token, pointer
