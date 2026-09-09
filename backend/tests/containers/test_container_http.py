from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.container import (
    require_cargo_description,
    require_container_no,
    require_container_remarks,
    require_container_shipment_id,
    require_container_source_ref,
    require_iso_size_type,
    require_packaging_code,
    require_seal_no_1,
    require_seal_no_2,
    require_seal_no_3,
    require_vessel_name,
    require_voyage_no,
)
from app.domain.errors import ResourceNotFound
from app.main import app
from app.models.container import Container
from app.models.shipment import Shipment
from tests.http_auth import bearer_auth_headers

_GOOD = "CSQU3054383"


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


class StubShipmentService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[Shipment] = []

    async def get_shipment(self, shipment_id: UUID) -> Shipment:
        for row in self.rows:
            if row.id == shipment_id:
                return row
        raise ResourceNotFound("nieznane zlecenie")


class StubContainerService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[Container] = []

    async def list_containers(self, *, iso_size_type: object | None = None) -> list[Container]:
        size_type = None if iso_size_type is None else require_iso_size_type(iso_size_type)
        return [
            row
            for row in self.rows
            if row.superseded_by is None and (size_type is None or row.iso_size_type == size_type)
        ]

    async def record_container(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        container_no: object,
        iso_size_type: object,
        shipment_id: object,
        source_ref: object,
        seal_no_1: object = None,
        seal_no_2: object = None,
        seal_no_3: object = None,
        vessel_name: object = None,
        voyage_no: object = None,
        remarks: object = None,
        cargo_description: object = None,
        packaging_code: object = None,
    ) -> Container:
        number = require_container_no(container_no)
        size_type = require_iso_size_type(iso_size_type)
        bound = require_container_shipment_id(shipment_id)
        origin = require_container_source_ref(source_ref)
        seal = require_seal_no_1(seal_no_1)
        seal2 = require_seal_no_2(seal_no_2)
        seal3 = require_seal_no_3(seal_no_3)
        vessel = require_vessel_name(vessel_name)
        voyage = require_voyage_no(voyage_no)
        note = require_container_remarks(remarks)
        goods = require_cargo_description(cargo_description)
        pack = require_packaging_code(packaging_code)
        current = next(
            (row for row in self.rows if row.container_no == number and row.superseded_by is None),
            None,
        )
        if (
            current is not None
            and current.iso_size_type == size_type
            and current.shipment_id == bound
            and current.source_ref == origin
            and current.seal_no_1 == seal
            and current.seal_no_2 == seal2
            and current.seal_no_3 == seal3
            and current.vessel_name == vessel
            and current.voyage_no == voyage
            and current.remarks == note
            and current.cargo_description == goods
            and current.packaging_code == pack
        ):
            return current
        successor = Container(
            id=uuid4(),
            organization_id=organization_id,
            container_no=number,
            iso_size_type=size_type,
            shipment_id=bound,
            source_ref=origin,
            seal_no_1=seal,
            seal_no_2=seal2,
            seal_no_3=seal3,
            vessel_name=vessel,
            voyage_no=voyage,
            remarks=note,
            cargo_description=goods,
            packaging_code=pack,
            created_by=user_id,
        )
        if current is not None:
            current.superseded_by = successor.id
        self.rows.append(successor)
        return successor


@pytest.fixture
def box_client(monkeypatch: pytest.MonkeyPatch) -> object:
    boxes = StubContainerService(object())
    jobs = StubShipmentService(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.containers.ContainerService", lambda _s: boxes)
    monkeypatch.setattr("app.api.containers.ShipmentService", lambda _s: jobs)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), boxes, jobs
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_list_supersede_and_reject_check_digit(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    payload = {
        "container_no": _GOOD,
        "iso_size_type": "22G1",
        "source_ref": "tenant:manual",
    }
    first = client.post("/api/v1/containers", headers=headers, json=payload)
    assert first.status_code == 201
    assert first.json()["organization_id"] == str(org_id)
    assert first.json()["seal_no_1"] is None
    assert first.json()["seal_no_2"] is None
    assert first.json()["seal_no_3"] is None
    assert first.json()["vessel_name"] is None
    assert first.json()["voyage_no"] is None
    assert first.json()["remarks"] is None
    assert first.json()["cargo_description"] is None
    assert first.json()["packaging_code"] is None
    assert "amount" not in first.json()
    assert "vgm" not in first.json()
    second = client.post(
        "/api/v1/containers",
        headers=headers,
        json={**payload, "iso_size_type": "45G1"},
    )
    assert second.status_code == 201
    assert second.json()["id"] != first.json()["id"]
    listed = client.get("/api/v1/containers", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == second.json()["id"]
    only_22 = client.get("/api/v1/containers", headers=headers, params={"iso_size_type": "22G1"})
    assert only_22.json() == []
    bad = client.post(
        "/api/v1/containers",
        headers=headers,
        json={**payload, "container_no": "CSQU3054384"},
    )
    assert bad.status_code == 400
    assert "kontrolna" in bad.json()["detail"]


def test_http_rejects_unknown_shipment(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "shipment_id": str(uuid4()),
            "source_ref": "tenant:manual",
        },
    )
    assert reply.status_code == 404
    assert "zlecenie" in reply.json()["detail"]


def test_http_create_container_with_seal_no_1(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "seal_no_1": " MSC1234567 ",
        },
    )
    assert created.status_code == 201
    assert created.json()["seal_no_1"] == "MSC1234567"
    assert "pin" not in created.json()
    assert "vgm" not in created.json()


def test_http_rejects_too_long_seal_no_1(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "seal_no_1": "x" * 33,
        },
    )
    assert reply.status_code == 400
    assert "plomba" in reply.json()["detail"]


def test_http_create_container_with_seal_no_2(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "seal_no_2": " HL987 ",
        },
    )
    assert created.status_code == 201
    assert created.json()["seal_no_2"] == "HL987"
    assert created.json()["seal_no_1"] is None
    assert "pin" not in created.json()


def test_http_rejects_too_long_seal_no_2(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "seal_no_2": "x" * 33,
        },
    )
    assert reply.status_code == 400
    assert "plomba" in reply.json()["detail"]


def test_http_create_container_with_seal_no_3(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "seal_no_3": " XY1 ",
        },
    )
    assert created.status_code == 201
    assert created.json()["seal_no_3"] == "XY1"
    assert created.json()["seal_no_1"] is None
    assert created.json()["seal_no_2"] is None
    assert "pin" not in created.json()


def test_http_rejects_too_long_seal_no_3(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "seal_no_3": "x" * 33,
        },
    )
    assert reply.status_code == 400
    assert "plomba" in reply.json()["detail"]


def test_http_create_container_with_vessel_name(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "vessel_name": " MSC GULSUN ",
        },
    )
    assert created.status_code == 201
    assert created.json()["vessel_name"] == "MSC GULSUN"
    assert created.json()["voyage_no"] is None
    assert "pin" not in created.json()


def test_http_rejects_too_long_vessel_name(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "vessel_name": "x" * 129,
        },
    )
    assert reply.status_code == 400
    assert "statek" in reply.json()["detail"]


def test_http_create_container_with_voyage_no(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "voyage_no": " 049W ",
        },
    )
    assert created.status_code == 201
    assert created.json()["voyage_no"] == "049W"
    assert created.json()["vessel_name"] is None
    assert "pin" not in created.json()
    assert "booking" not in created.json()


def test_http_rejects_too_long_voyage_no(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "voyage_no": "x" * 33,
        },
    )
    assert reply.status_code == 400
    assert "rejs" in reply.json()["detail"]


def test_http_create_container_with_remarks(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "remarks": " keep dry ",
        },
    )
    assert created.status_code == 201
    assert created.json()["remarks"] == "keep dry"
    assert "pin" not in created.json()
    assert "vgm" not in created.json()


def test_http_rejects_too_long_remarks(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "remarks": "x" * 257,
        },
    )
    assert reply.status_code == 400
    assert "uwaga" in reply.json()["detail"]


def test_http_create_container_with_cargo_description(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "cargo_description": " steel coils ",
        },
    )
    assert created.status_code == 201
    assert created.json()["cargo_description"] == "steel coils"
    assert created.json()["remarks"] is None
    assert "pin" not in created.json()
    assert "vgm" not in created.json()
    assert "weight_kg" not in created.json()


def test_http_rejects_too_long_cargo_description(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "cargo_description": "x" * 257,
        },
    )
    assert reply.status_code == 400
    assert "ładunek" in reply.json()["detail"]


def test_http_create_container_with_packaging_code(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "packaging_code": " CT ",
        },
    )
    assert created.status_code == 201
    assert created.json()["packaging_code"] == "CT"
    assert created.json()["cargo_description"] is None
    assert "pin" not in created.json()
    assert "vgm" not in created.json()
    assert "weight_kg" not in created.json()


def test_http_rejects_too_long_packaging_code(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "packaging_code": "x" * 33,
        },
    )
    assert reply.status_code == 400
    assert "opakowanie" in reply.json()["detail"]
