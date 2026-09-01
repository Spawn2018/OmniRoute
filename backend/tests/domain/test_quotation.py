from uuid import UUID, uuid4

import pytest
from hypothesis import assume, given
from hypothesis import strategies as st

from app.domain.errors import IncompleteQuotationSnapshot
from app.domain.quotation import require_lane_party_snapshot

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
