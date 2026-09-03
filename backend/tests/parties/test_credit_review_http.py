from datetime import date
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import UnknownCreditReview, UnknownParty
from app.main import app
from app.models.credit_review import CreditReview
from tests.http_auth import bearer_auth_headers

_MISSING_PARTY = UUID("00000000-0000-0000-0000-000000000000")


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
        self.rows: list[CreditReview] = []

    async def list_reviews(self) -> list[CreditReview]:
        return list(self.rows)

    async def resolve_review(self, *, party_id: UUID, on_date: date) -> CreditReview:
        matches = [
            row for row in self.rows if row.party_id == party_id and row.review_date <= on_date
        ]
        if not matches:
            raise UnknownCreditReview(f"brak recenzji kredytowej na {on_date.isoformat()}")
        return max(matches, key=lambda row: row.review_date)

    async def create_review(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: UUID,
        review_date: date,
        decision: object,
        note: object = None,
    ) -> CreditReview:
        if party_id == _MISSING_PARTY:
            raise UnknownParty(f"nieznany kontrahent: {party_id}")
        stored_note = None if note in (None, "") else str(note).strip()
        row = CreditReview(
            id=uuid4(),
            organization_id=organization_id,
            decision=str(decision).strip().lower(),
            review_date=review_date,
            party_id=party_id,
            note=stored_note or None,
            source_ref="tenant:manual",
            created_by=user_id,
        )
        self.rows.append(row)
        return row

    async def get_review(self, review_id: UUID) -> CreditReview:
        for row in self.rows:
            if row.id == review_id:
                return row
        raise UnknownCreditReview(f"nieznana recenzja kredytowa: {review_id}")

    async def attach_bureau(self, review_id: UUID, bureau_attachment_ref: object) -> CreditReview:
        from app.domain.credit_review import normalize_bureau_attachment_ref

        row = await self.get_review(review_id)
        row.bureau_attachment_ref = normalize_bureau_attachment_ref(bureau_attachment_ref)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubPartyService(object())

    def _factory(session: object) -> StubPartyService:
        return stub

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.credit_reviews.PartyService", _factory)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_list_and_resolve(catalog_client: TestClient) -> None:
    org_id = uuid4()
    party_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = catalog_client.post(
        "/api/v1/credit-reviews",
        headers=headers,
        json={
            "party_id": str(party_id),
            "review_date": "2026-09-01",
            "decision": "ok",
            "note": "księgowość",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["party_id"] == str(party_id)
    assert body["organization_id"] == str(org_id)
    assert body["decision"] == "ok"
    assert body["source_ref"] == "tenant:manual"
    assert "score" not in body
    assert "rating" not in body
    assert "credit_limit" not in body
    assert "margin" not in body

    listed = catalog_client.get("/api/v1/credit-reviews", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]

    resolved = catalog_client.get(
        "/api/v1/credit-reviews/resolve",
        headers=headers,
        params={"party_id": str(party_id), "on_date": "2026-09-05"},
    )
    assert resolved.status_code == 200
    assert resolved.json()["id"] == body["id"]


def test_http_resolve_unknown_is_rejected(catalog_client: TestClient) -> None:
    response = catalog_client.get(
        "/api/v1/credit-reviews/resolve",
        headers=bearer_auth_headers(),
        params={"party_id": str(uuid4()), "on_date": "2026-09-01"},
    )
    assert response.status_code == 400
    assert "brak recenzji kredytowej" in response.json()["detail"]


def test_http_create_unknown_party_is_rejected(catalog_client: TestClient) -> None:
    response = catalog_client.post(
        "/api/v1/credit-reviews",
        headers=bearer_auth_headers(),
        json={
            "party_id": str(_MISSING_PARTY),
            "review_date": "2026-09-01",
            "decision": "hold",
        },
    )
    assert response.status_code == 400
    assert "nieznany kontrahent" in response.json()["detail"]


def test_http_attach_bureau_keeps_source_ref_and_has_no_score(catalog_client: TestClient) -> None:
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = catalog_client.post(
        "/api/v1/credit-reviews",
        headers=headers,
        json={
            "party_id": str(uuid4()),
            "review_date": "2026-09-01",
            "decision": "ok",
        },
    )
    assert created.status_code == 201
    review_id = created.json()["id"]
    pointer = "file://wywiad/raport-1"
    attached = catalog_client.patch(
        f"/api/v1/credit-reviews/{review_id}/attach-bureau",
        headers=headers,
        json={"bureau_attachment_ref": pointer},
    )
    assert attached.status_code == 200
    body = attached.json()
    assert body["bureau_attachment_ref"] == pointer
    assert body["source_ref"] == "tenant:manual"
    assert body["decision"] == "ok"
    assert "risk_score" not in body
    assert "score" not in body
    assert "credit_limit" not in body


def test_http_attach_bureau_empty_ref_is_rejected(catalog_client: TestClient) -> None:
    headers = bearer_auth_headers()
    created = catalog_client.post(
        "/api/v1/credit-reviews",
        headers=headers,
        json={
            "party_id": str(uuid4()),
            "review_date": "2026-09-01",
            "decision": "hold",
        },
    )
    response = catalog_client.patch(
        f"/api/v1/credit-reviews/{created.json()['id']}/attach-bureau",
        headers=headers,
        json={"bureau_attachment_ref": "   "},
    )
    assert response.status_code == 400
    assert "wskazanie raportu" in response.json()["detail"]


def test_http_attach_bureau_too_long_ref_is_rejected(catalog_client: TestClient) -> None:
    headers = bearer_auth_headers()
    created = catalog_client.post(
        "/api/v1/credit-reviews",
        headers=headers,
        json={
            "party_id": str(uuid4()),
            "review_date": "2026-09-01",
            "decision": "refuse",
        },
    )
    response = catalog_client.patch(
        f"/api/v1/credit-reviews/{created.json()['id']}/attach-bureau",
        headers=headers,
        json={"bureau_attachment_ref": "x" * 257},
    )
    assert response.status_code == 400
    assert "za długie" in response.json()["detail"]


def test_http_create_rejects_client_source_ref(catalog_client: TestClient) -> None:
    response = catalog_client.post(
        "/api/v1/credit-reviews",
        headers=bearer_auth_headers(),
        json={
            "party_id": str(uuid4()),
            "review_date": "2026-09-01",
            "decision": "ok",
            "source_ref": "forged:origin",
        },
    )
    assert response.status_code == 422
