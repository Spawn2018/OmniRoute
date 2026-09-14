from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.inventory_finance_mark import parse_inventory_finance_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.inventory_finance_mark import InventoryFinanceMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount",)


def test_migration_381_creates_inventory_finance_mark_and_forces_rls() -> None:
    source = (
        _ROOT / "backend/alembic/versions/381_inventory_finance_mark.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "381_inventory_finance_mark"' in source
    assert 'down_revision: str | None = "380_rfid_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "inventory_finance_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "valuation_sql"):
        assert banned not in source


def test_importlinter_lists_inventory_finance_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.inventory_finance_marks" in forbidden
    assert "app.models.inventory_finance_mark" in forbidden


def test_fga_source_declares_inventory_finance_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_inventory_finance_marks: member" in source


def test_authorization_model_grants_inventory_finance_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_inventory_finance_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class InventoryFinanceMarkAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryInventoryFinanceDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[InventoryFinanceMark] = []

    async def list_marks(self) -> list[InventoryFinanceMark]:
        return list(self.rows)

    async def persist_inventory_finance_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        finance_kind: object,
        source_ref: object,
    ) -> InventoryFinanceMark:
        code, kind, origin = parse_inventory_finance_mark_row(
            mark_code,
            finance_kind,
            source_ref,
        )
        row = InventoryFinanceMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            finance_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def inventory_finance_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryInventoryFinanceDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.inventory_finance_marks.InventoryFinanceMarkService",
        lambda _s: desk,
    )
    set_authz_checker(InventoryFinanceMarkAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "inv_release_01",
        "finance_kind": "release",
        "source_ref": "fixture://inventory-finance/a",
    }
    body.update(extra)
    return body


def test_post_inventory_finance_mark_persists(inventory_finance_http: object) -> None:
    client, desk = inventory_finance_http
    response = client.post(
        "/api/v1/inventory-finance-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["finance_kind"] == "release"
    assert len(desk.rows) == 1


def test_post_inventory_finance_mark_rejects_amount(
    inventory_finance_http: object,
) -> None:
    client, _desk = inventory_finance_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/inventory-finance-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_inventory_finance_mark_rejects_bad_kind(
    inventory_finance_http: object,
) -> None:
    client, _desk = inventory_finance_http
    response = client.post(
        "/api/v1/inventory-finance-marks",
        headers=bearer_auth_headers(),
        json=_payload(finance_kind="live_valuation"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_inventory_finance_mark_rejects_foreign_source_ref(
    inventory_finance_http: object,
) -> None:
    client, _desk = inventory_finance_http
    response = client.post(
        "/api/v1/inventory-finance-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_inventory_finance_marks_lists_rows(
    inventory_finance_http: object,
) -> None:
    client, desk = inventory_finance_http
    client.post(
        "/api/v1/inventory-finance-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/inventory-finance-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
