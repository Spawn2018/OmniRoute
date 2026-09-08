from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.charge_template import (
    require_member_code,
    require_template_code,
    require_template_source_ref,
    require_validity_window,
)
from app.domain.errors import InvalidChargeTemplate
from app.main import app
from app.models.charge_template import ChargeTemplate
from tests.http_auth import bearer_auth_headers

_KNOWN = frozenset({"THC"})


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


class StubChargeTemplateService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[ChargeTemplate] = []

    async def list_templates(self) -> list[ChargeTemplate]:
        return list(self.rows)

    async def record_template(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        template_code: str,
        charge_code: str,
        valid_from: str,
        valid_until: str,
        source_ref: str,
    ) -> ChargeTemplate:
        token = require_member_code(charge_code)
        if token not in _KNOWN:
            raise InvalidChargeTemplate("nieznany kod opłaty")
        start, end = require_validity_window(valid_from, valid_until)
        row = ChargeTemplate(
            id=uuid4(),
            organization_id=organization_id,
            template_code=require_template_code(template_code),
            charge_code=token,
            valid_from=start,
            valid_until=end,
            source_ref=require_template_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    rows = StubChargeTemplateService(object())

    def _rows(_session: object) -> StubChargeTemplateService:
        return rows

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.charge_templates.ChargeTemplateService", _rows)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), rows
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "template_code": "spot_thc",
        "charge_code": "THC",
        "valid_from": "2026-01-01",
        "valid_until": "2026-12-31",
        "source_ref": "fixture://charge-template/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_charge_template(catalog_client: object) -> None:
    client, _rows = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/charge-templates", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["template_code"] == "spot_thc"
    assert body["charge_code"] == "THC"
    assert body["valid_from"] == "2026-01-01"
    assert "amount" not in body
    assert "buy_amount" not in body
    listed = client.get("/api/v1/charge-templates", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_template_bad_code_is_400(catalog_client: object) -> None:
    client, _rows = catalog_client
    response = client.post(
        "/api/v1/charge-templates",
        headers=bearer_auth_headers(),
        json=_payload(template_code="X"),
    )
    assert response.status_code == 400
    assert "szablon" in response.json()["detail"]


def test_http_create_template_unknown_charge_code_is_400(catalog_client: object) -> None:
    client, _rows = catalog_client
    response = client.post(
        "/api/v1/charge-templates",
        headers=bearer_auth_headers(),
        json=_payload(charge_code="XXXX"),
    )
    assert response.status_code == 400
    assert "kod" in response.json()["detail"]


def test_http_create_template_inverted_dates_is_400(catalog_client: object) -> None:
    client, _rows = catalog_client
    response = client.post(
        "/api/v1/charge-templates",
        headers=bearer_auth_headers(),
        json=_payload(valid_from="2026-12-31", valid_until="2026-01-01"),
    )
    assert response.status_code == 400
    assert "ważność" in response.json()["detail"]


def test_http_create_template_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _rows = catalog_client
    response = client.post(
        "/api/v1/charge-templates",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
