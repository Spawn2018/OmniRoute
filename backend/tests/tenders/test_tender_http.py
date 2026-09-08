from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.tender import (
    require_board_source_ref,
    require_buyer_id,
    require_deadline_at,
    require_incoterm,
    require_kind,
    require_named_place,
    require_side,
    require_status,
    require_trade_side,
)
from app.main import app
from app.models.party import Party
from app.models.tender import Tender
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


class StubTenderService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[Tender] = []

    async def list_boards(self) -> list[Tender]:
        return list(self.rows)

    async def record_board(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        side: object,
        kind: object,
        status: object,
        buyer_party_id: object,
        deadline_at: object,
        incoterm: object,
        trade_side: object,
        named_place: object,
        source_ref: object,
    ) -> Tender:
        token = require_incoterm(incoterm)
        row = Tender(
            id=uuid4(),
            organization_id=organization_id,
            side=require_side(side),
            kind=require_kind(kind),
            status=require_status(status),
            buyer_party_id=require_buyer_id(buyer_party_id),
            deadline_at=require_deadline_at(deadline_at),
            incoterm=token,
            trade_side=require_trade_side(trade_side),
            named_place=require_named_place(token, named_place),
            source_ref=require_board_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


def _buyer() -> Party:
    return Party(
        id=uuid4(),
        organization_id=uuid4(),
        legal_name="Buyer",
        country_code="PL",
        roles=["customer"],
        source_ref="tenant:manual",
        is_active=True,
        created_by=uuid4(),
    )


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    boards = StubTenderService(object())
    parties = StubPartyService(object())
    parties.row = _buyer()

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.tenders.TenderService", lambda _s: boards)
    monkeypatch.setattr("app.api.tenders.PartyService", lambda _s: parties)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), boards, parties
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(buyer_party_id: UUID, **overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "side": "sell",
        "kind": "open",
        "status": "draft",
        "buyer_party_id": str(buyer_party_id),
        "deadline_at": "2026-12-31",
        "incoterm": "FOB",
        "trade_side": "export",
        "named_place": "Gdynia",
        "source_ref": "fixture://tender/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_tender(catalog_client: object) -> None:
    client, _boards, parties = catalog_client
    assert parties.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/tenders",
        headers=headers,
        json=_payload(parties.row.id),
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["side"] == "sell"
    assert body["kind"] == "open"
    assert body["status"] == "draft"
    assert body["deadline_at"] == "2026-12-31"
    assert "buy_amount" not in body
    listed = client.get("/api/v1/tenders", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_tender_bad_side_is_400(catalog_client: object) -> None:
    client, _boards, parties = catalog_client
    assert parties.row is not None
    response = client.post(
        "/api/v1/tenders",
        headers=bearer_auth_headers(),
        json=_payload(parties.row.id, side="both"),
    )
    assert response.status_code == 400
    assert "strona" in response.json()["detail"]


def test_http_create_tender_dap_without_place_is_400(catalog_client: object) -> None:
    client, _boards, parties = catalog_client
    assert parties.row is not None
    response = client.post(
        "/api/v1/tenders",
        headers=bearer_auth_headers(),
        json=_payload(parties.row.id, incoterm="DAP", named_place=""),
    )
    assert response.status_code == 400
    assert "miejsce" in response.json()["detail"]


def test_http_create_tender_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _boards, parties = catalog_client
    assert parties.row is not None
    response = client.post(
        "/api/v1/tenders",
        headers=bearer_auth_headers(),
        json=_payload(parties.row.id, source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
