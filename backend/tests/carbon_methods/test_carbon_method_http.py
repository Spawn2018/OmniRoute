from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.carbon_method import (
    require_carbon_method_source_ref,
    require_method_code,
    require_method_version,
)
from app.main import app
from app.models.carbon_method import CarbonMethod
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


class StubMethodDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[CarbonMethod] = []

    async def list_methods(self) -> list[CarbonMethod]:
        return list(self.rows)

    async def persist_method(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        method_code: object,
        method_version: object,
        source_ref: object,
    ) -> CarbonMethod:
        row = CarbonMethod(
            id=uuid4(),
            organization_id=organization_id,
            method_code=require_method_code(method_code),
            method_version=require_method_version(method_version),
            source_ref=require_carbon_method_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    methods = StubMethodDesk(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.carbon_methods.CarbonMethodService",
        lambda _s: methods,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), methods
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "method_code": "glec",
        "method_version": "2023",
        "source_ref": "fixture://carbon-method/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_carbon_method(catalog_client: object) -> None:
    client, _methods = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/carbon-methods", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["method_code"] == "glec"
    assert body["method_version"] == "2023"
    assert "buy_amount" not in body
    assert "kg" not in body
    listed = client.get("/api/v1/carbon-methods", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_bad_method_code_is_400(catalog_client: object) -> None:
    client, _methods = catalog_client
    response = client.post(
        "/api/v1/carbon-methods",
        headers=bearer_auth_headers(),
        json=_payload(method_code="X"),
    )
    assert response.status_code == 400
    assert "metoda" in response.json()["detail"]


def test_http_create_carbon_method_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _methods = catalog_client
    response = client.post(
        "/api/v1/carbon-methods",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
