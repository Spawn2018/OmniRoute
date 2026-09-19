from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.resource import (
    require_adr_certified,
    require_capacity_kg,
    require_capacity_ldm,
    require_capacity_m3,
    require_display_name,
    require_inventory_no,
    require_reefer,
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
        inventory_no: object = None,
        capacity_kg: object = None,
        capacity_ldm: object = None,
        capacity_m3: object = None,
        adr_certified: object = None,
        reefer: object = None,
        source_ref: object,
    ) -> Resource:
        kind = require_resource_kind(resource_kind)
        label = require_display_name(display_name)
        plate = require_registration_no(registration_no)
        inventory = require_inventory_no(inventory_no)
        capacity = require_capacity_kg(capacity_kg)
        ldm = require_capacity_ldm(capacity_ldm)
        cubic = require_capacity_m3(capacity_m3)
        adr = require_adr_certified(adr_certified)
        cold = require_reefer(reefer)
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
        if (
            current is not None
            and current.registration_no == plate
            and current.inventory_no == inventory
            and current.capacity_kg == capacity
            and current.capacity_ldm == ldm
            and current.capacity_m3 == cubic
            and current.adr_certified == adr
            and current.reefer == cold
            and current.source_ref == origin
        ):
            return current
        successor = Resource(
            id=uuid4(),
            organization_id=organization_id,
            resource_kind=kind,
            display_name=label,
            registration_no=plate,
            inventory_no=inventory,
            capacity_kg=capacity,
            capacity_ldm=ldm,
            capacity_m3=cubic,
            adr_certified=adr,
            reefer=cold,
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
    assert first.json()["capacity_kg"] is None
    assert first.json()["capacity_ldm"] is None
    assert first.json()["capacity_m3"] is None
    assert first.json()["inventory_no"] is None
    assert first.json()["adr_certified"] is None
    assert first.json()["reefer"] is None
    assert "amount" not in first.json()
    with_kg = client.post(
        "/api/v1/resources",
        headers=headers,
        json={**payload, "capacity_kg": "24000"},
    )
    assert with_kg.status_code == 201
    assert with_kg.json()["capacity_kg"] == "24000.0000"
    assert with_kg.json()["id"] != first.json()["id"]
    with_ldm = client.post(
        "/api/v1/resources",
        headers=headers,
        json={**payload, "capacity_kg": "24000", "capacity_ldm": "13.6"},
    )
    assert with_ldm.status_code == 201
    assert with_ldm.json()["capacity_ldm"] == "13.6000"
    assert with_ldm.json()["id"] != with_kg.json()["id"]
    with_m3 = client.post(
        "/api/v1/resources",
        headers=headers,
        json={
            **payload,
            "capacity_kg": "24000",
            "capacity_ldm": "13.6",
            "capacity_m3": "90",
        },
    )
    assert with_m3.status_code == 201
    assert with_m3.json()["capacity_m3"] == "90.0000"
    assert with_m3.json()["id"] != with_ldm.json()["id"]
    second = client.post(
        "/api/v1/resources",
        headers=headers,
        json={
            **payload,
            "registration_no": "WX 2222",
            "capacity_kg": "24000",
            "capacity_ldm": "13.6",
            "capacity_m3": "90",
        },
    )
    assert second.status_code == 201
    assert second.json()["id"] != with_m3.json()["id"]
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
    bad_kg = client.post(
        "/api/v1/resources",
        headers=headers,
        json={**payload, "display_name": "Other", "capacity_kg": 0.5},
    )
    assert bad_kg.status_code == 400
    assert "pojemność" in bad_kg.json()["detail"]
    bad_ldm = client.post(
        "/api/v1/resources",
        headers=headers,
        json={**payload, "display_name": "Other2", "capacity_ldm": 0.5},
    )
    assert bad_ldm.status_code == 400
    assert "ldm" in bad_ldm.json()["detail"]
    bad_m3 = client.post(
        "/api/v1/resources",
        headers=headers,
        json={**payload, "display_name": "Other3", "capacity_m3": 0.5},
    )
    assert bad_m3.status_code == 400
    assert "m3" in bad_m3.json()["detail"]


def test_http_inventory_no_supersedes(fleet_client: object) -> None:
    client, _rows = fleet_client
    headers = bearer_auth_headers(organization_id=uuid4())
    payload = {
        "resource_kind": "trailer",
        "display_name": "Schmitz",
        "source_ref": "tenant:manual",
        "inventory_no": "INV-1",
    }
    first = client.post("/api/v1/resources", headers=headers, json=payload)
    assert first.status_code == 201
    assert first.json()["inventory_no"] == "INV-1"
    same = client.post("/api/v1/resources", headers=headers, json=payload)
    assert same.json()["id"] == first.json()["id"]
    changed = client.post(
        "/api/v1/resources",
        headers=headers,
        json={**payload, "inventory_no": "INV-2"},
    )
    assert changed.status_code == 201
    assert changed.json()["id"] != first.json()["id"]
    too_long = client.post(
        "/api/v1/resources",
        headers=headers,
        json={**payload, "display_name": "Inna", "inventory_no": "x" * 33},
    )
    assert too_long.status_code == 400
    assert "inwentarzowy" in too_long.json()["detail"]


def test_http_adr_certified_supersedes(fleet_client: object) -> None:
    client, _rows = fleet_client
    headers = bearer_auth_headers(organization_id=uuid4())
    payload = {
        "resource_kind": "vehicle",
        "display_name": "ADR MAN",
        "source_ref": "tenant:manual",
        "adr_certified": True,
    }
    first = client.post("/api/v1/resources", headers=headers, json=payload)
    assert first.status_code == 201
    assert first.json()["adr_certified"] is True
    same = client.post("/api/v1/resources", headers=headers, json=payload)
    assert same.json()["id"] == first.json()["id"]
    changed = client.post(
        "/api/v1/resources",
        headers=headers,
        json={**payload, "adr_certified": False},
    )
    assert changed.status_code == 201
    assert changed.json()["id"] != first.json()["id"]
    bad = client.post(
        "/api/v1/resources",
        headers=headers,
        json={**payload, "display_name": "Inna", "adr_certified": "tak"},
    )
    assert bad.status_code == 400
    assert "adr" in bad.json()["detail"]


def test_http_reefer_supersedes(fleet_client: object) -> None:
    client, _rows = fleet_client
    headers = bearer_auth_headers(organization_id=uuid4())
    payload = {
        "resource_kind": "trailer",
        "display_name": "Chlodnia",
        "source_ref": "tenant:manual",
        "reefer": True,
    }
    first = client.post("/api/v1/resources", headers=headers, json=payload)
    assert first.status_code == 201
    assert first.json()["reefer"] is True
    same = client.post("/api/v1/resources", headers=headers, json=payload)
    assert same.json()["id"] == first.json()["id"]
    changed = client.post(
        "/api/v1/resources",
        headers=headers,
        json={**payload, "reefer": False},
    )
    assert changed.status_code == 201
    assert changed.json()["id"] != first.json()["id"]
    bad = client.post(
        "/api/v1/resources",
        headers=headers,
        json={**payload, "display_name": "Inna", "reefer": "tak"},
    )
    assert bad.status_code == 400
    assert "reefer" in bad.json()["detail"]


def test_capacity_kg_decimal_roundtrip_type() -> None:
    assert require_capacity_kg("24000.5") == Decimal("24000.5000")
    assert require_capacity_kg(None) is None
    assert require_capacity_kg("") is None
