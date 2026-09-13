from decimal import Decimal
from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.interval_score import IntervalScore
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]


def test_migration_353_creates_interval_score_sql() -> None:
    source = (_ROOT / "backend/alembic/versions/353_interval_score.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "353_interval_score"' in source
    assert 'down_revision: str | None = "352_outcome_ledger_kind_fk"' in source
    assert "interval_mae" in source
    assert "interval_crps" in source
    assert "security_invoker" in source
    assert "IMMUTABLE" in source
    assert "CREATE VIEW interval_score" in source
    for banned in ("float(", "httpx", "brier"):
        assert banned not in source.lower()
    assert "prediction_ledger" not in source
    assert 'sa.Column("amount"' not in source


def test_service_does_not_compute_or_import_ledgers() -> None:
    source = (
        _ROOT / "backend/app/services/interval_scores/interval_score_service.py"
    ).read_text(encoding="utf-8")
    assert "float" not in source
    assert "prediction_ledgers" not in source
    assert "outcome_ledgers" not in source
    assert "suggestion_ledgers" not in source
    assert "persist" not in source
    assert "add(" not in source


def test_importlinter_lists_interval_score_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.interval_scores" in forbidden
    assert "app.models.interval_score" in forbidden


def test_api_types_include_interval_score() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "IntervalScoreResponse" in source
    assert "IntervalScoreCreate" not in source


def test_fga_source_declares_interval_score_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_interval_scores: member" in source


def test_fga_model_grants_interval_score_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_interval_scores"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitIntervalScoreAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryIntervalDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[IntervalScore] = []

    async def list_rows(self) -> list[IntervalScore]:
        return list(self.rows)


@pytest.fixture
def interval_score_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryIntervalDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.interval_scores.IntervalScoreService",
        lambda _s: desk,
    )
    set_authz_checker(PermitIntervalScoreAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_get_lists_computed_pair(interval_score_http: object) -> None:
    client, desk = interval_score_http
    desk.rows.append(
        IntervalScore(
            organization_id=uuid4(),
            outcome_id=uuid4(),
            suggestion_id=uuid4(),
            entity_id=uuid4(),
            interval_low=Decimal("0"),
            interval_high=Decimal("6"),
            actual_value=Decimal("3"),
            mae=Decimal("0"),
            crps=Decimal("0.5"),
        )
    )
    response = client.get(
        "/api/v1/interval-scores",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["mae"] == "0.0000"
    assert body[0]["crps"] == "0.5000"
    assert "amount" not in body[0]


def test_post_is_rejected(interval_score_http: object) -> None:
    client, _desk = interval_score_http
    response = client.post(
        "/api/v1/interval-scores",
        headers=bearer_auth_headers(),
        json={"crps": "0.1", "mae": "1", "amount": "10"},
    )
    assert response.status_code == 405
