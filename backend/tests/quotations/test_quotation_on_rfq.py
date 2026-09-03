from decimal import Decimal
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.customer_rfq import require_rfq_party
from app.domain.errors import InvalidCustomerRfq, ResourceNotFound, UnknownChargeCode
from app.main import app
from app.models.charge_code import ChargeCode
from app.models.customer_rfq import CustomerRfq
from app.models.quotation import Quotation
from app.repositories.quotations.quotation_repository import QUOTE_FROM_CURRENT_SQL
from app.services.customer_rfqs.customer_rfq_service import CustomerRfqService
from app.services.quotations.quotation_service import (
    QuotationService,
    _snapshot_integrity_error,
)
from tests.http_auth import bearer_auth_headers
from tests.quotations.test_quotation_http import AllowAllAuthz

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "029_quotation_customer_rfq.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def _catalog() -> ChargeCode:
    return ChargeCode(
        id=uuid4(),
        organization_id=uuid4(),
        code="THC",
        name="THC",
        aliases=[],
    )


def _quoted(*, customer_rfq_id=None) -> Quotation:
    return Quotation(
        id=uuid4(),
        organization_id=uuid4(),
        charge_code="THC",
        rate_line_id=uuid4(),
        amount=Decimal("10.0000"),
        currency="EUR",
        source_ref="tariff://a",
        customer_rfq_id=customer_rfq_id,
    )


def test_migration_029_links_quotation_to_rfq_and_downgrades() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "029_quotation_customer_rfq"' in source
    assert 'down_revision: str | None = "028_customer_rfq_rls"' in source
    assert "customer_rfq_id" in source
    assert "uq_customer_rfq_org_id" in source
    assert "fk_quotation_customer_rfq" in source
    assert "ix_quotation_org_customer_rfq_id" in source
    assert "FORCE ROW LEVEL SECURITY" not in source
    downgrade = source.split("def downgrade")[1]
    assert "customer_rfq_id" in downgrade
    assert "uq_customer_rfq_org_id" in downgrade


def test_quote_sql_binds_rfq_without_changing_rate_selection() -> None:
    sql = " ".join(QUOTE_FROM_CURRENT_SQL.split())
    assert ":customer_rfq_id" in sql
    assert "rl.amount" in sql
    assert "superseded_by IS NULL" in sql
    assert "rl.customer_rfq_id" not in sql
    assert "JOIN customer_rfq" not in sql


def test_require_rfq_party_rejects_missing_and_mismatch() -> None:
    party_id = uuid4()
    assert require_rfq_party(party_id, party_id) == party_id
    with pytest.raises(InvalidCustomerRfq, match="kontrahenta"):
        require_rfq_party(None, party_id)
    with pytest.raises(InvalidCustomerRfq, match="z zapytania"):
        require_rfq_party(uuid4(), party_id)


def test_rfq_fk_violation_maps_to_invalid_customer_rfq() -> None:
    mapped = _snapshot_integrity_error(
        IntegrityError("INSERT", {}, Exception("fk_quotation_customer_rfq")),
    )
    assert isinstance(mapped, InvalidCustomerRfq)


def test_quotation_model_has_composite_rfq_fk() -> None:
    names = {item.name for item in Quotation.__table_args__ if getattr(item, "name", None)}
    assert "fk_quotation_customer_rfq" in names
    assert Quotation.__table__.c["customer_rfq_id"].nullable is True


def test_quotation_service_does_not_import_rfq_or_inbound() -> None:
    source = (_SERVICES / "quotations" / "quotation_service.py").read_text(encoding="utf-8")
    assert "customer_rfqs" not in source
    assert "inbound_messages" not in source
    assert "inbound_message" not in source
    assert "from app.services.channel_quotes" not in source
    assert "from app.repositories.channel_quotes" not in source
    assert "from app.services.charges" not in source
    assert "from app.repositories.charges" not in source
    assert "from app.services.parties" not in source
    assert "from app.repositories.parties" not in source


def test_rfq_service_still_does_not_import_quotations() -> None:
    source = (_SERVICES / "customer_rfqs" / "customer_rfq_service.py").read_text(encoding="utf-8")
    assert "quotations" not in source
    assert "rate_line" not in source
    assert "amount" not in source


@pytest.mark.asyncio
async def test_quote_persists_customer_rfq_id_from_bind() -> None:
    rfq_id = uuid4()
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=_catalog())
    row = _quoted(customer_rfq_id=rfq_id)
    mappings = MagicMock()
    mappings.first.return_value = {
        "id": row.id,
        "organization_id": row.organization_id,
        "charge_code": row.charge_code,
        "rate_line_id": row.rate_line_id,
        "amount": row.amount,
        "currency": row.currency,
        "source_ref": row.source_ref,
        "created_by": None,
        "origin_port_id": None,
        "destination_port_id": None,
        "party_id": None,
        "customer_rfq_id": rfq_id,
    }
    execute_result = MagicMock()
    execute_result.mappings.return_value = mappings
    session.execute = AsyncMock(return_value=execute_result)
    service = QuotationService(session)
    quoted = await service.quote_from_current_rate(
        organization_id=uuid4(),
        user_id=uuid4(),
        charge_code="THC",
        origin_port_id=uuid4(),
        destination_port_id=uuid4(),
        party_id=uuid4(),
        customer_rfq_id=rfq_id,
    )
    assert quoted.customer_rfq_id == rfq_id
    assert quoted.amount == Decimal("10.0000")
    bound = session.execute.await_args.args[1]
    assert bound["customer_rfq_id"] == rfq_id


@pytest.mark.asyncio
async def test_get_rfq_raises_when_missing() -> None:
    session = AsyncMock()
    session.get = AsyncMock(return_value=None)
    with pytest.raises(ResourceNotFound, match="zapytanie"):
        await CustomerRfqService(session).get_rfq(uuid4())


class _StubRfq:
    def __init__(self, rfq: CustomerRfq) -> None:
        self._rfq = rfq

    async def get_rfq(self, rfq_id):
        if rfq_id != self._rfq.id:
            raise ResourceNotFound(f"nieznane zapytanie ofertowe: {rfq_id}")
        return self._rfq


class _StubQuote:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[Quotation] = []

    async def quote_from_current_rate(
        self,
        *,
        organization_id,
        user_id,
        charge_code,
        origin_port_id,
        destination_port_id,
        party_id,
        customer_rfq_id=None,
        commodity_code_id=None,
    ) -> Quotation:
        if charge_code == "LOOSE":
            raise UnknownChargeCode("nieznany kod opłaty: LOOSE")
        row = Quotation(
            id=uuid4(),
            organization_id=organization_id,
            charge_code=charge_code,
            rate_line_id=uuid4(),
            amount=Decimal("10.5000"),
            currency="EUR",
            source_ref="tariff://a",
            created_by=user_id,
            origin_port_id=origin_port_id,
            destination_port_id=destination_port_id,
            party_id=party_id,
            customer_rfq_id=customer_rfq_id,
            commodity_code_id=commodity_code_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def rfq_quote_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    party_id = uuid4()
    rfq = CustomerRfq(
        id=uuid4(),
        organization_id=uuid4(),
        inbound_message_id=uuid4(),
        source_ref="fixture://inbound-mail/s5",
        status="draft",
        party_id=party_id,
    )
    monkeypatch.setattr(
        "app.api.quotations.CustomerRfqService",
        lambda session: _StubRfq(rfq),
    )
    monkeypatch.setattr("app.api.quotations.QuotationService", _StubQuote)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = lambda: AsyncMock()
    client = TestClient(app)
    client.extra = {"rfq": rfq, "party_id": party_id}
    yield client
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_quote_from_rfq_returns_customer_rfq_id(rfq_quote_client: TestClient) -> None:
    rfq = rfq_quote_client.extra["rfq"]
    party_id = rfq_quote_client.extra["party_id"]
    response = rfq_quote_client.post(
        "/api/v1/quotations",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "origin_port_id": str(uuid4()),
            "destination_port_id": str(uuid4()),
            "party_id": str(party_id),
            "customer_rfq_id": str(rfq.id),
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["customer_rfq_id"] == str(rfq.id)
    assert body["amount"] == "10.5000"
    assert body["party_id"] == str(party_id)


def test_http_quote_from_rfq_rejects_party_mismatch(rfq_quote_client: TestClient) -> None:
    rfq = rfq_quote_client.extra["rfq"]
    response = rfq_quote_client.post(
        "/api/v1/quotations",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "origin_port_id": str(uuid4()),
            "destination_port_id": str(uuid4()),
            "party_id": str(uuid4()),
            "customer_rfq_id": str(rfq.id),
        },
    )
    assert response.status_code == 400
    assert "z zapytania" in response.json()["detail"]


def test_http_quote_from_unknown_rfq_is_404(rfq_quote_client: TestClient) -> None:
    party_id = rfq_quote_client.extra["party_id"]
    response = rfq_quote_client.post(
        "/api/v1/quotations",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "origin_port_id": str(uuid4()),
            "destination_port_id": str(uuid4()),
            "party_id": str(party_id),
            "customer_rfq_id": str(uuid4()),
        },
    )
    assert response.status_code == 404


def test_generated_api_types_include_customer_rfq_on_quotation() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "customer_rfq_id" in source
