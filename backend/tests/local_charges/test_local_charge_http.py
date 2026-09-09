from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.local_charge import (
    require_levy_amount,
    require_levy_currency,
    require_levy_iso,
    require_levy_kind,
    require_levy_port,
    require_levy_source_ref,
)
from app.main import app
from app.models.local_charge import LocalCharge
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


class StubLocalChargeService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[LocalCharge] = []

    async def list_levies(self) -> list[LocalCharge]:
        return list(self.rows)

    async def record_levy(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        charge_kind: str,
        amount: str,
        currency: str,
        source_ref: str,
        port_unlocode: str | None = None,
        iso_size_type: str | None = None,
    ) -> LocalCharge:
        row = LocalCharge(
            id=uuid4(),
            organization_id=organization_id,
            charge_kind=require_levy_kind(charge_kind),
            amount=require_levy_amount(amount),
            currency=require_levy_currency(currency),
            port_unlocode=require_levy_port(port_unlocode),
            iso_size_type=require_levy_iso(iso_size_type),
            source_ref=require_levy_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    rows = StubLocalChargeService(object())

    def _rows(_session: object) -> StubLocalChargeService:
        return rows

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.local_charges.LocalChargeService", _rows)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), rows
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "charge_kind": "thc",
        "amount": "80.0000",
        "currency": "EUR",
        "source_ref": "fixture://local-charge/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_local_charge(catalog_client: object) -> None:
    client, _rows = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/local-charges", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["charge_kind"] == "thc"
    assert body["amount"] == "80.0000"
    assert "buy_amount" not in body
    listed = client.get("/api/v1/local-charges", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]
    assert body["port_unlocode"] is None
    assert body["iso_size_type"] is None


def test_http_create_levy_with_port_unlocode(catalog_client: object) -> None:
    client, _rows = catalog_client
    created = client.post(
        "/api/v1/local-charges",
        headers=bearer_auth_headers(),
        json=_payload(port_unlocode="plgdy"),
    )
    assert created.status_code == 201
    assert created.json()["port_unlocode"] == "PLGDY"


def test_http_create_levy_with_iso_size_type(catalog_client: object) -> None:
    client, _rows = catalog_client
    created = client.post(
        "/api/v1/local-charges",
        headers=bearer_auth_headers(),
        json=_payload(iso_size_type="22g1"),
    )
    assert created.status_code == 201
    assert created.json()["iso_size_type"] == "22G1"


def test_http_create_levy_bad_iso_is_400(catalog_client: object) -> None:
    client, _rows = catalog_client
    response = client.post(
        "/api/v1/local-charges",
        headers=bearer_auth_headers(),
        json=_payload(iso_size_type="BOX"),
    )
    assert response.status_code == 400
    assert "typ" in response.json()["detail"]


def test_http_create_levy_bad_port_is_400(catalog_client: object) -> None:
    client, _rows = catalog_client
    response = client.post(
        "/api/v1/local-charges",
        headers=bearer_auth_headers(),
        json=_payload(port_unlocode="XX"),
    )
    assert response.status_code == 400
    assert "port" in response.json()["detail"]


def test_http_create_levy_bad_kind_is_400(catalog_client: object) -> None:
    client, _rows = catalog_client
    response = client.post(
        "/api/v1/local-charges",
        headers=bearer_auth_headers(),
        json=_payload(charge_kind="oil"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_http_create_levy_zero_amount_is_400(catalog_client: object) -> None:
    client, _rows = catalog_client
    response = client.post(
        "/api/v1/local-charges",
        headers=bearer_auth_headers(),
        json=_payload(amount="0"),
    )
    assert response.status_code == 400
    assert "kwota" in response.json()["detail"]


def test_http_create_levy_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _rows = catalog_client
    response = client.post(
        "/api/v1/local-charges",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
