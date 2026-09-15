from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.ingest_gate_mark import parse_ingest_gate_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.ingest_gate_mark import IngestGateMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount",)


def test_migration_383_creates_ingest_gate_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/413_ingest_gate_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "413_ingest_gate_mark"' in source
    assert 'down_revision: str | None = "412_data_source"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "ingest_gate_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "live_ingest"):
        assert banned not in source


def test_importlinter_lists_ingest_gate_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.ingest_gate_marks" in forbidden
    assert "app.models.ingest_gate_mark" in forbidden


def test_fga_source_declares_ingest_gate_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_ingest_gate_marks: member" in source


def test_authorization_model_grants_ingest_gate_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_ingest_gate_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class IngestGateMarkAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryLineImpactLayerDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[IngestGateMark] = []

    async def list_marks(self) -> list[IngestGateMark]:
        return list(self.rows)

    async def persist_ingest_gate_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        gate_kind: object,
        source_ref: object,
    ) -> IngestGateMark:
        code, kind, origin = parse_ingest_gate_mark_row(
            mark_code,
            gate_kind,
            source_ref,
        )
        row = IngestGateMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            gate_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def ops_room_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryLineImpactLayerDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.ingest_gate_marks.IngestGateMarkService",
        lambda _s: desk,
    )
    set_authz_checker(IngestGateMarkAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "ig_truth_01",
        "gate_kind": "truth",
        "source_ref": "fixture://ingest-gate-mark/a",
    }
    body.update(extra)
    return body


def test_post_ingest_gate_mark_persists(ops_room_http: object) -> None:
    client, desk = ops_room_http
    response = client.post(
        "/api/v1/ingest-gate-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["gate_kind"] == "truth"
    assert len(desk.rows) == 1


def test_post_ingest_gate_mark_rejects_amount(ops_room_http: object) -> None:
    client, _desk = ops_room_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/ingest-gate-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_ingest_gate_mark_rejects_bad_kind(ops_room_http: object) -> None:
    client, _desk = ops_room_http
    response = client.post(
        "/api/v1/ingest-gate-marks",
        headers=bearer_auth_headers(),
        json=_payload(gate_kind="live_ingest"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_ingest_gate_mark_rejects_foreign_source_ref(ops_room_http: object) -> None:
    client, _desk = ops_room_http
    response = client.post(
        "/api/v1/ingest-gate-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_ingest_gate_marks_lists_rows(ops_room_http: object) -> None:
    client, desk = ops_room_http
    client.post(
        "/api/v1/ingest-gate-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/ingest-gate-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
