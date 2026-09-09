from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.tower_impact import (
    contract_gap_label,
    require_chain_stage,
    require_contract_data_status,
    require_impact_source_ref,
)
from app.main import app
from app.models.tower_impact import TowerImpact
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


class StubImpactMarks:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[TowerImpact] = []

    async def list_marks(self) -> list[TowerImpact]:
        return list(self.rows)

    async def persist_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        chain_stage: object,
        contract_data_status: object,
        source_ref: object,
    ) -> TowerImpact:
        row = TowerImpact(
            id=uuid4(),
            organization_id=organization_id,
            chain_stage=require_chain_stage(chain_stage),
            contract_data_status=require_contract_data_status(contract_data_status),
            source_ref=require_impact_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    marks = StubImpactMarks(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.tower_impacts.TowerImpactService",
        lambda _s: marks,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), marks
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "chain_stage": "stock",
        "contract_data_status": "missing",
        "source_ref": "fixture://tower-impact/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_tower_impact(catalog_client: object) -> None:
    client, _marks = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/tower-impacts", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["chain_stage"] == "stock"
    assert body["contract_data_status"] == "missing"
    assert body["contract_gap_label"] == "brak danych umowy"
    assert "buy_amount" not in body
    assert "penalty" not in body
    listed = client.get("/api/v1/tower-impacts", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]
    assert listed.json()[0]["contract_gap_label"] == "brak danych umowy"


def test_http_create_bad_stage_is_400(catalog_client: object) -> None:
    client, _marks = catalog_client
    response = client.post(
        "/api/v1/tower-impacts",
        headers=bearer_auth_headers(),
        json=_payload(chain_stage="warehouse"),
    )
    assert response.status_code == 400
    assert "etap" in response.json()["detail"]


def test_http_create_bad_contract_status_is_400(catalog_client: object) -> None:
    client, _marks = catalog_client
    response = client.post(
        "/api/v1/tower-impacts",
        headers=bearer_auth_headers(),
        json=_payload(contract_data_status="sla_clause"),
    )
    assert response.status_code == 400
    assert "umowa" in response.json()["detail"]


def test_http_create_impact_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _marks = catalog_client
    response = client.post(
        "/api/v1/tower-impacts",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://tower.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]


def test_http_recorded_status_omits_gap_label(catalog_client: object) -> None:
    client, _marks = catalog_client
    response = client.post(
        "/api/v1/tower-impacts",
        headers=bearer_auth_headers(),
        json=_payload(contract_data_status="recorded", source_ref="tenant:manual"),
    )
    assert response.status_code == 201
    assert response.json()["contract_gap_label"] is None
    assert contract_gap_label("recorded") is None
