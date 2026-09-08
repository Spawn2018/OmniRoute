from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import UnknownParty
from app.domain.party_lane_scorecard import require_lane_window_days, required_lane_count
from app.domain.party_scorecard import optional_non_negative_hours, required_sample_size
from app.main import app
from app.models.party_lane_scorecard import PartyLaneScorecard
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


class StubPartyService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[PartyLaneScorecard] = []

    async def list_lane_scorecards(self) -> list[PartyLaneScorecard]:
        return list(self.rows)

    async def upsert_lane_scorecard(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: UUID,
        origin_port_id: UUID,
        destination_port_id: UUID,
        window_days: object | None = None,
        sample_size: object | None = None,
        answered_inquiry_count: object | None = None,
        shipment_count: object | None = None,
        cheapest_count: object | None = None,
        median_response_hours: object | None = None,
    ) -> PartyLaneScorecard:
        if str(party_id) == "00000000-0000-0000-0000-000000000000":
            raise UnknownParty(f"nieznany kontrahent: {party_id}")
        hours = optional_non_negative_hours(median_response_hours)
        window = require_lane_window_days(window_days)
        row = next(
            (
                item
                for item in self.rows
                if item.party_id == party_id
                and item.origin_port_id == origin_port_id
                and item.destination_port_id == destination_port_id
                and item.window_days == window
            ),
            None,
        )
        if row is None:
            row = PartyLaneScorecard(
                id=uuid4(),
                organization_id=organization_id,
                party_id=party_id,
                origin_port_id=origin_port_id,
                destination_port_id=destination_port_id,
                window_days=window,
                sample_size=required_sample_size(sample_size),
                answered_inquiry_count=required_lane_count(
                    answered_inquiry_count,
                    "answered_inquiry_count",
                ),
                shipment_count=required_lane_count(shipment_count, "shipment_count"),
                cheapest_count=required_lane_count(cheapest_count, "cheapest_count"),
                median_response_hours=hours,
                source_ref="tenant:manual",
                computed_at=datetime.now(UTC),
                created_by=user_id,
            )
            self.rows.append(row)
            return row
        row.sample_size = required_sample_size(sample_size)
        row.answered_inquiry_count = required_lane_count(
            answered_inquiry_count,
            "answered_inquiry_count",
        )
        row.shipment_count = required_lane_count(shipment_count, "shipment_count")
        row.cheapest_count = required_lane_count(cheapest_count, "cheapest_count")
        row.median_response_hours = hours
        return row


@pytest.fixture
def lane_client(monkeypatch: pytest.MonkeyPatch) -> object:
    stub = StubPartyService(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.party_lane_scorecards.PartyService", lambda _session: stub)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), stub
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_zero_sample_saves_and_hints_empty(lane_client: object) -> None:
    client, _stub = lane_client
    party_id = uuid4()
    origin = uuid4()
    dest = uuid4()
    created = client.post(
        "/api/v1/party-lane-scorecards",
        headers=bearer_auth_headers(),
        json={
            "party_id": str(party_id),
            "origin_port_id": str(origin),
            "destination_port_id": str(dest),
            "sample_size": 0,
        },
    )
    assert created.status_code == 200
    body = created.json()
    assert body["sample_size"] == 0
    assert "brak historii" in body["hint"]
    listed = client.get("/api/v1/party-lane-scorecards", headers=bearer_auth_headers())
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_negative_median_is_400(lane_client: object) -> None:
    client, _stub = lane_client
    response = client.post(
        "/api/v1/party-lane-scorecards",
        headers=bearer_auth_headers(),
        json={
            "party_id": str(uuid4()),
            "origin_port_id": str(uuid4()),
            "destination_port_id": str(uuid4()),
            "median_response_hours": "-1",
        },
    )
    assert response.status_code == 400
    assert "ujemna" in response.json()["detail"]


def test_http_same_party_lane_window_upserts(lane_client: object) -> None:
    client, _stub = lane_client
    payload = {
        "party_id": str(uuid4()),
        "origin_port_id": str(uuid4()),
        "destination_port_id": str(uuid4()),
        "window_days": 30,
        "sample_size": 0,
    }
    first = client.post(
        "/api/v1/party-lane-scorecards",
        headers=bearer_auth_headers(),
        json=payload,
    )
    second = client.post(
        "/api/v1/party-lane-scorecards",
        headers=bearer_auth_headers(),
        json={**payload, "sample_size": 2, "answered_inquiry_count": 2},
    )
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["id"] == second.json()["id"]
    assert second.json()["sample_size"] == 2
    assert "próba 2" in second.json()["hint"]


def test_http_unknown_party_is_400(lane_client: object) -> None:
    client, _stub = lane_client
    response = client.post(
        "/api/v1/party-lane-scorecards",
        headers=bearer_auth_headers(),
        json={
            "party_id": "00000000-0000-0000-0000-000000000000",
            "origin_port_id": str(uuid4()),
            "destination_port_id": str(uuid4()),
        },
    )
    assert response.status_code == 400
    assert "kontrahent" in response.json()["detail"]
