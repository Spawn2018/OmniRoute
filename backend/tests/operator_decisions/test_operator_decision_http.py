from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import OperatorDecisionConflict, ResourceNotFound
from app.domain.operator_decision import require_decide_status
from app.main import app
from app.models.operator_decision import OperatorDecision
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


class StubOperatorDecisionService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[OperatorDecision] = []

    async def list_decisions(self) -> list[OperatorDecision]:
        return list(self.rows)

    async def get_decision(self, decision_id: UUID) -> OperatorDecision:
        for row in self.rows:
            if row.id == decision_id:
                return row
        raise ResourceNotFound(f"nieznana decyzja operatora: {decision_id}")

    async def create_decision(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        subject_kind: str,
        subject_id: UUID,
        source_ref: str,
    ) -> OperatorDecision:
        if any(
            row.subject_kind == subject_kind
            and row.subject_id == subject_id
            and row.status == "pending"
            for row in self.rows
        ):
            raise OperatorDecisionConflict("pending na ten subject już istnieje")
        row = OperatorDecision(
            id=uuid4(),
            organization_id=organization_id,
            subject_kind=subject_kind,
            subject_id=subject_id,
            status="pending",
            lock_version=0,
            source_ref=source_ref,
            created_by=user_id,
        )
        self.rows.append(row)
        return row

    async def decide(
        self,
        decision_id: UUID,
        status: str,
        lock_version: int,
    ) -> OperatorDecision:
        row = await self.get_decision(decision_id)
        if row.status != "pending" or row.lock_version != lock_version:
            raise OperatorDecisionConflict("wersja nieaktualna albo decyzja już zapisana")
        row.status = require_decide_status(status)
        row.lock_version = lock_version + 1
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    decisions = StubOperatorDecisionService(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.operator_decisions.OperatorDecisionService",
        lambda _session: decisions,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), decisions
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_list_and_accept_operator_decision(catalog_client: object) -> None:
    client, _decisions = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    subject_id = uuid4()
    created = client.post(
        "/api/v1/operator-decisions",
        headers=headers,
        json={
            "subject_kind": "inbound_message",
            "subject_id": str(subject_id),
            "source_ref": "fixture://operator-decision/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["subject_id"] == str(subject_id)
    assert body["status"] == "pending"
    assert body["lock_version"] == 0
    assert body["decided_at"] is None
    assert "amount" not in body

    listed = client.get("/api/v1/operator-decisions", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]

    accepted = client.post(
        f"/api/v1/operator-decisions/{body['id']}/decide",
        headers=headers,
        json={"status": "accepted", "lock_version": 0},
    )
    assert accepted.status_code == 200
    assert accepted.json()["status"] == "accepted"
    assert accepted.json()["lock_version"] == 1


def test_http_duplicate_pending_is_conflict(catalog_client: object) -> None:
    client, _decisions = catalog_client
    headers = bearer_auth_headers()
    payload = {
        "subject_kind": "inbound_message",
        "subject_id": str(uuid4()),
        "source_ref": "fixture://operator-decision/1",
    }
    first = client.post("/api/v1/operator-decisions", headers=headers, json=payload)
    assert first.status_code == 201
    second = client.post("/api/v1/operator-decisions", headers=headers, json=payload)
    assert second.status_code == 400
    assert "już istnieje" in second.json()["detail"]


def test_http_second_decide_is_error(catalog_client: object) -> None:
    client, _decisions = catalog_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/operator-decisions",
        headers=headers,
        json={
            "subject_kind": "inbound_message",
            "subject_id": str(uuid4()),
            "source_ref": "fixture://operator-decision/1",
        },
    )
    decision_id = created.json()["id"]
    first = client.post(
        f"/api/v1/operator-decisions/{decision_id}/decide",
        headers=headers,
        json={"status": "rejected", "lock_version": 0},
    )
    assert first.status_code == 200
    second = client.post(
        f"/api/v1/operator-decisions/{decision_id}/decide",
        headers=headers,
        json={"status": "accepted", "lock_version": 0},
    )
    assert second.status_code == 400
    assert "nieaktualna" in second.json()["detail"]


def test_http_create_quotation_subject(catalog_client: object) -> None:
    client, _decisions = catalog_client
    quote_id = uuid4()
    created = client.post(
        "/api/v1/operator-decisions",
        headers=bearer_auth_headers(),
        json={
            "subject_kind": "quotation",
            "subject_id": str(quote_id),
            "source_ref": "tenant:manual",
        },
    )
    assert created.status_code == 201
    assert created.json()["subject_kind"] == "quotation"
    assert created.json()["subject_id"] == str(quote_id)
    assert created.json()["status"] == "pending"


def test_http_decide_changed(catalog_client: object) -> None:
    client, _decisions = catalog_client
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/operator-decisions",
        headers=headers,
        json={
            "subject_kind": "inbound_message",
            "subject_id": str(uuid4()),
            "source_ref": "fixture://operator-decision/1",
        },
    )
    decision_id = created.json()["id"]
    changed = client.post(
        f"/api/v1/operator-decisions/{decision_id}/decide",
        headers=headers,
        json={"status": "changed", "lock_version": 0},
    )
    assert changed.status_code == 200
    assert changed.json()["status"] == "changed"
    assert changed.json()["lock_version"] == 1


def test_http_unknown_decision_is_404(catalog_client: object) -> None:
    client, _decisions = catalog_client
    response = client.post(
        f"/api/v1/operator-decisions/{uuid4()}/decide",
        headers=bearer_auth_headers(),
        json={"status": "accepted", "lock_version": 0},
    )
    assert response.status_code == 404
