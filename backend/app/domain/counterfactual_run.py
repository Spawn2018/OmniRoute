import re
from dataclasses import dataclass

from app.domain.errors import InvalidCounterfactualRun

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MANUAL = "tenant:manual"
_FIX = "fixture://counterfactual-run/"


@dataclass(frozen=True)
class CounterfactualRunDraft:
    run_code: str
    baseline_label: str
    levers_label: str
    result_label: str
    source_ref: str


def _snake(raw: object, label: str) -> str:
    if type(raw) is not str:
        raise InvalidCounterfactualRun(f"{label} musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE.fullmatch(token) is None:
        raise InvalidCounterfactualRun(f"{label}: snake 2–32")
    return token


def _label(raw: object, name: str) -> str:
    if type(raw) is not str:
        raise InvalidCounterfactualRun(f"{name} musi być tekstem")
    token = raw.strip()
    if token == "" or len(token) > 256:
        raise InvalidCounterfactualRun(f"{name}: 1–256")
    return token


def _source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCounterfactualRun("obce source_ref")
    pointer = raw.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidCounterfactualRun("obce wskazanie zapisu przebiegu")
    if len(pointer) > 256:
        raise InvalidCounterfactualRun("obce wskazanie zapisu przebiegu za długie")
    return pointer


def parse_counterfactual_run_row(
    run_code: object,
    baseline_label: object,
    levers_label: object,
    result_label: object,
    source_ref: object,
) -> CounterfactualRunDraft:
    return CounterfactualRunDraft(
        run_code=_snake(run_code, "kod"),
        baseline_label=_label(baseline_label, "punkt"),
        levers_label=_label(levers_label, "dźwignie"),
        result_label=_label(result_label, "wynik"),
        source_ref=_source_ref(source_ref),
    )
