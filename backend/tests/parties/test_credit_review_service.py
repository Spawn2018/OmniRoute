from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.domain.errors import (
    CreditReviewConflict,
    InvalidCreditReview,
    UnknownCreditReview,
    UnknownParty,
)
from app.models.credit_review import CreditReview
from app.services.parties.party_service import PartyService


def _service() -> PartyService:
    service = PartyService(MagicMock())
    service._parties = MagicMock()
    return service


def _row(*, party_id, review_date: date, decision: str = "ok") -> CreditReview:
    return CreditReview(
        id=uuid4(),
        organization_id=uuid4(),
        decision=decision,
        review_date=review_date,
        party_id=party_id,
        note=None,
        source_ref="tenant:manual",
    )


@pytest.mark.asyncio
async def test_create_review_normalizes_and_keeps_manual_origin() -> None:
    service = _service()
    party_id = uuid4()
    org_id = uuid4()

    async def add(row: CreditReview) -> CreditReview:
        return row

    service._parties.get = AsyncMock(return_value=SimpleNamespace(id=party_id))
    service._parties.find_review_as_of = AsyncMock(return_value=None)
    service._parties.add_review = add
    stored = await service.create_review(
        organization_id=org_id,
        user_id=uuid4(),
        party_id=party_id,
        review_date=date(2026, 9, 1),
        decision=" HOLD ",
        note="  księgowość OK  ",
    )
    assert stored.decision == "hold"
    assert stored.note == "księgowość OK"
    assert stored.source_ref == "tenant:manual"
    assert stored.organization_id == org_id
    assert stored.party_id == party_id
    assert not hasattr(stored, "score") or getattr(stored, "score", None) is None


@pytest.mark.asyncio
async def test_create_review_unknown_party() -> None:
    service = _service()
    service._parties.get = AsyncMock(return_value=None)
    with pytest.raises(UnknownParty, match="nieznany kontrahent"):
        await service.create_review(
            organization_id=uuid4(),
            user_id=uuid4(),
            party_id=uuid4(),
            review_date=date(2026, 9, 1),
            decision="ok",
        )


@pytest.mark.asyncio
async def test_create_review_rejects_duplicate_day() -> None:
    service = _service()
    party_id = uuid4()
    day = date(2026, 9, 1)
    service._parties.get = AsyncMock(return_value=SimpleNamespace(id=party_id))
    service._parties.find_review_as_of = AsyncMock(
        return_value=_row(party_id=party_id, review_date=day),
    )
    with pytest.raises(CreditReviewConflict, match="2026-09-01"):
        await service.create_review(
            organization_id=uuid4(),
            user_id=uuid4(),
            party_id=party_id,
            review_date=day,
            decision="ok",
        )


@pytest.mark.asyncio
async def test_create_review_rejects_unknown_decision() -> None:
    service = _service()
    with pytest.raises(InvalidCreditReview, match="ok, hold albo refuse"):
        await service.create_review(
            organization_id=uuid4(),
            user_id=uuid4(),
            party_id=uuid4(),
            review_date=date(2026, 9, 1),
            decision="maybe",
        )


@pytest.mark.asyncio
async def test_resolve_review_returns_row() -> None:
    service = _service()
    party_id = uuid4()
    row = _row(party_id=party_id, review_date=date(2026, 9, 1))
    service._parties.get = AsyncMock(return_value=SimpleNamespace(id=party_id))
    service._parties.find_review_as_of = AsyncMock(return_value=row)
    found = await service.resolve_review(party_id=party_id, on_date=date(2026, 9, 5))
    assert found.id == row.id


@pytest.mark.asyncio
async def test_resolve_review_unknown() -> None:
    service = _service()
    party_id = uuid4()
    service._parties.get = AsyncMock(return_value=SimpleNamespace(id=party_id))
    service._parties.find_review_as_of = AsyncMock(return_value=None)
    with pytest.raises(UnknownCreditReview, match="brak recenzji"):
        await service.resolve_review(party_id=party_id, on_date=date(2026, 9, 1))


@pytest.mark.asyncio
async def test_attach_bureau_keeps_source_ref_and_does_not_touch_limit() -> None:
    service = _service()
    row = _row(party_id=uuid4(), review_date=date(2026, 9, 1))
    origin = row.source_ref
    service._parties.get_review = AsyncMock(return_value=row)
    stored = await service.attach_bureau(row.id, "  file://wywiad/raport-2  ")
    assert stored.bureau_attachment_ref == "file://wywiad/raport-2"
    assert stored.source_ref == origin
    assert stored.decision == "ok"
    assert not hasattr(stored, "credit_limit")


@pytest.mark.asyncio
async def test_attach_bureau_unknown_review() -> None:
    service = _service()
    service._parties.get_review = AsyncMock(return_value=None)
    with pytest.raises(UnknownCreditReview, match="nieznana recenzja"):
        await service.attach_bureau(uuid4(), "file://wywiad/raport-3")


@pytest.mark.asyncio
async def test_list_reviews_returns_repository_rows() -> None:
    service = _service()
    row = _row(party_id=uuid4(), review_date=date(2026, 9, 1))
    service._parties.list_reviews = AsyncMock(return_value=[row])
    listed = await service.list_reviews()
    assert listed == [row]
