from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.haulier_role_mark import parse_haulier_role_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.haulier_role_mark import HaulierRoleMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]

_FORBIDDEN = ("amount", "margin", "score")


def test_migration_336_creates_haulier_role_and_rls() -> None:
    source = (
        _ROOT / "backend/alembic/versions/336_haulier_role_mark.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "336_haulier_role_mark"' in source
    assert 'down_revision: str | None = "335_language_code_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "haulier_role_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source.lower()
    assert 'sa.Column("amount"' not in source
    assert 'sa.Column("party_id"' not in source


def test_importlinter_lists_haulier_role_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.haulier_role_marks" in forbidden
    assert "app.models.haulier_role_mark" in forbidden


def test_api_types_include_haulier_role_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "HaulierRoleMarkResponse" in source
    assert "HaulierRoleMarkCreate" in source


def test_fga_source_declares_haulier_role_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_haulier_role_marks: member" in source


def test_fga_model_grants_haulier_role_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_haulier_role_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitHaulierRoleAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryHaulierRoleDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[HaulierRoleMark] = []

    async def list_marks(self) -> list[HaulierRoleMark]:
        return list(self.rows)

    async def persist_haulier_role_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        role_kind: object,
        source_ref: object,
    ) -> HaulierRoleMark:
        code, kind, origin = parse_haulier_role_mark_row(
            mark_code,
            role_kind,
            source_ref,
        )
        row = HaulierRoleMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            role_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def haulier_role_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryHaulierRoleDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.haulier_role_marks.HaulierRoleMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitHaulierRoleAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "hrm_booked_main",
        "role_kind": "booked",
        "source_ref": "fixture://haulier-role-mark/a",
    }
    body.update(extra)
    return body


def test_post_persists(haulier_role_http: object) -> None:
    client, desk = haulier_role_http
    response = client.post(
        "/api/v1/haulier-role-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["role_kind"] == "booked"
    assert response.headers.get("X-Omni-Catalog") == "haulier-role-mark"
    assert len(desk.rows) == 1


def test_post_rejects_amount_margin_score(haulier_role_http: object) -> None:
    client, _desk = haulier_role_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/haulier-role-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(haulier_role_http: object) -> None:
    client, _desk = haulier_role_http
    response = client.post(
        "/api/v1/haulier-role-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_rejects_bad_kind(haulier_role_http: object) -> None:
    client, _desk = haulier_role_http
    response = client.post(
        "/api/v1/haulier-role-marks",
        headers=bearer_auth_headers(),
        json=_payload(role_kind="carrier"),
    )
    assert response.status_code == 400
    assert "roli" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(haulier_role_http: object) -> None:
    client, _desk = haulier_role_http
    response = client.post(
        "/api/v1/haulier-role-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(haulier_role_http: object) -> None:
    client, desk = haulier_role_http
    client.post(
        "/api/v1/haulier-role-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/haulier-role-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
