from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.impact_node_mark import parse_impact_node_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.impact_node_mark import ImpactNodeMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "bytes")


def test_migration_409_creates_impact_node_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/409_impact_node_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "409_impact_node_mark"' in source
    assert 'down_revision: str | None = "408_allocation_level"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "impact_node_mark_tenant_isolation" in source
    for banned in ("amount", "float(", "httpx", "currency", "bytes"):
        assert banned not in source.lower()
    assert "charge" not in source
    assert "TRUE CONTRIBUTION" not in source


def test_importlinter_lists_impact_node_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.impact_node_marks" in forbidden
    assert "app.models.impact_node_mark" in forbidden


def test_generated_api_types_include_impact_node_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "ImpactNodeMarkResponse" in source
    assert "ImpactNodeMarkCreate" in source


def test_fga_source_declares_impact_node_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_impact_node_marks: member" in source


def test_authorization_model_grants_impact_node_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_impact_node_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitYardAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryYardDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[ImpactNodeMark] = []

    async def list_marks(self) -> list[ImpactNodeMark]:
        return list(self.rows)

    async def persist_impact_node_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        node_kind: object,
        source_ref: object,
    ) -> ImpactNodeMark:
        code, kind, origin = parse_impact_node_mark_row(
            mark_code,
            node_kind,
            source_ref,
        )
        row = ImpactNodeMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            node_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def impact_node_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryYardDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.impact_node_marks.ImpactNodeMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitYardAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "shipment_01",
        "node_kind": "shipment",
        "source_ref": "fixture://impact-node-mark/a",
    }
    body.update(extra)
    return body


def test_post_impact_node_mark_persists(impact_node_http: object) -> None:
    client, desk = impact_node_http
    response = client.post(
        "/api/v1/impact-node-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["node_kind"] == "shipment"
    assert len(desk.rows) == 1


def test_post_impact_node_mark_rejects_amount_bytes(impact_node_http: object) -> None:
    client, _desk = impact_node_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/impact-node-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_impact_node_mark_rejects_bad_code(impact_node_http: object) -> None:
    client, _desk = impact_node_http
    response = client.post(
        "/api/v1/impact-node-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_impact_node_mark_rejects_bad_kind(impact_node_http: object) -> None:
    client, _desk = impact_node_http
    response = client.post(
        "/api/v1/impact-node-marks",
        headers=bearer_auth_headers(),
        json=_payload(node_kind="engine"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_impact_node_mark_rejects_foreign_source_ref(impact_node_http: object) -> None:
    client, _desk = impact_node_http
    response = client.post(
        "/api/v1/impact-node-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_impact_node_marks_lists_rows(impact_node_http: object) -> None:
    client, desk = impact_node_http
    client.post(
        "/api/v1/impact-node-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/impact-node-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
