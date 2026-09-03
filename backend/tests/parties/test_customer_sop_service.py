from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.domain.errors import (
    CustomerSopAlreadyApproved,
    CustomerSopConflict,
    InvalidCustomerSop,
    UnknownCustomerSop,
    UnknownParty,
)
from app.models.customer_sop import CustomerSop
from app.services.parties.party_service import PartyService


def _service() -> PartyService:
    service = PartyService(MagicMock())
    service._parties = MagicMock()
    return service


def _row(*, party_id, code: str = "pre_alert", status: str = "draft") -> CustomerSop:
    return CustomerSop(
        id=uuid4(),
        organization_id=uuid4(),
        party_id=party_id,
        status=status,
        code=code,
        title="Pre-alert",
        body="wyślij pre-alert 24h przed",
        approved_at=None if status == "draft" else datetime.now(UTC),
        source_ref="tenant:manual",
    )


@pytest.mark.asyncio
async def test_create_sop_starts_as_draft_with_manual_origin() -> None:
    service = _service()
    party_id = uuid4()
    org_id = uuid4()

    async def add(row: CustomerSop) -> CustomerSop:
        return row

    service._parties.get = AsyncMock(return_value=SimpleNamespace(id=party_id))
    service._parties.find_sop_by_party_and_code = AsyncMock(return_value=None)
    service._parties.add_sop = add
    stored = await service.create_sop(
        organization_id=org_id,
        user_id=uuid4(),
        party_id=party_id,
        code=" Pre-Alert ",
        title="  Pre alert  ",
        body="  treść procedury  ",
    )
    assert stored.code == "pre_alert"
    assert stored.title == "Pre alert"
    assert stored.body == "treść procedury"
    assert stored.status == "draft"
    assert stored.approved_at is None
    assert stored.source_ref == "tenant:manual"
    assert stored.organization_id == org_id
    assert stored.blocks_auto is True


@pytest.mark.asyncio
async def test_create_sop_unknown_party() -> None:
    service = _service()
    service._parties.get = AsyncMock(return_value=None)
    with pytest.raises(UnknownParty, match="nieznany kontrahent"):
        await service.create_sop(
            organization_id=uuid4(),
            user_id=uuid4(),
            party_id=uuid4(),
            code="booking",
            title="Booking",
            body="zarezerwuj slot",
        )


@pytest.mark.asyncio
async def test_create_sop_rejects_duplicate_code() -> None:
    service = _service()
    party_id = uuid4()
    service._parties.get = AsyncMock(return_value=SimpleNamespace(id=party_id))
    service._parties.find_sop_by_party_and_code = AsyncMock(
        return_value=_row(party_id=party_id, code="booking"),
    )
    with pytest.raises(CustomerSopConflict, match="booking"):
        await service.create_sop(
            organization_id=uuid4(),
            user_id=uuid4(),
            party_id=party_id,
            code="booking",
            title="Booking",
            body="zarezerwuj slot",
        )


@pytest.mark.asyncio
async def test_create_sop_rejects_blank_body() -> None:
    service = _service()
    with pytest.raises(InvalidCustomerSop, match="treść"):
        await service.create_sop(
            organization_id=uuid4(),
            user_id=uuid4(),
            party_id=uuid4(),
            code="booking",
            title="Booking",
            body="  ",
        )


@pytest.mark.asyncio
async def test_resolve_sop_returns_row() -> None:
    service = _service()
    party_id = uuid4()
    row = _row(party_id=party_id, code="booking")
    service._parties.get = AsyncMock(return_value=SimpleNamespace(id=party_id))
    service._parties.find_sop_by_party_and_code = AsyncMock(return_value=row)
    found = await service.resolve_sop(party_id, " BOOKING ")
    assert found.id == row.id


@pytest.mark.asyncio
async def test_resolve_sop_unknown() -> None:
    service = _service()
    party_id = uuid4()
    service._parties.get = AsyncMock(return_value=SimpleNamespace(id=party_id))
    service._parties.find_sop_by_party_and_code = AsyncMock(return_value=None)
    with pytest.raises(UnknownCustomerSop, match="nieznana procedura"):
        await service.resolve_sop(party_id, "missing")


@pytest.mark.asyncio
async def test_approve_sop_sets_timestamp() -> None:
    service = _service()
    row = _row(party_id=uuid4(), status="draft")
    service._parties.get_sop = AsyncMock(return_value=row)
    approved = await service.approve_sop(row.id)
    assert approved.status == "approved"
    assert approved.approved_at is not None


@pytest.mark.asyncio
async def test_approve_sop_rejects_already_approved() -> None:
    service = _service()
    row = _row(party_id=uuid4(), status="approved")
    service._parties.get_sop = AsyncMock(return_value=row)
    with pytest.raises(CustomerSopAlreadyApproved, match="zatwierdzona"):
        await service.approve_sop(row.id)


@pytest.mark.asyncio
async def test_approve_sop_unknown() -> None:
    service = _service()
    service._parties.get_sop = AsyncMock(return_value=None)
    with pytest.raises(UnknownCustomerSop, match="nieznana procedura"):
        await service.approve_sop(uuid4())


@pytest.mark.asyncio
async def test_party_blocks_auto_requires_known_party() -> None:
    service = _service()
    service._parties.get = AsyncMock(return_value=None)
    with pytest.raises(UnknownParty):
        await service.party_blocks_auto(uuid4())


@pytest.mark.asyncio
async def test_party_blocks_auto_reads_repository() -> None:
    service = _service()
    party_id = uuid4()
    service._parties.get = AsyncMock(return_value=SimpleNamespace(id=party_id))
    service._parties.approved_sop_blocks_auto = AsyncMock(return_value=True)
    assert await service.party_blocks_auto(party_id) is True
