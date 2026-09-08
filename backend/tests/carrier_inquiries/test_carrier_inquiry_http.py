from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.carrier_inquiry import (
    carrier_inquiry_draft_status,
    require_answered_quote,
    require_inquiry_status,
    require_member_batch,
)
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
        status: object = None,
        origin_port_id: object = None,
        destination_port_id: object = None,
        quoted_amount: object = None,
        quoted_currency: object = None,
        quoted_transit_days: object = None,
    ) -> CarrierInquiry:
        if network_member_id.hex == "0" * 32:
            raise UnknownNetworkMember("nieznany członek sieci")
        token = require_inquiry_status(
            carrier_inquiry_draft_status() if status is None else status,
        )
        money, iso, days = require_answered_quote(
            status=token,
            quoted_amount=quoted_amount,
            quoted_currency=quoted_currency,
            quoted_transit_days=quoted_transit_days,
        )
        _ = origin_port_id, destination_port_id
        row = CarrierInquiry(
            id=uuid4(),
            organization_id=organization_id,
            network_member_id=network_member_id,
            source_ref="tenant:manual",
            status=token,
            quoted_amount=money,
            quoted_currency=iso,
            quoted_transit_days=days,
            created_by=user_id,
        )
        self.rows.append(row)
        return row

    async def record_batch(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        network_member_ids: object,
        status: object = None,
        origin_port_id: object = None,
        destination_port_id: object = None,
        quoted_amount: object = None,
        quoted_currency: object = None,
        quoted_transit_days: object = None,
    ) -> list[CarrierInquiry]:
        rows: list[CarrierInquiry] = []
        for member_id in require_member_batch(network_member_ids):
            rows.append(
                await self.record_inquiry(
                    organization_id=organization_id,
                    user_id=user_id,
                    network_member_id=member_id,
                    status=status,
                    origin_port_id=origin_port_id,
                    destination_port_id=destination_port_id,
                    quoted_amount=quoted_amount,
                    quoted_currency=quoted_currency,
                    quoted_transit_days=quoted_transit_days,
                ),
            )
        return rows


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
    assert body["quoted_amount"] is None
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


def test_http_unknown_status_is_400(inquiry_client: object) -> None:
    client, _stub = inquiry_client
    response = client.post(
        "/api/v1/carrier-inquiries",
        headers=bearer_auth_headers(),
        json={"network_member_id": str(uuid4()), "status": "flying"},
    )
    assert response.status_code == 400
    assert "status" in response.json()["detail"]


def test_http_quoted_money_on_draft_is_400(inquiry_client: object) -> None:
    client, _stub = inquiry_client
    response = client.post(
        "/api/v1/carrier-inquiries",
        headers=bearer_auth_headers(),
        json={
            "network_member_id": str(uuid4()),
            "status": "draft",
            "quoted_amount": "10.0000",
            "quoted_currency": "USD",
        },
    )
    assert response.status_code == 400
    assert "answered" in response.json()["detail"]


def test_http_batch_records_three_members(inquiry_client: object) -> None:
    client, _stub = inquiry_client
    members = [str(uuid4()), str(uuid4()), str(uuid4())]
    response = client.post(
        "/api/v1/carrier-inquiries/batch",
        headers=bearer_auth_headers(),
        json={"network_member_ids": members, "status": "queued"},
    )
    assert response.status_code == 201
    body = response.json()
    assert len(body) == 3
    assert {row["network_member_id"] for row in body} == set(members)
    assert all(row["status"] == "queued" for row in body)
