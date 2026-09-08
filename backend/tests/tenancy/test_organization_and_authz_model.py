from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.integrations.openfga.model import authorization_model_request
from app.models.organization import Organization
from app.repositories.tenancy.organization_repository import OrganizationRepository


def test_authorization_model_includes_table_view_permission() -> None:
    request = authorization_model_request()
    org = next(td for td in request.type_definitions if td.type == "organization")
    assert "can_list_users" in org.relations
    assert "can_manage_table_views" in org.relations
    assert "can_review_extractions" in org.relations
    assert "can_manage_charge_codes" in org.relations
    assert "can_manage_commodity_codes" in org.relations
    assert "can_manage_nbp_rates" in org.relations
    assert "can_manage_dangerous_goods" in org.relations
    assert "can_manage_networks" in org.relations
    assert "can_manage_inbound_messages" in org.relations
    assert "can_manage_customer_rfqs" in org.relations
    assert "can_manage_operator_decisions" in org.relations
    assert "can_manage_operator_notices" in org.relations
    assert "can_manage_mail_drafts" in org.relations
    assert "can_manage_shipments" in org.relations
    assert "can_manage_tracking" in org.relations
    assert "can_manage_shipment_documents" in org.relations
    assert "can_manage_exceptions" in org.relations
    assert "can_manage_cargo_claims" in org.relations
    assert "can_manage_fraud_flags" in org.relations
    assert "can_manage_edi_messages" in org.relations
    assert "can_manage_sales_invoices" in org.relations
    assert "can_manage_quote_invoice_settlements" in org.relations
    assert "can_manage_bank_payments" in org.relations
    assert "can_manage_money_costs" in org.relations
    assert "can_manage_fx_differences" in org.relations
    assert "can_manage_cash_flows" in org.relations
    assert "can_manage_cost_to_serve" in org.relations
    assert "can_manage_bookkeeping" in org.relations
    assert "can_manage_collective_invoices" in org.relations
    assert "can_manage_gdpr_requests" in org.relations
    assert "can_manage_shipment_legs" in org.relations
    assert "can_manage_groupage_lines" in org.relations
    assert "can_manage_shipment_packages" in org.relations
    assert "can_manage_dock_appointments" in org.relations
    assert "can_manage_cod_instructions" in org.relations
    assert "can_manage_groupage_tariffs" in org.relations
    assert "can_manage_ocean_bills" in org.relations
    assert "can_manage_rate_lines" in org.relations
    assert "can_manage_charges" in org.relations
    assert "can_manage_quotations" in org.relations
    assert "can_manage_organization_settings" in org.relations
    assert "member" in org.relations
    assert "reviewer" in org.relations
    review = org.relations["can_review_extractions"]
    assert review.computed_userset is not None
    assert review.computed_userset.relation == "reviewer"
    listing = org.relations["can_list_users"]
    assert listing.computed_userset is not None
    assert listing.computed_userset.relation == "member"
    catalog = org.relations["can_manage_charge_codes"]
    assert catalog.computed_userset is not None
    assert catalog.computed_userset.relation == "member"
    commodities = org.relations["can_manage_commodity_codes"]
    assert commodities.computed_userset is not None
    assert commodities.computed_userset.relation == "member"
    nbp = org.relations["can_manage_nbp_rates"]
    assert nbp.computed_userset is not None
    assert nbp.computed_userset.relation == "member"
    dg = org.relations["can_manage_dangerous_goods"]
    assert dg.computed_userset is not None
    assert dg.computed_userset.relation == "member"
    networks = org.relations["can_manage_networks"]
    assert networks.computed_userset is not None
    assert networks.computed_userset.relation == "member"
    inbound = org.relations["can_manage_inbound_messages"]
    assert inbound.computed_userset is not None
    assert inbound.computed_userset.relation == "member"
    rfqs = org.relations["can_manage_customer_rfqs"]
    assert rfqs.computed_userset is not None
    assert rfqs.computed_userset.relation == "member"
    decisions = org.relations["can_manage_operator_decisions"]
    assert decisions.computed_userset is not None
    assert decisions.computed_userset.relation == "member"
    notices = org.relations["can_manage_operator_notices"]
    assert notices.computed_userset is not None
    assert notices.computed_userset.relation == "member"
    drafts = org.relations["can_manage_mail_drafts"]
    assert drafts.computed_userset is not None
    assert drafts.computed_userset.relation == "member"
    shipments = org.relations["can_manage_shipments"]
    assert shipments.computed_userset is not None
    assert shipments.computed_userset.relation == "member"
    tracking = org.relations["can_manage_tracking"]
    assert tracking.computed_userset is not None
    assert tracking.computed_userset.relation == "member"
    documents = org.relations["can_manage_shipment_documents"]
    assert documents.computed_userset is not None
    assert documents.computed_userset.relation == "member"
    exceptions = org.relations["can_manage_exceptions"]
    assert exceptions.computed_userset is not None
    assert exceptions.computed_userset.relation == "member"
    cargo_claims = org.relations["can_manage_cargo_claims"]
    assert cargo_claims.computed_userset is not None
    assert cargo_claims.computed_userset.relation == "member"
    fraud_flags = org.relations["can_manage_fraud_flags"]
    assert fraud_flags.computed_userset is not None
    assert fraud_flags.computed_userset.relation == "member"
    edi_messages = org.relations["can_manage_edi_messages"]
    assert edi_messages.computed_userset is not None
    assert edi_messages.computed_userset.relation == "member"
    sales_invoices = org.relations["can_manage_sales_invoices"]
    assert sales_invoices.computed_userset is not None
    assert sales_invoices.computed_userset.relation == "member"
    settlements = org.relations["can_manage_quote_invoice_settlements"]
    assert settlements.computed_userset is not None
    assert settlements.computed_userset.relation == "member"
    payments = org.relations["can_manage_bank_payments"]
    assert payments.computed_userset is not None
    assert payments.computed_userset.relation == "member"
    money_costs = org.relations["can_manage_money_costs"]
    assert money_costs.computed_userset is not None
    assert money_costs.computed_userset.relation == "member"
    fx_differences = org.relations["can_manage_fx_differences"]
    assert fx_differences.computed_userset is not None
    assert fx_differences.computed_userset.relation == "member"
    cash_flows = org.relations["can_manage_cash_flows"]
    assert cash_flows.computed_userset is not None
    assert cash_flows.computed_userset.relation == "member"
    cost_to_serve = org.relations["can_manage_cost_to_serve"]
    assert cost_to_serve.computed_userset is not None
    assert cost_to_serve.computed_userset.relation == "member"
    bookkeeping = org.relations["can_manage_bookkeeping"]
    assert bookkeeping.computed_userset is not None
    assert bookkeeping.computed_userset.relation == "member"
    collective = org.relations["can_manage_collective_invoices"]
    assert collective.computed_userset is not None
    assert collective.computed_userset.relation == "member"
    gdpr_requests = org.relations["can_manage_gdpr_requests"]
    assert gdpr_requests.computed_userset is not None
    assert gdpr_requests.computed_userset.relation == "member"
    shipment_legs = org.relations["can_manage_shipment_legs"]
    assert shipment_legs.computed_userset is not None
    assert shipment_legs.computed_userset.relation == "member"
    groupage_lines = org.relations["can_manage_groupage_lines"]
    assert groupage_lines.computed_userset is not None
    assert groupage_lines.computed_userset.relation == "member"
    shipment_packages = org.relations["can_manage_shipment_packages"]
    assert shipment_packages.computed_userset is not None
    assert shipment_packages.computed_userset.relation == "member"
    dock_appointments = org.relations["can_manage_dock_appointments"]
    assert dock_appointments.computed_userset is not None
    assert dock_appointments.computed_userset.relation == "member"
    cod_instructions = org.relations["can_manage_cod_instructions"]
    assert cod_instructions.computed_userset is not None
    assert cod_instructions.computed_userset.relation == "member"
    groupage_tariffs = org.relations["can_manage_groupage_tariffs"]
    assert groupage_tariffs.computed_userset is not None
    assert groupage_tariffs.computed_userset.relation == "member"
    ocean_bills = org.relations["can_manage_ocean_bills"]
    assert ocean_bills.computed_userset is not None
    assert ocean_bills.computed_userset.relation == "member"
    rates = org.relations["can_manage_rate_lines"]
    assert rates.computed_userset is not None
    assert rates.computed_userset.relation == "member"
    charges = org.relations["can_manage_charges"]
    assert charges.computed_userset is not None
    assert charges.computed_userset.relation == "member"
    quotations = org.relations["can_manage_quotations"]
    assert quotations.computed_userset is not None
    assert quotations.computed_userset.relation == "member"
    settings = org.relations["can_manage_organization_settings"]
    assert settings.computed_userset is not None
    assert settings.computed_userset.relation == "member"


@pytest.mark.asyncio
async def test_organization_repository_getters() -> None:
    session = AsyncMock()
    org = Organization(id=uuid4(), name="A", slug="a")
    session.get = AsyncMock(return_value=org)
    session.scalar = AsyncMock(return_value=org)
    repo = OrganizationRepository(session)

    assert await repo.get_by_id(org.id) is org
    assert await repo.get_by_slug("a") is org
    session.get.assert_awaited()
    session.scalar.assert_awaited()
