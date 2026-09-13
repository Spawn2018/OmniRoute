from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.route_plan_mark import parse_route_plan_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.route_plan_mark import RoutePlanMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "km")


def test_migration_360_creates_route_plan_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/360_route_plan_mk.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "360_route_plan_mk"' in source
    assert 'down_revision: str | None = "359_circle_pair"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "route_plan_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "valhalla"):
        assert banned not in source


def test_importlinter_lists_route_plan_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.route_plan_marks" in forbidden
    assert "app.models.route_plan_mark" in forbidden


def test_fga_source_declares_route_plan_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_route_plan_marks: member" in source


def test_authorization_model_grants_route_plan_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_route_plan_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitRoutePlanAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryRoutePlanDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[RoutePlanMark] = []

    async def list_marks(self) -> list[RoutePlanMark]:
        return list(self.rows)

    async def persist_route_plan_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        plan_kind: object,
        source_ref: object,
    ) -> RoutePlanMark:
        code, kind, origin = parse_route_plan_mark_row(
            mark_code,
            plan_kind,
            source_ref,
        )
        row = RoutePlanMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            plan_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def route_plan_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryRoutePlanDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr("app.api.route_plan_marks.RoutePlanMarkService", lambda _s: desk)
    set_authz_checker(PermitRoutePlanAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "route_gdn_osl",
        "plan_kind": "route",
        "source_ref": "fixture://route-plan-mark/a",
    }
    body.update(extra)
    return body


def test_post_route_plan_mark_persists(route_plan_http: object) -> None:
    client, desk = route_plan_http
    response = client.post(
        "/api/v1/route-plan-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["plan_kind"] == "route"
    assert len(desk.rows) == 1


def test_post_route_plan_mark_rejects_amount_km(route_plan_http: object) -> None:
    client, _desk = route_plan_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/route-plan-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_route_plan_mark_rejects_bad_kind(route_plan_http: object) -> None:
    client, _desk = route_plan_http
    response = client.post(
        "/api/v1/route-plan-marks",
        headers=bearer_auth_headers(),
        json=_payload(plan_kind="valhalla"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_route_plan_mark_rejects_foreign_source_ref(route_plan_http: object) -> None:
    client, _desk = route_plan_http
    response = client.post(
        "/api/v1/route-plan-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_route_plan_marks_lists_rows(route_plan_http: object) -> None:
    client, desk = route_plan_http
    client.post(
        "/api/v1/route-plan-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/route-plan-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
