from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.chassis_mark import parse_chassis_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.chassis_mark import ChassisMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]

_FORBIDDEN = ("amount", "teu", "score")


def test_migration_318_creates_chassis_and_rls() -> None:
    source = (
        _ROOT / "backend/alembic/versions/318_chassis_mark.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "318_chassis_mark"' in source
    assert 'down_revision: str | None = "317_ocean_feeder_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "chassis_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source.lower()
    assert 'sa.Column("amount"' not in source
    assert 'sa.Column("teu"' not in source


def test_importlinter_lists_chassis_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.chassis_marks" in forbidden
    assert "app.models.chassis_mark" in forbidden


def test_api_types_include_chassis_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "ChassisMarkResponse" in source
    assert "ChassisMarkCreate" in source


def test_fga_source_declares_chassis_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_chassis_marks: member" in source


def test_fga_model_grants_chassis_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_chassis_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitChassisAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryChassisDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[ChassisMark] = []

    async def list_marks(self) -> list[ChassisMark]:
        return list(self.rows)

    async def persist_chassis_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        chassis_kind: object,
        source_ref: object,
    ) -> ChassisMark:
        code, kind, origin = parse_chassis_mark_row(
            mark_code,
            chassis_kind,
            source_ref,
        )
        row = ChassisMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            chassis_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def chassis_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryChassisDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.chassis_marks.ChassisMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitChassisAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "chm_chassis_01",
        "chassis_kind": "chassis",
        "source_ref": "fixture://chassis-mark/a",
    }
    body.update(extra)
    return body


def test_post_persists(chassis_http: object) -> None:
    client, desk = chassis_http
    response = client.post(
        "/api/v1/chassis-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["chassis_kind"] == "chassis"
    assert response.headers.get("X-Omni-Catalog") == "chassis-mark"
    assert len(desk.rows) == 1


def test_post_rejects_amount_teu_score(chassis_http: object) -> None:
    client, _desk = chassis_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/chassis-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(chassis_http: object) -> None:
    client, _desk = chassis_http
    response = client.post(
        "/api/v1/chassis-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_rejects_bad_kind(chassis_http: object) -> None:
    client, _desk = chassis_http
    response = client.post(
        "/api/v1/chassis-marks",
        headers=bearer_auth_headers(),
        json=_payload(chassis_kind="pool_live"),
    )
    assert response.status_code == 400
    assert "rodzaj chassis" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(chassis_http: object) -> None:
    client, _desk = chassis_http
    response = client.post(
        "/api/v1/chassis-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(chassis_http: object) -> None:
    client, desk = chassis_http
    client.post(
        "/api/v1/chassis-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/chassis-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
