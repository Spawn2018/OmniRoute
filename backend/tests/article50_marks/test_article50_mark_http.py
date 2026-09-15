from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.article50_mark import parse_article50_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.article50_mark import Article50Mark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount",)


def test_migration_383_creates_article50_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/411_article50_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "411_article50_mark"' in source
    assert 'down_revision: str | None = "410_impact_edge_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "article50_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "auto_accept"):
        assert banned not in source


def test_importlinter_lists_article50_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.article50_marks" in forbidden
    assert "app.models.article50_mark" in forbidden


def test_fga_source_declares_article50_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_article50_marks: member" in source


def test_authorization_model_grants_article50_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_article50_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class Article50MarkAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryLineImpactLayerDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[Article50Mark] = []

    async def list_marks(self) -> list[Article50Mark]:
        return list(self.rows)

    async def persist_article50_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        label_kind: object,
        source_ref: object,
    ) -> Article50Mark:
        code, kind, origin = parse_article50_mark_row(
            mark_code,
            label_kind,
            source_ref,
        )
        row = Article50Mark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            label_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def ops_room_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryLineImpactLayerDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.article50_marks.Article50MarkService",
        lambda _s: desk,
    )
    set_authz_checker(Article50MarkAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "a50_generated_01",
        "label_kind": "generated",
        "source_ref": "fixture://article50-mark/a",
    }
    body.update(extra)
    return body


def test_post_article50_mark_persists(ops_room_http: object) -> None:
    client, desk = ops_room_http
    response = client.post(
        "/api/v1/article50-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["label_kind"] == "generated"
    assert len(desk.rows) == 1


def test_post_article50_mark_rejects_amount(ops_room_http: object) -> None:
    client, _desk = ops_room_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/article50-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_article50_mark_rejects_bad_kind(ops_room_http: object) -> None:
    client, _desk = ops_room_http
    response = client.post(
        "/api/v1/article50-marks",
        headers=bearer_auth_headers(),
        json=_payload(label_kind="auto_accept"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_article50_mark_rejects_foreign_source_ref(ops_room_http: object) -> None:
    client, _desk = ops_room_http
    response = client.post(
        "/api/v1/article50-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_article50_marks_lists_rows(ops_room_http: object) -> None:
    client, desk = ops_room_http
    client.post(
        "/api/v1/article50-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/article50-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
