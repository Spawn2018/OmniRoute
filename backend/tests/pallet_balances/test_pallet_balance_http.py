from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.pallet_balance import (
    require_balance_source_ref,
    require_pallet_kind,
    require_unit_count,
)
from app.main import app
from app.models.pallet_balance import PalletBalance
from app.models.party import Party
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
        self.row: Party | None = None

    async def get_party(self, party_id: UUID) -> Party:
        if self.row is None or self.row.id != party_id:
            raise ResourceNotFound("nieznany kontrahent")
        return self.row


class StubPalletBalanceService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[PalletBalance] = []

    async def list_balances(self) -> list[PalletBalance]:
        return list(self.rows)

    async def record_balance(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: UUID,
        pallet_kind: str,
        unit_count: int,
        source_ref: str,
    ) -> PalletBalance:
        row = PalletBalance(
            id=uuid4(),
            organization_id=organization_id,
            party_id=party_id,
            pallet_kind=require_pallet_kind(pallet_kind),
            unit_count=require_unit_count(unit_count),
            source_ref=require_balance_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


def _party() -> Party:
    return Party(
        id=uuid4(),
        organization_id=uuid4(),
        legal_name="Agent",
        country_code="PL",
        roles=["agent"],
        source_ref="tenant:manual",
        is_active=True,
    )


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    counterparts = StubPartyService(object())
    rows = StubPalletBalanceService(object())

    def _parties(_session: object) -> StubPartyService:
        return counterparts

    def _rows(_session: object) -> StubPalletBalanceService:
        return rows

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.pallet_balances.PartyService", _parties)
    monkeypatch.setattr("app.api.pallet_balances.PalletBalanceService", _rows)
    counterparts.row = _party()
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), counterparts, rows
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_pallet_balance(catalog_client: object) -> None:
    client, counterparts, _rows = catalog_client
    assert counterparts.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/pallet-balances",
        headers=headers,
        json={
            "party_id": str(counterparts.row.id),
            "pallet_kind": "chep",
            "unit_count": 12,
            "source_ref": "fixture://pallet-balance/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["party_id"] == str(counterparts.row.id)
    assert body["pallet_kind"] == "chep"
    assert body["unit_count"] == 12
    assert "amount" not in body
    assert "buy_amount" not in body
    listed = client.get("/api/v1/pallet-balances", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_pallet_unknown_party_is_404(catalog_client: object) -> None:
    client, _counterparts, _rows = catalog_client
    response = client.post(
        "/api/v1/pallet-balances",
        headers=bearer_auth_headers(),
        json={
            "party_id": str(uuid4()),
            "pallet_kind": "chep",
            "unit_count": 1,
            "source_ref": "fixture://pallet-balance/1",
        },
    )
    assert response.status_code == 404


def test_http_create_pallet_unknown_kind_is_400(catalog_client: object) -> None:
    client, counterparts, _rows = catalog_client
    assert counterparts.row is not None
    response = client.post(
        "/api/v1/pallet-balances",
        headers=bearer_auth_headers(),
        json={
            "party_id": str(counterparts.row.id),
            "pallet_kind": "euro",
            "unit_count": 1,
            "source_ref": "fixture://pallet-balance/1",
        },
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_http_create_pallet_negative_count_is_400(catalog_client: object) -> None:
    client, counterparts, _rows = catalog_client
    assert counterparts.row is not None
    response = client.post(
        "/api/v1/pallet-balances",
        headers=bearer_auth_headers(),
        json={
            "party_id": str(counterparts.row.id),
            "pallet_kind": "chep",
            "unit_count": -1,
            "source_ref": "fixture://pallet-balance/1",
        },
    )
    assert response.status_code == 400
    assert "sztuk" in response.json()["detail"]


def test_http_create_pallet_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, counterparts, _rows = catalog_client
    assert counterparts.row is not None
    response = client.post(
        "/api/v1/pallet-balances",
        headers=bearer_auth_headers(),
        json={
            "party_id": str(counterparts.row.id),
            "pallet_kind": "chep",
            "unit_count": 1,
            "source_ref": "http://hold.example/x",
        },
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
