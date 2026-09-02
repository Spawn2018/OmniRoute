from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import CustomerRfqConflict, ResourceNotFound
from app.main import app
from app.models.customer_rfq import CustomerRfq
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
        self.row: InboundMessage | None = None

    async def get_message(self, message_id: UUID) -> InboundMessage:
        if self.row is None or self.row.id != message_id:
            raise ResourceNotFound(f"nieznana wiadomość: {message_id}")
        return self.row


class StubCustomerRfqService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[CustomerRfq] = []

    async def list_rfqs(self) -> list[CustomerRfq]:
        return list(self.rows)

    async def create_rfq(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        inbound_message_id: UUID,
        source_ref: str,
        party_id: UUID | None,
    ) -> CustomerRfq:
        if any(row.inbound_message_id == inbound_message_id for row in self.rows):
            raise CustomerRfqConflict("to zapytanie już istnieje dla tej wiadomości")
        row = CustomerRfq(
            id=uuid4(),
            organization_id=organization_id,
            inbound_message_id=inbound_message_id,
            source_ref=source_ref,
            status="draft",
            party_id=party_id,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    messages = StubInboundMessageService(object())
    rfqs = StubCustomerRfqService(object())

    def _messages(_session: object) -> StubInboundMessageService:
        return messages

    def _rfqs(_session: object) -> StubCustomerRfqService:
        return rfqs

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.customer_rfqs.InboundMessageService", _messages)
    monkeypatch.setattr("app.api.customer_rfqs.CustomerRfqService", _rfqs)
    messages.row = InboundMessage(
        id=uuid4(),
        organization_id=uuid4(),
        source_ref="fixture://inbound-mail/1",
        from_address="ops@carrier.example",
        subject="RFQ",
        body_text="1x40HC",
        status="draft",
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), messages, rfqs
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_customer_rfq(catalog_client: object) -> None:
    client, messages, _rfqs = catalog_client
    assert messages.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/customer-rfqs",
        headers=headers,
        json={"inbound_message_id": str(messages.row.id)},
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["inbound_message_id"] == str(messages.row.id)
    assert body["source_ref"] == "fixture://inbound-mail/1"
    assert body["status"] == "draft"
    assert "amount" not in body
    assert "rate_line" not in body

    listed = client.get("/api/v1/customer-rfqs", headers=headers)
    assert listed.status_code == 200
    rows = listed.json()
    assert len(rows) == 1
    assert rows[0]["id"] == body["id"]


def test_http_create_rfq_unknown_message_is_404(catalog_client: object) -> None:
    client, _messages, _rfqs = catalog_client
    response = client.post(
        "/api/v1/customer-rfqs",
        headers=bearer_auth_headers(),
        json={"inbound_message_id": str(uuid4())},
    )
    assert response.status_code == 404


def test_http_duplicate_rfq_for_message_is_conflict(catalog_client: object) -> None:
    client, messages, _rfqs = catalog_client
    assert messages.row is not None
    headers = bearer_auth_headers()
    payload = {"inbound_message_id": str(messages.row.id)}
    first = client.post("/api/v1/customer-rfqs", headers=headers, json=payload)
    assert first.status_code == 201
    second = client.post("/api/v1/customer-rfqs", headers=headers, json=payload)
    assert second.status_code == 400
    assert "już istnieje" in second.json()["detail"]
