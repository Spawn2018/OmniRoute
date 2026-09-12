from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.role_view_mark import parse_role_view_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.role_view_mark import RoleViewMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]

_FORBIDDEN = ("amount", "board")


def test_migration_306_creates_role_view_and_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/306_role_view_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "306_role_view_mark"' in source
    assert 'down_revision: str | None = "305_mail_accept_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "role_view_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source


def test_importlinter_lists_role_view_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.role_view_marks" in forbidden
    assert "app.models.role_view_mark" in forbidden


def test_api_types_include_role_view_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "RoleViewMarkResponse" in source
    assert "RoleViewMarkCreate" in source


def test_fga_source_declares_role_view_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_role_view_marks: member" in source


def test_fga_model_grants_role_view_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_role_view_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitRoleViewAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryRoleViewDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[RoleViewMark] = []

    async def list_marks(self) -> list[RoleViewMark]:
        return list(self.rows)

    async def persist_role_view_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        view_kind: object,
        source_ref: object,
    ) -> RoleViewMark:
        code, kind, origin = parse_role_view_mark_row(
            mark_code,
            view_kind,
            source_ref,
        )
        row = RoleViewMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            view_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def role_view_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryRoleViewDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.role_view_marks.RoleViewMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitRoleViewAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "rvm_groupage_01",
        "view_kind": "groupage",
        "source_ref": "fixture://role-view-mark/a",
    }
    body.update(extra)
    return body


def test_post_persists(role_view_http: object) -> None:
    client, desk = role_view_http
    response = client.post(
        "/api/v1/role-view-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["view_kind"] == "groupage"
    assert len(desk.rows) == 1


def test_post_rejects_amount_board(role_view_http: object) -> None:
    client, _desk = role_view_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/role-view-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(role_view_http: object) -> None:
    client, _desk = role_view_http
    response = client.post(
        "/api/v1/role-view-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_rejects_bad_kind(role_view_http: object) -> None:
    client, _desk = role_view_http
    response = client.post(
        "/api/v1/role-view-marks",
        headers=bearer_auth_headers(),
        json=_payload(view_kind="timeline_board"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(role_view_http: object) -> None:
    client, _desk = role_view_http
    response = client.post(
        "/api/v1/role-view-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(role_view_http: object) -> None:
    client, desk = role_view_http
    client.post(
        "/api/v1/role-view-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/role-view-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
