from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.memory_edge import require_edge_kind, require_edge_source_ref
from app.main import app
from app.models.memory_edge import MemoryEdge
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


class StubEdges:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[MemoryEdge] = []

    async def list_links(self) -> list[MemoryEdge]:
        return list(self.rows)

    async def record_link(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        edge_kind: object,
        source_ref: object,
    ) -> MemoryEdge:
        row = MemoryEdge(
            id=uuid4(),
            organization_id=organization_id,
            edge_kind=require_edge_kind(edge_kind),
            source_ref=require_edge_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    edges = StubEdges(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.memory_edges.MemoryEdgeService", lambda _s: edges)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), edges
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "edge_kind": "recalls",
        "source_ref": "fixture://memory-edge/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_memory_edge(catalog_client: object) -> None:
    client, _edges = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/memory-edges", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["edge_kind"] == "recalls"
    assert "buy_amount" not in body
    listed = client.get("/api/v1/memory-edges", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_bad_kind_is_400(catalog_client: object) -> None:
    client, _edges = catalog_client
    response = client.post(
        "/api/v1/memory-edges",
        headers=bearer_auth_headers(),
        json=_payload(edge_kind="vector"),
    )
    assert response.status_code == 400
    assert "krawędź" in response.json()["detail"]


def test_http_create_memory_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _edges = catalog_client
    response = client.post(
        "/api/v1/memory-edges",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://memory.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
