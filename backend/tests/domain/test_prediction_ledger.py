from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidPredictionLedger
from app.domain.prediction_ledger import (
    require_crps,
    require_horizon_code,
    require_interval_bound,
    require_interval_order,
    require_ledger_source_ref,
    require_mae,
    require_model_code,
    require_prediction_kind,
)


@given(st.sampled_from(["eta", "transit", "disrupt"]))
def test_prediction_kind_accepts_allowlist(raw: str) -> None:
    assert require_prediction_kind(raw) == raw


@given(st.sampled_from(["", "person_score", "http://hold.example/x"]))
def test_prediction_kind_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidPredictionLedger, match="rodzaj"):
        require_prediction_kind(raw)


@given(st.sampled_from(["h1h", "h6h", "h24h", "h7d"]))
def test_horizon_accepts_allowlist(raw: str) -> None:
    assert require_horizon_code(raw) == raw


@given(st.sampled_from(["", "day", "24h"]))
def test_horizon_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidPredictionLedger, match="horyzont"):
        require_horizon_code(raw)


def test_crps_rejects_missing_and_float() -> None:
    with pytest.raises(InvalidPredictionLedger, match="crps"):
        require_crps("")
    with pytest.raises(InvalidPredictionLedger, match="crps"):
        require_crps(-1)
    with pytest.raises(InvalidPredictionLedger, match="crps"):
        require_crps(0.12)


def test_mae_and_interval_are_decimal() -> None:
    assert require_mae("12") == Decimal("12.0000")
    assert require_interval_bound("30") == Decimal("30.0000")
    require_interval_order(Decimal("30"), Decimal("90"))
    with pytest.raises(InvalidPredictionLedger, match="przedział"):
        require_interval_order(Decimal("90"), Decimal("30"))


def test_ledger_source_ref_accepts_fixture() -> None:
    assert require_ledger_source_ref(" fixture://prediction-ledger/1 ") == (
        "fixture://prediction-ledger/1"
    )


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_ledger_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidPredictionLedger, match="obce|wskazanie"):
        require_ledger_source_ref(raw)


def test_model_code_snake() -> None:
    assert require_model_code(" hist_eta ") == "hist_eta"
    with pytest.raises(InvalidPredictionLedger, match="model"):
        require_model_code("X")
