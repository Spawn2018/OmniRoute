from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.impact_edge_mark import parse_impact_edge_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.impact_edge_mark import ImpactEdgeMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "bytes")


def test_migration_410_creates_impact_edge_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/410_impact_edge_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "410_impact_edge_mark"' in source
    assert 'down_revision: str | None = "409_impact_node_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "impact_edge_mark_tenant_isolation" in source
    for banned in ("amount", "float(", "httpx", "currency", "bytes"):
        assert banned not in source.lower()
    assert "charge" not in source
    assert "impact_node_mark" not in source or "409_impact_node_mark" in source
    assert "TRUE CONTRIBUTION" not in source
    assert "FOREIGN KEY" not in source.upper() or "organization" in source.lower()


def test_importlinter_lists_impact_edge_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.impact_edge_marks" in forbidden
    assert "app.models.impact_edge_mark" in forbidden


def test_generated_api_types_include_impact_edge_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "ImpactEdgeMarkResponse" in source
    assert "ImpactEdgeMarkCreate" in source


def test_fga_source_declares_impact_edge_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_impact_edge_marks: member" in source


def test_authorization_model_grants_impact_edge_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_impact_edge_marks"]
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
        self.rows: list[ImpactEdgeMark] = []

    async def list_marks(self) -> list[ImpactEdgeMark]:
        return list(self.rows)

    async def persist_impact_edge_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        from_kind: object,
        to_kind: object,
        source_ref: object,
    ) -> ImpactEdgeMark:
        code, start, end, origin = parse_impact_edge_mark_row(
            mark_code,
            from_kind,
            to_kind,
            source_ref,
        )
        row = ImpactEdgeMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            from_kind=start,
            to_kind=end,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def impact_edge_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryYardDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.impact_edge_marks.ImpactEdgeMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitYardAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "ship_to_inv",
        "from_kind": "shipment",
        "to_kind": "inventory",
        "source_ref": "fixture://impact-edge-mark/a",
    }
    body.update(extra)
    return body


def test_post_impact_edge_mark_persists(impact_edge_http: object) -> None:
    client, desk = impact_edge_http
    response = client.post(
        "/api/v1/impact-edge-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["from_kind"] == "shipment"
    assert response.json()["to_kind"] == "inventory"
    assert len(desk.rows) == 1


def test_post_impact_edge_mark_rejects_amount_bytes(impact_edge_http: object) -> None:
    client, _desk = impact_edge_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/impact-edge-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_impact_edge_mark_rejects_bad_code(impact_edge_http: object) -> None:
    client, _desk = impact_edge_http
    response = client.post(
        "/api/v1/impact-edge-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_impact_edge_mark_rejects_bad_from_kind(impact_edge_http: object) -> None:
    client, _desk = impact_edge_http
    response = client.post(
        "/api/v1/impact-edge-marks",
        headers=bearer_auth_headers(),
        json=_payload(from_kind="engine"),
    )
    assert response.status_code == 400
    assert "from_kind" in response.json()["detail"]


def test_post_impact_edge_mark_rejects_bad_to_kind(impact_edge_http: object) -> None:
    client, _desk = impact_edge_http
    response = client.post(
        "/api/v1/impact-edge-marks",
        headers=bearer_auth_headers(),
        json=_payload(to_kind="engine"),
    )
    assert response.status_code == 400
    assert "to_kind" in response.json()["detail"]


def test_post_impact_edge_mark_rejects_foreign_source_ref(impact_edge_http: object) -> None:
    client, _desk = impact_edge_http
    response = client.post(
        "/api/v1/impact-edge-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_impact_edge_marks_lists_rows(impact_edge_http: object) -> None:
    client, desk = impact_edge_http
    client.post(
        "/api/v1/impact-edge-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/impact-edge-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
