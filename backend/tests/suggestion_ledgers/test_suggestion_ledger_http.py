from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.suggestion_ledger import parse_suggestion_ledger_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.suggestion_ledger import SuggestionLedger
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_ENTITY = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
_FORBIDDEN = ("amount", "margin", "score")


def test_migration_342_creates_suggestion_ledger_and_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/342_suggestion_ledger.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "342_suggestion_ledger"' in source
    assert 'down_revision: str | None = "341_quote_validity_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "suggestion_ledger_tenant_isolation" in source
    for banned in ("float(", "httpx"):
        assert banned not in source.lower()
    assert 'sa.Column("amount"' not in source
    assert 'sa.Column("margin"' not in source
    assert "ForeignKey" not in source or "organization.id" in source
    assert "shipment_id" not in source
    assert "openai" not in source.lower()


def test_migration_349_replaces_kind_list_with_fk() -> None:
    source = (_ROOT / "backend/alembic/versions/349_suggestion_ledger_kind_fk.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "349_suggestion_ledger_kind_fk"' in source
    assert 'down_revision: str | None = "348_autonomy_level"' in source
    assert "fk_suggestion_ledger_kind" in source
    assert "IN (" not in source
    assert "ck_suggestion_ledger_kind" in source


def test_importlinter_lists_suggestion_ledger_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.suggestion_ledgers" in forbidden
    assert "app.models.suggestion_ledger" in forbidden


def test_api_types_include_suggestion_ledger() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "SuggestionLedgerResponse" in source
    assert "SuggestionLedgerCreate" in source


def test_fga_source_declares_suggestion_ledger_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_suggestion_ledgers: member" in source


def test_fga_model_grants_suggestion_ledger_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_suggestion_ledgers"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitSuggestionLedgerAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemorySuggestionDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[SuggestionLedger] = []

    async def list_rows(self) -> list[SuggestionLedger]:
        return list(self.rows)

    async def persist_ledger(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        target_bc: object,
        entity_id: object,
        suggestion_kind: object,
        interval_low: object,
        interval_high: object,
        model_version: object,
        prompt_version: object,
        reaction: object,
        changed_to: object,
        source_ref: object,
    ) -> SuggestionLedger:
        draft = parse_suggestion_ledger_row(
            target_bc,
            entity_id,
            suggestion_kind,
            interval_low,
            interval_high,
            model_version,
            prompt_version,
            reaction,
            changed_to,
            source_ref,
        )
        row = SuggestionLedger(
            id=uuid4(),
            organization_id=organization_id,
            target_bc=draft.target_bc,
            entity_id=draft.entity_id,
            suggestion_kind=draft.suggestion_kind,
            interval_low=draft.interval_low,
            interval_high=draft.interval_high,
            model_version=draft.model_version,
            prompt_version=draft.prompt_version,
            reaction=draft.reaction,
            changed_to=draft.changed_to,
            source_ref=draft.source_ref,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def suggestion_ledger_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemorySuggestionDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.suggestion_ledgers.SuggestionLedgerService",
        lambda _s: desk,
    )
    set_authz_checker(PermitSuggestionLedgerAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "target_bc": "shipment",
        "entity_id": _ENTITY,
        "suggestion_kind": "eta",
        "interval_low": "30",
        "interval_high": "90",
        "model_version": "hist_eta",
        "prompt_version": "prompt_v1",
        "reaction": "accept",
        "changed_to": "none",
        "source_ref": "fixture://suggestion-ledger/a",
    }
    body.update(extra)
    return body


def test_post_persists(suggestion_ledger_http: object) -> None:
    client, desk = suggestion_ledger_http
    response = client.post(
        "/api/v1/suggestion-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["suggestion_kind"] == "eta"
    assert response.json()["reaction"] == "accept"
    assert response.json()["interval_low"] == "30.0000"
    assert response.headers.get("X-Omni-Catalog") == "suggestion-ledger"
    assert len(desk.rows) == 1


def test_post_rejects_amount_margin_score(suggestion_ledger_http: object) -> None:
    client, _desk = suggestion_ledger_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/suggestion-ledgers",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_float_interval(suggestion_ledger_http: object) -> None:
    client, _desk = suggestion_ledger_http
    response = client.post(
        "/api/v1/suggestion-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(interval_low=1.5),
    )
    assert response.status_code == 422


def test_post_accepts_open_kind(suggestion_ledger_http: object) -> None:
    client, desk = suggestion_ledger_http
    response = client.post(
        "/api/v1/suggestion-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(suggestion_kind="tender_twin"),
    )
    assert response.status_code == 201
    assert response.json()["suggestion_kind"] == "tender_twin"
    assert len(desk.rows) == 1


def test_post_rejects_bad_kind(suggestion_ledger_http: object) -> None:
    client, _desk = suggestion_ledger_http
    response = client.post(
        "/api/v1/suggestion-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(suggestion_kind="1x"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_rejects_inverted_interval(suggestion_ledger_http: object) -> None:
    client, _desk = suggestion_ledger_http
    response = client.post(
        "/api/v1/suggestion-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(interval_low="90", interval_high="30"),
    )
    assert response.status_code == 400
    assert "przedział" in response.json()["detail"]


def test_post_rejects_modify_none(suggestion_ledger_http: object) -> None:
    client, _desk = suggestion_ledger_http
    response = client.post(
        "/api/v1/suggestion-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(reaction="modify", changed_to="none"),
    )
    assert response.status_code == 400
    assert "zmiana" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(suggestion_ledger_http: object) -> None:
    client, _desk = suggestion_ledger_http
    response = client.post(
        "/api/v1/suggestion-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(suggestion_ledger_http: object) -> None:
    client, desk = suggestion_ledger_http
    client.post(
        "/api/v1/suggestion-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/suggestion-ledgers",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
