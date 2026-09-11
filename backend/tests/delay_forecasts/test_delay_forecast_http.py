from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.delay_forecast import parse_delay_forecast_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.delay_forecast import DelayForecast
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("shipment_id", "amount", "eta", "currency")


def test_migration_226_creates_delay_forecast_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/226_delay_forecast.py").read_text(encoding="utf-8")
    assert 'revision: str = "226_delay_forecast"' in source
    assert 'down_revision: str | None = "225_sla_clause"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "delay_forecast_tenant_isolation" in source


def test_importlinter_lists_delay_forecast_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.delay_forecasts" in forbidden
    assert "app.models.delay_forecast" in forbidden


def test_generated_api_types_include_delay_forecast() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "DelayForecastResponse" in source
    assert "DelayForecastCreate" in source


def test_fga_source_declares_delay_forecast_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_delay_forecasts: member" in source


def test_authorization_model_grants_delay_forecasts_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_delay_forecasts"]
    assert relation.computed_userset is not None


class PermitDelayAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryDelayDesk:
    def __init__(self, session: object) -> None:
        self.forecasts: list[DelayForecast] = []

    async def list_forecasts(self) -> list[DelayForecast]:
        return list(self.forecasts)

    async def persist_delay_forecast(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        forecast_code: object,
        horizon_hours: object,
        p_late: object,
        source_ref: object,
    ) -> DelayForecast:
        code, horizon, chance, origin = parse_delay_forecast_row(
            forecast_code, horizon_hours, p_late, source_ref
        )
        row = DelayForecast(
            id=uuid4(),
            organization_id=organization_id,
            forecast_code=code,
            horizon_hours=horizon,
            p_late=chance,
            source_ref=origin,
            created_by=user_id,
        )
        self.forecasts.append(row)
        return row


@pytest.fixture
def delay_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryDelayDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr("app.api.delay_forecasts.DelayForecastService", lambda _s: desk)
    set_authz_checker(PermitDelayAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_post_delay_forecast_persists(delay_http: object) -> None:
    client, desk = delay_http
    response = client.post(
        "/api/v1/delay-forecasts",
        headers=bearer_auth_headers(),
        json={
            "forecast_code": "late_24h_01",
            "horizon_hours": 24,
            "p_late": "0.3500",
            "source_ref": "fixture://delay-forecast/a",
        },
    )
    assert response.status_code == 201
    assert response.json()["forecast_code"] == "late_24h_01"
    assert len(desk.forecasts) == 1


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "forecast_code": "late_24h_01",
        "horizon_hours": 24,
        "p_late": "0.3500",
        "source_ref": "fixture://delay-forecast/a",
    }
    body.update(extra)
    return body


def test_post_delay_forecast_rejects_extra(delay_http: object) -> None:
    client, _desk = delay_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/delay-forecasts",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_delay_forecast_rejects_bad_code(delay_http: object) -> None:
    client, _desk = delay_http
    response = client.post(
        "/api/v1/delay-forecasts",
        headers=bearer_auth_headers(),
        json=_payload(forecast_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_delay_forecast_rejects_bad_horizon(delay_http: object) -> None:
    client, _desk = delay_http
    response = client.post(
        "/api/v1/delay-forecasts",
        headers=bearer_auth_headers(),
        json=_payload(horizon_hours=200),
    )
    assert response.status_code == 400
    assert "horyzont" in response.json()["detail"]


def test_post_delay_forecast_rejects_bad_p_late(delay_http: object) -> None:
    client, _desk = delay_http
    response = client.post(
        "/api/v1/delay-forecasts",
        headers=bearer_auth_headers(),
        json=_payload(p_late="1.5"),
    )
    assert response.status_code == 400
    assert "p_late" in response.json()["detail"]


def test_post_delay_forecast_rejects_foreign_source_ref(delay_http: object) -> None:
    client, _desk = delay_http
    response = client.post(
        "/api/v1/delay-forecasts",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_delay_forecasts_lists_rows(delay_http: object) -> None:
    client, desk = delay_http
    client.post(
        "/api/v1/delay-forecasts",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get("/api/v1/delay-forecasts", headers=bearer_auth_headers())
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.forecasts) == 1
