from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.document_dispatch_rule import (
    require_dispatch_document_kind,
    require_dispatch_incoterm,
    require_dispatch_source_ref,
    require_dispatch_trade_side,
    require_recipient_role,
)
from app.main import app
from app.models.document_dispatch_rule import DocumentDispatchRule
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


class StubDocumentDispatchRuleService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[DocumentDispatchRule] = []

    async def list_for_pair(
        self,
        *,
        incoterm: object,
        trade_side: object,
        document_kind: object = None,
    ) -> list[DocumentDispatchRule]:
        code = require_dispatch_incoterm(incoterm)
        side = require_dispatch_trade_side(trade_side)
        kind = None if document_kind is None else require_dispatch_document_kind(document_kind)
        return [
            row
            for row in self.rows
            if str(row.incoterm).strip() == code
            and row.trade_side == side
            and row.superseded_by is None
            and (kind is None or row.document_kind == kind)
        ]

    async def record_rule(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        incoterm: object,
        trade_side: object,
        document_kind: object,
        recipient_role: object,
        source_ref: object,
    ) -> DocumentDispatchRule:
        code = require_dispatch_incoterm(incoterm)
        side = require_dispatch_trade_side(trade_side)
        kind = require_dispatch_document_kind(document_kind)
        role = require_recipient_role(recipient_role)
        origin = require_dispatch_source_ref(source_ref)
        current = next(
            (
                row
                for row in self.rows
                if str(row.incoterm).strip() == code
                and row.trade_side == side
                and row.document_kind == kind
                and row.superseded_by is None
            ),
            None,
        )
        if current is not None and current.recipient_role == role and current.source_ref == origin:
            return current
        successor = DocumentDispatchRule(
            id=uuid4(),
            organization_id=organization_id,
            incoterm=code,
            trade_side=side,
            document_kind=kind,
            recipient_role=role,
            source_ref=origin,
            created_by=user_id,
        )
        if current is not None:
            current.superseded_by = successor.id
        self.rows.append(successor)
        return successor


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    rules = StubDocumentDispatchRuleService(object())

    def _rows(_session: object) -> StubDocumentDispatchRuleService:
        return rules

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.document_dispatch_rules.DocumentDispatchRuleService",
        _rows,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), rules
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_dispatch_rule_and_get_by_pair(catalog_client: object) -> None:
    client, _rules = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/document-dispatch-rules",
        headers=headers,
        json={
            "incoterm": "DAP",
            "trade_side": "import",
            "document_kind": "commercial_invoice",
            "recipient_role": "omni_customs",
            "source_ref": "tenant:manual",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["recipient_role"] == "omni_customs"
    assert "amount" not in body
    listed = client.get(
        "/api/v1/document-dispatch-rules",
        headers=headers,
        params={"incoterm": "DAP", "trade_side": "import"},
    )
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]
    filtered = client.get(
        "/api/v1/document-dispatch-rules",
        headers=headers,
        params={
            "incoterm": "DAP",
            "trade_side": "import",
            "document_kind": "packing_list",
        },
    )
    assert filtered.json() == []


def test_http_override_supersedes_and_rejects_noted_or_sold_to(
    catalog_client: object,
) -> None:
    client, _rules = catalog_client
    headers = bearer_auth_headers()
    payload = {
        "incoterm": "DAP",
        "trade_side": "import",
        "document_kind": "commercial_invoice",
        "recipient_role": "omni_customs",
        "source_ref": "tenant:manual",
    }
    first = client.post("/api/v1/document-dispatch-rules", headers=headers, json=payload)
    first_id = first.json()["id"]
    second = client.post(
        "/api/v1/document-dispatch-rules",
        headers=headers,
        json={**payload, "recipient_role": "client_customs"},
    )
    assert second.status_code == 201
    assert second.json()["id"] != first_id
    listed = client.get(
        "/api/v1/document-dispatch-rules",
        headers=headers,
        params={"incoterm": "DAP", "trade_side": "import"},
    )
    assert listed.json()[0]["id"] == second.json()["id"]
    noted = client.post(
        "/api/v1/document-dispatch-rules",
        headers=headers,
        json={**payload, "document_kind": "noted"},
    )
    assert noted.status_code == 400
    assert "rodzaj" in noted.json()["detail"]
    sold = client.post(
        "/api/v1/document-dispatch-rules",
        headers=headers,
        json={**payload, "recipient_role": "sold_to"},
    )
    assert sold.status_code == 400
    assert "adresata" in sold.json()["detail"]
