from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.outcome_kind import parse_outcome_kind_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.outcome_kind import OutcomeKind
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "margin", "score")


def test_migration_351_creates_outcome_kind_and_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/351_outcome_kind.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "351_outcome_kind"' in source
    assert 'down_revision: str | None = "350_twin_mark_kind_fk"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "outcome_kind_tenant_isolation" in source
    for banned in ("float(", "httpx", "crps", "mae"):
        assert banned not in source.lower()
    assert "IN (" not in source
    assert "outcome_ledger" not in source


def test_importlinter_lists_outcome_kind_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.outcome_kinds" in forbidden
    assert "app.models.outcome_kind" in forbidden


def test_api_types_include_outcome_kind() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "OutcomeKindResponse" in source
    assert "OutcomeKindCreate" in source


def test_fga_source_declares_outcome_kind_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_outcome_kinds: member" in source


def test_fga_model_grants_outcome_kind_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_outcome_kinds"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitOutcomeKindAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryOutcomeKindDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[OutcomeKind] = []

    async def list_rows(self) -> list[OutcomeKind]:
        return list(self.rows)

    async def persist_kind(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        kind_code: object,
        source_ref: object,
    ) -> OutcomeKind:
        draft = parse_outcome_kind_row(kind_code, source_ref)
        row = OutcomeKind(
            id=uuid4(),
            organization_id=organization_id,
            kind_code=draft.kind_code,
            source_ref=draft.source_ref,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def outcome_kind_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryOutcomeKindDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.outcome_kinds.OutcomeKindService",
        lambda _s: desk,
    )
    set_authz_checker(PermitOutcomeKindAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "kind_code": "tender",
        "source_ref": "fixture://outcome-kind/a",
    }
    body.update(extra)
    return body


def test_post_persists_open_kind(outcome_kind_http: object) -> None:
    client, desk = outcome_kind_http
    response = client.post(
        "/api/v1/outcome-kinds",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["kind_code"] == "tender"
    assert response.headers.get("X-Omni-Catalog") == "outcome-kind"
    assert len(desk.rows) == 1


def test_post_rejects_amount_margin_score(outcome_kind_http: object) -> None:
    client, _desk = outcome_kind_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/outcome-kinds",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(outcome_kind_http: object) -> None:
    client, _desk = outcome_kind_http
    response = client.post(
        "/api/v1/outcome-kinds",
        headers=bearer_auth_headers(),
        json=_payload(kind_code="1x"),
    )
    assert response.status_code == 400
    assert "kod" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(outcome_kind_http: object) -> None:
    client, _desk = outcome_kind_http
    response = client.post(
        "/api/v1/outcome-kinds",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(outcome_kind_http: object) -> None:
    client, desk = outcome_kind_http
    client.post(
        "/api/v1/outcome-kinds",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/outcome-kinds",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
