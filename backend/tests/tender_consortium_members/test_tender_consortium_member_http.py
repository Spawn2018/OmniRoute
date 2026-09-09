from datetime import date
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.tender_consortium_member import (
    require_board_id,
    require_party_id,
    require_seat_code,
    require_seat_source_ref,
)
from app.main import app
from app.models.party import Party
from app.models.tender import Tender
from app.models.tender_consortium_member import TenderConsortiumMember
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


class StubBoardLookup:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: Tender | None = None

    async def get_board(self, tender_id: UUID) -> Tender:
        if self.row is None or self.row.id != tender_id:
            raise ResourceNotFound("nieznany przetarg")
        return self.row


class StubPartyLookup:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: Party | None = None

    async def get_party(self, party_id: UUID) -> Party:
        if self.row is None or self.row.id != party_id:
            raise ResourceNotFound("nieznany kontrahent")
        return self.row


class StubSeatDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[TenderConsortiumMember] = []

    async def list_seats(self) -> list[TenderConsortiumMember]:
        return list(self.rows)

    async def persist_seat(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        tender_id: object,
        party_id: object,
        seat_code: object,
        source_ref: object,
    ) -> TenderConsortiumMember:
        row = TenderConsortiumMember(
            id=uuid4(),
            organization_id=organization_id,
            tender_id=require_board_id(tender_id),
            party_id=require_party_id(party_id),
            seat_code=require_seat_code(seat_code),
            source_ref=require_seat_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


def _board() -> Tender:
    return Tender(
        id=uuid4(),
        organization_id=uuid4(),
        side="sell",
        kind="open",
        status="draft",
        buyer_party_id=uuid4(),
        deadline_at=date(2026, 12, 31),
        incoterm="FOB",
        trade_side="export",
        named_place="Gdynia",
        source_ref="fixture://tender/1",
        created_by=uuid4(),
    )


def _party() -> Party:
    return Party(
        id=uuid4(),
        organization_id=uuid4(),
        legal_name="Seat Party",
        country_code="PL",
        roles=["agent"],
        source_ref="fixture://party/1",
        is_active=True,
        created_by=uuid4(),
    )


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    seats = StubSeatDesk(object())
    boards = StubBoardLookup(object())
    parties = StubPartyLookup(object())
    boards.row = _board()
    parties.row = _party()

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.tender_consortium_members.TenderConsortiumMemberService",
        lambda _s: seats,
    )
    monkeypatch.setattr("app.api.tender_consortium_members.TenderService", lambda _s: boards)
    monkeypatch.setattr("app.api.tender_consortium_members.PartyService", lambda _s: parties)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), seats, boards, parties
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(tender_id: UUID, party_id: UUID, **overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "tender_id": str(tender_id),
        "party_id": str(party_id),
        "seat_code": "lead",
        "source_ref": "fixture://tender-consortium-member/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_tender_consortium_member(catalog_client: object) -> None:
    client, _seats, boards, parties = catalog_client
    assert boards.row is not None
    assert parties.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/tender-consortium-members",
        headers=headers,
        json=_payload(boards.row.id, parties.row.id),
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["seat_code"] == "lead"
    assert "buy_amount" not in body
    listed = client.get("/api/v1/tender-consortium-members", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_bad_seat_code_is_400(catalog_client: object) -> None:
    client, _seats, boards, parties = catalog_client
    assert boards.row is not None
    assert parties.row is not None
    response = client.post(
        "/api/v1/tender-consortium-members",
        headers=bearer_auth_headers(),
        json=_payload(boards.row.id, parties.row.id, seat_code="chair"),
    )
    assert response.status_code == 400
    assert "fotel" in response.json()["detail"]


def test_http_create_seat_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _seats, boards, parties = catalog_client
    assert boards.row is not None
    assert parties.row is not None
    response = client.post(
        "/api/v1/tender-consortium-members",
        headers=bearer_auth_headers(),
        json=_payload(
            boards.row.id,
            parties.row.id,
            source_ref="http://hold.example/x",
        ),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
