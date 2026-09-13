from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.ai_transforms.extraction.mock_extractor import MockExtractor
from app.domain.errors import (
    DraftNotPending,
    ExtractionCandidatesNotEditable,
    ResourceNotFound,
)
from app.integrations.langfuse.tracer import LangfuseTracer, PromptTrace
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


class _RecordingTracer(LangfuseTracer):
    def __init__(self) -> None:
        super().__init__(enabled=False)
        self.traces: list[PromptTrace] = []

    def finish(self, trace: PromptTrace) -> None:
        self.traces.append(trace)
        super().finish(trace)


@pytest.mark.asyncio
async def test_extract_records_trace_without_input_text() -> None:
    session = AsyncMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    tracer = _RecordingTracer()
    service = ExtractionService(session, extractor=MockExtractor(), tracer=tracer)

    await service.extract_to_draft(
        organization_id=uuid4(),
        user_id=uuid4(),
        source_ref="doc://x",
        input_text="THC 10 EUR secret-should-not-trace",
    )

    assert len(tracer.traces) == 1
    trace = tracer.traces[0]
    assert trace.name == "extract"
    assert trace.metadata["source_ref"] == "doc://x"
    assert trace.metadata["candidate_count"] == 1
    assert "input_text" not in trace.metadata
    assert "secret-should-not-trace" not in str(trace.metadata)


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
async def test_patch_candidates_replaces_only_candidates() -> None:
    session = AsyncMock()
    session.flush = AsyncMock()
    extractor = MagicMock()
    draft = ExtractionDraft(
        id=uuid4(),
        organization_id=uuid4(),
        status="pending",
        draft_kind="rate_line",
        source_ref="doc://x",
        input_text="THC 10 EUR",
        payload={
            "source_ref": "doc://x",
            "unparsed_regions": ["weekend"],
            "candidates": [{"code": "THC", "amount_text": "10", "currency": "EUR"}],
            "parser_name": "plain",
        },
    )
    session.get = AsyncMock(return_value=draft)
    service = ExtractionService(session, extractor=extractor)
    patched = await service.patch_candidates(
        draft_id=draft.id,
        candidates=[{"code": "BAF", "amount_text": "12", "currency": "USD", "note": "poprawka"}],
    )
    assert patched.payload["candidates"] == [
        {"code": "BAF", "amount_text": "12", "currency": "USD", "note": "poprawka"},
    ]
    assert patched.payload["source_ref"] == "doc://x"
    assert patched.payload["unparsed_regions"] == ["weekend"]
    assert patched.payload["parser_name"] == "plain"
    extractor.extract.assert_not_called()


@pytest.mark.asyncio
async def test_patch_candidates_rejects_non_pending() -> None:
    session = AsyncMock()
    draft = ExtractionDraft(
        id=uuid4(),
        organization_id=uuid4(),
        status="accepted",
        draft_kind="rate_line",
        source_ref="doc://x",
        input_text="x",
        payload={"source_ref": "doc://x", "unparsed_regions": [], "candidates": []},
    )
    session.get = AsyncMock(return_value=draft)
    service = ExtractionService(session, extractor=MagicMock())
    with pytest.raises(DraftNotPending):
        await service.patch_candidates(draft_id=draft.id, candidates=[])


@pytest.mark.asyncio
async def test_patch_candidates_rejects_non_rate_line() -> None:
    session = AsyncMock()
    draft = ExtractionDraft(
        id=uuid4(),
        organization_id=uuid4(),
        status="pending",
        draft_kind="tender_rfp",
        source_ref="doc://rfp",
        input_text="RFP",
        payload={"source_ref": "doc://rfp", "unparsed_regions": [], "candidates": []},
    )
    session.get = AsyncMock(return_value=draft)
    service = ExtractionService(session, extractor=MagicMock())
    with pytest.raises(ExtractionCandidatesNotEditable):
        await service.patch_candidates(
            draft_id=draft.id,
            candidates=[{"code": "THC", "amount_text": "1", "currency": "EUR"}],
        )


@pytest.mark.asyncio
async def test_list_drafts_delegates() -> None:
    session = AsyncMock()
    session.scalars = AsyncMock(
        return_value=MagicMock(all=MagicMock(return_value=[])),
    )
    service = ExtractionService(session)
    assert await service.list_drafts("pending") == []
