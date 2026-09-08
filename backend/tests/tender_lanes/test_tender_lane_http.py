from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.tender_lane import require_lane_pair, require_lane_source_ref, require_lot_id
from app.main import app
from app.models.tender_lane import TenderLane
from app.models.tender_lot import TenderLot
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


class StubLotLookup:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: TenderLot | None = None

    async def get_lot(self, lot_id: UUID) -> TenderLot:
        if self.row is None or self.row.id != lot_id:
            raise ResourceNotFound("nieznana partia")
        return self.row


class StubLaneDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[TenderLane] = []

    async def list_marks(self) -> list[TenderLane]:
        return list(self.rows)

    async def record_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        tender_lot_id: object,
        origin_unlocode: object,
        destination_unlocode: object,
        source_ref: object,
    ) -> TenderLane:
        origin, dest = require_lane_pair(origin_unlocode, destination_unlocode)
        row = TenderLane(
            id=uuid4(),
            organization_id=organization_id,
            tender_lot_id=require_lot_id(tender_lot_id),
            origin_unlocode=origin,
            destination_unlocode=dest,
            source_ref=require_lane_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


def _lot_row() -> TenderLot:
    return TenderLot(
        id=uuid4(),
        organization_id=uuid4(),
        tender_id=uuid4(),
        lot_code="LOT-1",
        source_ref="fixture://tender-lot/1",
        created_by=uuid4(),
    )


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    lanes = StubLaneDesk(object())
    lots = StubLotLookup(object())
    lots.row = _lot_row()

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.tender_lanes.TenderLaneService", lambda _s: lanes)
    monkeypatch.setattr("app.api.tender_lanes.TenderLotService", lambda _s: lots)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), lanes, lots
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(lot_id: UUID, **overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "tender_lot_id": str(lot_id),
        "origin_unlocode": "PLGDY",
        "destination_unlocode": "DEHAM",
        "source_ref": "fixture://tender-lane/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_tender_lane(catalog_client: object) -> None:
    client, _lanes, lots = catalog_client
    assert lots.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/tender-lanes",
        headers=headers,
        json=_payload(lots.row.id),
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["origin_unlocode"] == "PLGDY"
    assert body["destination_unlocode"] == "DEHAM"
    assert "buy_amount" not in body
    listed = client.get("/api/v1/tender-lanes", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_lane_empty_origin_is_400(catalog_client: object) -> None:
    client, _lanes, lots = catalog_client
    assert lots.row is not None
    response = client.post(
        "/api/v1/tender-lanes",
        headers=bearer_auth_headers(),
        json=_payload(lots.row.id, origin_unlocode="  "),
    )
    assert response.status_code == 400
    assert "korytarz" in response.json()["detail"]


def test_http_create_lane_same_ends_is_400(catalog_client: object) -> None:
    client, _lanes, lots = catalog_client
    assert lots.row is not None
    response = client.post(
        "/api/v1/tender-lanes",
        headers=bearer_auth_headers(),
        json=_payload(
            lots.row.id,
            origin_unlocode="PLGDY",
            destination_unlocode="PLGDY",
        ),
    )
    assert response.status_code == 400
    assert "korytarz" in response.json()["detail"]


def test_http_create_lane_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _lanes, lots = catalog_client
    assert lots.row is not None
    response = client.post(
        "/api/v1/tender-lanes",
        headers=bearer_auth_headers(),
        json=_payload(lots.row.id, source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
