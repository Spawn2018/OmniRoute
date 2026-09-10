from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.visibility_connector import parse_visibility_row
from app.main import app
from app.models.visibility_connector import VisibilityConnector
from tests.http_auth import bearer_auth_headers

_SECRET_FIELDS = ("api_key", "ciphertext", "base_url")


class PermitVisibilityAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryVisibilityDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[VisibilityConnector] = []

    async def list_fixtures(self) -> list[VisibilityConnector]:
        return list(self.rows)

    async def persist_visibility_fixture(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        connector_code: object,
        system_kind: object,
        source_ref: object,
    ) -> VisibilityConnector:
        code, kind, origin = parse_visibility_row(connector_code, system_kind, source_ref)
        row = VisibilityConnector(
            id=uuid4(),
            organization_id=organization_id,
            connector_code=code,
            system_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def visibility_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryVisibilityDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.visibility_connectors.VisibilityConnectorService",
        lambda _s: desk,
    )
    set_authz_checker(PermitVisibilityAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "connector_code": "p44_desk_pl",
        "system_kind": "p44",
        "source_ref": "fixture://visibility/pl-1",
    }
    body.update(extra)
    return body


def test_http_create_and_list_visibility_fixture(visibility_http: object) -> None:
    client, _desk = visibility_http
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/visibility-connectors", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["connector_code"] == "p44_desk_pl"
    assert body["system_kind"] == "p44"
    listed = client.get("/api/v1/visibility-connectors", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_manual_origin(visibility_http: object) -> None:
    client, _desk = visibility_http
    posted = client.post(
        "/api/v1/visibility-connectors",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="tenant:manual"),
    )
    assert posted.status_code == 201
    assert posted.json()["source_ref"] == "tenant:manual"


def test_http_create_bad_code_is_400(visibility_http: object) -> None:
    client, _desk = visibility_http
    response = client.post(
        "/api/v1/visibility-connectors",
        headers=bearer_auth_headers(),
        json=_payload(connector_code="X"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


@pytest.mark.parametrize("vendor", ["fourkites", "shippeo"])
def test_http_create_foreign_vendor_is_400(visibility_http: object, vendor: str) -> None:
    client, _desk = visibility_http
    response = client.post(
        "/api/v1/visibility-connectors",
        headers=bearer_auth_headers(),
        json=_payload(system_kind=vendor),
    )
    assert response.status_code == 400
    assert "system" in response.json()["detail"]


def test_http_create_foreign_origin_is_400(visibility_http: object) -> None:
    client, _desk = visibility_http
    response = client.post(
        "/api/v1/visibility-connectors",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="https://p44.com/live"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]


@pytest.mark.parametrize("secret_field", _SECRET_FIELDS)
def test_http_create_rejects_secret_extra_fields(
    visibility_http: object, secret_field: str
) -> None:
    client, _desk = visibility_http
    response = client.post(
        "/api/v1/visibility-connectors",
        headers=bearer_auth_headers(),
        json=_payload(**{secret_field: "x"}),
    )
    assert response.status_code == 422
