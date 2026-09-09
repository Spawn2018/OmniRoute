from datetime import date
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.tender_award_review import (
    require_board_id,
    require_review_code,
    require_review_source_ref,
)
from app.main import app
from app.models.tender import Tender
from app.models.tender_award_review import TenderAwardReview
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


class StubReviewDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[TenderAwardReview] = []

    async def list_reviews(self) -> list[TenderAwardReview]:
        return list(self.rows)

    async def persist_review(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        tender_id: object,
        review_code: object,
        source_ref: object,
    ) -> TenderAwardReview:
        row = TenderAwardReview(
            id=uuid4(),
            organization_id=organization_id,
            tender_id=require_board_id(tender_id),
            review_code=require_review_code(review_code),
            source_ref=require_review_source_ref(source_ref),
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
    reviews = StubReviewDesk(object())
    boards = StubBoardLookup(object())
    boards.row = _board()

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.tender_award_reviews.TenderAwardReviewService",
        lambda _s: reviews,
    )
    monkeypatch.setattr("app.api.tender_award_reviews.TenderService", lambda _s: boards)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), reviews, boards
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(tender_id: UUID, **overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "tender_id": str(tender_id),
        "review_code": "countersign",
        "source_ref": "fixture://tender-award-review/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_tender_award_review(catalog_client: object) -> None:
    client, _reviews, boards = catalog_client
    assert boards.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/tender-award-reviews",
        headers=headers,
        json=_payload(boards.row.id),
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["review_code"] == "countersign"
    assert "buy_amount" not in body
    listed = client.get("/api/v1/tender-award-reviews", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_bad_review_code_is_400(catalog_client: object) -> None:
    client, _reviews, boards = catalog_client
    assert boards.row is not None
    response = client.post(
        "/api/v1/tender-award-reviews",
        headers=bearer_auth_headers(),
        json=_payload(boards.row.id, review_code="won"),
    )
    assert response.status_code == 400
    assert "przegląd" in response.json()["detail"]


def test_http_create_review_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _reviews, boards = catalog_client
    assert boards.row is not None
    response = client.post(
        "/api/v1/tender-award-reviews",
        headers=bearer_auth_headers(),
        json=_payload(boards.row.id, source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
