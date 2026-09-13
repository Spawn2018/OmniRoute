from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.outcome_ledger import parse_outcome_ledger_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.outcome_ledger import OutcomeLedger
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_ENTITY = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
_SUGGESTION = "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
_FORBIDDEN = ("amount", "margin", "score")


def test_migration_343_creates_outcome_ledger_and_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/343_outcome_ledger.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "343_outcome_ledger"' in source
    assert 'down_revision: str | None = "342_suggestion_ledger"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "outcome_ledger_tenant_isolation" in source
    for banned in ("float(", "httpx", "crps", "mae"):
        assert banned not in source.lower()
    assert 'sa.Column("amount"' not in source
    assert "suggestion_ledger.id" not in source


def test_migration_352_replaces_kind_list_with_fk() -> None:
    source = (_ROOT / "backend/alembic/versions/352_outcome_ledger_kind_fk.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "352_outcome_ledger_kind_fk"' in source
    assert 'down_revision: str | None = "351_outcome_kind"' in source
    assert "fk_outcome_ledger_kind" in source
    assert "IN (" not in source
    assert "ck_outcome_ledger_kind" in source


def test_service_maps_missing_dictionary_kind() -> None:
    source = (
        _ROOT / "backend/app/services/outcome_ledgers/outcome_ledger_service.py"
    ).read_text(encoding="utf-8")
    assert "fk_outcome_ledger_kind" in source


def test_importlinter_lists_outcome_ledger_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.outcome_ledgers" in forbidden
    assert "app.models.outcome_ledger" in forbidden


def test_api_types_include_outcome_ledger() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "OutcomeLedgerResponse" in source
    assert "OutcomeLedgerCreate" in source


def test_fga_source_declares_outcome_ledger_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_outcome_ledgers: member" in source


def test_fga_model_grants_outcome_ledger_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_outcome_ledgers"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitOutcomeLedgerAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryOutcomeDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[OutcomeLedger] = []

    async def list_rows(self) -> list[OutcomeLedger]:
        return list(self.rows)

    async def persist_ledger(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        target_bc: object,
        entity_id: object,
        suggestion_id: object,
        outcome_kind: object,
        actual_value: object,
        source_ref: object,
    ) -> OutcomeLedger:
        draft = parse_outcome_ledger_row(
            target_bc,
            entity_id,
            suggestion_id,
            outcome_kind,
            actual_value,
            source_ref,
        )
        row = OutcomeLedger(
            id=uuid4(),
            organization_id=organization_id,
            target_bc=draft.target_bc,
            entity_id=draft.entity_id,
            suggestion_id=draft.suggestion_id,
            outcome_kind=draft.outcome_kind,
            actual_value=draft.actual_value,
            source_ref=draft.source_ref,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def outcome_ledger_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryOutcomeDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.outcome_ledgers.OutcomeLedgerService",
        lambda _s: desk,
    )
    set_authz_checker(PermitOutcomeLedgerAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "target_bc": "shipment",
        "entity_id": _ENTITY,
        "suggestion_id": _SUGGESTION,
        "outcome_kind": "eta",
        "actual_value": "45",
        "source_ref": "fixture://outcome-ledger/a",
    }
    body.update(extra)
    return body


def test_post_persists(outcome_ledger_http: object) -> None:
    client, desk = outcome_ledger_http
    response = client.post(
        "/api/v1/outcome-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["outcome_kind"] == "eta"
    assert response.json()["actual_value"] == "45.0000"
    assert response.headers.get("X-Omni-Catalog") == "outcome-ledger"
    assert len(desk.rows) == 1


def test_post_rejects_amount_margin_score(outcome_ledger_http: object) -> None:
    client, _desk = outcome_ledger_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/outcome-ledgers",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_float_actual(outcome_ledger_http: object) -> None:
    client, _desk = outcome_ledger_http
    response = client.post(
        "/api/v1/outcome-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(actual_value=1.5),
    )
    assert response.status_code == 422


def test_post_accepts_open_kind(outcome_ledger_http: object) -> None:
    client, desk = outcome_ledger_http
    response = client.post(
        "/api/v1/outcome-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(outcome_kind="tender"),
    )
    assert response.status_code == 201
    assert response.json()["outcome_kind"] == "tender"
    assert len(desk.rows) == 1


def test_post_rejects_bad_kind(outcome_ledger_http: object) -> None:
    client, _desk = outcome_ledger_http
    response = client.post(
        "/api/v1/outcome-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(outcome_kind="1x"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_rejects_bad_suggestion_id(outcome_ledger_http: object) -> None:
    client, _desk = outcome_ledger_http
    response = client.post(
        "/api/v1/outcome-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(suggestion_id="not-a-uuid"),
    )
    assert response.status_code == 422


def test_post_rejects_foreign_source_ref(outcome_ledger_http: object) -> None:
    client, _desk = outcome_ledger_http
    response = client.post(
        "/api/v1/outcome-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(outcome_ledger_http: object) -> None:
    client, desk = outcome_ledger_http
    client.post(
        "/api/v1/outcome-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/outcome-ledgers",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
