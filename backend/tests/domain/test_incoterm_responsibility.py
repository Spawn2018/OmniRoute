import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidIncotermResponsibility
from app.domain.incoterm_responsibility import (
    omni_ops_seed_pairs,
    require_booking_scope,
    require_clearance_role,
    require_responsibility_incoterm,
    require_responsibility_source_ref,
)


def test_omni_ops_seed_has_twenty_two_pairs_and_ddp_seller_import() -> None:
    pairs = omni_ops_seed_pairs()
    assert len(pairs) == 22
    ddp_import = next(
        pair
        for pair in pairs
        if pair["incoterm"] == "DDP" and pair["trade_side"] == "import"
    )
    assert ddp_import["import_clearance_role"] == "seller"
    assert ddp_import["source_ref"] == "omni:incoterms2020:ops"
    assert "ICC" not in str(pairs)


def test_require_incoterm_and_role_allowlists() -> None:
    assert require_responsibility_incoterm(" ddp ") == "DDP"
    assert require_clearance_role("seller", field="export_clearance_role") == "seller"
    assert require_booking_scope([" ocean ", "ocean"]) == ["ocean"]


def test_reject_unknown_incoterm_and_icc_source() -> None:
    with pytest.raises(InvalidIncotermResponsibility, match="incoterm"):
        require_responsibility_incoterm("XXX")
    with pytest.raises(InvalidIncotermResponsibility, match="obce"):
        require_responsibility_source_ref("icc://incoterms-2020")


@given(st.sampled_from(["noted", "attached", "quoted"]))
def test_booking_scope_rejects_foreign_tokens(raw: str) -> None:
    with pytest.raises(InvalidIncotermResponsibility, match="zakres"):
        require_booking_scope([raw])
