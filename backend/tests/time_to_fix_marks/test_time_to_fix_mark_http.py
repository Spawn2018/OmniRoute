from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.time_to_fix_mark import parse_time_to_fix_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.time_to_fix_mark import TimeToFixMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "bytes")


def test_migration_258_creates_ttf_and_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/258_time_to_fix_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "258_time_to_fix_mark"' in source
    assert 'down_revision: str | None = "257_cutoff_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "time_to_fix_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "bytes"):
        assert banned not in source


def test_importlinter_lists_cutoff_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.time_to_fix_marks" in forbidden
    assert "app.models.time_to_fix_mark" in forbidden


def test_api_types_include_time_to_fix_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "TimeToFixMarkResponse" in source
    assert "TimeToFixMarkCreate" in source


def test_fga_source_declares_cutoff_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_time_to_fix_marks: member" in source


def test_fga_model_grants_cutoff_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_time_to_fix_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitTimeToFixAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryTimeToFixDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[TimeToFixMark] = []

    async def list_marks(self) -> list[TimeToFixMark]:
        return list(self.rows)

    async def persist_time_to_fix_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        fix_kind: object,
        source_ref: object,
    ) -> TimeToFixMark:
        code, kind, origin = parse_time_to_fix_mark_row(
            mark_code,
            fix_kind,
            source_ref,
        )
        row = TimeToFixMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            fix_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def time_to_fix_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryTimeToFixDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.time_to_fix_marks.TimeToFixMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitTimeToFixAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "open_01",
        "fix_kind": "open",
        "source_ref": "fixture://time-to-fix-mark/a",
    }
    body.update(extra)
    return body


def test_post_persists(time_to_fix_http: object) -> None:
    client, desk = time_to_fix_http
    response = client.post(
        "/api/v1/time-to-fix-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["fix_kind"] == "open"
    assert len(desk.rows) == 1


def test_post_rejects_amount_bytes(time_to_fix_http: object) -> None:
    client, _desk = time_to_fix_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/time-to-fix-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(time_to_fix_http: object) -> None:
    client, _desk = time_to_fix_http
    response = client.post(
        "/api/v1/time-to-fix-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_rejects_bad_kind(time_to_fix_http: object) -> None:
    client, _desk = time_to_fix_http
    response = client.post(
        "/api/v1/time-to-fix-marks",
        headers=bearer_auth_headers(),
        json=_payload(fix_kind="engine"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(time_to_fix_http: object) -> None:
    client, _desk = time_to_fix_http
    response = client.post(
        "/api/v1/time-to-fix-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(time_to_fix_http: object) -> None:
    client, desk = time_to_fix_http
    client.post(
        "/api/v1/time-to-fix-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/time-to-fix-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
