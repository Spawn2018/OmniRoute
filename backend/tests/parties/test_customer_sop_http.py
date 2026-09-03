from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import CustomerSopAlreadyApproved, UnknownCustomerSop, UnknownParty
from app.main import app
from app.models.customer_sop import CustomerSop
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
        self.rows: list[CustomerSop] = []

    async def list_sops(self) -> list[CustomerSop]:
        return list(self.rows)

    async def resolve_sop(self, party_id: UUID, code: object) -> CustomerSop:
        token = str(code).strip().lower().replace("-", "_")
        for row in self.rows:
            if row.party_id == party_id and row.code == token:
                return row
        raise UnknownCustomerSop(f"nieznana procedura: {token}")

    async def create_sop(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: UUID,
        code: object,
        title: object,
        body: object,
        blocks_auto: object = True,
    ) -> CustomerSop:
        if str(party_id) == "00000000-0000-0000-0000-000000000000":
            raise UnknownParty(f"nieznany kontrahent: {party_id}")
        token = str(code).strip().lower().replace("-", "_")
        row = CustomerSop(
            id=uuid4(),
            organization_id=organization_id,
            party_id=party_id,
            status="draft",
            code=token,
            title=str(title).strip(),
            body=str(body).strip(),
            approved_at=None,
            blocks_auto=bool(blocks_auto),
            source_ref="tenant:manual",
            created_by=user_id,
        )
        self.rows.append(row)
        return row

    async def party_blocks_auto(self, party_id: UUID) -> bool:
        return any(
            row.party_id == party_id and row.status == "approved" and row.blocks_auto
            for row in self.rows
        )

    async def approve_sop(self, sop_id: UUID) -> CustomerSop:
        for row in self.rows:
            if row.id == sop_id:
                if row.status != "draft":
                    raise CustomerSopAlreadyApproved("procedura już zatwierdzona")
                row.status = "approved"
                row.approved_at = datetime.now(UTC)
                return row
        raise UnknownCustomerSop(f"nieznana procedura: {sop_id}")


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubPartyService(object())

    def _factory(session: object) -> StubPartyService:
        return stub

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.customer_sops.PartyService", _factory)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_list_resolve_and_approve(catalog_client: TestClient) -> None:
    org_id = uuid4()
    party_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = catalog_client.post(
        "/api/v1/customer-sops",
        headers=headers,
        json={
            "party_id": str(party_id),
            "code": "pre_alert",
            "title": "Pre-alert",
            "body": "wyślij pre-alert 24h przed ETA",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["party_id"] == str(party_id)
    assert body["organization_id"] == str(org_id)
    assert body["status"] == "draft"
    assert body["approved_at"] is None
    assert body["source_ref"] == "tenant:manual"
    assert body["blocks_auto"] is True
    assert "amount" not in body

    draft_block = catalog_client.get(
        "/api/v1/customer-sops/auto-block",
        headers=headers,
        params={"party_id": str(party_id)},
    )
    assert draft_block.status_code == 200
    assert draft_block.json() == {"party_id": str(party_id), "blocks_auto": False}

    listed = catalog_client.get("/api/v1/customer-sops", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]

    resolved = catalog_client.get(
        "/api/v1/customer-sops/resolve",
        headers=headers,
        params={"party_id": str(party_id), "code": "pre_alert"},
    )
    assert resolved.status_code == 200
    assert resolved.json()["id"] == body["id"]

    approved = catalog_client.post(
        f"/api/v1/customer-sops/{body['id']}/approve",
        headers=headers,
    )
    assert approved.status_code == 200
    assert approved.json()["status"] == "approved"
    assert approved.json()["approved_at"] is not None
    assert approved.json()["blocks_auto"] is True

    blocked = catalog_client.get(
        "/api/v1/customer-sops/auto-block",
        headers=headers,
        params={"party_id": str(party_id)},
    )
    assert blocked.json()["blocks_auto"] is True


def test_http_resolve_unknown_is_rejected(catalog_client: TestClient) -> None:
    response = catalog_client.get(
        "/api/v1/customer-sops/resolve",
        headers=bearer_auth_headers(),
        params={"party_id": str(uuid4()), "code": "missing"},
    )
    assert response.status_code == 400
    assert "nieznana procedura" in response.json()["detail"]


def test_http_create_unknown_party_is_rejected(catalog_client: TestClient) -> None:
    response = catalog_client.post(
        "/api/v1/customer-sops",
        headers=bearer_auth_headers(),
        json={
            "party_id": "00000000-0000-0000-0000-000000000000",
            "code": "booking",
            "title": "Booking",
            "body": "zarezerwuj slot",
        },
    )
    assert response.status_code == 400
    assert "nieznany kontrahent" in response.json()["detail"]


def test_http_create_rejects_client_source_ref(catalog_client: TestClient) -> None:
    response = catalog_client.post(
        "/api/v1/customer-sops",
        headers=bearer_auth_headers(),
        json={
            "party_id": str(uuid4()),
            "code": "booking",
            "title": "Booking",
            "body": "zarezerwuj slot",
            "source_ref": "forged:origin",
        },
    )
    assert response.status_code == 422


def test_http_approve_twice_is_rejected(catalog_client: TestClient) -> None:
    headers = bearer_auth_headers()
    created = catalog_client.post(
        "/api/v1/customer-sops",
        headers=headers,
        json={
            "party_id": str(uuid4()),
            "code": "booking",
            "title": "Booking",
            "body": "zarezerwuj slot",
        },
    )
    sop_id = created.json()["id"]
    catalog_client.post(f"/api/v1/customer-sops/{sop_id}/approve", headers=headers)
    again = catalog_client.post(f"/api/v1/customer-sops/{sop_id}/approve", headers=headers)
    assert again.status_code == 400
    assert "zatwierdzona" in again.json()["detail"]
