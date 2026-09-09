from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.prediction_ledger import (
    require_crps,
    require_horizon_code,
    require_interval_bound,
    require_interval_order,
    require_ledger_source_ref,
    require_mae,
    require_model_code,
    require_prediction_kind,
)
from app.main import app
from app.models.prediction_ledger import PredictionLedger
from tests.http_auth import bearer_auth_headers


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


class StubLedgerDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[PredictionLedger] = []

    async def list_rows(self) -> list[PredictionLedger]:
        return list(self.rows)

    async def persist_ledger(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        prediction_kind: object,
        horizon_code: object,
        interval_low: object,
        interval_high: object,
        crps: object,
        mae: object,
        model_code: object,
        source_ref: object,
    ) -> PredictionLedger:
        low = require_interval_bound(interval_low)
        high = require_interval_bound(interval_high)
        require_interval_order(low, high)
        row = PredictionLedger(
            id=uuid4(),
            organization_id=organization_id,
            prediction_kind=require_prediction_kind(prediction_kind),
            horizon_code=require_horizon_code(horizon_code),
            interval_low=low,
            interval_high=high,
            crps=require_crps(crps),
            mae=require_mae(mae),
            model_code=require_model_code(model_code),
            source_ref=require_ledger_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = StubLedgerDesk(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.prediction_ledgers.PredictionLedgerService",
        lambda _s: desk,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "prediction_kind": "eta",
        "horizon_code": "h24h",
        "interval_low": "30",
        "interval_high": "90",
        "crps": "0.25",
        "mae": "12",
        "model_code": "hist_eta",
        "source_ref": "fixture://prediction-ledger/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_prediction_ledger(catalog_client: object) -> None:
    client, _desk = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/prediction-ledgers", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["prediction_kind"] == "eta"
    assert body["crps"] == "0.2500"
    assert "buy_amount" not in body
    listed = client.get("/api/v1/prediction-ledgers", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_missing_crps_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/prediction-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(crps=""),
    )
    assert response.status_code == 400
    assert "crps" in response.json()["detail"]


def test_http_create_bad_kind_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/prediction-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(prediction_kind="person_score"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_http_create_inverted_interval_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/prediction-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(interval_low="90", interval_high="30"),
    )
    assert response.status_code == 400
    assert "przedział" in response.json()["detail"]


def test_http_create_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/prediction-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
