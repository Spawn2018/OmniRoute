from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.document_checklist_rule import (
    require_blocks_dispatch,
    require_checklist_document_kind,
    require_checklist_incoterm,
    require_checklist_mode,
    require_checklist_trade_side,
)
from app.main import app
from app.models.document_checklist_rule import DocumentChecklistRule
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


class StubDocumentChecklistRuleService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[DocumentChecklistRule] = []

    async def list_for_triple(
        self,
        *,
        incoterm: object,
        trade_side: object,
        mode: object,
    ) -> list[DocumentChecklistRule]:
        rule = require_checklist_incoterm(incoterm)
        side = require_checklist_trade_side(trade_side)
        lane = require_checklist_mode(mode)
        return [
            row
            for row in self.rows
            if str(row.incoterm).strip() == rule
            and row.trade_side == side
            and row.mode == lane
        ]

    async def record_rule(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        incoterm: object,
        trade_side: object,
        mode: object,
        document_kind: object,
        blocks_dispatch: object,
    ) -> DocumentChecklistRule:
        row = DocumentChecklistRule(
            id=uuid4(),
            organization_id=organization_id,
            incoterm=require_checklist_incoterm(incoterm),
            trade_side=require_checklist_trade_side(trade_side),
            mode=require_checklist_mode(mode),
            document_kind=require_checklist_document_kind(document_kind),
            blocks_dispatch=require_blocks_dispatch(blocks_dispatch),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    rules = StubDocumentChecklistRuleService(object())

    def _rows(_session: object) -> StubDocumentChecklistRuleService:
        return rules

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.document_checklist_rules.DocumentChecklistRuleService",
        _rows,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), rules
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_checklist_blocks_dispatch_and_get_by_triple(
    catalog_client: object,
) -> None:
    client, _rules = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/document-checklist-rules",
        headers=headers,
        json={
            "incoterm": "FOB",
            "trade_side": "export",
            "mode": "ocean",
            "document_kind": "bill_of_lading",
            "blocks_dispatch": True,
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["blocks_dispatch"] is True
    assert "amount" not in body
    listed = client.get(
        "/api/v1/document-checklist-rules",
        headers=headers,
        params={"incoterm": "FOB", "trade_side": "export", "mode": "ocean"},
    )
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]
    miss = client.get(
        "/api/v1/document-checklist-rules",
        headers=headers,
        params={"incoterm": "FOB", "trade_side": "export", "mode": "road"},
    )
    assert miss.json() == []


def test_http_checklist_unknown_kind_is_400(catalog_client: object) -> None:
    client, _rules = catalog_client
    response = client.post(
        "/api/v1/document-checklist-rules",
        headers=bearer_auth_headers(),
        json={
            "incoterm": "FOB",
            "trade_side": "export",
            "mode": "ocean",
            "document_kind": "noted",
            "blocks_dispatch": False,
        },
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]
