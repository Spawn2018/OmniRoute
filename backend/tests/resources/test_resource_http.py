from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.resource import (
    require_display_name,
    require_registration_no,
    require_resource_kind,
    require_resource_source_ref,
)
from app.main import app
from app.models.resource import Resource
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


class StubResourceService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[Resource] = []

    async def list_resources(self, *, resource_kind: object | None = None) -> list[Resource]:
        kind = None if resource_kind is None else require_resource_kind(resource_kind)
        return [
            row
            for row in self.rows
            if row.superseded_by is None and (kind is None or row.resource_kind == kind)
        ]

    async def record_resource(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        resource_kind: object,
        display_name: object,
        registration_no: object,
        source_ref: object,
    ) -> Resource:
        kind = require_resource_kind(resource_kind)
        label = require_display_name(display_name)
        plate = require_registration_no(registration_no)
        origin = require_resource_source_ref(source_ref)
        current = next(
            (
                row
                for row in self.rows
                if row.resource_kind == kind
                and row.display_name == label
                and row.superseded_by is None
            ),
            None,
        )
        if current is not None and current.registration_no == plate:
            if current.source_ref == origin:
                return current
        successor = Resource(
            id=uuid4(),
            organization_id=organization_id,
            resource_kind=kind,
            display_name=label,
            registration_no=plate,
            source_ref=origin,
            created_by=user_id,
        )
        if current is not None:
            current.superseded_by = successor.id
        self.rows.append(successor)
        return successor


@pytest.fixture
def fleet_client(monkeypatch: pytest.MonkeyPatch) -> object:
    rows = StubResourceService(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.resources.ResourceService", lambda _s: rows)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), rows
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_list_supersede_and_reject_truck(fleet_client: object) -> None:
    client, _rows = fleet_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    payload = {
        "resource_kind": "vehicle",
        "display_name": "MAN TGX",
        "registration_no": "WX 1111",
        "source_ref": "tenant:manual",
    }
    first = client.post("/api/v1/resources", headers=headers, json=payload)
    assert first.status_code == 201
    assert first.json()["organization_id"] == str(org_id)
    assert "amount" not in first.json()
    second = client.post(
        "/api/v1/resources",
        headers=headers,
        json={**payload, "registration_no": "WX 2222"},
    )
    assert second.status_code == 201
    assert second.json()["id"] != first.json()["id"]
    listed = client.get("/api/v1/resources", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == second.json()["id"]
    drivers = client.get(
        "/api/v1/resources",
        headers=headers,
        params={"resource_kind": "driver"},
    )
    assert drivers.json() == []
    truck = client.post(
        "/api/v1/resources",
        headers=headers,
        json={**payload, "resource_kind": "truck"},
    )
    assert truck.status_code == 400
    assert "rodzaj" in truck.json()["detail"]
