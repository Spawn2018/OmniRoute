from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.erp_connector import (
    require_connector_code,
    require_erp_source_ref,
    require_system_kind,
)
from app.main import app
from app.models.erp_connector import ErpConnector
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


class StubErpConnectorDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[ErpConnector] = []

    async def list_rows(self) -> list[ErpConnector]:
        return list(self.rows)

    async def persist_erp_connector(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        connector_code: object,
        system_kind: object,
        source_ref: object,
    ) -> ErpConnector:
        row = ErpConnector(
            id=uuid4(),
            organization_id=organization_id,
            connector_code=require_connector_code(connector_code),
            system_kind=require_system_kind(system_kind),
            source_ref=require_erp_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = StubErpConnectorDesk(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.erp_connectors.ErpConnectorService",
        lambda _s: desk,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "connector_code": "optima_biuro",
        "system_kind": "optima",
        "source_ref": "fixture://optima/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_erp_connector(catalog_client: object) -> None:
    client, _desk = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/erp-connectors", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["connector_code"] == "optima_biuro"
    assert body["system_kind"] == "optima"
    assert "buy_amount" not in body
    assert "margin" not in body
    assert "credential" not in body
    listed = client.get("/api/v1/erp-connectors", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_bad_code_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/erp-connectors",
        headers=bearer_auth_headers(),
        json=_payload(connector_code="X"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_http_create_xl_kind_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/erp-connectors",
        headers=bearer_auth_headers(),
        json=_payload(system_kind="xl"),
    )
    assert response.status_code == 400
    assert "system" in response.json()["detail"]


def test_http_create_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/erp-connectors",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://optima.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
