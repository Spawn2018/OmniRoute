from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import InvalidMailDraft, ResourceNotFound
from app.main import app
from app.models.mail_draft import MailDraft
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


class StubMailDraftService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[MailDraft] = []

    async def list_drafts(self) -> list[MailDraft]:
        return list(self.rows)

    async def get_draft(self, draft_id: UUID) -> MailDraft:
        for row in self.rows:
            if row.id == draft_id:
                return row
        raise ResourceNotFound(f"nieznany szkic maila: {draft_id}")

    async def create_draft(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        subject_id: UUID,
        body: str,
        source_ref: str,
    ) -> MailDraft:
        row = MailDraft(
            id=uuid4(),
            organization_id=organization_id,
            subject_kind="extraction_draft",
            subject_id=subject_id,
            body=body,
            status="draft",
            source_ref=source_ref,
            created_by=user_id,
        )
        self.rows.append(row)
        return row

    async def mark_sent(self, draft_id: UUID, to_address: str) -> MailDraft:
        row = await self.get_draft(draft_id)
        if row.status == "sent":
            raise InvalidMailDraft("szkic już wysłany")
        row.to_address = to_address
        row.status = "sent"
        return row


class StubOperatorDecisionService:
    accepted: set[UUID] = set()

    def __init__(self, session: object) -> None:
        self._session = session

    async def has_accepted(self, subject_kind: str, subject_id: UUID) -> bool:
        _ = subject_kind
        return subject_id in StubOperatorDecisionService.accepted


class StubPartyService:
    blocked: set[UUID] = set()

    def __init__(self, session: object) -> None:
        self._session = session

    async def party_blocks_auto(self, party_id: UUID) -> bool:
        return party_id in StubPartyService.blocked


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    drafts = StubMailDraftService(object())
    StubOperatorDecisionService.accepted = set()
    StubPartyService.blocked = set()

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.mail_drafts.MailDraftService",
        lambda _session: drafts,
    )
    monkeypatch.setattr(
        "app.api.mail_drafts.OperatorDecisionService",
        StubOperatorDecisionService,
    )
    monkeypatch.setattr(
        "app.api.mail_drafts.PartyService",
        StubPartyService,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), drafts
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_mail_draft(catalog_client: object) -> None:
    client, _drafts = catalog_client
    org_id = uuid4()
    subject_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/mail-drafts",
        headers=headers,
        json={
            "subject_id": str(subject_id),
            "body": "odpowiedź do klienta",
            "source_ref": "fixture://mail-draft/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["status"] == "draft"
    assert body["subject_kind"] == "extraction_draft"
    assert body["subject_id"] == str(subject_id)
    assert "amount" not in body

    listed = client.get("/api/v1/mail-drafts", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]
    assert listed.json()[0]["to_address"] is None


def test_http_dispatch_mailto_requires_accepted_decision(catalog_client: object) -> None:
    client, _drafts = catalog_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/mail-drafts",
        headers=headers,
        json={
            "subject_id": str(uuid4()),
            "body": "odpowiedź do klienta",
            "source_ref": "fixture://mail-draft/1",
        },
    )
    draft_id = created.json()["id"]
    denied = client.post(
        f"/api/v1/mail-drafts/{draft_id}/dispatch-mailto",
        headers=headers,
        json={"to_address": "ops@carrier.example"},
    )
    assert denied.status_code == 400
    assert "akceptacji" in denied.json()["detail"]


def test_http_dispatch_mailto_is_idempotent_reject_on_second(
    catalog_client: object,
) -> None:
    client, _drafts = catalog_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/mail-drafts",
        headers=headers,
        json={
            "subject_id": str(uuid4()),
            "body": "RFQ Gdynia",
            "source_ref": "fixture://mail-draft/1",
        },
    )
    draft_id = UUID(created.json()["id"])
    StubOperatorDecisionService.accepted.add(draft_id)
    first = client.post(
        f"/api/v1/mail-drafts/{draft_id}/dispatch-mailto",
        headers=headers,
        json={"to_address": "ops@carrier.example"},
    )
    assert first.status_code == 200
    assert first.json()["status"] == "sent"
    assert first.json()["to_address"] == "ops@carrier.example"
    assert first.json()["mailto"].startswith("mailto:ops@carrier.example")
    assert first.json()["blocks_auto"] is None
    second = client.post(
        f"/api/v1/mail-drafts/{draft_id}/dispatch-mailto",
        headers=headers,
        json={"to_address": "ops@carrier.example"},
    )
    assert second.status_code == 400
    assert "wysłany" in second.json()["detail"]


def test_http_dispatch_mailto_keeps_going_when_sop_blocks_auto(
    catalog_client: object,
) -> None:
    client, _drafts = catalog_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/mail-drafts",
        headers=headers,
        json={
            "subject_id": str(uuid4()),
            "body": "RFQ",
            "source_ref": "fixture://mail-draft/1",
        },
    )
    draft_id = UUID(created.json()["id"])
    party_id = uuid4()
    StubOperatorDecisionService.accepted.add(draft_id)
    StubPartyService.blocked.add(party_id)
    sent = client.post(
        f"/api/v1/mail-drafts/{draft_id}/dispatch-mailto",
        headers=headers,
        json={"to_address": "ops@carrier.example", "party_id": str(party_id)},
    )
    assert sent.status_code == 200
    assert sent.json()["blocks_auto"] is True
    assert sent.json()["mailto"].startswith("mailto:")
