from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.api.deps import require_tenant_session, set_authz_checker
from app.core.database import bind_tenant
from app.domain.errors import MissingQuotationPrefix, ResourceNotFound
from app.domain.quotation import (
    format_quotation_document_number,
    require_document_number_prefix,
)
from app.main import app
from app.models.quotation import Quotation
from app.models.rate_line import RateLine
from app.repositories.quotations.quotation_repository import ISSUE_DOCUMENT_NUMBER_SQL
from app.services.quotations.quotation_service import QuotationService
from tests.http_auth import bearer_auth_headers
from tests.quotations.test_quotation_http import AllowAllAuthz, DenyAllAuthz, StubQuotationService

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "032_quotation_document_number.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def _quote(*, document_number: str | None = None) -> Quotation:
    return Quotation(
        id=uuid4(),
        organization_id=uuid4(),
        charge_code="THC",
        rate_line_id=uuid4(),
        amount=Decimal("10.0000"),
        currency="EUR",
        source_ref="tariff://a",
        document_number=document_number,
    )


def test_migration_032_adds_document_number_without_new_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "032_quotation_document_number"' in source
    assert 'down_revision: str | None = "031_commodity_on_rfq"' in source
    assert "document_number" in source
    assert "uq_quotation_org_document_number" in source
    assert "FORCE ROW LEVEL SECURITY" not in source
    downgrade = source.split("def downgrade")[1]
    assert "document_number" in downgrade


def test_quote_service_does_not_read_settings_keys() -> None:
    source = (_SERVICES / "quotations" / "quotation_service.py").read_text(encoding="utf-8")
    assert "organization_settings" not in source
    assert "quotation_number_prefix" not in source
    assert "quotation_print_template" not in source


def test_settings_service_still_does_not_import_quotations() -> None:
    source = (
        _SERVICES / "organization_settings" / "organization_setting_service.py"
    ).read_text(encoding="utf-8")
    assert "quotations" not in source


def test_prefix_required_and_format_is_prefix_plus_four_digits() -> None:
    assert require_document_number_prefix(" OR-Q. ") == "OR-Q."
    assert format_quotation_document_number("OR-Q.", 1) == "OR-Q.0001"
    assert format_quotation_document_number("OR-Q.", 12) == "OR-Q.0012"
    with pytest.raises(MissingQuotationPrefix, match="prefiksu"):
        require_document_number_prefix(None)
    with pytest.raises(MissingQuotationPrefix, match="prefiksu"):
        require_document_number_prefix("  ")


def test_issue_sql_counts_in_postgres_after_prefix() -> None:
    sql = " ".join(ISSUE_DOCUMENT_NUMBER_SQL.split())
    assert "MAX(" in sql
    assert "LENGTH(:prefix)" in sql
    assert "LPAD(" in sql
    assert "document_number IS NULL" in sql


@pytest.mark.asyncio
async def test_issue_returns_existing_number_without_rewrite() -> None:
    current = _quote(document_number="OR-Q.0001")
    session = AsyncMock()
    service = QuotationService(session)
    service._quotations.get = AsyncMock(return_value=current)
    service._quotations.issue_document_number = AsyncMock()
    issued = await service.issue_document_number(quotation_id=current.id, prefix="OR-Q.")
    assert issued.document_number == "OR-Q.0001"
    service._quotations.issue_document_number.assert_not_awaited()


@pytest.mark.asyncio
async def test_issue_unknown_quote_is_not_found() -> None:
    session = AsyncMock()
    service = QuotationService(session)
    service._quotations.get = AsyncMock(return_value=None)
    with pytest.raises(ResourceNotFound, match="wycena"):
        await service.issue_document_number(quotation_id=uuid4(), prefix="OR-Q.")


@pytest.mark.asyncio
async def test_issue_without_prefix_is_rejected() -> None:
    session = AsyncMock()
    service = QuotationService(session)
    with pytest.raises(MissingQuotationPrefix):
        await service.issue_document_number(quotation_id=uuid4(), prefix=None)


class StubSettingsService:
    def __init__(self, session: object) -> None:
        self.prefix = "OR-Q."
        self.template = "letter"

    async def get_setting(self, setting_key: str) -> SimpleNamespace | None:
        if setting_key == "quotation_number_prefix":
            return SimpleNamespace(setting_value=self.prefix)
        if setting_key == "quotation_print_template":
            return SimpleNamespace(setting_value=self.template)
        return None


@pytest.fixture
def document_number_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubQuotationService(object())

    def _quotes(session: object) -> StubQuotationService:
        return stub

    def _settings(session: object) -> StubSettingsService:
        return StubSettingsService(session)

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    async def _issue(
        self: StubQuotationService,
        *,
        quotation_id,
        prefix,
    ) -> Quotation:
        token = require_document_number_prefix(prefix)
        for row in self.rows:
            if row.id == quotation_id:
                if row.document_number is None:
                    row.document_number = format_quotation_document_number(token, 1)
                return row
        raise ResourceNotFound("nieznana wycena")

    stub.issue_document_number = _issue.__get__(stub, StubQuotationService)
    monkeypatch.setattr("app.api.quotations.QuotationService", _quotes)
    monkeypatch.setattr("app.api.quotations.OrganizationSettingService", _settings)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_document_layout_and_issue(document_number_client: TestClient) -> None:
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = document_number_client.post(
        "/api/v1/quotations",
        headers=headers,
        json={
            "charge_code": "THC",
            "origin_port_id": str(uuid4()),
            "destination_port_id": str(uuid4()),
            "party_id": str(uuid4()),
        },
    )
    assert created.status_code == 201
    assert created.json()["document_number"] is None
    quote_id = created.json()["id"]
    amount = created.json()["amount"]

    layout = document_number_client.get("/api/v1/quotations/document-layout", headers=headers)
    assert layout.status_code == 200
    assert layout.json() == {"prefix": "OR-Q.", "print_template": "letter"}

    issued = document_number_client.post(
        f"/api/v1/quotations/{quote_id}/document-number",
        headers=headers,
    )
    assert issued.status_code == 200
    assert issued.json()["document_number"] == "OR-Q.0001"
    assert issued.json()["amount"] == amount

    again = document_number_client.post(
        f"/api/v1/quotations/{quote_id}/document-number",
        headers=headers,
    )
    assert again.json()["document_number"] == "OR-Q.0001"


def test_http_document_number_forbidden_without_permission() -> None:
    set_authz_checker(DenyAllAuthz())
    client = TestClient(app)
    response = client.post(
        f"/api/v1/quotations/{uuid4()}/document-number",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 403
    set_authz_checker(None)


def _buy_rate(*, organization_id, created_by, source_ref: str) -> RateLine:
    return RateLine(
        id=uuid4(),
        organization_id=organization_id,
        charge_code="THC",
        amount=Decimal("10.0000"),
        currency="EUR",
        source_ref=source_ref,
        created_by=created_by,
    )


def _stored_quote(*, organization_id, created_by, rate_line_id, source_ref: str) -> Quotation:
    return Quotation(
        id=uuid4(),
        organization_id=organization_id,
        charge_code="THC",
        rate_line_id=rate_line_id,
        amount=Decimal("10.0000"),
        currency="EUR",
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_document_number_isolates_tenants_and_allows_same_text(
    session,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    rate_a = _buy_rate(organization_id=org_a.id, created_by=user_a.id, source_ref="tariff://a")
    session.add(rate_a)
    await session.flush()
    quote_a = _stored_quote(
        organization_id=org_a.id,
        created_by=user_a.id,
        rate_line_id=rate_a.id,
        source_ref="tariff://a",
    )
    extra_a = _stored_quote(
        organization_id=org_a.id,
        created_by=user_a.id,
        rate_line_id=rate_a.id,
        source_ref="tariff://a2",
    )
    session.add_all([quote_a, extra_a])
    await session.flush()

    service_a = QuotationService(session)
    first = await service_a.issue_document_number(quotation_id=quote_a.id, prefix="OR-Q.")
    assert first.document_number == "OR-Q.0001"
    assert first.amount == Decimal("10.0000")
    repeat = await service_a.issue_document_number(quotation_id=quote_a.id, prefix="OR-Q.")
    assert repeat.document_number == "OR-Q.0001"
    second = await service_a.issue_document_number(quotation_id=extra_a.id, prefix="OR-Q.")
    assert second.document_number == "OR-Q.0002"
    await session.flush()
    session.expunge_all()

    await bind_tenant(session, org_b.id)
    rate_b = _buy_rate(organization_id=org_b.id, created_by=user_b.id, source_ref="tariff://b")
    session.add(rate_b)
    await session.flush()
    quote_b = _stored_quote(
        organization_id=org_b.id,
        created_by=user_b.id,
        rate_line_id=rate_b.id,
        source_ref="tariff://b",
    )
    session.add(quote_b)
    await session.flush()
    issued_b = await QuotationService(session).issue_document_number(
        quotation_id=quote_b.id,
        prefix="OR-Q.",
    )
    assert issued_b.document_number == "OR-Q.0001"

    with pytest.raises(ResourceNotFound):
        await QuotationService(session).issue_document_number(
            quotation_id=quote_a.id,
            prefix="OR-Q.",
        )
    hidden = await session.scalar(select(Quotation).where(Quotation.id == quote_a.id))
    assert hidden is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_document_number_unique_per_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    rate = _buy_rate(organization_id=org_a.id, created_by=user_a.id, source_ref="tariff://u")
    session.add(rate)
    await session.flush()
    first = _stored_quote(
        organization_id=org_a.id,
        created_by=user_a.id,
        rate_line_id=rate.id,
        source_ref="tariff://u1",
    )
    first.document_number = "OR-Q.0001"
    clash = _stored_quote(
        organization_id=org_a.id,
        created_by=user_a.id,
        rate_line_id=rate.id,
        source_ref="tariff://u2",
    )
    clash.document_number = "OR-Q.0001"
    session.add(first)
    await session.flush()
    session.add(clash)
    with pytest.raises(IntegrityError):
        await session.flush()
