from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.groupage_dispatcher_mark import parse_groupage_dispatcher_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.groupage_dispatcher_mark import GroupageDispatcherMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount",)


def test_migration_368_creates_groupage_dispatcher_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/368_groupage_disp_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "368_groupage_disp_mark"' in source
    assert 'down_revision: str | None = "367_campaign_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "groupage_dispatcher_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source


def test_importlinter_lists_groupage_dispatcher_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.groupage_dispatcher_marks" in forbidden
    assert "app.models.groupage_dispatcher_mark" in forbidden


def test_fga_source_declares_groupage_dispatcher_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_groupage_dispatcher_marks: member" in source


def test_authorization_model_grants_groupage_dispatcher_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_groupage_dispatcher_marks"]
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
        self.rows: list[GroupageDispatcherMark] = []

    async def list_marks(self) -> list[GroupageDispatcherMark]:
        return list(self.rows)

    async def persist_groupage_dispatcher_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        dispatcher_kind: object,
        source_ref: object,
    ) -> GroupageDispatcherMark:
        code, kind, origin = parse_groupage_dispatcher_mark_row(
            mark_code,
            dispatcher_kind,
            source_ref,
        )
        row = GroupageDispatcherMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            dispatcher_kind=kind,
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
        "app.api.groupage_dispatcher_marks.GroupageDispatcherMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitMarkAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "gdp_line_01",
        "dispatcher_kind": "line",
        "source_ref": "fixture://groupage-dispatcher-mark/a",
    }
    body.update(extra)
    return body


def test_post_groupage_dispatcher_mark_persists(mark_http: object) -> None:
    client, desk = mark_http
    response = client.post(
        "/api/v1/groupage-dispatcher-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["dispatcher_kind"] == "line"
    assert len(desk.rows) == 1


def test_post_groupage_dispatcher_mark_rejects_amount(mark_http: object) -> None:
    client, _desk = mark_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/groupage-dispatcher-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_groupage_dispatcher_mark_rejects_bad_kind(mark_http: object) -> None:
    client, _desk = mark_http
    response = client.post(
        "/api/v1/groupage-dispatcher-marks",
        headers=bearer_auth_headers(),
        json=_payload(dispatcher_kind="engine"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_groupage_dispatcher_mark_rejects_foreign_source_ref(mark_http: object) -> None:
    client, _desk = mark_http
    response = client.post(
        "/api/v1/groupage-dispatcher-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_groupage_dispatcher_marks_lists_rows(mark_http: object) -> None:
    client, desk = mark_http
    client.post(
        "/api/v1/groupage-dispatcher-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/groupage-dispatcher-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
