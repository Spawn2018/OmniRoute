from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.copy_ban_mark import parse_copy_ban_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.copy_ban_mark import CopyBanMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]

_FORBIDDEN = ("amount", "claim")


def test_migration_308_creates_copy_ban_and_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/308_copy_ban_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "308_copy_ban_mark"' in source
    assert 'down_revision: str | None = "307_rag_sop_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "copy_ban_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source


def test_importlinter_lists_copy_ban_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.copy_ban_marks" in forbidden
    assert "app.models.copy_ban_mark" in forbidden


def test_api_types_include_copy_ban_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "CopyBanMarkResponse" in source
    assert "CopyBanMarkCreate" in source


def test_fga_source_declares_copy_ban_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_copy_ban_marks: member" in source


def test_fga_model_grants_copy_ban_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_copy_ban_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitCopyBanAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryCopyBanDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[CopyBanMark] = []

    async def list_marks(self) -> list[CopyBanMark]:
        return list(self.rows)

    async def persist_copy_ban_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        ban_kind: object,
        source_ref: object,
    ) -> CopyBanMark:
        code, kind, origin = parse_copy_ban_mark_row(
            mark_code,
            ban_kind,
            source_ref,
        )
        row = CopyBanMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            ban_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def copy_ban_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryCopyBanDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.copy_ban_marks.CopyBanMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitCopyBanAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "cbm_eight_min_01",
        "ban_kind": "eight_min",
        "source_ref": "fixture://copy-ban-mark/a",
    }
    body.update(extra)
    return body


def test_post_persists(copy_ban_http: object) -> None:
    client, desk = copy_ban_http
    response = client.post(
        "/api/v1/copy-ban-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["ban_kind"] == "eight_min"
    assert len(desk.rows) == 1


def test_post_rejects_amount_claim(copy_ban_http: object) -> None:
    client, _desk = copy_ban_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/copy-ban-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(copy_ban_http: object) -> None:
    client, _desk = copy_ban_http
    response = client.post(
        "/api/v1/copy-ban-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_rejects_bad_kind(copy_ban_http: object) -> None:
    client, _desk = copy_ban_http
    response = client.post(
        "/api/v1/copy-ban-marks",
        headers=bearer_auth_headers(),
        json=_payload(ban_kind="bayer_live"),
    )
    assert response.status_code == 400
    assert "zakaz" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(copy_ban_http: object) -> None:
    client, _desk = copy_ban_http
    response = client.post(
        "/api/v1/copy-ban-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(copy_ban_http: object) -> None:
    client, desk = copy_ban_http
    client.post(
        "/api/v1/copy-ban-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/copy-ban-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
