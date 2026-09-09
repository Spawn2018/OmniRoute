from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.twin_mark import require_twin_kind, require_twin_source_ref
from app.main import app
from app.models.twin_mark import TwinMark
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


class StubTwinMarks:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[TwinMark] = []

    async def list_marks(self) -> list[TwinMark]:
        return list(self.rows)

    async def persist_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        twin_kind: object,
        source_ref: object,
    ) -> TwinMark:
        row = TwinMark(
            id=uuid4(),
            organization_id=organization_id,
            twin_kind=require_twin_kind(twin_kind),
            source_ref=require_twin_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    marks = StubTwinMarks(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.twin_marks.TwinMarkService", lambda _s: marks)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), marks
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "twin_kind": "vehicle",
        "source_ref": "fixture://twin-mark/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_twin_mark(catalog_client: object) -> None:
    client, _marks = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/twin-marks", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["twin_kind"] == "vehicle"
    assert "buy_amount" not in body
    listed = client.get("/api/v1/twin-marks", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_bad_kind_is_400(catalog_client: object) -> None:
    client, _marks = catalog_client
    response = client.post(
        "/api/v1/twin-marks",
        headers=bearer_auth_headers(),
        json=_payload(twin_kind="physics"),
    )
    assert response.status_code == 400
    assert "postać" in response.json()["detail"]


def test_http_create_twin_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _marks = catalog_client
    response = client.post(
        "/api/v1/twin-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://twin.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
