from datetime import date, timedelta
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.carrier_inquiry import (
    InquiryMemberRank,
    carrier_inquiry_draft_status,
    require_answered_quote,
    require_inquiry_status,
    require_member_batch,
    require_no_reply_after,
    require_silent_filter,
)
from app.domain.errors import ResourceNotFound, UnknownNetworkMember
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


class StubEventService:
    def __init__(self) -> None:
        self.writes: list[dict[str, object]] = []

    async def create_event(self, **write: object) -> object:
        self.writes.append(write)
        return object()


class StubInquiryService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[CarrierInquiry] = []

    async def list_inquiries(self, silent: object = None) -> list[CarrierInquiry]:
        if require_silent_filter(silent) == "overdue":
            today = date.today()
            return [
                row
                for row in self.rows
                if row.no_reply_after is not None and row.no_reply_after < today
            ]
        return list(self.rows)

    async def set_no_reply_after(
        self,
        inquiry_id: UUID,
        no_reply_after: object,
    ) -> CarrierInquiry:
        for row in self.rows:
            if row.id == inquiry_id:
                row.no_reply_after = require_no_reply_after(no_reply_after)
                return row
        raise ResourceNotFound(f"nieznane zapytanie: {inquiry_id}")

    async def list_member_ranks(self) -> list[InquiryMemberRank]:
        tallies: dict[UUID, int] = {}
        for row in self.rows:
            tallies[row.network_member_id] = tallies.get(row.network_member_id, 0)
            if row.status == "answered":
                tallies[row.network_member_id] += 1
        return sorted(
            (InquiryMemberRank(member_id, count) for member_id, count in tallies.items()),
            key=lambda rank: (-rank.answered_count, rank.network_member_id),
        )

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
        no_reply_after: object = None,
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
            no_reply_after=require_no_reply_after(no_reply_after),
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
        no_reply_after: object = None,
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
                    no_reply_after=no_reply_after,
                ),
            )
        return rows


@pytest.fixture
def inquiry_client(monkeypatch: pytest.MonkeyPatch) -> object:
    stub = StubInquiryService(object())
    ledger = StubEventService()
    stub.ledger = ledger

    def _service(_session: object) -> StubInquiryService:
        return stub

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.carrier_inquiries.CarrierInquiryService", _service)
    monkeypatch.setattr("app.api.carrier_inquiries.EntityEventService", lambda _s: ledger)
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


def test_http_ranking_orders_answered_then_zero(inquiry_client: object) -> None:
    client, stub = inquiry_client
    org_id = uuid4()
    user_id = uuid4()
    high = uuid4()
    mid = uuid4()
    zero = uuid4()
    headers = bearer_auth_headers(organization_id=org_id, user_id=user_id)
    for member_id, status, money in (
        (high, "answered", "10.0000"),
        (high, "answered", "12.0000"),
        (mid, "answered", "8.0000"),
        (zero, "draft", None),
    ):
        created = client.post(
            "/api/v1/carrier-inquiries",
            headers=headers,
            json=(
                {
                    "network_member_id": str(member_id),
                    "status": status,
                    "quoted_amount": money,
                    "quoted_currency": "USD",
                }
                if money is not None
                else {"network_member_id": str(member_id), "status": status}
            ),
        )
        assert created.status_code == 201
    _ = stub
    ranked = client.get("/api/v1/carrier-inquiries/ranking", headers=headers)
    assert ranked.status_code == 200
    body = ranked.json()
    assert [row["network_member_id"] for row in body] == [str(high), str(mid), str(zero)]
    assert [row["answered_count"] for row in body] == [2, 1, 0]


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


def test_http_overdue_filter_skips_blank_and_future(inquiry_client: object) -> None:
    client, _stub = inquiry_client
    headers = bearer_auth_headers()
    past = (date.today() - timedelta(days=1)).isoformat()
    future = (date.today() + timedelta(days=1)).isoformat()
    overdue = client.post(
        "/api/v1/carrier-inquiries",
        headers=headers,
        json={"network_member_id": str(uuid4()), "no_reply_after": past},
    )
    blank = client.post(
        "/api/v1/carrier-inquiries",
        headers=headers,
        json={"network_member_id": str(uuid4())},
    )
    later = client.post(
        "/api/v1/carrier-inquiries",
        headers=headers,
        json={"network_member_id": str(uuid4()), "no_reply_after": future},
    )
    assert overdue.status_code == 201
    assert blank.status_code == 201
    assert later.status_code == 201
    listed = client.get("/api/v1/carrier-inquiries?silent=overdue", headers=headers)
    assert listed.status_code == 200
    assert [row["id"] for row in listed.json()] == [overdue.json()["id"]]
    bad = client.get("/api/v1/carrier-inquiries?silent=thread", headers=headers)
    assert bad.status_code == 400


def test_http_patch_sets_no_reply_after(inquiry_client: object) -> None:
    client, _stub = inquiry_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/carrier-inquiries",
        headers=headers,
        json={"network_member_id": str(uuid4())},
    )
    assert created.status_code == 201
    past = (date.today() - timedelta(days=2)).isoformat()
    patched = client.patch(
        f"/api/v1/carrier-inquiries/{created.json()['id']}",
        headers=headers,
        json={"no_reply_after": past},
    )
    assert patched.status_code == 200
    assert patched.json()["no_reply_after"] == past


def test_http_queued_inquiry_appends_entity_event(inquiry_client: object) -> None:
    client, stub = inquiry_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/carrier-inquiries",
        headers=headers,
        json={"network_member_id": str(uuid4()), "status": "queued"},
    )
    assert created.status_code == 201
    assert created.json()["status"] == "queued"
    assert len(stub.ledger.writes) == 1
    write = stub.ledger.writes[0]
    assert write["event_kind"] == "inquiry_queued"
    assert write["subject_kind"] == "carrier_inquiry"
    assert write["subject_id"] == UUID(created.json()["id"])
    assert write["source_ref"] == "tenant:manual"


def test_http_draft_inquiry_skips_entity_event(inquiry_client: object) -> None:
    client, stub = inquiry_client
    created = client.post(
        "/api/v1/carrier-inquiries",
        headers=bearer_auth_headers(),
        json={"network_member_id": str(uuid4())},
    )
    assert created.status_code == 201
    assert created.json()["status"] == "draft"
    assert stub.ledger.writes == []

def test_http_sent_inquiry_appends_entity_event(inquiry_client: object) -> None:
    client, stub = inquiry_client
    created = client.post(
        "/api/v1/carrier-inquiries",
        headers=bearer_auth_headers(),
        json={"network_member_id": str(uuid4()), "status": "sent"},
    )
    assert created.status_code == 201
    assert created.json()["status"] == "sent"
    assert len(stub.ledger.writes) == 1
    write = stub.ledger.writes[0]
    assert write["event_kind"] == "inquiry_sent"
    assert write["subject_kind"] == "carrier_inquiry"
    assert write["subject_id"] == UUID(created.json()["id"])
    assert write["source_ref"] == "tenant:manual"


def test_http_answered_inquiry_appends_quote_recorded(inquiry_client: object) -> None:
    client, stub = inquiry_client
    created = client.post(
        "/api/v1/carrier-inquiries",
        headers=bearer_auth_headers(),
        json={
            "network_member_id": str(uuid4()),
            "status": "answered",
            "quoted_amount": "10.0000",
            "quoted_currency": "USD",
        },
    )
    assert created.status_code == 201
    assert created.json()["status"] == "answered"
    assert len(stub.ledger.writes) == 1
    write = stub.ledger.writes[0]
    assert write["event_kind"] == "quote_recorded"
    assert write["subject_kind"] == "carrier_inquiry"
    assert write["subject_id"] == UUID(created.json()["id"])
    assert write["source_ref"] == "tenant:manual"


def test_http_declined_inquiry_skips_entity_event(inquiry_client: object) -> None:
    client, stub = inquiry_client
    created = client.post(
        "/api/v1/carrier-inquiries",
        headers=bearer_auth_headers(),
        json={"network_member_id": str(uuid4()), "status": "declined"},
    )
    assert created.status_code == 201
    assert created.json()["status"] == "declined"
    assert stub.ledger.writes == []
