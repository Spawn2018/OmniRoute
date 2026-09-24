from datetime import date
from uuid import UUID, uuid4

import pytest
from hypothesis import assume, given
from hypothesis import strategies as st

from app.domain.errors import (
    IncompleteQuotationSnapshot,
    InvalidQuotation,
    InvalidQuotationBatch,
    InvalidQuotationIncoterm,
    QuotationNamedPlaceRequired,
)
from app.domain.quotation import (
    require_batch_charge_codes,
    require_lane_party_snapshot,
    require_quotation_incoterm,
    require_revision_no,
    require_valid_until,
)

_UUIDS = st.uuids()
_OPTIONAL = st.one_of(st.none(), _UUIDS)


def test_complete_triple_returns_ids() -> None:
    origin = uuid4()
    destination = uuid4()
    party = uuid4()
    assert require_lane_party_snapshot(origin, destination, party) == (
        origin,
        destination,
        party,
    )


def test_missing_any_id_is_incomplete() -> None:
    origin = uuid4()
    destination = uuid4()
    party = uuid4()
    with pytest.raises(IncompleteQuotationSnapshot, match="POL"):
        require_lane_party_snapshot(None, destination, party)
    with pytest.raises(IncompleteQuotationSnapshot, match="POD"):
        require_lane_party_snapshot(origin, None, party)
    with pytest.raises(IncompleteQuotationSnapshot, match="kontrahenta"):
        require_lane_party_snapshot(origin, destination, None)
    with pytest.raises(IncompleteQuotationSnapshot):
        require_lane_party_snapshot(None, None, None)


@given(origin=_UUIDS, destination=_UUIDS, party=_UUIDS)
def test_any_complete_triple_is_accepted(
    origin: UUID,
    destination: UUID,
    party: UUID,
) -> None:
    assert require_lane_party_snapshot(origin, destination, party) == (
        origin,
        destination,
        party,
    )


@given(origin=_OPTIONAL, destination=_OPTIONAL, party=_OPTIONAL)
def test_any_partial_or_empty_triple_is_rejected(
    origin: UUID | None,
    destination: UUID | None,
    party: UUID | None,
) -> None:
    assume(origin is None or destination is None or party is None)
    with pytest.raises(IncompleteQuotationSnapshot):
        require_lane_party_snapshot(origin, destination, party)


def test_batch_codes_dedupe_and_reject_empty_or_too_many() -> None:
    assert require_batch_charge_codes([" thc ", "THC", "baf"]) == ["THC", "BAF"]
    with pytest.raises(InvalidQuotationBatch, match="co najmniej"):
        require_batch_charge_codes([])
    with pytest.raises(InvalidQuotationBatch, match="max 20"):
        require_batch_charge_codes([f"C{index:02d}" for index in range(21)])


def test_quotation_incoterm_blank_is_none() -> None:
    assert require_quotation_incoterm() == (None, None, None, None)


def test_quotation_incoterm_rejects_unknown() -> None:
    with pytest.raises(InvalidQuotationIncoterm, match="allowlisty"):
        require_quotation_incoterm("FOOBAR", "2020", "import", None)


def test_quotation_dap_requires_named_place() -> None:
    with pytest.raises(QuotationNamedPlaceRequired, match="named_place"):
        require_quotation_incoterm("DAP", "2020", "import", None)
    assert require_quotation_incoterm("DAP", "2020", "import", " Gdynia ") == (
        "DAP",
        "2020",
        "import",
        "Gdynia",
    )


def test_quotation_valid_until_is_calendar_day() -> None:
    assert require_valid_until(None) is None
    assert require_valid_until("  ") is None
    assert require_valid_until("2026-10-01") == date(2026, 10, 1)
    with pytest.raises(InvalidQuotation, match="ważność"):
        require_valid_until("2026-10-01T00:00:00")
    with pytest.raises(InvalidQuotation, match="ważność"):
        require_valid_until(True)
    with pytest.raises(InvalidQuotation, match="ważność"):
        require_valid_until(1)


def test_quotation_revision_no_is_positive_int() -> None:
    assert require_revision_no(None) is None
    assert require_revision_no("  ") is None
    assert require_revision_no(1) == 1
    assert require_revision_no("2") == 2
    with pytest.raises(InvalidQuotation, match="rewizja"):
        require_revision_no(0)
    with pytest.raises(InvalidQuotation, match="rewizja"):
        require_revision_no(-1)
    with pytest.raises(InvalidQuotation, match="rewizja"):
        require_revision_no(1.5)
    with pytest.raises(InvalidQuotation, match="rewizja"):
        require_revision_no(True)

