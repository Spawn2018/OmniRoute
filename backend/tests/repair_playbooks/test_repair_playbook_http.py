from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.repair_playbook import parse_repair_playbook_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.repair_playbook import RepairPlaybook
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "mail_body")


def test_migration_231_creates_repair_playbook_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/231_repair_playbook.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "231_repair_playbook"' in source
    assert 'down_revision: str | None = "230_calibration_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "repair_playbook_tenant_isolation" in source
    for banned in ("amount", "mail_body", "float(", "httpx", "currency"):
        assert banned not in source


def test_importlinter_lists_repair_playbook_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.repair_playbooks" in forbidden
    assert "app.models.repair_playbook" in forbidden


def test_generated_api_types_include_repair_playbook() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "RepairPlaybookResponse" in source
    assert "RepairPlaybookCreate" in source


def test_fga_source_declares_repair_playbook_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_repair_playbooks: member" in source


def test_authorization_model_grants_repair_playbooks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_repair_playbooks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitRepairAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryRepairDesk:
    def __init__(self, session: object) -> None:
        self.playbooks: list[RepairPlaybook] = []

    async def list_playbooks(self) -> list[RepairPlaybook]:
        return list(self.playbooks)

    async def persist_repair_playbook(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        playbook_code: object,
        stance_kind: object,
        source_ref: object,
    ) -> RepairPlaybook:
        code, stance, origin = parse_repair_playbook_row(
            playbook_code, stance_kind, source_ref
        )
        row = RepairPlaybook(
            id=uuid4(),
            organization_id=organization_id,
            playbook_code=code,
            stance_kind=stance,
            source_ref=origin,
            created_by=user_id,
        )
        self.playbooks.append(row)
        return row


@pytest.fixture
def repair_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryRepairDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.repair_playbooks.RepairPlaybookService",
        lambda _s: desk,
    )
    set_authz_checker(PermitRepairAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "playbook_code": "contain_lane_01",
        "stance_kind": "contain",
        "source_ref": "fixture://repair-playbook/a",
    }
    body.update(extra)
    return body


def test_post_repair_playbook_persists(repair_http: object) -> None:
    client, desk = repair_http
    response = client.post(
        "/api/v1/repair-playbooks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["stance_kind"] == "contain"
    assert len(desk.playbooks) == 1


def test_post_repair_playbook_rejects_extra(repair_http: object) -> None:
    client, _desk = repair_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/repair-playbooks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_repair_playbook_rejects_bad_kind(repair_http: object) -> None:
    client, _desk = repair_http
    response = client.post(
        "/api/v1/repair-playbooks",
        headers=bearer_auth_headers(),
        json=_payload(stance_kind="auto_send"),
    )
    assert response.status_code == 400
    assert "postawa" in response.json()["detail"]


def test_post_repair_playbook_rejects_foreign_source_ref(
    repair_http: object,
) -> None:
    client, _desk = repair_http
    response = client.post(
        "/api/v1/repair-playbooks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_repair_playbooks_lists_rows(repair_http: object) -> None:
    client, desk = repair_http
    client.post(
        "/api/v1/repair-playbooks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/repair-playbooks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.playbooks) == 1
