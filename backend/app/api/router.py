from fastapi import APIRouter

from app.api import (
    bank_payments,
    bookkeeping,
    cargo_claims,
    carrier_inquiries,
    cash_flows,
    channel_quotes,
    charge_codes,
    charges,
    collective_invoices,
    commodity_codes,
    cost_to_serve,
    credit_reviews,
    customer_rfqs,
    customer_sops,
    dangerous_goods,
    edi_messages,
    extractions,
    fraud_flags,
    fx_differences,
    gdpr_requests,
    inbound_messages,
    locations,
    mail_drafts,
    money_costs,
    nbp_rates,
    networks,
    operational_exceptions,
    operator_decisions,
    operator_notices,
    organization_settings,
    outbox_events,
    parties,
    party_scorecards,
    port_surcharges,
    ports,
    quotations,
    quote_invoice_settlements,
    rate_lines,
    sales_invoices,
    session,
    shipment_documents,
    shipment_legs,
    shipments,
    table_views,
    tenancy,
    terminals,
    tracking_events,
)
from app.domain.errors import PermissionDenied

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(session.router)
api_router.include_router(tenancy.router)
api_router.include_router(table_views.router)
api_router.include_router(extractions.router)
api_router.include_router(charge_codes.router)
api_router.include_router(commodity_codes.router)
api_router.include_router(dangerous_goods.router)
api_router.include_router(networks.router)
api_router.include_router(carrier_inquiries.router)
api_router.include_router(inbound_messages.router)
api_router.include_router(customer_rfqs.router)
api_router.include_router(operator_decisions.router)
api_router.include_router(operator_notices.router)
api_router.include_router(mail_drafts.router)
api_router.include_router(outbox_events.router)
api_router.include_router(nbp_rates.router)
api_router.include_router(charges.router)
api_router.include_router(rate_lines.router)
api_router.include_router(channel_quotes.router)
api_router.include_router(quotations.router)
api_router.include_router(shipments.router)
api_router.include_router(tracking_events.router)
api_router.include_router(shipment_documents.router)
api_router.include_router(operational_exceptions.router)
api_router.include_router(cargo_claims.router)
api_router.include_router(fraud_flags.router)
api_router.include_router(edi_messages.router)
api_router.include_router(sales_invoices.router)
api_router.include_router(quote_invoice_settlements.router)
api_router.include_router(bank_payments.router)
api_router.include_router(money_costs.router)
api_router.include_router(fx_differences.router)
api_router.include_router(cash_flows.router)
api_router.include_router(cost_to_serve.router)
api_router.include_router(bookkeeping.router)
api_router.include_router(collective_invoices.router)
api_router.include_router(gdpr_requests.router)
api_router.include_router(shipment_legs.router)
api_router.include_router(organization_settings.router)
api_router.include_router(parties.router)
api_router.include_router(party_scorecards.router)
api_router.include_router(credit_reviews.router)
api_router.include_router(customer_sops.router)
api_router.include_router(ports.router)
api_router.include_router(port_surcharges.router)
api_router.include_router(locations.router)
api_router.include_router(terminals.router)


@api_router.api_route(
    "/{undeclared_path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
    include_in_schema=False,
)
async def deny_undeclared_path(undeclared_path: str) -> None:
    _ = undeclared_path
    raise PermissionDenied("Brak deklaracji uprawnień")
