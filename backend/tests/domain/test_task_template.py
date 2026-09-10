import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidTaskTemplate
from app.domain.task_template import (
    require_task_applies_when,
    require_task_template_code,
    require_task_template_source_ref,
)


@given(st.sampled_from(["gate_in", "vgm_cut", "si_window"]))
def test_task_template_code_snake(raw: str) -> None:
    assert require_task_template_code(raw) == raw


@given(st.sampled_from(["", "Gate In", "1bad"]))
def test_task_template_code_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidTaskTemplate, match="szablon"):
        require_task_template_code(raw)


def test_task_applies_when_trims() -> None:
    assert require_task_applies_when("  CY cutoff  ") == "CY cutoff"


@given(st.sampled_from(["", "   "]))
def test_task_applies_when_rejects_blank(raw: str) -> None:
    with pytest.raises(InvalidTaskTemplate, match="warunek"):
        require_task_applies_when(raw)


def test_task_template_source_ref_accepts_fixture() -> None:
    assert (
        require_task_template_source_ref(" fixture://task-template/1 ")
        == "fixture://task-template/1"
    )


@given(st.sampled_from(["", "   ", "http://tasks.example/x"]))
def test_task_template_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidTaskTemplate, match="obce|wskazanie"):
        require_task_template_source_ref(raw)
