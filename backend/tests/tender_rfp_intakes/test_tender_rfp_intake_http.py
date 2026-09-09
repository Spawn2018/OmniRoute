from datetime import date
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.tender_rfp_intake import (
    require_board_id,
    require_intake_code,
    require_intake_source_ref,
)
from app.main import app
from app.models.tender import Tender
from app.models.tender_rfp_intake import TenderRfpIntake
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


class StubIntakeDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[TenderRfpIntake] = []

    async def list_intakes(self) -> list[TenderRfpIntake]:
        return list(self.rows)

    async def persist_intake(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        tender_id: object,
        intake_code: object,
        source_ref: object,
    ) -> TenderRfpIntake:
        row = TenderRfpIntake(
            id=uuid4(),
            organization_id=organization_id,
            tender_id=require_board_id(tender_id),
            intake_code=require_intake_code(intake_code),
            source_ref=require_intake_source_ref(source_ref),
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


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    intakes = StubIntakeDesk(object())
    boards = StubBoardLookup(object())
    boards.row = _board()

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.tender_rfp_intakes.TenderRfpIntakeService", lambda _s: intakes)
    monkeypatch.setattr("app.api.tender_rfp_intakes.TenderService", lambda _s: boards)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), intakes, boards
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(tender_id: UUID, **overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "tender_id": str(tender_id),
        "intake_code": "scope",
        "source_ref": "fixture://tender-rfp-intake/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_tender_rfp_intake(catalog_client: object) -> None:
    client, _intakes, boards = catalog_client
    assert boards.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/tender-rfp-intakes",
        headers=headers,
        json=_payload(boards.row.id),
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["intake_code"] == "scope"
    assert "buy_amount" not in body
    listed = client.get("/api/v1/tender-rfp-intakes", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_bad_intake_code_is_400(catalog_client: object) -> None:
    client, _intakes, boards = catalog_client
    assert boards.row is not None
    response = client.post(
        "/api/v1/tender-rfp-intakes",
        headers=bearer_auth_headers(),
        json=_payload(boards.row.id, intake_code="X"),
    )
    assert response.status_code == 400
    assert "przyjęcie" in response.json()["detail"]


def test_http_create_intake_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _intakes, boards = catalog_client
    assert boards.row is not None
    response = client.post(
        "/api/v1/tender-rfp-intakes",
        headers=bearer_auth_headers(),
        json=_payload(boards.row.id, source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
