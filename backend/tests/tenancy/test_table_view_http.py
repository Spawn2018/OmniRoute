from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.table_view import normalize_table_view_config
from app.main import app
from app.models.table_view import TableView
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


class StubTableViewService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[TableView] = []

    async def create_view(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        table_key: str,
        name: str,
        config: dict[str, object],
    ) -> TableView:
        row = TableView(
            id=uuid4(),
            organization_id=organization_id,
            user_id=user_id,
            table_key=table_key,
            name=name.strip(),
            config=normalize_table_view_config(config),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def view_client(monkeypatch: pytest.MonkeyPatch) -> object:
    stub = StubTableViewService(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.table_views.TableViewService", lambda _session: stub)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_accepts_thread_group_by(view_client: object) -> None:
    response = view_client.post(
        "/api/v1/tenancy/table-views",
        headers=bearer_auth_headers(),
        json={
            "table_key": "carrier_inquiry",
            "name": "buy-desk",
            "config": {"group_by": "thread"},
        },
    )
    assert response.status_code == 201
    assert response.json()["config"]["group_by"] == "thread"


def test_http_accepts_party_group_by(view_client: object) -> None:
    response = view_client.post(
        "/api/v1/tenancy/table-views",
        headers=bearer_auth_headers(),
        json={
            "table_key": "inbound_message",
            "name": "buy-desk",
            "config": {"group_by": "party"},
        },
    )
    assert response.status_code == 201
    assert response.json()["config"]["group_by"] == "party"
