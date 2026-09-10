from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.task_template import (
    require_task_applies_when,
    require_task_template_code,
    require_task_template_source_ref,
)
from app.main import app
from app.models.task_template import TaskTemplate
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


class StubBlueprints:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[TaskTemplate] = []

    async def list_templates(self) -> list[TaskTemplate]:
        return list(self.rows)

    async def record_template(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        template_code: object,
        applies_when: object,
        source_ref: object,
    ) -> TaskTemplate:
        row = TaskTemplate(
            id=uuid4(),
            organization_id=organization_id,
            template_code=require_task_template_code(template_code),
            applies_when=require_task_applies_when(applies_when),
            source_ref=require_task_template_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


class StubOutbox:
    def __init__(self, session: object) -> None:
        self._session = session
        self.saved: list[UUID] = []

    async def record_template_saved(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        subject_id: object,
        source_ref: str,
    ) -> None:
        _ = organization_id, user_id, source_ref
        self.saved.append(UUID(str(subject_id)))


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    blueprints = StubBlueprints(object())
    outbox = StubOutbox(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.task_templates.TaskTemplateService",
        lambda _s: blueprints,
    )
    monkeypatch.setattr(
        "app.api.task_templates.OutboxEventService",
        lambda _s: outbox,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), blueprints, outbox
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "template_code": "gate_in",
        "applies_when": "container at CY",
        "source_ref": "fixture://task-template/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_task_template(catalog_client: object) -> None:
    client, _rows, outbox = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/task-templates", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["template_code"] == "gate_in"
    assert body["applies_when"] == "container at CY"
    assert "buy_amount" not in body
    assert outbox.saved == [UUID(body["id"])]
    listed = client.get("/api/v1/task-templates", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_bad_code_is_400(catalog_client: object) -> None:
    client, _rows, _outbox = catalog_client
    response = client.post(
        "/api/v1/task-templates",
        headers=bearer_auth_headers(),
        json=_payload(template_code="Gate In"),
    )
    assert response.status_code == 400
    assert "szablon" in response.json()["detail"]


def test_http_create_blank_when_is_400(catalog_client: object) -> None:
    client, _rows, _outbox = catalog_client
    response = client.post(
        "/api/v1/task-templates",
        headers=bearer_auth_headers(),
        json=_payload(applies_when="  "),
    )
    assert response.status_code == 400
    assert "warunek" in response.json()["detail"]


def test_http_create_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _rows, _outbox = catalog_client
    response = client.post(
        "/api/v1/task-templates",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://tasks.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
