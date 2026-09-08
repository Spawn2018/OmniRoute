from datetime import date
from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.tender_matrix_cell import (
    require_board_id,
    require_cell_amount,
    require_cell_code,
    require_cell_currency,
    require_cell_source_ref,
)
from app.main import app
from app.models.tender import Tender
from app.models.tender_matrix_cell import TenderMatrixCell
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


class StubCellDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[TenderMatrixCell] = []

    async def list_cells(self) -> list[TenderMatrixCell]:
        return list(self.rows)

    async def record_cell(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        tender_id: object,
        cell_code: object,
        amount: object,
        currency: object,
        source_ref: object,
    ) -> TenderMatrixCell:
        row = TenderMatrixCell(
            id=uuid4(),
            organization_id=organization_id,
            tender_id=require_board_id(tender_id),
            cell_code=require_cell_code(cell_code),
            amount=require_cell_amount(amount),
            currency=require_cell_currency(currency),
            source_ref=require_cell_source_ref(source_ref),
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
    cells = StubCellDesk(object())
    boards = StubBoardLookup(object())
    boards.row = _board()

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.tender_matrix_cells.TenderMatrixCellService", lambda _s: cells)
    monkeypatch.setattr("app.api.tender_matrix_cells.TenderService", lambda _s: boards)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), cells, boards
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(tender_id: UUID, **overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "tender_id": str(tender_id),
        "cell_code": "ocean_fcl",
        "amount": "10.5000",
        "currency": "EUR",
        "source_ref": "fixture://tender-matrix-cell/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_tender_matrix_cell(catalog_client: object) -> None:
    client, _cells, boards = catalog_client
    assert boards.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/tender-matrix-cells",
        headers=headers,
        json=_payload(boards.row.id),
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["cell_code"] == "ocean_fcl"
    assert Decimal(body["amount"]) == Decimal("10.5000")
    assert "buy_amount" not in body
    listed = client.get("/api/v1/tender-matrix-cells", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_bad_cell_code_is_400(catalog_client: object) -> None:
    client, _cells, boards = catalog_client
    assert boards.row is not None
    response = client.post(
        "/api/v1/tender-matrix-cells",
        headers=bearer_auth_headers(),
        json=_payload(boards.row.id, cell_code="X"),
    )
    assert response.status_code == 400
    assert "komórka" in response.json()["detail"]


def test_http_create_zero_amount_is_400(catalog_client: object) -> None:
    client, _cells, boards = catalog_client
    assert boards.row is not None
    response = client.post(
        "/api/v1/tender-matrix-cells",
        headers=bearer_auth_headers(),
        json=_payload(boards.row.id, amount="0"),
    )
    assert response.status_code == 400
    assert "kwota" in response.json()["detail"]


def test_http_create_cell_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _cells, boards = catalog_client
    assert boards.row is not None
    response = client.post(
        "/api/v1/tender-matrix-cells",
        headers=bearer_auth_headers(),
        json=_payload(boards.row.id, source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
