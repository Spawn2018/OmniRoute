from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.subcontract_edge_mark import parse_subcontract_edge_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.subcontract_edge_mark import SubcontractEdgeMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "bytes")


def test_migration_255_creates_subcontract_edge_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/255_subcontract_edge_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "255_subcontract_edge_mark"' in source
    assert 'down_revision: str | None = "254_sanctions_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "subcontract_edge_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "bytes"):
        assert banned not in source


def test_importlinter_lists_subcontract_edge_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.subcontract_edge_marks" in forbidden
    assert "app.models.subcontract_edge_mark" in forbidden


def test_generated_api_types_include_subcontract_edge_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "SubcontractEdgeMarkResponse" in source
    assert "SubcontractEdgeMarkCreate" in source


def test_fga_source_declares_subcontract_edge_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_subcontract_edge_marks: member" in source


def test_authorization_model_grants_subcontract_edge_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_subcontract_edge_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitSubcontractEdgeAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemorySubcontractEdgeDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[SubcontractEdgeMark] = []

    async def list_marks(self) -> list[SubcontractEdgeMark]:
        return list(self.rows)

    async def persist_subcontract_edge_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        edge_kind: object,
        source_ref: object,
    ) -> SubcontractEdgeMark:
        code, kind, origin = parse_subcontract_edge_mark_row(
            mark_code,
            edge_kind,
            source_ref,
        )
        row = SubcontractEdgeMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            edge_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def subcontract_edge_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemorySubcontractEdgeDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.subcontract_edge_marks.SubcontractEdgeMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitSubcontractEdgeAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "prime_01",
        "edge_kind": "prime",
        "source_ref": "fixture://subcontract-edge-mark/a",
    }
    body.update(extra)
    return body


def test_post_subcontract_edge_mark_persists(subcontract_edge_http: object) -> None:
    client, desk = subcontract_edge_http
    response = client.post(
        "/api/v1/subcontract-edge-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["edge_kind"] == "prime"
    assert len(desk.rows) == 1


def test_post_subcontract_edge_mark_rejects_amount_bytes(subcontract_edge_http: object) -> None:
    client, _desk = subcontract_edge_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/subcontract-edge-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_subcontract_edge_mark_rejects_bad_code(subcontract_edge_http: object) -> None:
    client, _desk = subcontract_edge_http
    response = client.post(
        "/api/v1/subcontract-edge-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_subcontract_edge_mark_rejects_bad_kind(subcontract_edge_http: object) -> None:
    client, _desk = subcontract_edge_http
    response = client.post(
        "/api/v1/subcontract-edge-marks",
        headers=bearer_auth_headers(),
        json=_payload(edge_kind="engine"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(subcontract_edge_http: object) -> None:
    client, _desk = subcontract_edge_http
    response = client.post(
        "/api/v1/subcontract-edge-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_subcontract_edge_marks_lists_rows(subcontract_edge_http: object) -> None:
    client, desk = subcontract_edge_http
    client.post(
        "/api/v1/subcontract-edge-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/subcontract-edge-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
