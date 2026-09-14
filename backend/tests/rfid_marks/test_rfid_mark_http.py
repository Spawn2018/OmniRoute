from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.rfid_mark import parse_rfid_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.rfid_mark import RfidMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount",)


def test_migration_380_creates_rfid_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/380_rfid_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "380_rfid_mark"' in source
    assert 'down_revision: str | None = "379_wms_flow_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "rfid_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "epc", "impinj"):
        assert banned not in source


def test_importlinter_lists_rfid_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.rfid_marks" in forbidden
    assert "app.models.rfid_mark" in forbidden


def test_fga_source_declares_rfid_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_rfid_marks: member" in source


def test_authorization_model_grants_rfid_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_rfid_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class RfidMarkAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryRfidDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[RfidMark] = []

    async def list_marks(self) -> list[RfidMark]:
        return list(self.rows)

    async def persist_rfid_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        rfid_kind: object,
        source_ref: object,
    ) -> RfidMark:
        code, kind, origin = parse_rfid_mark_row(mark_code, rfid_kind, source_ref)
        row = RfidMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            rfid_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def rfid_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryRfidDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.rfid_marks.RfidMarkService",
        lambda _s: desk,
    )
    set_authz_checker(RfidMarkAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "rfid_gate_01",
        "rfid_kind": "gate",
        "source_ref": "fixture://rfid/a",
    }
    body.update(extra)
    return body


def test_post_rfid_mark_persists(rfid_http: object) -> None:
    client, desk = rfid_http
    response = client.post(
        "/api/v1/rfid-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["rfid_kind"] == "gate"
    assert len(desk.rows) == 1


def test_post_rfid_mark_rejects_amount(rfid_http: object) -> None:
    client, _desk = rfid_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/rfid-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rfid_mark_rejects_bad_kind(rfid_http: object) -> None:
    client, _desk = rfid_http
    response = client.post(
        "/api/v1/rfid-marks",
        headers=bearer_auth_headers(),
        json=_payload(rfid_kind="live_rfid"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_rfid_mark_rejects_foreign_source_ref(rfid_http: object) -> None:
    client, _desk = rfid_http
    response = client.post(
        "/api/v1/rfid-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_rfid_marks_lists_rows(rfid_http: object) -> None:
    client, desk = rfid_http
    client.post(
        "/api/v1/rfid-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/rfid-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
