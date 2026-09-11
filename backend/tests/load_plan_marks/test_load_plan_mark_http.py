from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.load_plan_mark import parse_load_plan_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.load_plan_mark import LoadPlanMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "axle")


def test_migration_239_creates_load_plan_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/239_load_plan_mark.py").read_text(encoding="utf-8")
    assert 'revision: str = "239_load_plan_mark"' in source
    assert 'down_revision: str | None = "238_oog_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "load_plan_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "axle"):
        assert banned not in source


def test_importlinter_lists_load_plan_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.load_plan_marks" in forbidden
    assert "app.models.load_plan_mark" in forbidden


def test_generated_api_types_include_load_plan_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "LoadPlanMarkResponse" in source
    assert "LoadPlanMarkCreate" in source


def test_fga_source_declares_load_plan_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_load_plan_marks: member" in source


def test_authorization_model_grants_load_plan_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_load_plan_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitLoadPlanAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryLoadPlanDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[LoadPlanMark] = []

    async def list_marks(self) -> list[LoadPlanMark]:
        return list(self.rows)

    async def persist_load_plan_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        stance_kind: object,
        source_ref: object,
    ) -> LoadPlanMark:
        code, kind, origin = parse_load_plan_mark_row(
            mark_code,
            stance_kind,
            source_ref,
        )
        row = LoadPlanMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            stance_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def load_plan_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryLoadPlanDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr("app.api.load_plan_marks.LoadPlanMarkService", lambda _s: desk)
    set_authz_checker(PermitLoadPlanAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "load_axes_01",
        "stance_kind": "axes",
        "source_ref": "fixture://load-plan-mark/a",
    }
    body.update(extra)
    return body


def test_post_load_plan_mark_persists(load_plan_http: object) -> None:
    client, desk = load_plan_http
    response = client.post(
        "/api/v1/load-plan-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["stance_kind"] == "axes"
    assert len(desk.rows) == 1


def test_post_load_plan_mark_rejects_amount_axle(load_plan_http: object) -> None:
    client, _desk = load_plan_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/load-plan-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_load_plan_mark_rejects_bad_kind(load_plan_http: object) -> None:
    client, _desk = load_plan_http
    response = client.post(
        "/api/v1/load-plan-marks",
        headers=bearer_auth_headers(),
        json=_payload(stance_kind="or_solver"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_load_plan_mark_rejects_foreign_source_ref(load_plan_http: object) -> None:
    client, _desk = load_plan_http
    response = client.post(
        "/api/v1/load-plan-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_load_plan_marks_lists_rows(load_plan_http: object) -> None:
    client, desk = load_plan_http
    client.post(
        "/api/v1/load-plan-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/load-plan-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
