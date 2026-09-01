from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import UnknownPort, UnknownPortSurcharge
from app.main import app
from app.models.port_surcharge import PortSurcharge
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


class StubPortSurchargeService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[PortSurcharge] = []

    async def list_surcharges(self) -> list[PortSurcharge]:
        return list(self.rows)

    async def resolve(self, port_id: UUID, code: object) -> PortSurcharge:
        token = str(code).strip().lower().replace("-", "_")
        for row in self.rows:
            if row.port_id == port_id and row.code == token:
                return row
        raise UnknownPortSurcharge(f"nieznane extra portowe: {token}")

    async def create_surcharge(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        port_id: UUID,
        code: object,
        title: object,
        applies_when: object,
        amount: object,
        currency: object,
    ) -> PortSurcharge:
        if str(port_id) == "00000000-0000-0000-0000-000000000000":
            raise UnknownPort(f"nieznany port: {port_id}")
        token = str(code).strip().lower().replace("-", "_")
        row = PortSurcharge(
            id=uuid4(),
            organization_id=organization_id,
            amount=Decimal(str(amount)),
            currency=str(currency).strip().upper(),
            port_id=port_id,
            code=token,
            title=str(title).strip(),
            applies_when=str(applies_when).strip(),
            source_ref="tenant:manual",
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubPortSurchargeService(object())

    def _factory(session: object) -> StubPortSurchargeService:
        return stub

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.port_surcharges.PortSurchargeService", _factory)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_list_and_resolve(catalog_client: TestClient) -> None:
    org_id = uuid4()
    port_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = catalog_client.post(
        "/api/v1/port-surcharges",
        headers=headers,
        json={
            "port_id": str(port_id),
            "code": "thc",
            "title": "THC",
            "applies_when": "kontener 40HC w weekend",
            "amount": "85.0000",
            "currency": "EUR",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["port_id"] == str(port_id)
    assert body["organization_id"] == str(org_id)
    assert body["amount"] == "85.0000"
    assert isinstance(body["amount"], str)
    assert body["currency"] == "EUR"
    assert body["source_ref"] == "tenant:manual"
    assert "buy_amount" not in body
    assert "margin" not in body

    listed = catalog_client.get("/api/v1/port-surcharges", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]

    resolved = catalog_client.get(
        "/api/v1/port-surcharges/resolve",
        headers=headers,
        params={"port_id": str(port_id), "code": "thc"},
    )
    assert resolved.status_code == 200
    assert resolved.json()["id"] == body["id"]


def test_http_resolve_unknown_is_rejected(catalog_client: TestClient) -> None:
    response = catalog_client.get(
        "/api/v1/port-surcharges/resolve",
        headers=bearer_auth_headers(),
        params={"port_id": str(uuid4()), "code": "missing"},
    )
    assert response.status_code == 400
    assert "nieznane extra" in response.json()["detail"]


def test_http_create_unknown_port_is_rejected(catalog_client: TestClient) -> None:
    response = catalog_client.post(
        "/api/v1/port-surcharges",
        headers=bearer_auth_headers(),
        json={
            "port_id": "00000000-0000-0000-0000-000000000000",
            "code": "thc",
            "title": "THC",
            "applies_when": "weekend",
            "amount": "10.0000",
            "currency": "EUR",
        },
    )
    assert response.status_code == 400
    assert "nieznany port" in response.json()["detail"]


def test_http_create_rejects_client_source_ref(catalog_client: TestClient) -> None:
    response = catalog_client.post(
        "/api/v1/port-surcharges",
        headers=bearer_auth_headers(),
        json={
            "port_id": str(uuid4()),
            "code": "thc",
            "title": "THC",
            "applies_when": "weekend",
            "amount": "10.0000",
            "currency": "EUR",
            "source_ref": "forged:origin",
        },
    )
    assert response.status_code == 422
