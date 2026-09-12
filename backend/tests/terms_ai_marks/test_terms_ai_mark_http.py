from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.terms_ai_mark import parse_terms_ai_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.terms_ai_mark import TermsAiMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]

_FORBIDDEN = ("amount", "bytes")

def test_migration_304_creates_terms_ai_and_rls() -> None:

    source = (_ROOT / "backend/alembic/versions/304_terms_ai_mark.py").read_text(

        encoding="utf-8",

    )

    assert 'revision: str = "304_terms_ai_mark"' in source

    assert 'down_revision: str | None = "303_funnel_mark"' in source

    assert "FORCE ROW LEVEL SECURITY" in source

    assert "terms_ai_mark_tenant_isolation" in source

    for banned in ("amount", "margin", "float(", "httpx", "currency", "bytes"):

        assert banned not in source

def test_importlinter_lists_terms_ai_on_deny() -> None:

    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")

    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]

    assert "app.services.terms_ai_marks" in forbidden

    assert "app.models.terms_ai_mark" in forbidden

def test_api_types_include_terms_ai_mark() -> None:

    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")

    assert "TermsAiMarkResponse" in source

    assert "TermsAiMarkCreate" in source

def test_fga_source_declares_ab_sus_relation() -> None:

    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")

    assert "can_manage_terms_ai_marks: member" in source

def test_fga_model_grants_ab_sus_to_member() -> None:

    organization = next(

        definition

        for definition in authorization_model_request().type_definitions

        if definition.type == "organization"

    )

    relation = organization.relations["can_manage_terms_ai_marks"]

    assert relation.computed_userset is not None

    assert relation.computed_userset.relation == "member"

class PermitTermsAiAuthz:

    async def check(

        self,

        *,

        user_id: UUID,

        relation: str,

        object_type: str,

        object_id: UUID,

    ) -> bool:

        return True

class InMemoryFleetCostDesk:

    def __init__(self, session: object) -> None:

        self.rows: list[TermsAiMark] = []

    async def list_marks(self) -> list[TermsAiMark]:

        return list(self.rows)

    async def persist_terms_ai_mark(

        self,

        *,

        organization_id: UUID,

        user_id: UUID,

        mark_code: object,

        terms_kind: object,

        source_ref: object,

    ) -> TermsAiMark:

        code, kind, origin = parse_terms_ai_mark_row(

            mark_code,

            terms_kind,

            source_ref,

        )

        row = TermsAiMark(

            id=uuid4(),

            organization_id=organization_id,

            mark_code=code,

            terms_kind=kind,

            source_ref=origin,

            created_by=user_id,

        )

        self.rows.append(row)

        return row

@pytest.fixture

def terms_ai_http(monkeypatch: pytest.MonkeyPatch) -> object:

    desk = InMemoryFleetCostDesk(object())

    async def _session() -> object:

        handle = AsyncMock()

        handle.commit = AsyncMock()

        return handle

    monkeypatch.setattr(

        "app.api.terms_ai_marks.TermsAiMarkService",

        lambda _s: desk,

    )

    set_authz_checker(PermitTermsAiAuthz())

    app.dependency_overrides[require_tenant_session] = _session

    yield TestClient(app), desk

    app.dependency_overrides.clear()

    set_authz_checker(None)

def _payload(**extra: object) -> dict[str, object]:

    body: dict[str, object] = {

        "mark_code": "tai_draft_01",

        "terms_kind": "draft",

        "source_ref": "fixture://terms-ai-mark/a",

    }

    body.update(extra)

    return body

def test_post_persists(terms_ai_http: object) -> None:

    client, desk = terms_ai_http

    response = client.post(

        "/api/v1/terms-ai-marks",

        headers=bearer_auth_headers(),

        json=_payload(),

    )

    assert response.status_code == 201

    assert response.json()["terms_kind"] == "draft"

    assert len(desk.rows) == 1

def test_post_rejects_amount_bytes(terms_ai_http: object) -> None:

    client, _desk = terms_ai_http

    for field in _FORBIDDEN:

        response = client.post(

            "/api/v1/terms-ai-marks",

            headers=bearer_auth_headers(),

            json=_payload(**{field: "x"}),

        )

        assert response.status_code == 422, field

def test_post_rejects_bad_code(terms_ai_http: object) -> None:

    client, _desk = terms_ai_http

    response = client.post(

        "/api/v1/terms-ai-marks",

        headers=bearer_auth_headers(),

        json=_payload(mark_code="BAD"),

    )

    assert response.status_code == 400

    assert "oznaczenie" in response.json()["detail"]

def test_post_rejects_bad_kind(terms_ai_http: object) -> None:

    client, _desk = terms_ai_http

    response = client.post(

        "/api/v1/terms-ai-marks",

        headers=bearer_auth_headers(),

        json=_payload(terms_kind="live_terms"),

    )

    assert response.status_code == 400

    assert "rodzaj" in response.json()["detail"]

def test_post_rejects_foreign_source_ref(terms_ai_http: object) -> None:

    client, _desk = terms_ai_http

    response = client.post(

        "/api/v1/terms-ai-marks",

        headers=bearer_auth_headers(),

        json=_payload(source_ref="http://evil.example/x"),

    )

    assert response.status_code == 400

    assert "wskazanie" in response.json()["detail"]

def test_get_lists_rows(terms_ai_http: object) -> None:

    client, desk = terms_ai_http

    client.post(

        "/api/v1/terms-ai-marks",

        headers=bearer_auth_headers(),

        json=_payload(),

    )

    response = client.get(

        "/api/v1/terms-ai-marks",

        headers=bearer_auth_headers(),

    )

    assert response.status_code == 200

    assert len(response.json()) == 1

    assert len(desk.rows) == 1

