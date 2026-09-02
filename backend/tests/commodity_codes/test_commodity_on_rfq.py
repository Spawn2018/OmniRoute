from decimal import Decimal
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.customer_rfq import inherit_rfq_commodity_code_id
from app.domain.errors import ResourceNotFound, UnknownChargeCode, UnknownCommodityCode
from app.main import app
from app.models.charge_code import ChargeCode
from app.models.commodity_code import CommodityCode
from app.models.customer_rfq import CustomerRfq
from app.models.quotation import Quotation
from app.repositories.quotations.quotation_repository import QUOTE_FROM_CURRENT_SQL
from app.services.commodity_codes.commodity_code_service import CommodityCodeService
from app.services.quotations.quotation_service import (
    QuotationService,
    _snapshot_integrity_error,
)
from tests.http_auth import bearer_auth_headers
from tests.quotations.test_quotation_http import AllowAllAuthz

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "031_commodity_on_rfq.py"
_SERVICES = _ROOT / "backend" / "app" / "services"
_EXTRACT = _SERVICES / "extraction"


def test_migration_031_links_hs_and_downgrades() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "031_commodity_on_rfq"' in source
    assert 'down_revision: str | None = "030_port_surcharge_when"' in source
    assert "uq_commodity_code_org_id" in source
    assert "fk_customer_rfq_commodity_code" in source
    assert "fk_quotation_commodity_code" in source
    assert "create_table" not in source
    assert "FORCE ROW LEVEL SECURITY" not in source
    downgrade = source.split("def downgrade")[1]
    assert "commodity_code_id" in downgrade
    assert "uq_commodity_code_org_id" in downgrade


def test_quote_sql_binds_hs_without_changing_rate_selection() -> None:
    sql = " ".join(QUOTE_FROM_CURRENT_SQL.split())
    assert ":commodity_code_id" in sql
    assert "rl.amount" in sql
    assert "superseded_by IS NULL" in sql
    assert "rl.commodity_code_id" not in sql
    assert "JOIN commodity_code" not in sql


def test_inherit_prefers_selected_over_rfq() -> None:
    selected = uuid4()
    from_rfq = uuid4()
    assert inherit_rfq_commodity_code_id(selected, from_rfq) == selected
    assert inherit_rfq_commodity_code_id(None, from_rfq) == from_rfq
    assert inherit_rfq_commodity_code_id(None, None) is None


def test_hs_fk_violation_maps_to_unknown_commodity() -> None:
    mapped = _snapshot_integrity_error(
        IntegrityError("INSERT", {}, Exception("fk_quotation_commodity_code")),
    )
    assert isinstance(mapped, UnknownCommodityCode)


def test_catalog_service_does_not_write_rfq_or_quote() -> None:
    source = (_SERVICES / "commodity_codes" / "commodity_code_service.py").read_text(
        encoding="utf-8",
    )
    assert "customer_rfq" not in source
    assert "quotation" not in source
    assert "app.services.charges" not in source


def test_rfq_and_quote_services_do_not_import_catalog() -> None:
    rfq = (_SERVICES / "customer_rfqs" / "customer_rfq_service.py").read_text(
        encoding="utf-8",
    )
    quote = (_SERVICES / "quotations" / "quotation_service.py").read_text(encoding="utf-8")
    assert "commodity_codes" not in rfq
    assert "commodity_codes" not in quote


def test_extraction_service_does_not_import_commodity_codes() -> None:
    for path in _EXTRACT.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert "commodity_codes" not in source
        assert "customer_rfq" not in source


@pytest.mark.asyncio
async def test_get_code_raises_when_missing() -> None:
    session = AsyncMock()
    session.get = AsyncMock(return_value=None)
    with pytest.raises(UnknownCommodityCode, match="kod towarowy"):
        await CommodityCodeService(session).get_code(uuid4())


@pytest.mark.asyncio
async def test_quote_persists_commodity_code_id_from_bind() -> None:
    hs_id = uuid4()
    session = AsyncMock()
    session.scalar = AsyncMock(
        return_value=ChargeCode(
            id=uuid4(),
            organization_id=uuid4(),
            code="THC",
            name="THC",
            aliases=[],
        ),
    )
    mappings = MagicMock()
    mappings.first.return_value = {
        "id": uuid4(),
        "organization_id": uuid4(),
        "charge_code": "THC",
        "rate_line_id": uuid4(),
        "amount": Decimal("10.0000"),
        "currency": "EUR",
        "source_ref": "tariff://a",
        "created_by": None,
        "origin_port_id": None,
        "destination_port_id": None,
        "party_id": None,
        "customer_rfq_id": None,
        "commodity_code_id": hs_id,
    }
    execute_result = MagicMock()
    execute_result.mappings.return_value = mappings
    session.execute = AsyncMock(return_value=execute_result)
    quoted = await QuotationService(session).quote_from_current_rate(
        organization_id=uuid4(),
        user_id=uuid4(),
        charge_code="THC",
        origin_port_id=uuid4(),
        destination_port_id=uuid4(),
        party_id=uuid4(),
        commodity_code_id=hs_id,
    )
    assert quoted.commodity_code_id == hs_id
    assert quoted.amount == Decimal("10.0000")
    bound = session.execute.await_args.args[1]
    assert bound["commodity_code_id"] == hs_id


class _StubRfq:
    def __init__(self, rfq: CustomerRfq) -> None:
        self._rfq = rfq

    async def get_rfq(self, rfq_id):
        if rfq_id != self._rfq.id:
            raise ResourceNotFound(f"nieznane zapytanie ofertowe: {rfq_id}")
        return self._rfq


class _StubCatalog:
    def __init__(self, code_id):
        self._code_id = code_id

    async def get_code(self, code_id):
        if code_id != self._code_id:
            raise UnknownCommodityCode(f"nieznany kod towarowy: {code_id}")
        return CommodityCode(
            id=code_id,
            organization_id=uuid4(),
            code="0901",
            name="Coffee",
            aliases=[],
            source_ref="tenant:manual",
        )


class _StubQuote:
    def __init__(self, session: object) -> None:
        self._session = session

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
        return Quotation(
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


@pytest.fixture
def hs_quote_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    party_id = uuid4()
    hs_id = uuid4()
    rfq = CustomerRfq(
        id=uuid4(),
        organization_id=uuid4(),
        inbound_message_id=uuid4(),
        source_ref="fixture://inbound-mail/s7",
        status="draft",
        party_id=party_id,
        commodity_code_id=hs_id,
    )
    monkeypatch.setattr("app.api.quotations.CustomerRfqService", lambda session: _StubRfq(rfq))
    monkeypatch.setattr(
        "app.api.quotations.CommodityCodeService",
        lambda session: _StubCatalog(hs_id),
    )
    monkeypatch.setattr("app.api.quotations.QuotationService", _StubQuote)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = lambda: AsyncMock()
    client = TestClient(app)
    client.extra = {"rfq": rfq, "party_id": party_id, "hs_id": hs_id}
    yield client
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_quote_inherits_hs_from_rfq(hs_quote_client: TestClient) -> None:
    rfq = hs_quote_client.extra["rfq"]
    party_id = hs_quote_client.extra["party_id"]
    hs_id = hs_quote_client.extra["hs_id"]
    response = hs_quote_client.post(
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
    assert body["commodity_code_id"] == str(hs_id)
    assert body["amount"] == "10.5000"


def test_http_quote_unknown_hs_is_400(hs_quote_client: TestClient) -> None:
    party_id = hs_quote_client.extra["party_id"]
    response = hs_quote_client.post(
        "/api/v1/quotations",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "origin_port_id": str(uuid4()),
            "destination_port_id": str(uuid4()),
            "party_id": str(party_id),
            "commodity_code_id": str(uuid4()),
        },
    )
    assert response.status_code == 400
    assert "kod towarowy" in response.json()["detail"]


def test_generated_api_types_include_commodity_on_rfq_and_quote() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "commodity_code_id" in source
    assert "CustomerRfqPatch" in source or "Patch" in source
