from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.network_print_gate_mark import parse_network_print_gate_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.network_print_gate_mark import NetworkPrintGateMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "margin")


def test_migration_504_creates_network_print_gate_mark_and_forces_rls() -> None:
    source = (
        _ROOT / "backend/alembic/versions/504_network_print_gate_mark.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "504_network_print_gate_mark"' in source
    assert 'down_revision: str | None = "503_clone_carry_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "network_print_gate_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source


def test_importlinter_lists_network_print_gate_marks_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.network_print_gate_marks" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.network_print_gate_marks" in forbidden
    assert "app.models.network_print_gate_mark" in forbidden


def test_fga_source_declares_network_print_gate_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_network_print_gate_marks: member" in source


def test_authorization_model_grants_network_print_gate_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_network_print_gate_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


def test_generated_api_types_include_network_print_gate_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "NetworkPrintGateMarkResponse" in source
    assert "NetworkPrintGateMarkCreate" in source


def test_agents_forbids_requirement_import() -> None:
    agents = (
        _ROOT / "backend/app/services/network_print_gate_marks/AGENTS.md"
    ).read_text(encoding="utf-8")
    assert "network_print_requirements" in agents
    assert "UPDATE / DELETE" in agents or "UPDATE / DELETE wiersza" in agents


def test_service_file_avoids_requirement_import() -> None:
    source = (
        _ROOT
        / "backend/app/services/network_print_gate_marks"
        / "network_print_gate_mark_service.py"
    ).read_text(encoding="utf-8")
    assert "network_print_requirements" not in source
    assert "charges" not in source


class PermitMarkAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryMarkDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[NetworkPrintGateMark] = []

    async def list_marks(self) -> list[NetworkPrintGateMark]:
        return list(self.rows)

    async def persist_network_print_gate_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        gate_kind: object,
        source_ref: object,
    ) -> NetworkPrintGateMark:
        code, kind, origin = parse_network_print_gate_mark_row(
            mark_code,
            gate_kind,
            source_ref,
        )
        row = NetworkPrintGateMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            gate_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def mark_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryMarkDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.network_print_gate_marks.NetworkPrintGateMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitMarkAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "gate_block_01",
        "gate_kind": "block_409",
        "source_ref": "fixture://network-print-gate/a",
    }
    body.update(extra)
    return body


def test_post_network_print_gate_mark_persists(mark_http: object) -> None:
    client, desk = mark_http
    response = client.post(
        "/api/v1/network-print-gate-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["gate_kind"] == "block_409"
    assert len(desk.rows) == 1


def test_post_network_print_gate_mark_rejects_bad_kind(mark_http: object) -> None:
    client, _desk = mark_http
    response = client.post(
        "/api/v1/network-print-gate-marks",
        headers=bearer_auth_headers(),
        json=_payload(gate_kind="live"),
    )
    assert response.status_code == 400
    assert "gate" in response.json()["detail"]


def test_post_network_print_gate_mark_rejects_amount(mark_http: object) -> None:
    client, _desk = mark_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/network-print-gate-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_get_network_print_gate_marks_lists(mark_http: object) -> None:
    client, desk = mark_http
    client.post(
        "/api/v1/network-print-gate-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/network-print-gate-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
