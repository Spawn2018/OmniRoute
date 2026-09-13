from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.tacho_plan_mark import parse_tacho_plan_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.tacho_plan_mark import TachoPlanMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount",)


def test_migration_370_creates_tacho_plan_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/370_tacho_plan_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "370_tacho_plan_mark"' in source
    assert 'down_revision: str | None = "369_load_order_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "tacho_plan_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source


def test_importlinter_lists_tacho_plan_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.tacho_plan_marks" in forbidden
    assert "app.models.tacho_plan_mark" in forbidden


def test_fga_source_declares_tacho_plan_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_tacho_plan_marks: member" in source


def test_authorization_model_grants_tacho_plan_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_tacho_plan_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitMarkAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryMarkDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[TachoPlanMark] = []

    async def list_marks(self) -> list[TachoPlanMark]:
        return list(self.rows)

    async def persist_tacho_plan_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        constraint_kind: object,
        source_ref: object,
    ) -> TachoPlanMark:
        code, kind, origin = parse_tacho_plan_mark_row(
            mark_code,
            constraint_kind,
            source_ref,
        )
        row = TachoPlanMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            constraint_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def mark_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryMarkDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.tacho_plan_marks.TachoPlanMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitMarkAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "tpm_plan_01",
        "constraint_kind": "plan",
        "source_ref": "fixture://tacho-plan-mark/a",
    }
    body.update(extra)
    return body


def test_post_tacho_plan_mark_persists(mark_http: object) -> None:
    client, desk = mark_http
    response = client.post(
        "/api/v1/tacho-plan-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["constraint_kind"] == "plan"
    assert len(desk.rows) == 1


def test_post_tacho_plan_mark_rejects_amount(mark_http: object) -> None:
    client, _desk = mark_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/tacho-plan-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_tacho_plan_mark_rejects_bad_kind(mark_http: object) -> None:
    client, _desk = mark_http
    response = client.post(
        "/api/v1/tacho-plan-marks",
        headers=bearer_auth_headers(),
        json=_payload(constraint_kind="hours"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_tacho_plan_mark_rejects_foreign_source_ref(mark_http: object) -> None:
    client, _desk = mark_http
    response = client.post(
        "/api/v1/tacho-plan-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_tacho_plan_marks_lists_rows(mark_http: object) -> None:
    client, desk = mark_http
    client.post(
        "/api/v1/tacho-plan-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/tacho-plan-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
