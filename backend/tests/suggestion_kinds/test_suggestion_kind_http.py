from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.suggestion_kind import parse_suggestion_kind_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.suggestion_kind import SuggestionKind
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "margin", "score")


def test_migration_346_creates_suggestion_kind_and_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/346_suggestion_kind.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "346_suggestion_kind"' in source
    assert 'down_revision: str | None = "345_benefit_ledger"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "suggestion_kind_tenant_isolation" in source
    for banned in ("float(", "httpx", "crps", "mae"):
        assert banned not in source.lower()
    assert "IN (" not in source
    assert "suggestion_ledger" not in source


def test_importlinter_lists_suggestion_kind_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.suggestion_kinds" in forbidden
    assert "app.models.suggestion_kind" in forbidden


def test_api_types_include_suggestion_kind() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "SuggestionKindResponse" in source
    assert "SuggestionKindCreate" in source


def test_fga_source_declares_suggestion_kind_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_suggestion_kinds: member" in source


def test_fga_model_grants_suggestion_kind_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_suggestion_kinds"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitSuggestionKindAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemorySuggestionKindDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[SuggestionKind] = []

    async def list_rows(self) -> list[SuggestionKind]:
        return list(self.rows)

    async def persist_kind(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        kind_code: object,
        source_ref: object,
    ) -> SuggestionKind:
        draft = parse_suggestion_kind_row(kind_code, source_ref)
        row = SuggestionKind(
            id=uuid4(),
            organization_id=organization_id,
            kind_code=draft.kind_code,
            source_ref=draft.source_ref,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def suggestion_kind_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemorySuggestionKindDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.suggestion_kinds.SuggestionKindService",
        lambda _s: desk,
    )
    set_authz_checker(PermitSuggestionKindAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "kind_code": "tender_twin",
        "source_ref": "fixture://suggestion-kind/a",
    }
    body.update(extra)
    return body


def test_post_persists_open_kind(suggestion_kind_http: object) -> None:
    client, desk = suggestion_kind_http
    response = client.post(
        "/api/v1/suggestion-kinds",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["kind_code"] == "tender_twin"
    assert response.headers.get("X-Omni-Catalog") == "suggestion-kind"
    assert len(desk.rows) == 1


def test_post_rejects_amount_margin_score(suggestion_kind_http: object) -> None:
    client, _desk = suggestion_kind_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/suggestion-kinds",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(suggestion_kind_http: object) -> None:
    client, _desk = suggestion_kind_http
    response = client.post(
        "/api/v1/suggestion-kinds",
        headers=bearer_auth_headers(),
        json=_payload(kind_code="1x"),
    )
    assert response.status_code == 400
    assert "kod" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(suggestion_kind_http: object) -> None:
    client, _desk = suggestion_kind_http
    response = client.post(
        "/api/v1/suggestion-kinds",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(suggestion_kind_http: object) -> None:
    client, desk = suggestion_kind_http
    client.post(
        "/api/v1/suggestion-kinds",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/suggestion-kinds",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
