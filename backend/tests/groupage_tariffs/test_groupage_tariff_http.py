from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.groupage_tariff import (
    require_chargeable_weight,
    require_tariff_amount,
    require_tariff_code,
    require_tariff_currency,
    require_tariff_source_ref,
)
from app.main import app
from app.models.groupage_tariff import GroupageTariff
from app.models.location import Location
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


class StubLocationService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: Location | None = None

    async def get_location(self, location_id: UUID) -> Location:
        if self.row is None or self.row.id != location_id:
            raise ResourceNotFound("nieznana lokalizacja")
        return self.row


class StubGroupageTariffService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[GroupageTariff] = []

    async def list_tariffs(self) -> list[GroupageTariff]:
        return list(self.rows)

    async def record_tariff(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        location_id: UUID,
        tariff_code: str,
        chargeable_weight: str,
        amount: str,
        currency: str,
        source_ref: str,
    ) -> GroupageTariff:
        row = GroupageTariff(
            id=uuid4(),
            organization_id=organization_id,
            location_id=location_id,
            tariff_code=require_tariff_code(tariff_code),
            chargeable_weight=require_chargeable_weight(chargeable_weight),
            amount=require_tariff_amount(amount),
            currency=require_tariff_currency(currency),
            source_ref=require_tariff_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


def _zone(*, kind: str = "postal_zone") -> Location:
    return Location(
        id=uuid4(),
        organization_id=uuid4(),
        kind=kind,
        name="strefa",
        code="PL_A",
        source_ref="tenant:manual",
    )


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    places = StubLocationService(object())
    rows = StubGroupageTariffService(object())

    def _places(_session: object) -> StubLocationService:
        return places

    def _rows(_session: object) -> StubGroupageTariffService:
        return rows

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.groupage_tariffs.LocationService", _places)
    monkeypatch.setattr("app.api.groupage_tariffs.GroupageTariffService", _rows)
    places.row = _zone()
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), places, rows
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_groupage_tariff(catalog_client: object) -> None:
    client, places, _rows = catalog_client
    assert places.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/groupage-tariffs",
        headers=headers,
        json={
            "location_id": str(places.row.id),
            "tariff_code": "band_west",
            "chargeable_weight": "100.0000",
            "amount": "85.5000",
            "currency": "EUR",
            "source_ref": "fixture://groupage-tariff/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["location_id"] == str(places.row.id)
    assert body["tariff_code"] == "band_west"
    assert Decimal(body["amount"]) == Decimal("85.5000")
    assert "buy_amount" not in body
    listed = client.get("/api/v1/groupage-tariffs", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_tariff_unlocode_is_400(catalog_client: object) -> None:
    client, places, _rows = catalog_client
    assert places.row is not None
    places.row.kind = "unlocode"
    response = client.post(
        "/api/v1/groupage-tariffs",
        headers=bearer_auth_headers(),
        json={
            "location_id": str(places.row.id),
            "tariff_code": "band_west",
            "chargeable_weight": "100.0000",
            "amount": "85.5000",
            "currency": "EUR",
            "source_ref": "fixture://groupage-tariff/1",
        },
    )
    assert response.status_code == 400
    assert "strefa" in response.json()["detail"]


def test_http_create_tariff_unknown_location_is_404(catalog_client: object) -> None:
    client, _places, _rows = catalog_client
    response = client.post(
        "/api/v1/groupage-tariffs",
        headers=bearer_auth_headers(),
        json={
            "location_id": str(uuid4()),
            "tariff_code": "band_west",
            "chargeable_weight": "100.0000",
            "amount": "85.5000",
            "currency": "EUR",
            "source_ref": "fixture://groupage-tariff/1",
        },
    )
    assert response.status_code == 404


def test_http_create_tariff_zero_amount_is_400(catalog_client: object) -> None:
    client, places, _rows = catalog_client
    assert places.row is not None
    response = client.post(
        "/api/v1/groupage-tariffs",
        headers=bearer_auth_headers(),
        json={
            "location_id": str(places.row.id),
            "tariff_code": "band_west",
            "chargeable_weight": "100.0000",
            "amount": "0",
            "currency": "EUR",
            "source_ref": "fixture://groupage-tariff/1",
        },
    )
    assert response.status_code == 400
    assert "dodatnia" in response.json()["detail"]
