from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.po_line import parse_po_line_row
from app.main import app
from app.models.po_line import PoLine
from tests.http_auth import bearer_auth_headers

_MONEY_FIELDS = ("asn", "shipment_id", "amount", "currency", "buy_amount")


class PermitPoLineAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryPoLineDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.lines: list[PoLine] = []
        self.known_headers: set[UUID] = set()

    async def list_lines(self) -> list[PoLine]:
        return list(self.lines)

    async def persist_po_line(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        purchase_order_id: object,
        line_code: object,
        sku_code: object,
        qty: object,
        uom_code: object,
        plant_label: object,
        batch_label: object,
        serial_label: object,
        coo_label: object,
        source_ref: object,
    ) -> PoLine:
        packed = parse_po_line_row(
            purchase_order_id=purchase_order_id,
            line_code=line_code,
            sku_code=sku_code,
            qty=qty,
            uom_code=uom_code,
            plant_label=plant_label,
            batch_label=batch_label,
            serial_label=serial_label,
            coo_label=coo_label,
            source_ref=source_ref,
        )
        header = packed[0]
        if header not in self.known_headers:
            raise ResourceNotFound("nieznane zamówienie")
        row = PoLine(
            id=uuid4(),
            organization_id=organization_id,
            purchase_order_id=header,
            line_code=packed[1],
            sku_code=packed[2],
            qty=packed[3],
            uom_code=packed[4],
            plant_label=packed[5],
            batch_label=packed[6],
            serial_label=packed[7],
            coo_label=packed[8],
            source_ref=packed[9],
            created_by=user_id,
        )
        self.lines.append(row)
        return row


@pytest.fixture
def po_line_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryPoLineDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr("app.api.po_lines.PoLineService", lambda _s: desk)
    set_authz_checker(PermitPoLineAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(header: UUID, **extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "purchase_order_id": str(header),
        "line_code": "line_01",
        "sku_code": "SKU-4401",
        "qty": "12.5",
        "uom_code": "pcs",
        "plant_label": "Gdańsk",
        "batch_label": "B-1",
        "serial_label": "S-9",
        "coo_label": "PL",
        "source_ref": "fixture://po-line/pl-1",
    }
    body.update(extra)
    return body


def test_http_create_and_list_po_line(po_line_http: object) -> None:
    client, desk = po_line_http
    header = uuid4()
    desk.known_headers.add(header)
    org_id = uuid4()
    created = client.post(
        "/api/v1/po-lines",
        headers=bearer_auth_headers(organization_id=org_id),
        json=_payload(header),
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["purchase_order_id"] == str(header)
    assert body["line_code"] == "line_01"
    assert body["sku_code"] == "SKU-4401"
    assert body["qty"] == "12.5000"
    assert body["uom_code"] == "pcs"
    assert "amount" not in body
    listed = client.get("/api/v1/po-lines", headers=bearer_auth_headers(organization_id=org_id))
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_unknown_header_is_404(po_line_http: object) -> None:
    client, _desk = po_line_http
    response = client.post(
        "/api/v1/po-lines",
        headers=bearer_auth_headers(),
        json=_payload(uuid4()),
    )
    assert response.status_code == 404
    assert "nieznane zamówienie" in response.json()["detail"]


def test_http_create_bad_line_code_is_400(po_line_http: object) -> None:
    client, desk = po_line_http
    header = uuid4()
    desk.known_headers.add(header)
    response = client.post(
        "/api/v1/po-lines",
        headers=bearer_auth_headers(),
        json=_payload(header, line_code="X"),
    )
    assert response.status_code == 400
    assert "linia" in response.json()["detail"]


def test_http_create_float_qty_is_400(po_line_http: object) -> None:
    client, desk = po_line_http
    header = uuid4()
    desk.known_headers.add(header)
    response = client.post(
        "/api/v1/po-lines",
        headers=bearer_auth_headers(),
        json=_payload(header, qty=1.5),
    )
    assert response.status_code == 400
    assert "ilość" in response.json()["detail"]


def test_http_create_foreign_origin_is_400(po_line_http: object) -> None:
    client, desk = po_line_http
    header = uuid4()
    desk.known_headers.add(header)
    response = client.post(
        "/api/v1/po-lines",
        headers=bearer_auth_headers(),
        json=_payload(header, source_ref="https://vendor.example/asn"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]


@pytest.mark.parametrize("money_field", _MONEY_FIELDS)
def test_http_create_rejects_asn_or_money_fields(
    po_line_http: object, money_field: str
) -> None:
    client, desk = po_line_http
    header = uuid4()
    desk.known_headers.add(header)
    response = client.post(
        "/api/v1/po-lines",
        headers=bearer_auth_headers(),
        json=_payload(header, **{money_field: "x"}),
    )
    assert response.status_code == 422
