from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.weather_observation import (
    require_condition_code,
    require_observed_at,
    require_provider_code,
    require_station_unlocode,
    require_weather_source_ref,
)
from app.main import app
from app.models.weather_observation import WeatherObservation
from tests.http_auth import bearer_auth_headers

_HITL_ISO = "2026-09-09T12:00:00+00:00"


class AllowAllAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class StubWeatherDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[WeatherObservation] = []

    async def list_marks(self) -> list[WeatherObservation]:
        return list(self.rows)

    async def persist_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        condition_code: object,
        station_unlocode: object,
        observed_at: object,
        provider_code: object,
        source_ref: object,
    ) -> WeatherObservation:
        row = WeatherObservation(
            id=uuid4(),
            organization_id=organization_id,
            condition_code=require_condition_code(condition_code),
            station_unlocode=require_station_unlocode(station_unlocode),
            observed_at=require_observed_at(observed_at),
            provider_code=require_provider_code(provider_code),
            source_ref=require_weather_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    marks = StubWeatherDesk(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.weather_observations.WeatherObservationService",
        lambda _s: marks,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), marks
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "condition_code": "rain",
        "station_unlocode": "PLGDY",
        "observed_at": _HITL_ISO,
        "provider_code": "hitl",
        "source_ref": "fixture://weather-observation/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_weather_observation(catalog_client: object) -> None:
    client, _marks = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/weather-observations", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["condition_code"] == "rain"
    assert body["station_unlocode"] == "PLGDY"
    assert body["observed_at"].startswith("2026-09-09T12:00:00")
    assert "buy_amount" not in body
    assert "open_meteo" not in body
    listed = client.get("/api/v1/weather-observations", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_bad_condition_is_400(catalog_client: object) -> None:
    client, _marks = catalog_client
    response = client.post(
        "/api/v1/weather-observations",
        headers=bearer_auth_headers(),
        json=_payload(condition_code="storm"),
    )
    assert response.status_code == 400
    assert "warunek" in response.json()["detail"]


def test_http_create_naive_observed_at_is_400(catalog_client: object) -> None:
    client, _marks = catalog_client
    response = client.post(
        "/api/v1/weather-observations",
        headers=bearer_auth_headers(),
        json=_payload(observed_at="2026-09-09T12:00:00"),
    )
    assert response.status_code == 400
    assert "obserwacja" in response.json()["detail"]


def test_http_create_open_meteo_provider_is_400(catalog_client: object) -> None:
    client, _marks = catalog_client
    response = client.post(
        "/api/v1/weather-observations",
        headers=bearer_auth_headers(),
        json=_payload(provider_code="open_meteo"),
    )
    assert response.status_code == 400
    assert "dostawca" in response.json()["detail"]


def test_http_create_weather_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _marks = catalog_client
    response = client.post(
        "/api/v1/weather-observations",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
