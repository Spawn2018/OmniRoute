import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidTowerImpact
from app.domain.tower_impact import (
    contract_gap_label,
    require_chain_stage,
    require_contract_data_status,
    require_impact_source_ref,
)


@given(st.sampled_from(["stock", "production", "sales", "ebitda"]))
def test_chain_stage_allowlist(raw: str) -> None:
    assert require_chain_stage(raw) == raw


@given(st.sampled_from(["", "warehouse", "STOCK kg"]))
def test_chain_stage_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidTowerImpact, match="etap"):
        require_chain_stage(raw)


@given(st.sampled_from(["missing", "recorded"]))
def test_contract_data_status_allowlist(raw: str) -> None:
    assert require_contract_data_status(raw) == raw


@given(st.sampled_from(["", "sla_clause", "present"]))
def test_contract_data_status_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidTowerImpact, match="umowa"):
        require_contract_data_status(raw)


def test_missing_status_exposes_brak_danych_umowy() -> None:
    assert contract_gap_label("missing") == "brak danych umowy"
    assert contract_gap_label("recorded") is None


def test_impact_source_ref_accepts_fixture() -> None:
    assert (
        require_impact_source_ref(" fixture://tower-impact/1 ")
        == "fixture://tower-impact/1"
    )


@given(st.sampled_from(["", "   ", "http://tower.example/x"]))
def test_impact_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidTowerImpact, match="obce|wskazanie"):
        require_impact_source_ref(raw)
