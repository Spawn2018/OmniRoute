from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.executive_mark import require_brief_source_ref, require_question_kind
from app.main import app
from app.models.executive_mark import ExecutiveMark
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


class StubBriefs:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[ExecutiveMark] = []

    async def list_briefs(self) -> list[ExecutiveMark]:
        return list(self.rows)

    async def record_brief(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        question_kind: object,
        source_ref: object,
    ) -> ExecutiveMark:
        row = ExecutiveMark(
            id=uuid4(),
            organization_id=organization_id,
            question_kind=require_question_kind(question_kind),
            source_ref=require_brief_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    briefs = StubBriefs(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.executive_marks.ExecutiveMarkService", lambda _s: briefs)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), briefs
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "question_kind": "loss",
        "source_ref": "fixture://executive-mark/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_executive_mark(catalog_client: object) -> None:
    client, _briefs = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/executive-marks", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["question_kind"] == "loss"
    assert "buy_amount" not in body
    listed = client.get("/api/v1/executive-marks", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_bad_kind_is_400(catalog_client: object) -> None:
    client, _briefs = catalog_client
    response = client.post(
        "/api/v1/executive-marks",
        headers=bearer_auth_headers(),
        json=_payload(question_kind="ebitda"),
    )
    assert response.status_code == 400
    assert "pytanie" in response.json()["detail"]


def test_http_create_exec_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _briefs = catalog_client
    response = client.post(
        "/api/v1/executive-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://exec.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
