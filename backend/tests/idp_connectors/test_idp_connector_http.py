from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.idp_connector import (
    require_connector_code,
    require_idp_source_ref,
    require_provider_code,
    require_public_domain,
)
from app.main import app
from app.models.idp_connector import IdpConnector
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


class StubIdpConnectorDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[IdpConnector] = []

    async def list_rows(self) -> list[IdpConnector]:
        return list(self.rows)

    async def persist_idp_connector(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        connector_code: object,
        provider_code: object,
        source_ref: object,
        public_domain: object = None,
    ) -> IdpConnector:
        row = IdpConnector(
            id=uuid4(),
            organization_id=organization_id,
            connector_code=require_connector_code(connector_code),
            provider_code=require_provider_code(provider_code),
            public_domain=require_public_domain(public_domain),
            source_ref=require_idp_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = StubIdpConnectorDesk(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.idp_connectors.IdpConnectorService",
        lambda _s: desk,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "connector_code": "auth0_eu_desk",
        "provider_code": "auth0",
        "source_ref": "fixture://auth0/eu-1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_idp_connector(catalog_client: object) -> None:
    client, _desk = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/idp-connectors", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["connector_code"] == "auth0_eu_desk"
    assert body["provider_code"] == "auth0"
    assert body["public_domain"] is None
    assert "buy_amount" not in body
    assert "margin" not in body
    assert "client_secret" not in body
    assert "ciphertext" not in body
    listed = client.get("/api/v1/idp-connectors", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_stores_public_domain_as_text(catalog_client: object) -> None:
    client, _desk = catalog_client
    created = client.post(
        "/api/v1/idp-connectors",
        headers=bearer_auth_headers(),
        json=_payload(public_domain="acme.eu.auth0.com"),
    )
    assert created.status_code == 201
    assert created.json()["public_domain"] == "acme.eu.auth0.com"


def test_http_create_bad_code_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/idp-connectors",
        headers=bearer_auth_headers(),
        json=_payload(connector_code="X"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_http_create_okta_provider_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/idp-connectors",
        headers=bearer_auth_headers(),
        json=_payload(provider_code="okta"),
    )
    assert response.status_code == 400
    assert "dostawca" in response.json()["detail"]


def test_http_create_issuer_url_domain_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/idp-connectors",
        headers=bearer_auth_headers(),
        json=_payload(public_domain="https://acme.eu.auth0.com"),
    )
    assert response.status_code == 400
    assert "domena" in response.json()["detail"]


def test_http_create_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/idp-connectors",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="https://auth0.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]


@pytest.mark.parametrize("secret_field", ["client_secret", "ciphertext", "jwks_uri"])
def test_http_create_rejects_secret_fields(catalog_client: object, secret_field: str) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/idp-connectors",
        headers=bearer_auth_headers(),
        json=_payload(**{secret_field: "x"}),
    )
    assert response.status_code == 422
