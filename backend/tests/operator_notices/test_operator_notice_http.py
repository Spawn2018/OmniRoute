from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.operator_notice import (
    operator_notice_manual_kind,
    require_notice_kind,
)
from app.main import app
from app.models.operator_notice import OperatorNotice
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


class StubOperatorNoticeService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[OperatorNotice] = []

    async def list_notices(self) -> list[OperatorNotice]:
        return list(self.rows)

    async def get_notice(self, notice_id: UUID) -> OperatorNotice:
        for row in self.rows:
            if row.id == notice_id:
                return row
        raise ResourceNotFound(f"nieznane powiadomienie: {notice_id}")

    async def create_notice(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        body: str,
        source_ref: str,
        kind: object = None,
    ) -> OperatorNotice:
        token = (
            operator_notice_manual_kind() if kind is None else require_notice_kind(kind)
        )
        row = OperatorNotice(
            id=uuid4(),
            organization_id=organization_id,
            kind=token,
            body=body,
            status="unread",
            source_ref=source_ref,
            created_by=user_id,
        )
        self.rows.append(row)
        return row

    async def mark_read(self, notice_id: UUID) -> OperatorNotice:
        row = await self.get_notice(notice_id)
        if row.status == "read" and row.read_at is not None:
            return row
        row.status = "read"
        row.read_at = datetime.now(UTC)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    notices = StubOperatorNoticeService(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.operator_notices.OperatorNoticeService",
        lambda _session: notices,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), notices
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_list_and_read_operator_notice(catalog_client: object) -> None:
    client, _notices = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/operator-notices",
        headers=headers,
        json={"body": "sprawdź mail", "source_ref": "fixture://operator-notice/1"},
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["status"] == "unread"
    assert body["kind"] == "manual"
    assert body["read_at"] is None
    assert "amount" not in body

    listed = client.get("/api/v1/operator-notices", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]

    read = client.post(f"/api/v1/operator-notices/{body['id']}/read", headers=headers)
    assert read.status_code == 200
    assert read.json()["status"] == "read"
    again = client.post(f"/api/v1/operator-notices/{body['id']}/read", headers=headers)
    assert again.status_code == 200
    assert again.json()["status"] == "read"


def test_http_creates_no_reply_notice_unread(catalog_client: object) -> None:
    client, _notices = catalog_client
    created = client.post(
        "/api/v1/operator-notices",
        headers=bearer_auth_headers(),
        json={
            "body": "cisza agenta",
            "source_ref": "tenant:manual:inquiry:1",
            "kind": "no_reply",
        },
    )
    assert created.status_code == 201
    assert created.json()["kind"] == "no_reply"
    assert created.json()["status"] == "unread"
    rejected = client.post(
        "/api/v1/operator-notices",
        headers=bearer_auth_headers(),
        json={
            "body": "filtr wycen",
            "source_ref": "tenant:manual:quote",
            "kind": "offer_acceptance",
        },
    )
    assert rejected.status_code == 400


def test_http_unknown_notice_is_404(catalog_client: object) -> None:
    client, _notices = catalog_client
    response = client.post(
        f"/api/v1/operator-notices/{uuid4()}/read",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 404
