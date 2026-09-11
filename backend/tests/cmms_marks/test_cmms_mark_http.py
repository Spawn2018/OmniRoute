from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.cmms_mark import parse_cmms_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.cmms_mark import CmmsMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "penalty")


def test_migration_240_creates_cmms_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/240_cmms_mark.py").read_text(encoding="utf-8")
    assert 'revision: str = "240_cmms_mark"' in source
    assert 'down_revision: str | None = "239_load_plan_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "cmms_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "penalty"):
        assert banned not in source


def test_importlinter_lists_cmms_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.cmms_marks" in forbidden
    assert "app.models.cmms_mark" in forbidden


def test_generated_api_types_include_cmms_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "CmmsMarkResponse" in source
    assert "CmmsMarkCreate" in source


def test_fga_source_declares_cmms_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_cmms_marks: member" in source


def test_authorization_model_grants_cmms_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_cmms_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitCmmsAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryCmmsDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[CmmsMark] = []

    async def list_marks(self) -> list[CmmsMark]:
        return list(self.rows)

    async def persist_cmms_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        work_kind: object,
        source_ref: object,
    ) -> CmmsMark:
        code, kind, origin = parse_cmms_mark_row(
            mark_code,
            work_kind,
            source_ref,
        )
        row = CmmsMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            work_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def cmms_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryCmmsDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr("app.api.cmms_marks.CmmsMarkService", lambda _s: desk)
    set_authz_checker(PermitCmmsAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "cmms_wo_01",
        "work_kind": "work_order",
        "source_ref": "fixture://cmms-mark/a",
    }
    body.update(extra)
    return body


def test_post_cmms_mark_persists(cmms_http: object) -> None:
    client, desk = cmms_http
    response = client.post(
        "/api/v1/cmms-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["work_kind"] == "work_order"
    assert len(desk.rows) == 1


def test_post_cmms_mark_rejects_amount_penalty(cmms_http: object) -> None:
    client, _desk = cmms_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/cmms-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_cmms_mark_rejects_bad_kind(cmms_http: object) -> None:
    client, _desk = cmms_http
    response = client.post(
        "/api/v1/cmms-marks",
        headers=bearer_auth_headers(),
        json=_payload(work_kind="engine"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_cmms_mark_rejects_foreign_source_ref(cmms_http: object) -> None:
    client, _desk = cmms_http
    response = client.post(
        "/api/v1/cmms-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_cmms_marks_lists_rows(cmms_http: object) -> None:
    client, desk = cmms_http
    client.post(
        "/api/v1/cmms-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/cmms-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
