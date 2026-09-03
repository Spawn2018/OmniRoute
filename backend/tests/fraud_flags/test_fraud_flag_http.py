from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.fraud_flag import require_flag_kind, require_flag_source_ref
from app.main import app
from app.models.fraud_flag import FraudFlag
from app.models.party import Party
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


class StubPartyService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: Party | None = None

    async def get_party(self, party_id: UUID) -> Party:
        if self.row is None or self.row.id != party_id:
            raise ResourceNotFound("nieznany kontrahent")
        return self.row


class StubFraudFlagService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[FraudFlag] = []

    async def list_flags(self) -> list[FraudFlag]:
        return list(self.rows)

    async def record_flag(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: UUID,
        flag_kind: str,
        source_ref: str,
    ) -> FraudFlag:
        row = FraudFlag(
            id=uuid4(),
            organization_id=organization_id,
            party_id=party_id,
            flag_kind=require_flag_kind(flag_kind),
            source_ref=require_flag_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


def _party() -> Party:
    return Party(
        id=uuid4(),
        organization_id=uuid4(),
        legal_name="Agent",
        country_code="PL",
        roles=["agent"],
        source_ref="tenant:manual",
        is_active=True,
    )


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    parties = StubPartyService(object())
    flags = StubFraudFlagService(object())

    def _parties(_session: object) -> StubPartyService:
        return parties

    def _rows(_session: object) -> StubFraudFlagService:
        return flags

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.fraud_flags.PartyService", _parties)
    monkeypatch.setattr("app.api.fraud_flags.FraudFlagService", _rows)
    parties.row = _party()
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), parties, flags
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_fraud_flag(catalog_client: object) -> None:
    client, parties, _flags = catalog_client
    assert parties.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/fraud-flags",
        headers=headers,
        json={
            "party_id": str(parties.row.id),
            "flag_kind": "billing",
            "source_ref": "fixture://fraud-flag/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["party_id"] == str(parties.row.id)
    assert body["flag_kind"] == "billing"
    assert "amount" not in body
    assert "risk_score" not in body
    listed = client.get("/api/v1/fraud-flags", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_flag_unknown_party_is_404(catalog_client: object) -> None:
    client, _parties, _flags = catalog_client
    response = client.post(
        "/api/v1/fraud-flags",
        headers=bearer_auth_headers(),
        json={
            "party_id": str(uuid4()),
            "flag_kind": "billing",
            "source_ref": "fixture://fraud-flag/1",
        },
    )
    assert response.status_code == 404


def test_http_create_flag_unknown_kind_is_400(catalog_client: object) -> None:
    client, parties, _flags = catalog_client
    assert parties.row is not None
    response = client.post(
        "/api/v1/fraud-flags",
        headers=bearer_auth_headers(),
        json={
            "party_id": str(parties.row.id),
            "flag_kind": "score",
            "source_ref": "fixture://fraud-flag/1",
        },
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_http_create_flag_empty_source_ref_is_400(catalog_client: object) -> None:
    client, parties, _flags = catalog_client
    assert parties.row is not None
    response = client.post(
        "/api/v1/fraud-flags",
        headers=bearer_auth_headers(),
        json={
            "party_id": str(parties.row.id),
            "flag_kind": "billing",
            "source_ref": "   ",
        },
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]
