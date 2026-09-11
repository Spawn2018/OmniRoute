from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.asn import parse_asn_row
from app.domain.errors import ResourceNotFound
from app.main import app
from app.models.asn import Asn
from tests.http_auth import bearer_auth_headers

_FORBIDDEN_FIELDS = ("shipment_id", "edi", "amount", "currency", "buy_amount", "payload")


class PermitAsnAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryAsnDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.notices: list[Asn] = []
        self.known_headers: set[UUID] = set()

    async def list_notices(self) -> list[Asn]:
        return list(self.notices)

    async def persist_asn(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        purchase_order_id: object,
        asn_code: object,
        plant_label: object,
        carrier_label: object,
        ship_ref_label: object,
        source_ref: object,
    ) -> Asn:
        packed = parse_asn_row(
            purchase_order_id=purchase_order_id,
            asn_code=asn_code,
            plant_label=plant_label,
            carrier_label=carrier_label,
            ship_ref_label=ship_ref_label,
            source_ref=source_ref,
        )
        header = packed[0]
        if header not in self.known_headers:
            raise ResourceNotFound("nieznane zamówienie")
        row = Asn(
            id=uuid4(),
            organization_id=organization_id,
            purchase_order_id=header,
            asn_code=packed[1],
            plant_label=packed[2],
            carrier_label=packed[3],
            ship_ref_label=packed[4],
            source_ref=packed[5],
            created_by=user_id,
        )
        self.notices.append(row)
        return row


@pytest.fixture
def asn_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryAsnDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr("app.api.asns.AsnService", lambda _s: desk)
    set_authz_checker(PermitAsnAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(header: UUID, **extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "purchase_order_id": str(header),
        "asn_code": "asn_01",
        "plant_label": "Gdańsk",
        "carrier_label": "DB Schenker",
        "ship_ref_label": "REF-9",
        "source_ref": "fixture://asn/pl-1",
    }
    body.update(extra)
    return body


def test_http_lists_and_creates_asn(asn_http: object) -> None:
    client, desk = asn_http
    header = uuid4()
    desk.known_headers.add(header)
    created = client.post(
        "/api/v1/asns",
        headers=bearer_auth_headers(),
        json=_payload(header),
    )
    assert created.status_code == 201
    body = created.json()
    assert body["asn_code"] == "asn_01"
    assert body["purchase_order_id"] == str(header)
    assert body["plant_label"] == "Gdańsk"
    listed = client.get("/api/v1/asns", headers=bearer_auth_headers())
    assert listed.status_code == 200
    assert len(listed.json()) == 1


def test_http_rejects_bad_asn_code(asn_http: object) -> None:
    client, desk = asn_http
    header = uuid4()
    desk.known_headers.add(header)
    response = client.post(
        "/api/v1/asns",
        headers=bearer_auth_headers(),
        json=_payload(header, asn_code="X"),
    )
    assert response.status_code == 400
    assert "awizo" in response.json()["detail"]


def test_http_rejects_unknown_header(asn_http: object) -> None:
    client, _desk = asn_http
    response = client.post(
        "/api/v1/asns",
        headers=bearer_auth_headers(),
        json=_payload(uuid4()),
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "nieznane zamówienie"


@pytest.mark.parametrize("field", _FORBIDDEN_FIELDS)
def test_http_forbids_shipment_and_money_fields(asn_http: object, field: str) -> None:
    client, desk = asn_http
    header = uuid4()
    desk.known_headers.add(header)
    body = _payload(header)
    body[field] = "x" if field != "amount" else "1"
    response = client.post(
        "/api/v1/asns",
        headers=bearer_auth_headers(),
        json=body,
    )
    assert response.status_code == 422
