from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.main import app
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
    assert "amount" not in body
    assert "party_id" not in body

    listed = catalog_client.get("/api/v1/inbound-messages", headers=headers)
    assert listed.status_code == 200
    rows = listed.json()
    assert len(rows) == 1
    assert rows[0]["id"] == body["id"]


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
