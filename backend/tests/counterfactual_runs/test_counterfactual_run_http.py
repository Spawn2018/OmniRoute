from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.counterfactual_run import parse_counterfactual_run_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.counterfactual_run import CounterfactualRun
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "margin", "score")


def test_migration_344_creates_counterfactual_run_and_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/344_counterfactual_run.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "344_counterfactual_run"' in source
    assert 'down_revision: str | None = "343_outcome_ledger"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "counterfactual_run_tenant_isolation" in source
    for banned in ("float(", "httpx"):
        assert banned not in source.lower()
    assert 'sa.Column("amount"' not in source
    assert "plan_snapshot.id" not in source


def test_importlinter_lists_counterfactual_run_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.counterfactual_runs" in forbidden
    assert "app.models.counterfactual_run" in forbidden


def test_api_types_include_counterfactual_run() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "CounterfactualRunResponse" in source
    assert "CounterfactualRunCreate" in source


def test_fga_source_declares_counterfactual_run_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_counterfactual_runs: member" in source


def test_fga_model_grants_counterfactual_run_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_counterfactual_runs"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitCounterfactualAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryCounterfactualDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[CounterfactualRun] = []

    async def list_rows(self) -> list[CounterfactualRun]:
        return list(self.rows)

    async def persist_run(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        run_code: object,
        baseline_label: object,
        levers_label: object,
        result_label: object,
        source_ref: object,
    ) -> CounterfactualRun:
        draft = parse_counterfactual_run_row(
            run_code,
            baseline_label,
            levers_label,
            result_label,
            source_ref,
        )
        row = CounterfactualRun(
            id=uuid4(),
            organization_id=organization_id,
            run_code=draft.run_code,
            baseline_label=draft.baseline_label,
            levers_label=draft.levers_label,
            result_label=draft.result_label,
            source_ref=draft.source_ref,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def counterfactual_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryCounterfactualDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.counterfactual_runs.CounterfactualRunService",
        lambda _s: desk,
    )
    set_authz_checker(PermitCounterfactualAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "run_code": "fuel_spike",
        "baseline_label": "plan z wczoraj",
        "levers_label": "paliwo w gore",
        "result_label": "eta plus dwie godziny",
        "source_ref": "fixture://counterfactual-run/a",
    }
    body.update(extra)
    return body


def test_post_persists(counterfactual_http: object) -> None:
    client, desk = counterfactual_http
    response = client.post(
        "/api/v1/counterfactual-runs",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["run_code"] == "fuel_spike"
    assert response.headers.get("X-Omni-Catalog") == "counterfactual-run"
    assert len(desk.rows) == 1


def test_post_rejects_amount_margin_score(counterfactual_http: object) -> None:
    client, _desk = counterfactual_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/counterfactual-runs",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(counterfactual_http: object) -> None:
    client, _desk = counterfactual_http
    response = client.post(
        "/api/v1/counterfactual-runs",
        headers=bearer_auth_headers(),
        json=_payload(run_code="1x"),
    )
    assert response.status_code == 400
    assert "kod" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(counterfactual_http: object) -> None:
    client, _desk = counterfactual_http
    response = client.post(
        "/api/v1/counterfactual-runs",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(counterfactual_http: object) -> None:
    client, desk = counterfactual_http
    client.post(
        "/api/v1/counterfactual-runs",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/counterfactual-runs",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
