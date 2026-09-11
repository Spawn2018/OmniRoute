from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.impact_scenario import parse_impact_scenario_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.impact_scenario import ImpactScenario
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("shipment_id", "amount", "ebitda", "currency")


def test_migration_228_creates_impact_scenario_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/228_impact_scenario.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "228_impact_scenario"' in source
    assert 'down_revision: str | None = "227_remediation_option"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "impact_scenario_tenant_isolation" in source


def test_importlinter_lists_impact_scenario_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.impact_scenarios" in forbidden
    assert "app.models.impact_scenario" in forbidden


def test_generated_api_types_include_impact_scenario() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "ImpactScenarioResponse" in source
    assert "ImpactScenarioCreate" in source


def test_fga_source_declares_impact_scenario_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_impact_scenarios: member" in source


def test_authorization_model_grants_impact_scenarios_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_impact_scenarios"]
    assert relation.computed_userset is not None


class PermitImpactAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryImpactDesk:
    def __init__(self, session: object) -> None:
        self.scenarios: list[ImpactScenario] = []

    async def list_scenarios(self) -> list[ImpactScenario]:
        return list(self.scenarios)

    async def persist_impact_scenario(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        scenario_code: object,
        chain_label: object,
        source_ref: object,
    ) -> ImpactScenario:
        code, label, origin = parse_impact_scenario_row(
            scenario_code, chain_label, source_ref
        )
        row = ImpactScenario(
            id=uuid4(),
            organization_id=organization_id,
            scenario_code=code,
            chain_label=label,
            source_ref=origin,
            created_by=user_id,
        )
        self.scenarios.append(row)
        return row


@pytest.fixture
def impact_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryImpactDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.impact_scenarios.ImpactScenarioService",
        lambda _s: desk,
    )
    set_authz_checker(PermitImpactAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "scenario_code": "stock_to_sales_01",
        "chain_label": "stock to sales",
        "source_ref": "fixture://impact-scenario/a",
    }
    body.update(extra)
    return body


def test_post_impact_scenario_persists(impact_http: object) -> None:
    client, desk = impact_http
    response = client.post(
        "/api/v1/impact-scenarios",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["chain_label"] == "stock to sales"
    assert len(desk.scenarios) == 1


def test_post_impact_scenario_rejects_extra(impact_http: object) -> None:
    client, _desk = impact_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/impact-scenarios",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_impact_scenario_rejects_bad_label(impact_http: object) -> None:
    client, _desk = impact_http
    response = client.post(
        "/api/v1/impact-scenarios",
        headers=bearer_auth_headers(),
        json=_payload(chain_label=""),
    )
    assert response.status_code == 400
    assert "etykieta" in response.json()["detail"]


def test_post_impact_scenario_rejects_foreign_source_ref(impact_http: object) -> None:
    client, _desk = impact_http
    response = client.post(
        "/api/v1/impact-scenarios",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_impact_scenarios_lists_rows(impact_http: object) -> None:
    client, desk = impact_http
    client.post(
        "/api/v1/impact-scenarios",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get("/api/v1/impact-scenarios", headers=bearer_auth_headers())
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.scenarios) == 1
