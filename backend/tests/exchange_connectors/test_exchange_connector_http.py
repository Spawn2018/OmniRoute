from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.exchange_connector import (
    require_connector_code,
    require_exchange_source_ref,
    require_system_kind,
)
from app.main import app
from app.models.exchange_connector import ExchangeConnector
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


class StubExchangeConnectorDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[ExchangeConnector] = []

    async def list_rows(self) -> list[ExchangeConnector]:
        return list(self.rows)

    async def persist_exchange_connector(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        connector_code: object,
        system_kind: object,
        source_ref: object,
    ) -> ExchangeConnector:
        row = ExchangeConnector(
            id=uuid4(),
            organization_id=organization_id,
            connector_code=require_connector_code(connector_code),
            system_kind=require_system_kind(system_kind),
            source_ref=require_exchange_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = StubExchangeConnectorDesk(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.exchange_connectors.ExchangeConnectorService",
        lambda _s: desk,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "connector_code": "trans_eu_desk",
        "system_kind": "trans_eu",
        "source_ref": "fixture://portal/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_exchange_connector(catalog_client: object) -> None:
    client, _desk = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/exchange-connectors", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["connector_code"] == "trans_eu_desk"
    assert body["system_kind"] == "trans_eu"
    assert "buy_amount" not in body
    assert "margin" not in body
    assert "client_secret" not in body
    listed = client.get("/api/v1/exchange-connectors", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_bad_code_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/exchange-connectors",
        headers=bearer_auth_headers(),
        json=_payload(connector_code="X"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_http_create_timocom_kind_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/exchange-connectors",
        headers=bearer_auth_headers(),
        json=_payload(system_kind="timocom"),
    )
    assert response.status_code == 400
    assert "system" in response.json()["detail"]


def test_http_create_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/exchange-connectors",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="https://trans.eu/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]


@pytest.mark.parametrize("secret_field", ["client_secret", "ciphertext", "base_url"])
def test_http_create_rejects_secret_fields(catalog_client: object, secret_field: str) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/exchange-connectors",
        headers=bearer_auth_headers(),
        json=_payload(**{secret_field: "x"}),
    )
    assert response.status_code == 422
