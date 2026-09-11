from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.intervention_outcome import parse_intervention_outcome_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.intervention_outcome import InterventionOutcome
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "saved", "predicted_loss", "repair_cost", "actual_loss")


def test_migration_234_creates_intervention_outcome_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/234_intervention_outcome.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "234_intervention_outcome"' in source
    assert 'down_revision: str | None = "233_penalty_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "intervention_outcome_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "saved"):
        assert banned not in source


def test_importlinter_lists_intervention_outcome_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.intervention_outcomes" in forbidden
    assert "app.models.intervention_outcome" in forbidden


def test_generated_api_types_include_intervention_outcome() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "InterventionOutcomeResponse" in source
    assert "InterventionOutcomeCreate" in source


def test_fga_source_declares_intervention_outcome_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_intervention_outcomes: member" in source


def test_authorization_model_grants_intervention_outcomes_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_intervention_outcomes"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitOutcomeAuthz:
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
        self.outcomes: list[InterventionOutcome] = []

    async def list_outcomes(self) -> list[InterventionOutcome]:
        return list(self.outcomes)

    async def persist_intervention_outcome(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        outcome_code: object,
        result_kind: object,
        source_ref: object,
    ) -> InterventionOutcome:
        code, kind, origin = parse_intervention_outcome_row(
            outcome_code,
            result_kind,
            source_ref,
        )
        row = InterventionOutcome(
            id=uuid4(),
            organization_id=organization_id,
            outcome_code=code,
            result_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.outcomes.append(row)
        return row


@pytest.fixture
def outcome_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryOutcomeDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.intervention_outcomes.InterventionOutcomeService",
        lambda _s: desk,
    )
    set_authz_checker(PermitOutcomeAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "outcome_code": "contained_01",
        "result_kind": "contained",
        "source_ref": "fixture://intervention-outcome/a",
    }
    body.update(extra)
    return body


def test_post_intervention_outcome_persists(outcome_http: object) -> None:
    client, desk = outcome_http
    response = client.post(
        "/api/v1/intervention-outcomes",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["result_kind"] == "contained"
    assert len(desk.outcomes) == 1


def test_post_intervention_outcome_rejects_amount_saved(outcome_http: object) -> None:
    client, _desk = outcome_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/intervention-outcomes",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_intervention_outcome_rejects_bad_kind(outcome_http: object) -> None:
    client, _desk = outcome_http
    response = client.post(
        "/api/v1/intervention-outcomes",
        headers=bearer_auth_headers(),
        json=_payload(result_kind="sql_saved"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_intervention_outcome_rejects_bad_code(outcome_http: object) -> None:
    client, _desk = outcome_http
    response = client.post(
        "/api/v1/intervention-outcomes",
        headers=bearer_auth_headers(),
        json=_payload(outcome_code="Bad Code"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_intervention_outcome_rejects_foreign_source_ref(outcome_http: object) -> None:
    client, _desk = outcome_http
    response = client.post(
        "/api/v1/intervention-outcomes",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_intervention_outcomes_lists_rows(outcome_http: object) -> None:
    client, desk = outcome_http
    client.post(
        "/api/v1/intervention-outcomes",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/intervention-outcomes",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.outcomes) == 1
