import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidMonitoringScheme
from app.domain.monitoring_scheme import require_scheme_code, require_scheme_source_ref


@given(st.sampled_from(["sent", "ekaer", "e_transport"]))
def test_scheme_code_normalizes_snake(raw: str) -> None:
    assert require_scheme_code(raw) == raw


@given(st.sampled_from(["", "X", "SENT XML", "http://puesc.gov.pl/x"]))
def test_scheme_code_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidMonitoringScheme, match="schemat"):
        require_scheme_code(raw)


def test_scheme_source_ref_accepts_fixture() -> None:
    assert require_scheme_source_ref(" fixture://monitoring-scheme/1 ") == (
        "fixture://monitoring-scheme/1"
    )


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_scheme_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidMonitoringScheme, match="obce|wskazanie"):
        require_scheme_source_ref(raw)
