from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.field_carry_forward import require_field_map
from app.main import app
from app.models.field_carry_forward import FieldCarryForward
from app.models.shipment import Shipment
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


class StubShipmentService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: Shipment | None = None

    async def get_shipment(self, shipment_id: UUID) -> Shipment:
        if self.row is None or self.row.id != shipment_id:
            raise ResourceNotFound("nieznane zlecenie")
        return self.row


class StubFieldCarryForwardService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[FieldCarryForward] = []

    async def list_for_shipment(self, shipment_id: UUID) -> list[FieldCarryForward]:
        return [row for row in self.rows if row.shipment_id == shipment_id]

    async def record_fields(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        quotation_id: UUID,
        shipment_id: UUID,
        fields: object,
    ) -> list[FieldCarryForward]:
        mapped = require_field_map(fields)
        recorded: list[FieldCarryForward] = []
        for key, value in mapped.items():
            current = next(
                (
                    row
                    for row in self.rows
                    if row.quotation_id == quotation_id
                    and row.shipment_id == shipment_id
                    and row.field_key == key
                    and row.superseded_by is None
                ),
                None,
            )
            if current is not None and current.field_value == value:
                recorded.append(current)
                continue
            successor = FieldCarryForward(
                id=uuid4(),
                organization_id=organization_id,
                quotation_id=quotation_id,
                shipment_id=shipment_id,
                field_key=key,
                field_value=value,
                created_by=user_id,
            )
            if current is not None:
                current.superseded_by = successor.id
            self.rows.append(successor)
            recorded.append(successor)
        return recorded


def _shipment() -> Shipment:
    return Shipment(
        id=uuid4(),
        organization_id=uuid4(),
        quotation_id=uuid4(),
        party_id=uuid4(),
        source_ref="fixture://shipment/1",
        status="draft",
    )


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    ships = StubShipmentService(object())
    carries = StubFieldCarryForwardService(object())

    def _ships(_session: object) -> StubShipmentService:
        return ships

    def _rows(_session: object) -> StubFieldCarryForwardService:
        return carries

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.field_carry_forwards.ShipmentService", _ships)
    monkeypatch.setattr("app.api.field_carry_forwards.FieldCarryForwardService", _rows)
    ships.row = _shipment()
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), ships, carries
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_carry_allowlist_and_reject_foreign_key(catalog_client: object) -> None:
    client, ships, _rows = catalog_client
    assert ships.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/field-carry-forwards",
        headers=headers,
        json={
            "quotation_id": str(ships.row.quotation_id),
            "shipment_id": str(ships.row.id),
            "fields": {"incoterm": "FOB", "trade_side": "export", "named_place": ""},
        },
    )
    assert created.status_code == 201
    body = created.json()
    keys = {row["field_key"] for row in body}
    assert keys == {"incoterm", "trade_side", "named_place"}
    assert all(row["organization_id"] == str(org_id) for row in body)
    assert "amount" not in body[0]
    foreign = client.post(
        "/api/v1/field-carry-forwards",
        headers=headers,
        json={
            "quotation_id": str(ships.row.quotation_id),
            "shipment_id": str(ships.row.id),
            "fields": {"weight": "12"},
        },
    )
    assert foreign.status_code == 400
    assert "pole" in foreign.json()["detail"]


def test_http_change_incoterm_supersedes_previous_row(catalog_client: object) -> None:
    client, ships, _rows = catalog_client
    assert ships.row is not None
    headers = bearer_auth_headers()
    first = client.post(
        "/api/v1/field-carry-forwards",
        headers=headers,
        json={
            "quotation_id": str(ships.row.quotation_id),
            "shipment_id": str(ships.row.id),
            "fields": {"incoterm": "FOB"},
        },
    )
    first_id = first.json()[0]["id"]
    second = client.post(
        "/api/v1/field-carry-forwards",
        headers=headers,
        json={
            "quotation_id": str(ships.row.quotation_id),
            "shipment_id": str(ships.row.id),
            "fields": {"incoterm": "CIF"},
        },
    )
    assert second.status_code == 201
    successor = second.json()[0]
    assert successor["id"] != first_id
    listed = client.get(
        "/api/v1/field-carry-forwards",
        headers=headers,
        params={"shipment_id": str(ships.row.id)},
    )
    assert listed.status_code == 200
    by_id = {row["id"]: row for row in listed.json()}
    assert by_id[first_id]["superseded_by"] == successor["id"]
    assert successor["superseded_by"] is None
    same = client.post(
        "/api/v1/field-carry-forwards",
        headers=headers,
        json={
            "quotation_id": str(ships.row.quotation_id),
            "shipment_id": str(ships.row.id),
            "fields": {"incoterm": "CIF"},
        },
    )
    assert same.json()[0]["id"] == successor["id"]


def test_http_carry_unknown_shipment_is_404(catalog_client: object) -> None:
    client, _ships, _rows = catalog_client
    response = client.post(
        "/api/v1/field-carry-forwards",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(uuid4()),
            "shipment_id": str(uuid4()),
            "fields": {"incoterm": "FOB"},
        },
    )
    assert response.status_code == 404


def test_http_carry_mismatched_quotation_is_400(catalog_client: object) -> None:
    client, ships, _rows = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/field-carry-forwards",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(uuid4()),
            "shipment_id": str(ships.row.id),
            "fields": {"incoterm": "FOB"},
        },
    )
    assert response.status_code == 400
    assert "wyceny" in response.json()["detail"]
