from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.task import parse_task_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.task import Task
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]


def test_migration_491_creates_task_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/491_task.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "491_task"' in source
    assert 'down_revision: str | None = "490_charge_fx_rate"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "task_tenant_isolation" in source
    for banned in ("amount", "float(", "httpx", "shipment_id"):
        assert banned not in source


def test_importlinter_lists_tasks_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.tasks" in forbidden
    assert "app.models.task" in forbidden


def test_fga_source_declares_tasks_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_tasks: member" in source


def test_authorization_model_grants_tasks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_tasks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class TaskAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryTaskDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[Task] = []

    async def list_tasks(self) -> list[Task]:
        return list(self.rows)

    async def persist_task(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        task_code: object,
        template_code: object,
        status_kind: object,
        source_ref: object,
    ) -> Task:
        code, template, status, origin = parse_task_row(
            task_code,
            template_code,
            status_kind,
            source_ref,
        )
        row = Task(
            id=uuid4(),
            organization_id=organization_id,
            task_code=code,
            template_code=template,
            status_kind=status,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def task_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    desk = InMemoryTaskDesk(object())

    def _factory(session: object) -> InMemoryTaskDesk:
        return desk

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.tasks.TaskService", _factory)
    set_authz_checker(TaskAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    client = TestClient(app)
    client.desk = desk  # type: ignore[attr-defined]
    yield client
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_creates_task(task_client: TestClient) -> None:
    response = task_client.post(
        "/api/v1/tasks",
        headers=bearer_auth_headers(),
        json={
            "task_code": "gate_check_01",
            "template_code": "gate_in",
            "status_kind": "open",
            "source_ref": "tenant:manual",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["task_code"] == "gate_check_01"
    assert body["template_code"] == "gate_in"
    assert body["status_kind"] == "open"


def test_http_rejects_bad_task_code(task_client: TestClient) -> None:
    response = task_client.post(
        "/api/v1/tasks",
        headers=bearer_auth_headers(),
        json={
            "task_code": "Gate Check",
            "template_code": "gate_in",
            "status_kind": "open",
            "source_ref": "tenant:manual",
        },
    )
    assert response.status_code == 400
    assert "zadanie" in response.json()["detail"]


def test_http_rejects_bad_status(task_client: TestClient) -> None:
    response = task_client.post(
        "/api/v1/tasks",
        headers=bearer_auth_headers(),
        json={
            "task_code": "gate_check_01",
            "template_code": "gate_in",
            "status_kind": "closed",
            "source_ref": "tenant:manual",
        },
    )
    assert response.status_code == 400
    assert "status" in response.json()["detail"]


def test_http_lists_tasks(task_client: TestClient) -> None:
    desk: InMemoryTaskDesk = task_client.desk  # type: ignore[attr-defined]
    desk.rows.append(
        Task(
            id=uuid4(),
            organization_id=uuid4(),
            task_code="gate_a",
            template_code="gate_in",
            status_kind="open",
            source_ref="fixture://task/a",
            created_by=uuid4(),
        ),
    )
    response = task_client.get(
        "/api/v1/tasks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_task_service_does_not_import_parents() -> None:
    service = (
        _ROOT / "backend/app/services/tasks/task_service.py"
    ).read_text(encoding="utf-8")
    for banned in (
        "app.services.charges",
        "app.services.shipments",
        "app.services.outbox_events",
        "app.services.task_templates",
        "app.services.extraction",
        "httpx",
        "float(",
    ):
        assert banned not in service
