from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.silk_corridor_mark import parse_silk_corridor_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.silk_corridor_mark import SilkCorridorMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount",)


def test_migration_375_creates_silk_corridor_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/375_silk_corridor_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "375_silk_corridor_mark"' in source
    assert 'down_revision: str | None = "374_nac_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "silk_corridor_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "origin_unlocode"):
        assert banned not in source


def test_importlister_lists_silk_corridor_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.silk_corridor_marks" in forbidden
    assert "app.models.silk_corridor_mark" in forbidden


def test_fga_source_declares_silk_corridor_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_silk_corridor_marks: member" in source


def test_authorization_model_grants_silk_corridor_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_silk_corridor_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class SilkCorridorMarkAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemorySilkCorridorDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[SilkCorridorMark] = []

    async def list_marks(self) -> list[SilkCorridorMark]:
        return list(self.rows)

    async def persist_silk_corridor_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        corridor_kind: object,
        source_ref: object,
    ) -> SilkCorridorMark:
        code, kind, origin = parse_silk_corridor_mark_row(
            mark_code,
            corridor_kind,
            source_ref,
        )
        row = SilkCorridorMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            corridor_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def silk_corridor_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemorySilkCorridorDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.silk_corridor_marks.SilkCorridorMarkService",
        lambda _s: desk,
    )
    set_authz_checker(SilkCorridorMarkAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "scm_silk_01",
        "corridor_kind": "silk",
        "source_ref": "fixture://silk-corridor-mark/a",
    }
    body.update(extra)
    return body


def test_post_silk_corridor_mark_persists(silk_corridor_http: object) -> None:
    client, desk = silk_corridor_http
    response = client.post(
        "/api/v1/silk-corridor-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["corridor_kind"] == "silk"
    assert len(desk.rows) == 1


def test_post_silk_corridor_mark_rejects_amount(silk_corridor_http: object) -> None:
    client, _desk = silk_corridor_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/silk-corridor-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_silk_corridor_mark_rejects_bad_kind(silk_corridor_http: object) -> None:
    client, _desk = silk_corridor_http
    response = client.post(
        "/api/v1/silk-corridor-marks",
        headers=bearer_auth_headers(),
        json=_payload(corridor_kind="cr_express_live"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_silk_corridor_mark_rejects_foreign_source_ref(silk_corridor_http: object) -> None:
    client, _desk = silk_corridor_http
    response = client.post(
        "/api/v1/silk-corridor-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_silk_corridor_marks_lists_rows(silk_corridor_http: object) -> None:
    client, desk = silk_corridor_http
    client.post(
        "/api/v1/silk-corridor-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/silk-corridor-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
