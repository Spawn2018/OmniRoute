from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.container import require_iso_size_type
from app.domain.errors import ResourceNotFound
from app.main import app
from app.models.container import Container
from app.models.party import Party
from app.models.shipment import Shipment
from app.models.shipment_leg import ShipmentLeg
from app.services.containers.container_service import (
    _box_draft,
    _box_unchanged,
    _container_row,
    _WriteBox,
)
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


class StubPartyService:
    def __init__(self) -> None:
        self.rows: list[Party] = []

    async def get_party(self, party_id: UUID) -> Party:
        for row in self.rows:
            if row.id == party_id:
                return row
        raise ResourceNotFound(f"nieznany kontrahent: {party_id}")


class StubShipmentLegService:
    def __init__(self) -> None:
        self.rows: list[ShipmentLeg] = []

    async def get_leg(self, leg_id: UUID) -> ShipmentLeg:
        for row in self.rows:
            if row.id == leg_id:
                return row
        raise ResourceNotFound(f"nieznany odcinek: {leg_id}")


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
        write: _WriteBox,
    ) -> Container:
        draft = _box_draft(write)
        current = next(
            (
                row
                for row in self.rows
                if row.container_no == draft.number and row.superseded_by is None
            ),
            None,
        )
        if current is not None and _box_unchanged(current, draft):
            return current
        successor = _container_row(organization_id, user_id, draft)
        if current is not None:
            current.superseded_by = successor.id
        self.rows.append(successor)
        return successor


@pytest.fixture
def box_client(monkeypatch: pytest.MonkeyPatch) -> object:
    boxes = StubContainerService(object())
    jobs = StubShipmentService(object())
    counterparts = StubPartyService()
    legs = StubShipmentLegService()
    boxes.counterparts = counterparts
    boxes.legs = legs

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.containers.ContainerService", lambda _s: boxes)
    monkeypatch.setattr("app.api.containers.ShipmentService", lambda _s: jobs)
    monkeypatch.setattr("app.api.containers.PartyService", lambda _s: counterparts)
    monkeypatch.setattr("app.api.containers.ShipmentLegService", lambda _s: legs)
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
    assert first.json()["ref_1"] is None
    assert first.json()["ref_2"] is None
    assert first.json()["ref_3"] is None
    assert first.json()["ref_4"] is None
    assert first.json()["ref_5"] is None
    assert first.json()["reefer"] is False
    assert first.json()["pickup_terminal"] is None
    assert first.json()["return_terminal"] is None
    assert first.json()["bl_kind"] is None
    assert first.json()["free_time_origin_h"] is None
    assert first.json()["free_time_dest_h"] is None
    assert first.json()["demurrage_free_days"] is None
    assert first.json()["detention_free_days"] is None
    assert first.json()["mixed_dd_days"] is None
    assert first.json()["si_cutoff_at"] is None
    assert first.json()["ams_cutoff_at"] is None
    assert first.json()["cy_cutoff_at"] is None
    assert first.json()["cfs_cutoff_at"] is None
    assert first.json()["vgm_kg"] is None
    assert first.json()["tare_kg"] is None
    assert first.json()["pin_code"] is None
    assert first.json()["payload_kg"] is None
    assert first.json()["teu"] is None
    assert first.json()["quantity"] is None
    assert first.json()["vgm_method"] is None
    assert first.json()["vgm_cutoff_at"] is None
    assert first.json()["last_survey_at"] is None
    assert first.json()["booking_no"] is None
    assert first.json()["carrier_party_id"] is None
    assert first.json()["shipment_leg_id"] is None
    assert "amount" not in first.json()
    assert "vgm" not in first.json()
    assert "tare" not in first.json()
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
    assert created.json()["weight_kg"] is None


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
    assert created.json()["weight_kg"] is None


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


def test_http_create_container_with_ref_1(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "ref_1": " PO123 ",
        },
    )
    assert created.status_code == 201
    assert created.json()["ref_1"] == "PO123"
    assert created.json()["packaging_code"] is None
    assert "pin" not in created.json()
    assert "vgm" not in created.json()
    assert created.json()["booking_no"] is None


def test_http_rejects_too_long_ref_1(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "ref_1": "x" * 65,
        },
    )
    assert reply.status_code == 400
    assert "referencja" in reply.json()["detail"]


def test_http_create_container_with_ref_2(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "ref_2": " BL456 ",
        },
    )
    assert created.status_code == 201
    assert created.json()["ref_2"] == "BL456"
    assert created.json()["ref_1"] is None
    assert "pin" not in created.json()
    assert "vgm" not in created.json()


def test_http_rejects_too_long_ref_2(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "ref_2": "x" * 65,
        },
    )
    assert reply.status_code == 400
    assert "referencja" in reply.json()["detail"]


def test_http_create_container_with_ref_3(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "ref_3": " PO789 ",
        },
    )
    assert created.status_code == 201
    assert created.json()["ref_3"] == "PO789"
    assert created.json()["ref_1"] is None
    assert created.json()["ref_2"] is None
    assert "pin" not in created.json()
    assert "vgm" not in created.json()


def test_http_rejects_too_long_ref_3(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "ref_3": "x" * 65,
        },
    )
    assert reply.status_code == 400
    assert "referencja" in reply.json()["detail"]


def test_http_create_container_with_ref_4(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "ref_4": " BK012 ",
        },
    )
    assert created.status_code == 201
    assert created.json()["ref_4"] == "BK012"
    assert created.json()["ref_1"] is None
    assert created.json()["ref_3"] is None
    assert "pin" not in created.json()
    assert "vgm" not in created.json()


def test_http_rejects_too_long_ref_4(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "ref_4": "x" * 65,
        },
    )
    assert reply.status_code == 400
    assert "referencja" in reply.json()["detail"]


def test_http_create_container_with_ref_5(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "ref_5": " SI345 ",
        },
    )
    assert created.status_code == 201
    assert created.json()["ref_5"] == "SI345"
    assert created.json()["ref_1"] is None
    assert created.json()["ref_4"] is None
    assert "pin" not in created.json()
    assert "vgm" not in created.json()


def test_http_rejects_too_long_ref_5(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "ref_5": "x" * 65,
        },
    )
    assert reply.status_code == 400
    assert "referencja" in reply.json()["detail"]


def test_http_create_container_with_reefer(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "reefer": True,
        },
    )
    assert created.status_code == 201
    assert created.json()["reefer"] is True
    assert created.json()["ref_5"] is None
    assert "temp_min" not in created.json()
    assert "pin" not in created.json()
    assert "vgm" not in created.json()


def test_http_rejects_non_bool_reefer(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "reefer": "yes",
        },
    )
    assert reply.status_code == 400
    assert "chłodniczy" in reply.json()["detail"]


def test_http_create_container_with_pickup_terminal(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "pickup_terminal": " GCT ",
        },
    )
    assert created.status_code == 201
    assert created.json()["pickup_terminal"] == "GCT"
    assert created.json()["reefer"] is False
    assert "pin" not in created.json()
    assert "vgm" not in created.json()


def test_http_rejects_too_long_pickup_terminal(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "pickup_terminal": "x" * 33,
        },
    )
    assert reply.status_code == 400
    assert "terminal" in reply.json()["detail"]


def test_http_create_container_with_return_terminal(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "return_terminal": " ECT ",
        },
    )
    assert created.status_code == 201
    assert created.json()["return_terminal"] == "ECT"
    assert created.json()["pickup_terminal"] is None
    assert "pin" not in created.json()
    assert "vgm" not in created.json()


def test_http_rejects_too_long_return_terminal(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "return_terminal": "x" * 33,
        },
    )
    assert reply.status_code == 400
    assert "terminal" in reply.json()["detail"]


def test_http_create_container_with_bl_kind(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "bl_kind": " original ",
        },
    )
    assert created.status_code == 201
    assert created.json()["bl_kind"] == "original"
    assert created.json()["return_terminal"] is None
    assert "hbl" not in created.json()
    assert "vgm" not in created.json()


def test_http_rejects_ocean_bill_kind_on_container(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "bl_kind": "hbl",
        },
    )
    assert reply.status_code == 400
    assert "list" in reply.json()["detail"]


def test_http_create_container_with_free_time_origin_h(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "free_time_origin_h": 48,
        },
    )
    assert created.status_code == 201
    assert created.json()["free_time_origin_h"] == 48
    assert created.json()["bl_kind"] is None
    assert "remaining" not in created.json()
    assert "vgm" not in created.json()


def test_http_rejects_negative_free_time_origin_h(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "free_time_origin_h": -1,
        },
    )
    assert reply.status_code == 400
    assert "godziny" in reply.json()["detail"]


def test_http_create_container_with_free_time_dest_h(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "free_time_dest_h": 24,
        },
    )
    assert created.status_code == 201
    assert created.json()["free_time_dest_h"] == 24
    assert created.json()["free_time_origin_h"] is None
    assert "remaining" not in created.json()
    assert "vgm" not in created.json()


def test_http_rejects_negative_free_time_dest_h(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "free_time_dest_h": -1,
        },
    )
    assert reply.status_code == 400
    assert "godziny" in reply.json()["detail"]


def test_http_create_container_with_demurrage_free_days(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "demurrage_free_days": 7,
        },
    )
    assert created.status_code == 201
    assert created.json()["demurrage_free_days"] == 7
    assert created.json()["free_time_dest_h"] is None
    assert "remaining" not in created.json()
    assert "countdown" not in created.json()


def test_http_rejects_negative_demurrage_free_days(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "demurrage_free_days": -1,
        },
    )
    assert reply.status_code == 400
    assert "dni" in reply.json()["detail"]


def test_http_create_container_with_detention_free_days(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "detention_free_days": 5,
        },
    )
    assert created.status_code == 201
    assert created.json()["detention_free_days"] == 5
    assert created.json()["demurrage_free_days"] is None
    assert "remaining" not in created.json()
    assert "countdown" not in created.json()


def test_http_rejects_negative_detention_free_days(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "detention_free_days": -1,
        },
    )
    assert reply.status_code == 400
    assert "dni" in reply.json()["detail"]


def test_http_create_container_with_mixed_dd_days(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "mixed_dd_days": 3,
        },
    )
    assert created.status_code == 201
    assert created.json()["mixed_dd_days"] == 3
    assert created.json()["detention_free_days"] is None
    assert "remaining" not in created.json()
    assert "countdown" not in created.json()


def test_http_create_container_with_tare_kg(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "tare_kg": "2200.5000",
        },
    )
    assert created.status_code == 201
    assert created.json()["tare_kg"] == "2200.5000"
    assert created.json()["vgm_kg"] is None
    assert "amount" not in created.json()
    assert "pin" not in created.json()


def test_http_rejects_float_tare_kg(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "tare_kg": 12.5,
        },
    )
    assert reply.status_code == 400
    assert "tara" in reply.json()["detail"]


def test_http_create_container_with_pin_code(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "pin_code": "GATE-18",
        },
    )
    assert created.status_code == 201
    assert created.json()["pin_code"] == "GATE-18"
    assert created.json()["tare_kg"] is None
    assert created.json()["booking_no"] is None
    assert "ciphertext" not in created.json()


def test_http_rejects_non_text_pin_code(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "pin_code": 12,
        },
    )
    assert reply.status_code == 400
    assert "pin" in reply.json()["detail"]


def test_http_create_container_with_payload_kg(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "payload_kg": "28000.5000",
        },
    )
    assert created.status_code == 201
    assert created.json()["payload_kg"] == "28000.5000"
    assert created.json()["tare_kg"] is None
    assert created.json()["vgm_kg"] is None
    assert created.json()["pin_code"] is None
    assert created.json()["quantity"] is None


def test_http_rejects_float_payload_kg(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "payload_kg": 12.5,
        },
    )
    assert reply.status_code == 400
    assert "ładowność" in reply.json()["detail"]


def test_http_create_container_with_teu(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "teu": "2.2500",
        },
    )
    assert created.status_code == 201
    assert created.json()["teu"] == "2.2500"
    assert created.json()["payload_kg"] is None
    assert created.json()["iso_size_type"] == "22G1"
    assert created.json()["quantity"] is None


def test_http_rejects_float_teu(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "teu": 1.5,
        },
    )
    assert reply.status_code == 400
    assert "teu" in reply.json()["detail"]


def test_http_create_container_with_quantity(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "quantity": 3,
        },
    )
    assert created.status_code == 201
    assert created.json()["quantity"] == 3
    assert created.json()["teu"] is None
    assert created.json()["weight_kg"] is None
    assert "stop_id" not in created.json()


def test_http_rejects_negative_container_quantity(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "quantity": -1,
        },
    )
    assert reply.status_code == 400
    assert "ilość" in reply.json()["detail"]


def test_http_create_container_with_weight_kg(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "weight_kg": "1250.5000",
        },
    )
    assert created.status_code == 201
    assert created.json()["weight_kg"] == "1250.5000"
    assert created.json()["quantity"] is None
    assert created.json()["tare_kg"] is None
    assert created.json()["vgm_kg"] is None
    assert created.json()["volume_m3"] is None


def test_http_rejects_zero_container_weight(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "weight_kg": "0",
        },
    )
    assert reply.status_code == 400
    assert "waga" in reply.json()["detail"]


def test_http_create_container_with_volume_m3(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "volume_m3": "12.5000",
        },
    )
    assert created.status_code == 201
    assert created.json()["volume_m3"] == "12.5000"
    assert created.json()["weight_kg"] is None
    assert created.json()["pickup_date"] is None


def test_http_rejects_zero_container_volume(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "volume_m3": "0",
        },
    )
    assert reply.status_code == 400
    assert "objętość" in reply.json()["detail"]


def test_http_create_container_with_pickup_date(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "pickup_date": "2026-09-19",
        },
    )
    assert created.status_code == 201
    assert created.json()["pickup_date"] == "2026-09-19"
    assert created.json()["volume_m3"] is None


def test_http_rejects_timestamp_container_pickup(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "pickup_date": "2026-09-19T00:00:00",
        },
    )
    assert reply.status_code == 400
    assert "data odbioru" in reply.json()["detail"]


def test_http_rejects_negative_mixed_dd_days(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "mixed_dd_days": -1,
        },
    )
    assert reply.status_code == 400
    assert "dni" in reply.json()["detail"]


def test_http_create_container_with_si_cutoff_at(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "si_cutoff_at": "2026-09-10T12:00:00+00:00",
        },
    )
    assert created.status_code == 201
    assert created.json()["si_cutoff_at"].startswith("2026-09-10T12:00:00")
    assert created.json()["free_time_dest_h"] is None
    assert "pin" not in created.json()
    assert "vgm" not in created.json()


def test_http_rejects_naive_si_cutoff_at(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "si_cutoff_at": "2026-09-10T12:00:00",
        },
    )
    assert reply.status_code == 400
    assert "si" in reply.json()["detail"]


def test_http_create_container_with_ams_cutoff_at(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "ams_cutoff_at": "2026-09-10T12:00:00+00:00",
        },
    )
    assert created.status_code == 201
    assert created.json()["ams_cutoff_at"].startswith("2026-09-10T12:00:00")
    assert created.json()["si_cutoff_at"] is None
    assert "pin" not in created.json()
    assert "vgm" not in created.json()


def test_http_rejects_naive_ams_cutoff_at(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "ams_cutoff_at": "2026-09-10T12:00:00",
        },
    )
    assert reply.status_code == 400
    assert "ams" in reply.json()["detail"]


def test_http_create_container_with_cy_cutoff_at(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "cy_cutoff_at": "2026-09-10T12:00:00+00:00",
        },
    )
    assert created.status_code == 201
    assert created.json()["cy_cutoff_at"].startswith("2026-09-10T12:00:00")
    assert created.json()["ams_cutoff_at"] is None
    assert "pin" not in created.json()
    assert "vgm" not in created.json()


def test_http_rejects_naive_cy_cutoff_at(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "cy_cutoff_at": "2026-09-10T12:00:00",
        },
    )
    assert reply.status_code == 400
    assert "cy" in reply.json()["detail"]


def test_http_create_container_with_cfs_cutoff_at(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "cfs_cutoff_at": "2026-09-10T12:00:00+00:00",
        },
    )
    assert created.status_code == 201
    assert created.json()["cfs_cutoff_at"].startswith("2026-09-10T12:00:00")
    assert created.json()["cy_cutoff_at"] is None
    assert "pin" not in created.json()
    assert "vgm" not in created.json()


def test_http_rejects_naive_cfs_cutoff_at(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "cfs_cutoff_at": "2026-09-10T12:00:00",
        },
    )
    assert reply.status_code == 400
    assert "cfs" in reply.json()["detail"]


def test_http_create_container_with_vgm_bundle(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "vgm_kg": "12345.5000",
            "vgm_method": "method1",
            "vgm_cutoff_at": "2026-09-10T12:00:00+00:00",
        },
    )
    assert created.status_code == 201
    assert created.json()["vgm_kg"] == "12345.5000"
    assert created.json()["vgm_method"] == "method1"
    assert created.json()["vgm_cutoff_at"].startswith("2026-09-10T12:00:00")
    assert "pin" not in created.json()
    assert "amount" not in created.json()


def test_http_rejects_float_vgm_kg(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "vgm_kg": 12.5,
        },
    )
    assert reply.status_code == 400
    assert "vgm" in reply.json()["detail"]


def test_http_rejects_unknown_vgm_method(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "vgm_method": "weighed",
        },
    )
    assert reply.status_code == 400
    assert "vgm" in reply.json()["detail"]


def test_http_rejects_naive_vgm_cutoff_at(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "vgm_cutoff_at": "2026-09-10T12:00:00",
        },
    )
    assert reply.status_code == 400
    assert "vgm" in reply.json()["detail"]


def test_http_create_container_with_last_survey_at(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "last_survey_at": "2026-09-10T12:00:00+00:00",
        },
    )
    assert created.status_code == 201
    assert created.json()["last_survey_at"].startswith("2026-09-10T12:00:00")
    assert created.json()["vgm_cutoff_at"] is None
    assert "pin" not in created.json()


def test_http_rejects_naive_last_survey_at(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "last_survey_at": "2026-09-10T12:00:00",
        },
    )
    assert reply.status_code == 400
    assert "survey" in reply.json()["detail"]


def test_http_create_container_with_booking_no(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "booking_no": " BK123456 ",
        },
    )
    assert created.status_code == 201
    assert created.json()["booking_no"] == "BK123456"
    assert created.json()["last_survey_at"] is None
    assert "pin" not in created.json()


def test_http_rejects_too_long_booking_no(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "booking_no": "x" * 65,
        },
    )
    assert reply.status_code == 400
    assert "booking" in reply.json()["detail"]


def test_http_create_container_with_carrier_party_id(box_client: object) -> None:
    client, boxes, _jobs = box_client
    headers = bearer_auth_headers()
    carrier = Party(
        id=uuid4(),
        organization_id=uuid4(),
        legal_name="Line",
        country_code="PL",
        roles=["carrier"],
        source_ref="tenant:manual",
        is_active=True,
    )
    boxes.counterparts.rows.append(carrier)
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "carrier_party_id": str(carrier.id),
        },
    )
    assert created.status_code == 201
    assert created.json()["carrier_party_id"] == str(carrier.id)
    assert created.json()["booking_no"] is None
    assert "pin" not in created.json()


def test_http_rejects_unknown_carrier_party_id(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "carrier_party_id": str(uuid4()),
        },
    )
    assert reply.status_code == 404
    assert "kontrahent" in reply.json()["detail"]


def test_http_create_container_with_shipment_leg_id(box_client: object) -> None:
    client, boxes, _jobs = box_client
    headers = bearer_auth_headers()
    leg = ShipmentLeg(
        id=uuid4(),
        organization_id=uuid4(),
        shipment_id=uuid4(),
        origin_location_id=uuid4(),
        destination_location_id=uuid4(),
        leg_kind="road",
        source_ref="fixture://shipment-leg/http",
    )
    boxes.legs.rows.append(leg)
    created = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "shipment_leg_id": str(leg.id),
        },
    )
    assert created.status_code == 201
    assert created.json()["shipment_leg_id"] == str(leg.id)
    assert created.json()["carrier_party_id"] is None
    assert "pin" not in created.json()


def test_http_rejects_unknown_shipment_leg_id(box_client: object) -> None:
    client, _boxes, _jobs = box_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/containers",
        headers=headers,
        json={
            "container_no": _GOOD,
            "iso_size_type": "22G1",
            "source_ref": "tenant:manual",
            "shipment_leg_id": str(uuid4()),
        },
    )
    assert reply.status_code == 404
    assert "odcinek" in reply.json()["detail"]
