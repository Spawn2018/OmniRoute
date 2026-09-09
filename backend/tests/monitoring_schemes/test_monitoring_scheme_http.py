from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.monitoring_scheme import require_scheme_code, require_scheme_source_ref
from app.main import app
from app.models.monitoring_scheme import MonitoringScheme
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


class StubSchemeDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[MonitoringScheme] = []

    async def list_schemes(self) -> list[MonitoringScheme]:
        return list(self.rows)

    async def persist_scheme(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        scheme_code: object,
        source_ref: object,
    ) -> MonitoringScheme:
        row = MonitoringScheme(
            id=uuid4(),
            organization_id=organization_id,
            scheme_code=require_scheme_code(scheme_code),
            source_ref=require_scheme_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    schemes = StubSchemeDesk(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.monitoring_schemes.MonitoringSchemeService",
        lambda _s: schemes,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), schemes
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "scheme_code": "sent",
        "source_ref": "fixture://monitoring-scheme/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_monitoring_scheme(catalog_client: object) -> None:
    client, _schemes = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/monitoring-schemes", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["scheme_code"] == "sent"
    assert "buy_amount" not in body
    listed = client.get("/api/v1/monitoring-schemes", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_bad_scheme_code_is_400(catalog_client: object) -> None:
    client, _schemes = catalog_client
    response = client.post(
        "/api/v1/monitoring-schemes",
        headers=bearer_auth_headers(),
        json=_payload(scheme_code="X"),
    )
    assert response.status_code == 400
    assert "schemat" in response.json()["detail"]


def test_http_create_scheme_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _schemes = catalog_client
    response = client.post(
        "/api/v1/monitoring-schemes",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
