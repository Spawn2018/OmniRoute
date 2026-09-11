from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.sap_connector import (
    require_connector_code,
    require_sap_source_ref,
    require_system_kind,
)
from app.main import app
from app.models.sap_connector import SapConnector
from tests.http_auth import bearer_auth_headers

_FORBIDDEN = ("base_url", "api_key", "amount", "credential_ciphertext")


class PermitSapAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemorySapDesk:
    def __init__(self, session: object) -> None:
        self.connectors: list[SapConnector] = []

    async def list_connectors(self) -> list[SapConnector]:
        return list(self.connectors)

    async def persist_sap_connector(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        connector_code: object,
        system_kind: object,
        source_ref: object,
    ) -> SapConnector:
        row = SapConnector(
            id=uuid4(),
            organization_id=organization_id,
            connector_code=require_connector_code(connector_code),
            system_kind=require_system_kind(system_kind),
            source_ref=require_sap_source_ref(source_ref),
            created_by=user_id,
        )
        self.connectors.append(row)
        return row


@pytest.fixture
def sap_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemorySapDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr("app.api.sap_connectors.SapConnectorService", lambda _s: desk)
    set_authz_checker(PermitSapAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "connector_code": "sap_pl_01",
        "system_kind": "sap",
        "source_ref": "fixture://sap-connector/pl-1",
    }
    body.update(extra)
    return body


def test_http_lists_and_creates_sap_connector(sap_http: object) -> None:
    client, _desk = sap_http
    created = client.post(
        "/api/v1/sap-connectors",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert created.status_code == 201
    assert created.json()["system_kind"] == "sap"
    listed = client.get("/api/v1/sap-connectors", headers=bearer_auth_headers())
    assert listed.status_code == 200
    assert len(listed.json()) == 1


def test_http_rejects_bad_kind(sap_http: object) -> None:
    client, _desk = sap_http
    response = client.post(
        "/api/v1/sap-connectors",
        headers=bearer_auth_headers(),
        json=_payload(system_kind="optima"),
    )
    assert response.status_code == 400
    assert "system" in response.json()["detail"]


@pytest.mark.parametrize("field", _FORBIDDEN)
def test_http_forbids_secret_and_money_fields(sap_http: object, field: str) -> None:
    client, _desk = sap_http
    body = _payload()
    body[field] = "x"
    response = client.post(
        "/api/v1/sap-connectors",
        headers=bearer_auth_headers(),
        json=body,
    )
    assert response.status_code == 422
