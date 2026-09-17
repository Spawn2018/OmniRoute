from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.product_ticket import parse_product_ticket_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.product_ticket import ProductTicket
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]


def test_migration_426_creates_product_ticket_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/426_product_ticket.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "426_product_ticket"' in source
    assert 'down_revision: str | None = "425_od_margin_floor"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "product_ticket_tenant_isolation" in source
    for banned in ("amount", "float(", "httpx", "auto_fix", "capa"):
        assert banned not in source


def test_importlinter_lists_product_ticket_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.product_tickets" in forbidden
    assert "app.models.product_ticket" in forbidden


def test_fga_source_declares_product_ticket_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_product_tickets: member" in source


def test_authorization_model_grants_product_tickets_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_product_tickets"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class ProductTicketAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryProductTicketDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[ProductTicket] = []

    async def list_tickets(self) -> list[ProductTicket]:
        return list(self.rows)

    async def persist_product_ticket(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        ticket_code: object,
        title: object,
        body: object,
        ticket_kind: object,
        source_ref: object,
    ) -> ProductTicket:
        code, heading, text, kind, origin = parse_product_ticket_row(
            ticket_code,
            title,
            body,
            ticket_kind,
            source_ref,
        )
        row = ProductTicket(
            id=uuid4(),
            organization_id=organization_id,
            ticket_code=code,
            title=heading,
            body=text,
            ticket_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def product_ticket_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    desk = InMemoryProductTicketDesk(object())

    def _factory(session: object) -> InMemoryProductTicketDesk:
        return desk

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.product_tickets.ProductTicketService",
        _factory,
    )
    set_authz_checker(ProductTicketAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    client = TestClient(app)
    client.desk = desk  # type: ignore[attr-defined]
    yield client
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_creates_product_ticket(product_ticket_client: TestClient) -> None:
    response = product_ticket_client.post(
        "/api/v1/product-tickets",
        headers=bearer_auth_headers(),
        json={
            "ticket_code": "bug_login_01",
            "title": "Login stuck",
            "body": "Operator cannot enter after refresh",
            "ticket_kind": "report",
            "source_ref": "tenant:manual",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["ticket_code"] == "bug_login_01"
    assert body["ticket_kind"] == "report"
    assert body["title"] == "Login stuck"


def test_http_rejects_blank_title(product_ticket_client: TestClient) -> None:
    response = product_ticket_client.post(
        "/api/v1/product-tickets",
        headers=bearer_auth_headers(),
        json={
            "ticket_code": "bug_login_01",
            "title": "   ",
            "body": "Operator cannot enter after refresh",
            "ticket_kind": "report",
            "source_ref": "tenant:manual",
        },
    )
    assert response.status_code == 400
    assert "tytuł" in response.json()["detail"]


def test_http_rejects_unknown_kind(product_ticket_client: TestClient) -> None:
    response = product_ticket_client.post(
        "/api/v1/product-tickets",
        headers=bearer_auth_headers(),
        json={
            "ticket_code": "bug_login_01",
            "title": "Login stuck",
            "body": "Operator cannot enter after refresh",
            "ticket_kind": "closed",
            "source_ref": "tenant:manual",
        },
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_http_lists_product_tickets(product_ticket_client: TestClient) -> None:
    desk: InMemoryProductTicketDesk = product_ticket_client.desk  # type: ignore[attr-defined]
    desk.rows.append(
        ProductTicket(
            id=uuid4(),
            organization_id=uuid4(),
            ticket_code="bug_a",
            title="A",
            body="Body A",
            ticket_kind="report",
            source_ref="fixture://product-ticket/a",
            created_by=uuid4(),
        ),
    )
    response = product_ticket_client.get(
        "/api/v1/product-tickets",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
