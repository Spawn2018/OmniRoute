from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.customer_contract import (
    require_contract_code,
    require_contract_source_ref,
    require_shipper_label,
    require_their_customer_label,
)
from app.main import app
from app.models.customer_contract import CustomerContract
from tests.http_auth import bearer_auth_headers

_BODY_KEYS = ("body", "blob_ciphertext", "wrapped_dek", "plaintext")


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


class StubContractDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[CustomerContract] = []

    async def list_rows(self) -> list[CustomerContract]:
        return list(self.rows)

    async def persist_customer_contract(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        contract_code: object,
        shipper_label: object,
        their_customer_label: object,
        source_ref: object,
    ) -> CustomerContract:
        row = CustomerContract(
            id=uuid4(),
            organization_id=organization_id,
            contract_code=require_contract_code(contract_code),
            shipper_label=require_shipper_label(shipper_label),
            their_customer_label=require_their_customer_label(their_customer_label),
            source_ref=require_contract_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = StubContractDesk(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.customer_contracts.CustomerContractService",
        lambda _s: desk,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "contract_code": "acme_pl_2026",
        "shipper_label": "Acme Logistics",
        "their_customer_label": "Bayer PL",
        "source_ref": "fixture://contract/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_customer_contract(catalog_client: object) -> None:
    client, _desk = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/customer-contracts", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["contract_code"] == "acme_pl_2026"
    assert body["shipper_label"] == "Acme Logistics"
    assert body["their_customer_label"] == "Bayer PL"
    assert "buy_amount" not in body
    assert "margin" not in body
    for hidden in _BODY_KEYS:
        assert hidden not in body
    listed = client.get("/api/v1/customer-contracts", headers=headers)
    assert listed.status_code == 200
    listed_row = listed.json()[0]
    assert listed_row["id"] == body["id"]
    for hidden in _BODY_KEYS:
        assert hidden not in listed_row


def test_http_create_bad_code_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/customer-contracts",
        headers=bearer_auth_headers(),
        json=_payload(contract_code="X"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_http_create_bad_shipper_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/customer-contracts",
        headers=bearer_auth_headers(),
        json=_payload(shipper_label=""),
    )
    assert response.status_code == 400
    assert "załadowca" in response.json()["detail"]


def test_http_create_bad_customer_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/customer-contracts",
        headers=bearer_auth_headers(),
        json=_payload(their_customer_label=""),
    )
    assert response.status_code == 400
    assert "odbiorca" in response.json()["detail"]


def test_http_create_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/customer-contracts",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="https://contracts.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]


@pytest.mark.parametrize("secret_field", list(_BODY_KEYS))
def test_http_create_rejects_contract_body_fields(
    catalog_client: object,
    secret_field: str,
) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/customer-contracts",
        headers=bearer_auth_headers(),
        json=_payload(**{secret_field: "x"}),
    )
    assert response.status_code == 422
