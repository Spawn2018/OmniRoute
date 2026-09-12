from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.rag_sop_mark import parse_rag_sop_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.rag_sop_mark import RagSopMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]

_FORBIDDEN = ("amount", "vector")


def test_migration_307_creates_rag_sop_and_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/307_rag_sop_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "307_rag_sop_mark"' in source
    assert 'down_revision: str | None = "306_role_view_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "rag_sop_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source


def test_importlinter_lists_rag_sop_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.rag_sop_marks" in forbidden
    assert "app.models.rag_sop_mark" in forbidden


def test_api_types_include_rag_sop_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "RagSopMarkResponse" in source
    assert "RagSopMarkCreate" in source


def test_fga_source_declares_rag_sop_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_rag_sop_marks: member" in source


def test_fga_model_grants_rag_sop_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_rag_sop_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitRagSopAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryRagSopDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[RagSopMark] = []

    async def list_marks(self) -> list[RagSopMark]:
        return list(self.rows)

    async def persist_rag_sop_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        scope_kind: object,
        source_ref: object,
    ) -> RagSopMark:
        code, kind, origin = parse_rag_sop_mark_row(
            mark_code,
            scope_kind,
            source_ref,
        )
        row = RagSopMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            scope_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def rag_sop_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryRagSopDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.rag_sop_marks.RagSopMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitRagSopAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "rsm_sop_01",
        "scope_kind": "sop",
        "source_ref": "fixture://rag-sop-mark/a",
    }
    body.update(extra)
    return body


def test_post_persists(rag_sop_http: object) -> None:
    client, desk = rag_sop_http
    response = client.post(
        "/api/v1/rag-sop-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["scope_kind"] == "sop"
    assert len(desk.rows) == 1


def test_post_rejects_amount_vector(rag_sop_http: object) -> None:
    client, _desk = rag_sop_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/rag-sop-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(rag_sop_http: object) -> None:
    client, _desk = rag_sop_http
    response = client.post(
        "/api/v1/rag-sop-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_rejects_bad_kind(rag_sop_http: object) -> None:
    client, _desk = rag_sop_http
    response = client.post(
        "/api/v1/rag-sop-marks",
        headers=bearer_auth_headers(),
        json=_payload(scope_kind="pgvector_index"),
    )
    assert response.status_code == 400
    assert "zakres" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(rag_sop_http: object) -> None:
    client, _desk = rag_sop_http
    response = client.post(
        "/api/v1/rag-sop-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(rag_sop_http: object) -> None:
    client, desk = rag_sop_http
    client.post(
        "/api/v1/rag-sop-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/rag-sop-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
