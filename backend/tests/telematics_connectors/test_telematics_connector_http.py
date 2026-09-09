from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.telematics_connector import (
    require_connector_source_ref,
    require_observation_kind,
    require_provider_code,
)
from app.main import app
from app.models.telematics_connector import TelematicsConnector
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


class StubConnectorMarks:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[TelematicsConnector] = []

    async def list_marks(self) -> list[TelematicsConnector]:
        return list(self.rows)

    async def persist_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        observation_kind: object,
        provider_code: object,
        source_ref: object,
    ) -> TelematicsConnector:
        row = TelematicsConnector(
            id=uuid4(),
            organization_id=organization_id,
            observation_kind=require_observation_kind(observation_kind),
            provider_code=require_provider_code(provider_code),
            source_ref=require_connector_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    marks = StubConnectorMarks(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.telematics_connectors.TelematicsConnectorService",
        lambda _s: marks,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), marks
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "observation_kind": "external_api",
        "provider_code": "gbox",
        "source_ref": "fixture://telematics-connector/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_telematics_connector(catalog_client: object) -> None:
    client, _marks = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/telematics-connectors", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["observation_kind"] == "external_api"
    assert body["provider_code"] == "gbox"
    assert "buy_amount" not in body
    assert "lat" not in body
    listed = client.get("/api/v1/telematics-connectors", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_bad_kind_is_400(catalog_client: object) -> None:
    client, _marks = catalog_client
    response = client.post(
        "/api/v1/telematics-connectors",
        headers=bearer_auth_headers(),
        json=_payload(observation_kind="fleet"),
    )
    assert response.status_code == 400
    assert "reżim" in response.json()["detail"]


def test_http_create_bad_provider_is_400(catalog_client: object) -> None:
    client, _marks = catalog_client
    response = client.post(
        "/api/v1/telematics-connectors",
        headers=bearer_auth_headers(),
        json=_payload(provider_code="trans_eu"),
    )
    assert response.status_code == 400
    assert "dostawca" in response.json()["detail"]


def test_http_create_connector_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _marks = catalog_client
    response = client.post(
        "/api/v1/telematics-connectors",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://gps.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
