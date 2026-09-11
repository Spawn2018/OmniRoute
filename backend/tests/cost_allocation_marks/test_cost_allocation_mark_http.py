from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.cost_allocation_mark import parse_cost_allocation_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.cost_allocation_mark import CostAllocationMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "bytes")


def test_migration_252_creates_cost_allocation_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/252_cost_allocation_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "252_cost_allocation_mark"' in source
    assert 'down_revision: str | None = "251_make_or_buy_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "cost_allocation_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "bytes"):
        assert banned not in source


def test_importlinter_lists_cost_allocation_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.cost_allocation_marks" in forbidden
    assert "app.models.cost_allocation_mark" in forbidden


def test_generated_api_types_include_cost_allocation_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "CostAllocationMarkResponse" in source
    assert "CostAllocationMarkCreate" in source


def test_fga_source_declares_cost_allocation_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_cost_allocation_marks: member" in source


def test_authorization_model_grants_cost_allocation_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_cost_allocation_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitYardAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryYardDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[CostAllocationMark] = []

    async def list_marks(self) -> list[CostAllocationMark]:
        return list(self.rows)

    async def persist_cost_allocation_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        alloc_kind: object,
        source_ref: object,
    ) -> CostAllocationMark:
        code, kind, origin = parse_cost_allocation_mark_row(
            mark_code,
            alloc_kind,
            source_ref,
        )
        row = CostAllocationMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            alloc_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def cost_allocation_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryYardDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.cost_allocation_marks.CostAllocationMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitYardAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "direct_01",
        "alloc_kind": "direct",
        "source_ref": "fixture://cost-allocation-mark/a",
    }
    body.update(extra)
    return body


def test_post_cost_allocation_mark_persists(cost_allocation_http: object) -> None:
    client, desk = cost_allocation_http
    response = client.post(
        "/api/v1/cost-allocation-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["alloc_kind"] == "direct"
    assert len(desk.rows) == 1


def test_post_cost_allocation_mark_rejects_amount_bytes(cost_allocation_http: object) -> None:
    client, _desk = cost_allocation_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/cost-allocation-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_cost_allocation_mark_rejects_bad_code(cost_allocation_http: object) -> None:
    client, _desk = cost_allocation_http
    response = client.post(
        "/api/v1/cost-allocation-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_cost_allocation_mark_rejects_bad_kind(cost_allocation_http: object) -> None:
    client, _desk = cost_allocation_http
    response = client.post(
        "/api/v1/cost-allocation-marks",
        headers=bearer_auth_headers(),
        json=_payload(alloc_kind="engine"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_cost_allocation_mark_rejects_foreign_source_ref(cost_allocation_http: object) -> None:
    client, _desk = cost_allocation_http
    response = client.post(
        "/api/v1/cost-allocation-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_cost_allocation_marks_lists_rows(cost_allocation_http: object) -> None:
    client, desk = cost_allocation_http
    client.post(
        "/api/v1/cost-allocation-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/cost-allocation-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
