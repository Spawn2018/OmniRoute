from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.gdpr_request import (
    ERASED_DISPLAY_NAME,
    erasure_mailbox,
    require_gdpr_request_kind,
    require_gdpr_request_source_ref,
    require_open_gdpr_request,
)
from app.main import app
from app.models.gdpr_request import GdprRequest
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


class _User:
    def __init__(self, row_id: UUID) -> None:
        self.id = row_id


class StubTenancyService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: _User | None = None
        self.erased: list[UUID] = []

    async def get_user(self, user_id: UUID) -> _User | None:
        if self.row is None or self.row.id != user_id:
            return None
        return self.row

    async def erase_directory_subject(
        self,
        user_id: UUID,
        *,
        email: str,
        display_name: str,
    ) -> _User:
        found = await self.get_user(user_id)
        if found is None:
            raise ResourceNotFound("nieznane konto")
        assert email == erasure_mailbox(user_id)
        assert display_name == ERASED_DISPLAY_NAME
        self.erased.append(user_id)
        return found


class StubGdprRequestService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[GdprRequest] = []

    async def list_rows(self) -> list[GdprRequest]:
        return list(self.rows)

    async def record_row(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        app_user_id: UUID,
        request_kind: str,
        source_ref: str,
    ) -> GdprRequest:
        row = GdprRequest(
            id=uuid4(),
            organization_id=organization_id,
            app_user_id=app_user_id,
            request_kind=require_gdpr_request_kind(request_kind),
            status="open",
            source_ref=require_gdpr_request_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row

    async def fulfill(self, request_id: UUID) -> GdprRequest:
        for row in self.rows:
            if row.id != request_id:
                continue
            require_open_gdpr_request(row.status)
            row.status = "fulfilled"
            return row
        raise ResourceNotFound("nieznany wniosek")


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    users = StubTenancyService(object())
    rows = StubGdprRequestService(object())
    users.row = _User(uuid4())

    def _users(_session: object) -> StubTenancyService:
        return users

    def _rows(_session: object) -> StubGdprRequestService:
        return rows

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.gdpr_requests.TenancyService", _users)
    monkeypatch.setattr("app.api.gdpr_requests.GdprRequestService", _rows)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), users, rows
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_gdpr_request(catalog_client: object) -> None:
    client, users, _rows = catalog_client
    assert users.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/gdpr-requests",
        headers=headers,
        json={
            "app_user_id": str(users.row.id),
            "request_kind": "access",
            "source_ref": "fixture://gdpr-request/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["app_user_id"] == str(users.row.id)
    assert body["request_kind"] == "access"
    assert body["status"] == "open"
    assert "amount" not in body
    assert "password_hash" not in body
    listed = client.get("/api/v1/gdpr-requests", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_unknown_user_is_404(catalog_client: object) -> None:
    client, _users, _rows = catalog_client
    response = client.post(
        "/api/v1/gdpr-requests",
        headers=bearer_auth_headers(),
        json={
            "app_user_id": str(uuid4()),
            "request_kind": "access",
            "source_ref": "fixture://gdpr-request/1",
        },
    )
    assert response.status_code == 404


def test_http_create_empty_source_ref_is_400(catalog_client: object) -> None:
    client, users, _rows = catalog_client
    assert users.row is not None
    response = client.post(
        "/api/v1/gdpr-requests",
        headers=bearer_auth_headers(),
        json={
            "app_user_id": str(users.row.id),
            "request_kind": "access",
            "source_ref": "   ",
        },
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_http_fulfill_erasure_calls_tenancy_tombstone(catalog_client: object) -> None:
    client, users, _rows = catalog_client
    assert users.row is not None
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/gdpr-requests",
        headers=headers,
        json={
            "app_user_id": str(users.row.id),
            "request_kind": "erasure",
            "source_ref": "fixture://gdpr-request/erase",
        },
    )
    assert created.status_code == 201
    fulfilled = client.post(
        f"/api/v1/gdpr-requests/{created.json()['id']}/fulfill",
        headers=headers,
    )
    assert fulfilled.status_code == 200
    assert fulfilled.json()["status"] == "fulfilled"
    assert users.erased == [users.row.id]


def test_http_fulfill_access_does_not_erase_account(catalog_client: object) -> None:
    client, users, _rows = catalog_client
    assert users.row is not None
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/gdpr-requests",
        headers=headers,
        json={
            "app_user_id": str(users.row.id),
            "request_kind": "access",
            "source_ref": "fixture://gdpr-request/access",
        },
    )
    fulfilled = client.post(
        f"/api/v1/gdpr-requests/{created.json()['id']}/fulfill",
        headers=headers,
    )
    assert fulfilled.status_code == 200
    assert users.erased == []
