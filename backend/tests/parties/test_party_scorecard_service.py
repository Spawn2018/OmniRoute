from datetime import UTC, datetime
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.domain.errors import InvalidPartyScorecard, ResourceNotFound, UnknownPartyScorecard
from app.models.party_scorecard import PartyScorecard
from app.services.parties.party_service import PartyService


def _service() -> PartyService:
    service = PartyService(MagicMock())
    service._parties = MagicMock()
    return service


def _card(*, party_id, response_rate: Decimal | None = Decimal("0.5000")) -> PartyScorecard:
    return PartyScorecard(
        id=uuid4(),
        organization_id=uuid4(),
        party_id=party_id,
        window_days=90,
        sample_size=2,
        response_rate=response_rate,
        source_ref="tenant:manual",
        computed_at=datetime.now(UTC),
    )


@pytest.mark.asyncio
async def test_get_scorecard_unknown_party_is_not_found() -> None:
    service = _service()
    service._parties.get = AsyncMock(return_value=None)
    with pytest.raises(ResourceNotFound):
        await service.get_scorecard(uuid4())


@pytest.mark.asyncio
async def test_get_scorecard_missing_card() -> None:
    service = _service()
    party_id = uuid4()
    service._parties.get = AsyncMock(return_value=SimpleNamespace(id=party_id))
    service._parties.get_scorecard = AsyncMock(return_value=None)
    with pytest.raises(UnknownPartyScorecard, match="brak karty"):
        await service.get_scorecard(party_id)


@pytest.mark.asyncio
async def test_upsert_scorecard_rejects_rate_above_one() -> None:
    service = _service()
    party_id = uuid4()
    service._parties.get = AsyncMock(return_value=SimpleNamespace(id=party_id))
    with pytest.raises(InvalidPartyScorecard, match="0–1"):
        await service.upsert_scorecard(
            organization_id=uuid4(),
            user_id=uuid4(),
            party_id=party_id,
            response_rate="1.2",
        )


@pytest.mark.asyncio
async def test_upsert_scorecard_updates_existing_snapshot() -> None:
    service = _service()
    party_id = uuid4()
    existing = _card(party_id=party_id, response_rate=Decimal("0.1000"))
    service._parties.get = AsyncMock(return_value=SimpleNamespace(id=party_id))
    service._parties.get_scorecard = AsyncMock(return_value=existing)
    updated = await service.upsert_scorecard(
        organization_id=existing.organization_id,
        user_id=uuid4(),
        party_id=party_id,
        response_rate="0.7500",
        sample_size=4,
        window_days=30,
    )
    assert updated.id == existing.id
    assert updated.response_rate == Decimal("0.7500")
    assert updated.sample_size == 4
    assert updated.window_days == 30
    assert updated.source_ref == "tenant:manual"
    service._parties.add_scorecard.assert_not_called()


@pytest.mark.asyncio
async def test_upsert_scorecard_inserts_when_missing() -> None:
    service = _service()
    party_id = uuid4()
    created = _card(party_id=party_id)

    async def add(row: PartyScorecard) -> PartyScorecard:
        return row

    service._parties.get = AsyncMock(return_value=SimpleNamespace(id=party_id))
    service._parties.get_scorecard = AsyncMock(return_value=None)
    service._parties.add_scorecard = add
    stored = await service.upsert_scorecard(
        organization_id=created.organization_id,
        user_id=uuid4(),
        party_id=party_id,
        response_rate="0.4000",
        sample_size=1,
        window_days=45,
    )
    assert stored.party_id == party_id
    assert stored.response_rate == Decimal("0.4000")
    assert stored.window_days == 45
    assert stored.source_ref == "tenant:manual"
