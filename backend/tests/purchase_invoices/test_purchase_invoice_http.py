from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.purchase_invoice import parse_purchase_invoice_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.purchase_invoice import PurchaseInvoice
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "bytes")


def test_migration_429_creates_purchase_invoice_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/429_purchase_invoice.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "429_purchase_invoice"' in source
    assert 'down_revision: str | None = "428_self_billing_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "purchase_invoice_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "bytes"):
        assert banned not in source


def test_importlinter_lists_purchase_invoice_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.purchase_invoices" in forbidden
    assert "app.models.purchase_invoice" in forbidden


def test_fga_source_declares_purchase_invoice_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_purchase_invoices: member" in source


def test_authorization_model_grants_purchase_invoices_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_purchase_invoices"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[PurchaseInvoice] = []

    async def list_invoices(self) -> list[PurchaseInvoice]:
        return list(self.rows)

    async def persist_purchase_invoice(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        invoice_ref: object,
        invoice_kind: object,
        source_ref: object,
    ) -> PurchaseInvoice:
        ref, kind, origin = parse_purchase_invoice_row(
            invoice_ref,
            invoice_kind,
            source_ref,
        )
        row = PurchaseInvoice(
            id=uuid4(),
            organization_id=organization_id,
            invoice_ref=ref,
            invoice_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def purchase_invoice_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.purchase_invoices.PurchaseInvoiceService",
        lambda _session: desk,
    )
    set_authz_checker(PermitAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "invoice_ref": "FV/2026/01",
        "invoice_kind": "noted",
        "source_ref": "fixture://purchase-invoice/a",
    }
    body.update(extra)
    return body


def test_post_purchase_invoice_persists(purchase_invoice_http: object) -> None:
    client, desk = purchase_invoice_http
    response = client.post(
        "/api/v1/purchase-invoices",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["invoice_kind"] == "noted"
    assert len(desk.rows) == 1


def test_post_purchase_invoice_rejects_amount_bytes(purchase_invoice_http: object) -> None:
    client, _desk = purchase_invoice_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/purchase-invoices",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_purchase_invoice_rejects_bad_kind(purchase_invoice_http: object) -> None:
    client, _desk = purchase_invoice_http
    response = client.post(
        "/api/v1/purchase-invoices",
        headers=bearer_auth_headers(),
        json=_payload(invoice_kind="paid"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_get_purchase_invoices_lists_rows(purchase_invoice_http: object) -> None:
    client, desk = purchase_invoice_http
    client.post(
        "/api/v1/purchase-invoices",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/purchase-invoices",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
