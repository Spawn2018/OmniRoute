from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.ai_transforms.extraction.mock_extractor import MockExtractor
from app.domain.errors import DraftNotPending, ResourceNotFound
from app.models.extraction_draft import ExtractionDraft
from app.services.extraction.extraction_service import ExtractionService


@pytest.mark.asyncio
async def test_extract_to_draft_stores_payload_without_rate_line() -> None:
    session = AsyncMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    service = ExtractionService(session, extractor=MockExtractor())
    org_id = uuid4()
    user_id = uuid4()

    draft = await service.extract_to_draft(
        organization_id=org_id,
        user_id=user_id,
        source_ref="doc://x",
        input_text="THC 10 EUR",
    )

    assert draft.status == "pending"
    assert draft.payload["source_ref"] == "doc://x"
    assert "unparsed_regions" in draft.payload
    assert draft.payload["candidates"][0]["code"] == "THC"
    session.add.assert_called_once()


@pytest.mark.asyncio
async def test_accept_marks_pending_only() -> None:
    session = AsyncMock()
    session.flush = AsyncMock()
    draft = ExtractionDraft(
        id=uuid4(),
        organization_id=uuid4(),
        status="pending",
        source_ref="doc://x",
        input_text="THC 10 EUR",
        payload={"source_ref": "doc://x", "unparsed_regions": [], "candidates": []},
    )
    session.get = AsyncMock(return_value=draft)
    service = ExtractionService(session)
    user_id = uuid4()

    accepted = await service.accept(draft_id=draft.id, user_id=user_id)
    assert accepted.status == "accepted"
    assert accepted.reviewed_by == user_id
    assert accepted.reviewed_at is not None


@pytest.mark.asyncio
async def test_accept_rejects_non_pending() -> None:
    session = AsyncMock()
    draft = ExtractionDraft(
        id=uuid4(),
        organization_id=uuid4(),
        status="accepted",
        source_ref="doc://x",
        input_text="x",
        payload={"source_ref": "doc://x", "unparsed_regions": [], "candidates": []},
    )
    session.get = AsyncMock(return_value=draft)
    service = ExtractionService(session)
    with pytest.raises(DraftNotPending):
        await service.accept(draft_id=draft.id, user_id=uuid4())


@pytest.mark.asyncio
async def test_accept_missing_draft() -> None:
    session = AsyncMock()
    session.get = AsyncMock(return_value=None)
    service = ExtractionService(session)
    with pytest.raises(ResourceNotFound):
        await service.accept(draft_id=uuid4(), user_id=uuid4())


@pytest.mark.asyncio
async def test_reject_marks_pending() -> None:
    session = AsyncMock()
    session.flush = AsyncMock()
    draft = ExtractionDraft(
        id=uuid4(),
        organization_id=uuid4(),
        status="pending",
        source_ref="doc://x",
        input_text="THC 10 EUR",
        payload={"source_ref": "doc://x", "unparsed_regions": [], "candidates": []},
    )
    session.get = AsyncMock(return_value=draft)
    service = ExtractionService(session)
    user_id = uuid4()

    rejected = await service.reject(draft_id=draft.id, user_id=user_id)
    assert rejected.status == "rejected"
    assert rejected.reviewed_by == user_id


@pytest.mark.asyncio
async def test_list_drafts_delegates() -> None:
    session = AsyncMock()
    session.scalars = AsyncMock(
        return_value=MagicMock(all=MagicMock(return_value=[])),
    )
    service = ExtractionService(session)
    assert await service.list_drafts("pending") == []
