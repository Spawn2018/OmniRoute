from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.accept_extraction import ExtractionAcceptResult
from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.extraction_draft import require_extraction_draft_kind
from app.domain.errors import UnknownChargeCode
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


class StubAcceptToRates:
    def __init__(self, _session: object, stub: StubExtractionService) -> None:
        self._stub = stub

    async def accept(
        self,
        *,
        draft_id: UUID,
        user_id: UUID,
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

        async def accept(self, *, draft_id: UUID, user_id: UUID):
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
