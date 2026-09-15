from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.accept_extraction import ExtractionAcceptResult
from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import (
    DraftNotPending,
    ResourceNotFound,
    UnknownChargeCode,
)
from app.domain.extraction_draft import (
    require_extraction_draft_kind,
    require_rate_candidates_editable,
    undo_extraction_history,
)
from app.main import app
from app.models.extraction_draft import ExtractionDraft
from app.models.rate_line import RateLine
from tests.http_auth import bearer_auth_headers

_NOW = datetime(2026, 8, 31, 12, 0, tzinfo=UTC)


class AllowAllAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class StubExtractionService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.draft: ExtractionDraft | None = None

    async def extract_to_draft(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        source_ref: str,
        input_text: str,
        parser_name: str = "plain",
        parser_challenger: str | None = None,
        ab_delta_chars: int | None = None,
        **_unused: object,
    ) -> ExtractionDraft:
        kind = require_extraction_draft_kind(_unused.get("draft_kind"))
        extract_path = _unused.get("extract_path") or "text"
        self.draft = ExtractionDraft(
            id=uuid4(),
            organization_id=organization_id,
            status="pending",
            draft_kind=kind,
            source_ref=source_ref,
            input_text=input_text,
            payload={
                "source_ref": source_ref,
                "unparsed_regions": [],
                "candidates": [{"code": "THC", "amount_text": "10", "currency": "EUR"}],
                "parser_name": parser_name,
                "parser_challenger": parser_challenger,
                "ab_delta_chars": ab_delta_chars,
                "revision": 0,
                "extract_path": extract_path,
                "history": [],
            },
            created_at=_NOW,
            updated_at=_NOW,
            created_by=user_id,
        )
        return self.draft

    async def extract_from_document(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        source_ref: str,
        raw_bytes: bytes,
        **_unused: object,
    ) -> ExtractionDraft:
        return await self.extract_to_draft(
            organization_id=organization_id,
            user_id=user_id,
            source_ref=source_ref,
            input_text=raw_bytes.decode("utf-8"),
            parser_name="stub",
            extract_path=_unused.get("extract_path"),
        )

    async def accept(self, *, draft_id: UUID, user_id: UUID) -> ExtractionDraft:
        if self.draft is None or self.draft.id != draft_id:
            raise AssertionError("accept bez wcześniejszego extract")
        self.draft.status = "accepted"
        self.draft.reviewed_by = user_id
        self.draft.reviewed_at = _NOW
        return self.draft

    async def reject(self, *, draft_id: UUID, user_id: UUID) -> ExtractionDraft:
        if self.draft is None or self.draft.id != draft_id:
            raise AssertionError("reject bez wcześniejszego extract")
        self.draft.status = "rejected"
        self.draft.reviewed_by = user_id
        self.draft.reviewed_at = _NOW
        return self.draft

    async def list_drafts(self, status: str | None = "pending") -> list[ExtractionDraft]:
        if self.draft is None:
            return []
        return [self.draft]

    async def patch_candidates(
        self,
        *,
        draft_id: UUID,
        candidates: list[dict[str, object]],
    ) -> ExtractionDraft:
        if self.draft is None or self.draft.id != draft_id:
            raise ResourceNotFound("Szkic ekstrakcji nie istnieje")
        if self.draft.status != "pending":
            raise DraftNotPending("Szkic nie jest w statusie pending")
        require_rate_candidates_editable(self.draft.draft_kind)
        payload = dict(self.draft.payload)
        prior_revision = payload.get("revision")
        prior_candidates = payload.get("candidates")
        history = payload.get("history")
        entries = list(history) if type(history) is list else []
        entries.append(
            {
                "revision": prior_revision if type(prior_revision) is int else 0,
                "candidates": list(prior_candidates) if type(prior_candidates) is list else [],
            },
        )
        payload["history"] = entries
        payload["candidates"] = candidates
        current = payload.get("revision")
        payload["revision"] = current + 1 if type(current) is int else 1
        self.draft.payload = payload
        return self.draft

    async def undo_candidates(self, *, draft_id: UUID) -> ExtractionDraft:
        if self.draft is None or self.draft.id != draft_id:
            raise ResourceNotFound("Szkic ekstrakcji nie istnieje")
        if self.draft.status != "pending":
            raise DraftNotPending("Szkic nie jest w statusie pending")
        require_rate_candidates_editable(self.draft.draft_kind)
        undone = undo_extraction_history(self.draft.payload.get("history"))
        payload = dict(self.draft.payload)
        payload["history"] = undone.history
        payload["candidates"] = undone.candidates
        payload["revision"] = undone.revision
        self.draft.payload = payload
        return self.draft


class StubAcceptToRates:
    def __init__(self, _session: object, stub: StubExtractionService) -> None:
        self._stub = stub

    async def accept(
        self,
        *,
        draft_id: UUID,
        user_id: UUID,
        candidate_indexes: list[int] | None = None,
    ) -> ExtractionAcceptResult:
        draft = await self._stub.accept(draft_id=draft_id, user_id=user_id)
        rate = RateLine(
            id=uuid4(),
            organization_id=draft.organization_id,
            charge_code="THC",
            amount="10.0000",
            currency="EUR",
            source_ref=draft.source_ref,
        )
        if candidate_indexes is not None and len(candidate_indexes) == 0:
            raise AssertionError("puste indeksy")
        return ExtractionAcceptResult(draft, [rate], [])


@pytest.fixture
def happy_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubExtractionService(object())

    def _factory(session: object) -> StubExtractionService:
        return stub

    def _orchestrator(session: object) -> StubAcceptToRates:
        return StubAcceptToRates(session, stub)

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.extractions.ExtractionService", _factory)
    monkeypatch.setattr("app.api.extractions.AcceptExtractionToRates", _orchestrator)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_extract_input_text_creates_pending_draft(happy_client: TestClient) -> None:
    org_id = uuid4()
    user_id = uuid4()
    response = happy_client.post(
        "/api/v1/extractions",
        headers=bearer_auth_headers(organization_id=org_id, user_id=user_id),
        json={"source_ref": "doc://x", "input_text": "THC 10 EUR"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "pending"
    assert body["organization_id"] == str(org_id)
    assert body["source_ref"] == "doc://x"
    assert body["payload"]["candidates"][0]["amount_text"] == "10"
    assert body["rate_line_ids"] == []
    assert "rate_line" not in body["payload"]


def test_http_extract_document_base64_creates_pending_draft(happy_client: TestClient) -> None:
    response = happy_client.post(
        "/api/v1/extractions",
        headers=bearer_auth_headers(),
        json={"source_ref": "doc://pdf", "document_base64": "VEhDIDEwIEVVUg=="},
    )
    assert response.status_code == 201
    assert response.json()["status"] == "pending"
    assert response.json()["payload"]["parser_name"] == "stub"
    assert response.json()["payload"]["extract_path"] == "text"


def test_http_extract_document_image_path_still_uses_stub_parser(
    happy_client: TestClient,
) -> None:
    response = happy_client.post(
        "/api/v1/extractions",
        headers=bearer_auth_headers(),
        json={
            "source_ref": "doc://pdf",
            "document_base64": "VEhDIDEwIEVVUg==",
            "extract_path": "image",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["payload"]["extract_path"] == "image"
    assert body["payload"]["parser_name"] == "stub"
    assert body["payload"]["candidates"][0]["code"] == "THC"


def test_http_accept_marks_draft_accepted(happy_client: TestClient) -> None:
    org_id = uuid4()
    user_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id, user_id=user_id)
    created = happy_client.post(
        "/api/v1/extractions",
        headers=headers,
        json={"source_ref": "doc://x", "input_text": "THC 10 EUR"},
    )
    draft_id = created.json()["id"]
    accepted = happy_client.post(f"/api/v1/extractions/{draft_id}/accept", headers=headers)
    assert accepted.status_code == 200
    body = accepted.json()
    assert body["status"] == "accepted"
    assert body["reviewed_by"] == str(user_id)
    assert len(body["rate_line_ids"]) == 1
    assert "rate_line" not in body["payload"]


def test_http_reject_marks_draft_rejected(happy_client: TestClient) -> None:
    headers = bearer_auth_headers()
    created = happy_client.post(
        "/api/v1/extractions",
        headers=headers,
        json={"source_ref": "doc://x", "input_text": "THC 10 EUR"},
    )
    draft_id = created.json()["id"]
    rejected = happy_client.post(f"/api/v1/extractions/{draft_id}/reject", headers=headers)
    assert rejected.status_code == 200
    assert rejected.json()["status"] == "rejected"


def test_http_list_returns_created_draft(happy_client: TestClient) -> None:
    headers = bearer_auth_headers()
    created = happy_client.post(
        "/api/v1/extractions",
        headers=headers,
        json={"source_ref": "doc://x", "input_text": "THC 10 EUR"},
    )
    listed = happy_client.get("/api/v1/extractions", headers=headers)
    assert listed.status_code == 200
    rows = listed.json()
    assert len(rows) == 1
    assert rows[0]["id"] == created.json()["id"]


def test_http_accept_unknown_code_returns_polish_400(monkeypatch: pytest.MonkeyPatch) -> None:
    stub = StubExtractionService(object())

    class _FailingOrchestrator:
        def __init__(self, _session: object) -> None:
            pass

        async def accept(self, *, draft_id: UUID, user_id: UUID, **_unused: object):
            await stub.accept(draft_id=draft_id, user_id=user_id)
            raise UnknownChargeCode("nieznany kod opłaty: LOOSE")

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.extractions.ExtractionService", lambda session: stub)
    monkeypatch.setattr("app.api.extractions.AcceptExtractionToRates", _FailingOrchestrator)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    client = TestClient(app)
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/extractions",
        headers=headers,
        json={"source_ref": "doc://x", "input_text": "THC 10 EUR"},
    )
    draft_id = created.json()["id"]
    accepted = client.post(f"/api/v1/extractions/{draft_id}/accept", headers=headers)
    app.dependency_overrides.clear()
    set_authz_checker(None)
    assert accepted.status_code == 400
    assert accepted.json()["detail"] == "nieznany kod opłaty: LOOSE"


def test_http_extract_rejects_invalid_base64(happy_client: TestClient) -> None:
    response = happy_client.post(
        "/api/v1/extractions",
        headers=bearer_auth_headers(),
        json={"source_ref": "doc://x", "document_base64": "%%%"},
    )
    assert response.status_code == 400


def test_http_rejects_unknown_draft_kind(happy_client: TestClient) -> None:
    response = happy_client.post(
        "/api/v1/extractions",
        headers=bearer_auth_headers(),
        json={
            "source_ref": "doc://x",
            "input_text": "oferta",
            "draft_kind": "purchase_invoice",
        },
    )
    assert response.status_code == 400
    assert "allowlist" in response.json()["detail"]


def test_http_patch_pending_rate_line_replaces_candidates(happy_client: TestClient) -> None:
    headers = bearer_auth_headers()
    created = happy_client.post(
        "/api/v1/extractions",
        headers=headers,
        json={"source_ref": "doc://x", "input_text": "THC 10 EUR"},
    )
    draft_id = created.json()["id"]
    patched = happy_client.patch(
        f"/api/v1/extractions/{draft_id}",
        headers=headers,
        json={
            "candidates": [
                {"code": "BAF", "amount_text": "12", "currency": "USD", "note": "HITL"},
            ],
        },
    )
    assert patched.status_code == 200
    body = patched.json()
    assert body["payload"]["candidates"] == [
        {
            "code": "BAF",
            "amount_text": "12",
            "currency": "USD",
            "note": "HITL",
            "bbox_text": "",
            "confidence_text": "",
        },
    ]
    assert body["payload"]["source_ref"] == "doc://x"
    listed = happy_client.get("/api/v1/extractions", headers=headers)
    assert listed.json()[0]["payload"]["candidates"][0]["code"] == "BAF"
    assert created.json()["payload"]["revision"] == 0
    assert created.json()["payload"]["history"] == []
    assert body["payload"]["revision"] == 1
    assert body["payload"]["history"] == [
        {
            "revision": 0,
            "candidates": [
                {"code": "THC", "amount_text": "10", "currency": "EUR"},
            ],
        },
    ]


def test_http_undo_restores_prior_candidates(happy_client: TestClient) -> None:
    headers = bearer_auth_headers()
    created = happy_client.post(
        "/api/v1/extractions",
        headers=headers,
        json={"source_ref": "doc://x", "input_text": "THC 10 EUR"},
    )
    draft_id = created.json()["id"]
    happy_client.patch(
        f"/api/v1/extractions/{draft_id}",
        headers=headers,
        json={
            "candidates": [
                {"code": "BAF", "amount_text": "12", "currency": "USD"},
            ],
        },
    )
    undone = happy_client.post(f"/api/v1/extractions/{draft_id}/undo", headers=headers)
    assert undone.status_code == 200
    body = undone.json()
    assert body["payload"]["revision"] == 0
    assert body["payload"]["history"] == []
    assert body["payload"]["candidates"][0]["code"] == "THC"


def test_http_undo_empty_history_returns_400(happy_client: TestClient) -> None:
    headers = bearer_auth_headers()
    created = happy_client.post(
        "/api/v1/extractions",
        headers=headers,
        json={"source_ref": "doc://x", "input_text": "THC 10 EUR"},
    )
    draft_id = created.json()["id"]
    response = happy_client.post(f"/api/v1/extractions/{draft_id}/undo", headers=headers)
    assert response.status_code == 400


def test_http_patch_not_pending_returns_409(happy_client: TestClient) -> None:
    headers = bearer_auth_headers()
    created = happy_client.post(
        "/api/v1/extractions",
        headers=headers,
        json={"source_ref": "doc://x", "input_text": "THC 10 EUR"},
    )
    draft_id = created.json()["id"]
    happy_client.post(f"/api/v1/extractions/{draft_id}/reject", headers=headers)
    patched = happy_client.patch(
        f"/api/v1/extractions/{draft_id}",
        headers=headers,
        json={"candidates": [{"code": "THC", "amount_text": "11", "currency": "EUR"}]},
    )
    assert patched.status_code == 409


def test_http_extract_defaults_path_text(happy_client: TestClient) -> None:
    response = happy_client.post(
        "/api/v1/extractions",
        headers=bearer_auth_headers(),
        json={"source_ref": "doc://x", "input_text": "THC 10 EUR"},
    )
    assert response.status_code == 201
    assert response.json()["payload"]["extract_path"] == "text"


def test_http_extract_records_image_path_without_vision(happy_client: TestClient) -> None:
    response = happy_client.post(
        "/api/v1/extractions",
        headers=bearer_auth_headers(),
        json={
            "source_ref": "doc://x",
            "input_text": "THC 10 EUR",
            "extract_path": "image",
        },
    )
    assert response.status_code == 201
    assert response.json()["payload"]["extract_path"] == "image"
    assert response.json()["payload"]["candidates"][0]["code"] == "THC"


def test_http_extract_rejects_unknown_path(happy_client: TestClient) -> None:
    response = happy_client.post(
        "/api/v1/extractions",
        headers=bearer_auth_headers(),
        json={
            "source_ref": "doc://x",
            "input_text": "THC 10 EUR",
            "extract_path": "pixels",
        },
    )
    assert response.status_code == 422


def test_http_extract_starts_revision_at_zero(happy_client: TestClient) -> None:
    response = happy_client.post(
        "/api/v1/extractions",
        headers=bearer_auth_headers(),
        json={"source_ref": "doc://x", "input_text": "THC 10 EUR"},
    )
    assert response.status_code == 201
    assert response.json()["payload"]["revision"] == 0


def test_http_patch_bbox_and_confidence_text(happy_client: TestClient) -> None:
    headers = bearer_auth_headers()
    created = happy_client.post(
        "/api/v1/extractions",
        headers=headers,
        json={"source_ref": "doc://x", "input_text": "THC 10 EUR"},
    )
    draft_id = created.json()["id"]
    patched = happy_client.patch(
        f"/api/v1/extractions/{draft_id}",
        headers=headers,
        json={
            "candidates": [
                {
                    "code": "THC",
                    "amount_text": "10",
                    "currency": "EUR",
                    "bbox_text": "10,20,80,40",
                    "confidence_text": "high",
                },
            ],
        },
    )
    assert patched.status_code == 200
    row = patched.json()["payload"]["candidates"][0]
    assert row["bbox_text"] == "10,20,80,40"
    assert row["confidence_text"] == "high"
    assert patched.json()["payload"]["revision"] == 1


def test_http_patch_float_confidence_returns_422(happy_client: TestClient) -> None:
    headers = bearer_auth_headers()
    created = happy_client.post(
        "/api/v1/extractions",
        headers=headers,
        json={"source_ref": "doc://x", "input_text": "THC 10 EUR"},
    )
    draft_id = created.json()["id"]
    patched = happy_client.patch(
        f"/api/v1/extractions/{draft_id}",
        headers=headers,
        json={
            "candidates": [
                {
                    "code": "THC",
                    "amount_text": "10",
                    "currency": "EUR",
                    "confidence": 0.9,
                },
            ],
        },
    )
    assert patched.status_code == 422


def test_http_patch_extra_field_returns_422(happy_client: TestClient) -> None:
    headers = bearer_auth_headers()
    created = happy_client.post(
        "/api/v1/extractions",
        headers=headers,
        json={"source_ref": "doc://x", "input_text": "THC 10 EUR"},
    )
    draft_id = created.json()["id"]
    patched = happy_client.patch(
        f"/api/v1/extractions/{draft_id}",
        headers=headers,
        json={
            "candidates": [{"code": "THC", "amount_text": "10", "currency": "EUR"}],
            "status": "accepted",
        },
    )
    assert patched.status_code == 422


def test_http_patch_computed_amount_returns_422(happy_client: TestClient) -> None:
    headers = bearer_auth_headers()
    created = happy_client.post(
        "/api/v1/extractions",
        headers=headers,
        json={"source_ref": "doc://x", "input_text": "THC 10 EUR"},
    )
    draft_id = created.json()["id"]
    patched = happy_client.patch(
        f"/api/v1/extractions/{draft_id}",
        headers=headers,
        json={
            "candidates": [
                {
                    "code": "THC",
                    "amount_text": "10",
                    "currency": "EUR",
                    "amount": "10.0000",
                },
            ],
        },
    )
    assert patched.status_code == 422


def test_http_patch_pending_tender_rfp_replaces_candidates(happy_client: TestClient) -> None:
    headers = bearer_auth_headers()
    created = happy_client.post(
        "/api/v1/extractions",
        headers=headers,
        json={
            "source_ref": "doc://rfp",
            "input_text": "RFP",
            "draft_kind": "tender_rfp",
            "rfp": {
                "tender_id": str(uuid4()),
                "intake_code": "scope",
            },
        },
    )
    draft_id = created.json()["id"]
    patched = happy_client.patch(
        f"/api/v1/extractions/{draft_id}",
        headers=headers,
        json={"candidates": [{"code": "THC", "amount_text": "1", "currency": "EUR"}]},
    )
    assert patched.status_code == 200
    body = patched.json()
    assert body["payload"]["candidates"] == [
        {
            "code": "THC",
            "amount_text": "1",
            "currency": "EUR",
            "note": "",
            "bbox_text": "",
            "confidence_text": "",
        },
    ]
    assert body["payload"]["revision"] == 1


def test_http_accepts_tender_rfp_draft_kind(happy_client: TestClient) -> None:
    response = happy_client.post(
        "/api/v1/extractions",
        headers=bearer_auth_headers(),
        json={
            "source_ref": "doc://rfp",
            "input_text": "RFP",
            "draft_kind": "tender_rfp",
            "rfp": {
                "tender_id": str(uuid4()),
                "intake_code": "scope",
            },
        },
    )
    assert response.status_code == 201
    assert response.json()["draft_kind"] == "tender_rfp"
