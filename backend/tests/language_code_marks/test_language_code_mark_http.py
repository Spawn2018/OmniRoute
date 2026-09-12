from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.language_code_mark import parse_language_code_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.language_code_mark import LanguageCodeMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]

_FORBIDDEN = ("amount", "margin", "score")


def test_migration_335_creates_language_code_and_rls() -> None:
    source = (
        _ROOT / "backend/alembic/versions/335_language_code_mark.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "335_language_code_mark"' in source
    assert 'down_revision: str | None = "334_payment_terms_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "language_code_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source.lower()
    assert 'sa.Column("amount"' not in source
    assert 'sa.Column("preferred_language"' not in source


def test_importlinter_lists_language_code_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.language_code_marks" in forbidden
    assert "app.models.language_code_mark" in forbidden


def test_api_types_include_language_code_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "LanguageCodeMarkResponse" in source
    assert "LanguageCodeMarkCreate" in source


def test_fga_source_declares_language_code_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_language_code_marks: member" in source


def test_fga_model_grants_language_code_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_language_code_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitLanguageCodeAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryLanguageCodeDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[LanguageCodeMark] = []

    async def list_marks(self) -> list[LanguageCodeMark]:
        return list(self.rows)

    async def persist_language_code_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        locale_kind: object,
        source_ref: object,
    ) -> LanguageCodeMark:
        code, kind, origin = parse_language_code_mark_row(
            mark_code,
            locale_kind,
            source_ref,
        )
        row = LanguageCodeMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            locale_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def language_code_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryLanguageCodeDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.language_code_marks.LanguageCodeMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitLanguageCodeAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "lcm_pl_docs",
        "locale_kind": "pl",
        "source_ref": "fixture://language-code-mark/a",
    }
    body.update(extra)
    return body


def test_post_persists(language_code_http: object) -> None:
    client, desk = language_code_http
    response = client.post(
        "/api/v1/language-code-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["locale_kind"] == "pl"
    assert response.headers.get("X-Omni-Catalog") == "language-code-mark"
    assert len(desk.rows) == 1


def test_post_rejects_amount_margin_score(language_code_http: object) -> None:
    client, _desk = language_code_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/language-code-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(language_code_http: object) -> None:
    client, _desk = language_code_http
    response = client.post(
        "/api/v1/language-code-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_rejects_bad_kind(language_code_http: object) -> None:
    client, _desk = language_code_http
    response = client.post(
        "/api/v1/language-code-marks",
        headers=bearer_auth_headers(),
        json=_payload(locale_kind="fr"),
    )
    assert response.status_code == 400
    assert "locale" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(language_code_http: object) -> None:
    client, _desk = language_code_http
    response = client.post(
        "/api/v1/language-code-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(language_code_http: object) -> None:
    client, desk = language_code_http
    client.post(
        "/api/v1/language-code-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/language-code-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
