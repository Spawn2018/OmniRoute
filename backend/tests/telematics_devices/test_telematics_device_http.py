from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.telematics_device import parse_telematics_device_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.telematics_device import TelematicsDevice
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "pair")


def test_migration_363_creates_telematics_device_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/363_telematics_device.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "363_telematics_device"' in source
    assert 'down_revision: str | None = "362_position_event"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "telematics_device_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source


def test_importlinter_lists_telematics_device_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.telematics_devices" in forbidden
    assert "app.models.telematics_device" in forbidden


def test_fga_source_declares_telematics_device_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_telematics_devices: member" in source


def test_authorization_model_grants_telematics_devices_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_telematics_devices"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitDeviceAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryDeviceDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[TelematicsDevice] = []

    async def list_devices(self) -> list[TelematicsDevice]:
        return list(self.rows)

    async def persist_telematics_device(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        device_code: object,
        device_kind: object,
        source_ref: object,
    ) -> TelematicsDevice:
        code, kind, origin = parse_telematics_device_row(
            device_code,
            device_kind,
            source_ref,
        )
        row = TelematicsDevice(
            id=uuid4(),
            organization_id=organization_id,
            device_code=code,
            device_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def device_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryDeviceDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.telematics_devices.TelematicsDeviceService",
        lambda _s: desk,
    )
    set_authz_checker(PermitDeviceAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "device_code": "trk_yard_01",
        "device_kind": "tracker",
        "source_ref": "fixture://telematics-device/a",
    }
    body.update(extra)
    return body


def test_post_telematics_device_persists(device_http: object) -> None:
    client, desk = device_http
    response = client.post(
        "/api/v1/telematics-devices",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["device_kind"] == "tracker"
    assert len(desk.rows) == 1


def test_post_telematics_device_rejects_amount_pair(device_http: object) -> None:
    client, _desk = device_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/telematics-devices",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_telematics_device_rejects_bad_kind(device_http: object) -> None:
    client, _desk = device_http
    response = client.post(
        "/api/v1/telematics-devices",
        headers=bearer_auth_headers(),
        json=_payload(device_kind="poll"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_telematics_device_rejects_foreign_source_ref(
    device_http: object,
) -> None:
    client, _desk = device_http
    response = client.post(
        "/api/v1/telematics-devices",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_telematics_devices_lists_rows(device_http: object) -> None:
    client, desk = device_http
    client.post(
        "/api/v1/telematics-devices",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/telematics-devices",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
