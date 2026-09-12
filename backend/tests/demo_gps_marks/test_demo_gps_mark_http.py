from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.demo_gps_mark import parse_demo_gps_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.demo_gps_mark import DemoGpsMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]

_FORBIDDEN = ("lat", "lng", "amount", "score")


def test_migration_312_creates_demo_gps_and_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/312_demo_gps_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "312_demo_gps_mark"' in source
    assert 'down_revision: str | None = "311_job_metric_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "demo_gps_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source
    assert 'sa.Column("lat"' not in source
    assert 'sa.Column("lng"' not in source


def test_importlinter_lists_demo_gps_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.demo_gps_marks" in forbidden
    assert "app.models.demo_gps_mark" in forbidden


def test_api_types_include_demo_gps_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "DemoGpsMarkResponse" in source
    assert "DemoGpsMarkCreate" in source


def test_fga_source_declares_demo_gps_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_demo_gps_marks: member" in source


def test_fga_model_grants_demo_gps_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_demo_gps_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitDemoGpsAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryDemoGpsDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[DemoGpsMark] = []

    async def list_marks(self) -> list[DemoGpsMark]:
        return list(self.rows)

    async def persist_demo_gps_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        demo_kind: object,
        source_ref: object,
    ) -> DemoGpsMark:
        code, kind, origin = parse_demo_gps_mark_row(
            mark_code,
            demo_kind,
            source_ref,
        )
        row = DemoGpsMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            demo_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def demo_gps_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryDemoGpsDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.demo_gps_marks.DemoGpsMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitDemoGpsAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "dgm_seven_day_01",
        "demo_kind": "seven_day",
        "source_ref": "fixture://demo-gps-mark/a",
    }
    body.update(extra)
    return body


def test_post_persists(demo_gps_http: object) -> None:
    client, desk = demo_gps_http
    response = client.post(
        "/api/v1/demo-gps-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["demo_kind"] == "seven_day"
    assert response.headers.get("X-Omni-Catalog") == "demo-gps-mark"
    assert len(desk.rows) == 1


def test_post_rejects_lat_lng_amount_score(demo_gps_http: object) -> None:
    client, _desk = demo_gps_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/demo-gps-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(demo_gps_http: object) -> None:
    client, _desk = demo_gps_http
    response = client.post(
        "/api/v1/demo-gps-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_rejects_bad_kind(demo_gps_http: object) -> None:
    client, _desk = demo_gps_http
    response = client.post(
        "/api/v1/demo-gps-marks",
        headers=bearer_auth_headers(),
        json=_payload(demo_kind="live_track"),
    )
    assert response.status_code == 400
    assert "rodzaj demo" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(demo_gps_http: object) -> None:
    client, _desk = demo_gps_http
    response = client.post(
        "/api/v1/demo-gps-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(demo_gps_http: object) -> None:
    client, desk = demo_gps_http
    client.post(
        "/api/v1/demo-gps-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/demo-gps-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
