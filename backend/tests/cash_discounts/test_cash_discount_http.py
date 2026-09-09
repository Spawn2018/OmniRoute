from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.cash_discount import (
    require_cash_discount_source_ref,
    require_discount_kind,
    require_invoice_id,
)
from app.domain.errors import ResourceNotFound
from app.main import app
from app.models.cash_discount import CashDiscount
from app.models.sales_invoice import SalesInvoice
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


class StubInvoiceLookup:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: SalesInvoice | None = None

    async def get_invoice(self, invoice_id: UUID) -> SalesInvoice:
        if self.row is None or self.row.id != invoice_id:
            raise ResourceNotFound("nieznana faktura")
        return self.row


class StubSkontoDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[CashDiscount] = []

    async def list_discounts(self) -> list[CashDiscount]:
        return list(self.rows)

    async def persist_discount(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        sales_invoice_id: object,
        discount_kind: object,
        source_ref: object,
    ) -> CashDiscount:
        row = CashDiscount(
            id=uuid4(),
            organization_id=organization_id,
            sales_invoice_id=require_invoice_id(sales_invoice_id),
            discount_kind=require_discount_kind(discount_kind),
            source_ref=require_cash_discount_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


def _invoice() -> SalesInvoice:
    return SalesInvoice(
        id=uuid4(),
        organization_id=uuid4(),
        shipment_id=uuid4(),
        invoice_kind="issued",
        invoice_ref="FV/1",
        source_ref="fixture://sales-invoice/1",
        created_by=uuid4(),
    )


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    discounts = StubSkontoDesk(object())
    invoices = StubInvoiceLookup(object())
    invoices.row = _invoice()

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.cash_discounts.CashDiscountService",
        lambda _s: discounts,
    )
    monkeypatch.setattr(
        "app.api.cash_discounts.SalesInvoiceService",
        lambda _s: invoices,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), discounts, invoices
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(invoice_id: UUID, **overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "sales_invoice_id": str(invoice_id),
        "discount_kind": "skonto",
        "source_ref": "fixture://cash-discount/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_cash_discount(catalog_client: object) -> None:
    client, _discounts, invoices = catalog_client
    assert invoices.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/cash-discounts",
        headers=headers,
        json=_payload(invoices.row.id),
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["discount_kind"] == "skonto"
    assert "buy_amount" not in body
    listed = client.get("/api/v1/cash-discounts", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_bad_discount_kind_is_400(catalog_client: object) -> None:
    client, _discounts, invoices = catalog_client
    assert invoices.row is not None
    response = client.post(
        "/api/v1/cash-discounts",
        headers=bearer_auth_headers(),
        json=_payload(invoices.row.id, discount_kind="X"),
    )
    assert response.status_code == 400
    assert "skonto" in response.json()["detail"]


def test_http_create_cash_discount_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _discounts, invoices = catalog_client
    assert invoices.row is not None
    response = client.post(
        "/api/v1/cash-discounts",
        headers=bearer_auth_headers(),
        json=_payload(invoices.row.id, source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
