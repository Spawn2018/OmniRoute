from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.main import app
from app.models.extraction_draft import ExtractionDraft
from app.models.inbound_message import InboundMessage
from tests.http_auth import bearer_auth_headers


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


class StubInboundMessageService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[InboundMessage] = []

    async def list_messages(self) -> list[InboundMessage]:
        return list(self.rows)

    async def create_message(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        source_ref: str,
        from_address: str,
        subject: str,
        body_text: str,
    ) -> InboundMessage:
        row = InboundMessage(
            id=uuid4(),
            organization_id=organization_id,
            source_ref=source_ref.strip(),
            from_address=from_address.strip().lower(),
            subject=subject.strip(),
            body_text=body_text.strip(),
            status="draft",
            created_by=user_id,
        )
        self.rows.append(row)
        return row

    async def get_message(self, message_id: UUID) -> InboundMessage:
        for row in self.rows:
            if row.id == message_id:
                return row
        raise ResourceNotFound(f"nieznana wiadomość: {message_id}")

    async def attach_party(self, message_id: UUID, party_id: UUID) -> InboundMessage:
        row = await self.get_message(message_id)
        row.party_id = party_id
        return row

    async def ingest_by_external_id(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        external_id: str,
        source_ref: str,
        from_address: str,
        subject: str,
        body_text: str,
        require_origin: object,
    ) -> InboundMessage:
        _ = require_origin
        for row in self.rows:
            if row.external_id == external_id:
                return row
        row = InboundMessage(
            id=uuid4(),
            organization_id=organization_id,
            source_ref=source_ref,
            from_address=from_address,
            subject=subject,
            body_text=body_text,
            status="draft",
            external_id=external_id,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


class StubPartyService:
    last_id = uuid4()

    def __init__(self, session: object) -> None:
        self._session = session

    async def resolve_email(self, raw: str) -> object:
        _ = raw
        return type("PartyRow", (), {"id": StubPartyService.last_id})()


class StubOutboxEventService:
    recorded: list[object] = []

    def __init__(self, session: object) -> None:
        self._session = session

    async def record_message_saved(self, **kwargs: object) -> None:
        StubOutboxEventService.recorded.append(kwargs)


class StubExtractionService:
    last_text = ""

    def __init__(self, session: object) -> None:
        self._session = session

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
    ) -> ExtractionDraft:
        _ = parser_name, parser_challenger, ab_delta_chars
        StubExtractionService.last_text = input_text
        return ExtractionDraft(
            id=uuid4(),
            organization_id=organization_id,
            status="pending",
            source_ref=source_ref,
            input_text=input_text,
            payload={"source_ref": source_ref, "candidates": [], "unparsed_regions": []},
            created_by=user_id,
        )


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubInboundMessageService(object())

    def _factory(session: object) -> StubInboundMessageService:
        return stub

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.inbound_messages.InboundMessageService",
        _factory,
    )
    monkeypatch.setattr(
        "app.api.inbound_messages.PartyService",
        StubPartyService,
    )
    monkeypatch.setattr(
        "app.api.inbound_messages.ExtractionService",
        StubExtractionService,
    )
    StubOutboxEventService.recorded = []
    monkeypatch.setattr(
        "app.api.inbound_messages.OutboxEventService",
        StubOutboxEventService,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_inbound_messages(catalog_client: TestClient) -> None:
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = catalog_client.post(
        "/api/v1/inbound-messages",
        headers=headers,
        json={
            "source_ref": "fixture://inbound-mail/1",
            "from_address": "ops@carrier.example",
            "subject": "RFQ Gdynia",
            "body_text": "1x40HC",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["source_ref"] == "fixture://inbound-mail/1"
    assert body["status"] == "draft"
    assert body["party_id"] is None
    assert "amount" not in body

    listed = catalog_client.get("/api/v1/inbound-messages", headers=headers)
    assert listed.status_code == 200
    rows = listed.json()
    assert len(rows) == 1
    assert rows[0]["id"] == body["id"]
    assert len(StubOutboxEventService.recorded) == 1


def test_http_create_rejects_client_status(catalog_client: TestClient) -> None:
    response = catalog_client.post(
        "/api/v1/inbound-messages",
        headers=bearer_auth_headers(),
        json={
            "source_ref": "fixture://inbound-mail/1",
            "from_address": "ops@carrier.example",
            "subject": "RFQ",
            "body_text": "treść",
            "status": "accepted",
        },
    )
    assert response.status_code == 422


def test_http_resolve_email_attaches_party(catalog_client: TestClient) -> None:
    headers = bearer_auth_headers()
    created = catalog_client.post(
        "/api/v1/inbound-messages",
        headers=headers,
        json={
            "source_ref": "fixture://inbound-mail/1",
            "from_address": "ops@carrier.example",
            "subject": "RFQ",
            "body_text": "treść",
        },
    )
    message_id = created.json()["id"]
    resolved = catalog_client.post(
        f"/api/v1/inbound-messages/{message_id}/resolve-email",
        headers=headers,
    )
    assert resolved.status_code == 200
    assert resolved.json()["party_id"] == str(StubPartyService.last_id)


def test_http_extract_creates_pending_draft_without_rate_line(
    catalog_client: TestClient,
) -> None:
    headers = bearer_auth_headers()
    created = catalog_client.post(
        "/api/v1/inbound-messages",
        headers=headers,
        json={
            "source_ref": "fixture://inbound-mail/1",
            "from_address": "ops@carrier.example",
            "subject": "RFQ",
            "body_text": "1x40HC",
        },
    )
    message_id = created.json()["id"]
    extracted = catalog_client.post(
        f"/api/v1/inbound-messages/{message_id}/extract",
        headers=headers,
    )
    assert extracted.status_code == 201
    body = extracted.json()
    assert body["status"] == "pending"
    assert body["source_ref"] == "fixture://inbound-mail/1"
    assert "rate_line" not in body
    assert StubExtractionService.last_text == "RFQ\n\n1x40HC"


def test_http_extract_unknown_message_is_404(catalog_client: TestClient) -> None:
    response = catalog_client.post(
        f"/api/v1/inbound-messages/{uuid4()}/extract",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 404


def test_http_ingest_graph_is_idempotent_on_external_id(catalog_client: TestClient) -> None:
    headers = bearer_auth_headers()
    payload = {
        "external_id": "AAMk-demo-1",
        "source_ref": "graph://inbox/1",
        "from_address": "ops@carrier.example",
        "subject": "RFQ Graph",
        "body_text": "1x40HC",
    }
    first = catalog_client.post(
        "/api/v1/inbound-messages/ingest-graph",
        headers=headers,
        json=payload,
    )
    assert first.status_code == 200
    assert first.json()["external_id"] == "AAMk-demo-1"
    assert first.json()["source_ref"] == "graph://inbox/1"
    second = catalog_client.post(
        "/api/v1/inbound-messages/ingest-graph",
        headers=headers,
        json=payload,
    )
    assert second.status_code == 200
    assert second.json()["id"] == first.json()["id"]


def test_http_ingest_mailbox_is_idempotent_on_external_id(catalog_client: TestClient) -> None:
    headers = bearer_auth_headers()
    payload = {
        "external_id": "uid-demo-1",
        "source_ref": "imap://inbox/1",
        "from_address": "ops@carrier.example",
        "subject": "RFQ mailbox",
        "body_text": "1x40HC",
    }
    first = catalog_client.post(
        "/api/v1/inbound-messages/ingest-imap",
        headers=headers,
        json=payload,
    )
    assert first.status_code == 200
    assert first.json()["external_id"] == "uid-demo-1"
    second = catalog_client.post(
        "/api/v1/inbound-messages/ingest-imap",
        headers=headers,
        json=payload,
    )
    assert second.status_code == 200
    assert second.json()["id"] == first.json()["id"]
