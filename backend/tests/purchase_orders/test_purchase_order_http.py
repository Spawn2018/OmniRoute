from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.purchase_order import parse_purchase_order_row
from app.main import app
from app.models.purchase_order import PurchaseOrder
from tests.http_auth import bearer_auth_headers

_LINE_FIELDS = ("sku", "qty", "quantity", "uom", "asn", "shipment_id", "amount")


class PermitPurchaseOrderAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryPurchaseOrderDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.headers: list[PurchaseOrder] = []

    async def list_headers(self) -> list[PurchaseOrder]:
        return list(self.headers)

    async def persist_purchase_order(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        po_code: object,
        plant_label: object,
        source_ref: object,
    ) -> PurchaseOrder:
        code, plant, origin = parse_purchase_order_row(po_code, plant_label, source_ref)
        row = PurchaseOrder(
            id=uuid4(),
            organization_id=organization_id,
            po_code=code,
            plant_label=plant,
            source_ref=origin,
            created_by=user_id,
        )
        self.headers.append(row)
        return row


@pytest.fixture
def purchase_order_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryPurchaseOrderDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.purchase_orders.PurchaseOrderService",
        lambda _s: desk,
    )
    set_authz_checker(PermitPurchaseOrderAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "po_code": "po_gdansk_01",
        "plant_label": "Gdańsk",
        "source_ref": "fixture://purchase-order/pl-1",
    }
    body.update(extra)
    return body


def test_http_create_and_list_purchase_order(purchase_order_http: object) -> None:
    client, _desk = purchase_order_http
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/purchase-orders", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["po_code"] == "po_gdansk_01"
    assert body["plant_label"] == "Gdańsk"
    listed = client.get("/api/v1/purchase-orders", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_omits_plant_label(purchase_order_http: object) -> None:
    client, _desk = purchase_order_http
    posted = client.post(
        "/api/v1/purchase-orders",
        headers=bearer_auth_headers(),
        json={"po_code": "po_no_plant", "source_ref": "tenant:manual"},
    )
    assert posted.status_code == 201
    assert posted.json()["plant_label"] is None
    assert posted.json()["source_ref"] == "tenant:manual"


def test_http_create_blank_plant_becomes_null(purchase_order_http: object) -> None:
    client, _desk = purchase_order_http
    posted = client.post(
        "/api/v1/purchase-orders",
        headers=bearer_auth_headers(),
        json=_payload(plant_label="   "),
    )
    assert posted.status_code == 201
    assert posted.json()["plant_label"] is None


def test_http_create_bad_code_is_400(purchase_order_http: object) -> None:
    client, _desk = purchase_order_http
    response = client.post(
        "/api/v1/purchase-orders",
        headers=bearer_auth_headers(),
        json=_payload(po_code="X"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_http_create_long_plant_is_400(purchase_order_http: object) -> None:
    client, _desk = purchase_order_http
    response = client.post(
        "/api/v1/purchase-orders",
        headers=bearer_auth_headers(),
        json=_payload(plant_label="x" * 129),
    )
    assert response.status_code == 400
    assert "zakład" in response.json()["detail"]


def test_http_create_foreign_origin_is_400(purchase_order_http: object) -> None:
    client, _desk = purchase_order_http
    response = client.post(
        "/api/v1/purchase-orders",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="https://vendor.example/po"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]


@pytest.mark.parametrize("line_field", _LINE_FIELDS)
def test_http_create_rejects_line_or_money_fields(
    purchase_order_http: object, line_field: str
) -> None:
    client, _desk = purchase_order_http
    response = client.post(
        "/api/v1/purchase-orders",
        headers=bearer_auth_headers(),
        json=_payload(**{line_field: "x"}),
    )
    assert response.status_code == 422
