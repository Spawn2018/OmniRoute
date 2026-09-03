from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import UnknownNetworkMember
from app.main import app
from app.models.carrier_inquiry import CarrierInquiry
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


class StubInquiryService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[CarrierInquiry] = []

    async def list_inquiries(self) -> list[CarrierInquiry]:
        return list(self.rows)

    async def record_inquiry(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        network_member_id: UUID,
    ) -> CarrierInquiry:
        if network_member_id.hex == "0" * 32:
            raise UnknownNetworkMember("nieznany członek sieci")
        row = CarrierInquiry(
            id=uuid4(),
            organization_id=organization_id,
            network_member_id=network_member_id,
            source_ref="tenant:manual",
            status="draft",
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def inquiry_client(monkeypatch: pytest.MonkeyPatch) -> object:
    stub = StubInquiryService(object())

    def _service(_session: object) -> StubInquiryService:
        return stub

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.carrier_inquiries.CarrierInquiryService", _service)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), stub
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_records_and_lists_carrier_inquiry(inquiry_client: object) -> None:
    client, _stub = inquiry_client
    org_id = uuid4()
    member_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/carrier-inquiries",
        headers=headers,
        json={"network_member_id": str(member_id)},
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["network_member_id"] == str(member_id)
    assert body["source_ref"] == "tenant:manual"
    assert body["status"] == "draft"
    assert "amount" not in body
    listed = client.get("/api/v1/carrier-inquiries", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_unknown_member_is_400(inquiry_client: object) -> None:
    client, _stub = inquiry_client
    response = client.post(
        "/api/v1/carrier-inquiries",
        headers=bearer_auth_headers(),
        json={"network_member_id": "00000000-0000-0000-0000-000000000000"},
    )
    assert response.status_code == 400
    assert "członek" in response.json()["detail"]
