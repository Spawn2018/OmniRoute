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
    assert "can_manage_consignments" in org.relations
    assert "can_manage_pallet_balances" in org.relations
    assert "can_manage_document_templates" in org.relations
    assert "can_manage_rate_cards" in org.relations
    assert "can_manage_charge_templates" in org.relations
    assert "can_manage_fuel_indexes" in org.relations
    assert "can_manage_local_charges" in org.relations
    assert "can_manage_tender_quotes" in org.relations
    assert "can_manage_tenders" in org.relations
    assert "can_manage_tender_lots" in org.relations
    assert "can_manage_tender_lanes" in org.relations
    assert "can_manage_tender_rounds" in org.relations
    assert "can_manage_tender_data_rooms" in org.relations
    assert "can_manage_tender_matrix_cells" in org.relations
    assert "can_manage_tender_playbooks" in org.relations
    assert "can_manage_tender_win_losses" in org.relations
    assert "can_manage_tender_consortium_members" in org.relations
    assert "can_manage_tender_prospects" in org.relations
    assert "can_manage_tender_bid_stances" in org.relations
    assert "can_manage_tender_carbon_marks" in org.relations
    assert "can_manage_lane_patterns" in org.relations
    assert "can_manage_kreptd_licences" in org.relations
    assert "can_manage_monitoring_schemes" in org.relations
    assert "can_manage_party_documents" in org.relations
    assert "can_manage_customer_contracts" in org.relations
    assert "can_manage_tenant_contract_keks" in org.relations
    assert "can_manage_cash_discounts" in org.relations
    assert "can_manage_carbon_methods" in org.relations
    assert "can_manage_prediction_ledgers" in org.relations
    assert "can_manage_suggestion_ledgers" in org.relations
    assert "can_manage_outcome_ledgers" in org.relations
    assert "can_manage_interval_scores" in org.relations
    assert "can_manage_counterfactual_runs" in org.relations
    assert "can_manage_benefit_ledgers" in org.relations
    assert "can_manage_suggestion_kinds" in org.relations
    assert "can_manage_autonomy_levels" in org.relations
    assert "can_manage_plan_snapshots" in org.relations
    assert "can_manage_circle_sims" in org.relations
    assert "can_manage_lane_kms" in org.relations
    assert "can_manage_weather_observations" in org.relations
    assert "can_manage_free_time_clocks" in org.relations
    assert "can_manage_telematics_connectors" in org.relations
    assert "can_manage_erp_connectors" in org.relations
    assert "can_manage_exchange_connectors" in org.relations
    assert "can_manage_idp_connectors" in org.relations
    assert "can_manage_terminal_slot_connectors" in org.relations
    assert "can_manage_tower_impacts" in org.relations
    assert "can_manage_twin_kinds" in org.relations
    assert "can_manage_twin_marks" in org.relations
    assert "can_manage_war_room_marks" in org.relations
    assert "can_manage_memory_edges" in org.relations
    assert "can_manage_executive_marks" in org.relations
    assert "can_manage_rank_marks" in org.relations
    assert "can_manage_task_templates" in org.relations
    assert "can_manage_tender_award_reviews" in org.relations
    assert "can_manage_tender_ted_notices" in org.relations
    assert "can_manage_tender_rfp_intakes" in org.relations
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
    consignments = org.relations["can_manage_consignments"]
    assert consignments.computed_userset is not None
    assert consignments.computed_userset.relation == "member"
    pallet_balances = org.relations["can_manage_pallet_balances"]
    assert pallet_balances.computed_userset is not None
    assert pallet_balances.computed_userset.relation == "member"
    document_templates = org.relations["can_manage_document_templates"]
    assert document_templates.computed_userset is not None
    assert document_templates.computed_userset.relation == "member"
    rate_cards = org.relations["can_manage_rate_cards"]
    assert rate_cards.computed_userset is not None
    assert rate_cards.computed_userset.relation == "member"
    charge_templates = org.relations["can_manage_charge_templates"]
    assert charge_templates.computed_userset is not None
    assert charge_templates.computed_userset.relation == "member"
    fuel_indexes = org.relations["can_manage_fuel_indexes"]
    assert fuel_indexes.computed_userset is not None
    assert fuel_indexes.computed_userset.relation == "member"
    local_charges = org.relations["can_manage_local_charges"]
    assert local_charges.computed_userset is not None
    assert local_charges.computed_userset.relation == "member"
    tender_quotes = org.relations["can_manage_tender_quotes"]
    assert tender_quotes.computed_userset is not None
    assert tender_quotes.computed_userset.relation == "member"
    tenders = org.relations["can_manage_tenders"]
    assert tenders.computed_userset is not None
    assert tenders.computed_userset.relation == "member"
    tender_lots = org.relations["can_manage_tender_lots"]
    assert tender_lots.computed_userset is not None
    assert tender_lots.computed_userset.relation == "member"
    tender_lanes = org.relations["can_manage_tender_lanes"]
    assert tender_lanes.computed_userset is not None
    assert tender_lanes.computed_userset.relation == "member"
    tender_rounds = org.relations["can_manage_tender_rounds"]
    assert tender_rounds.computed_userset is not None
    assert tender_rounds.computed_userset.relation == "member"
    tender_data_rooms = org.relations["can_manage_tender_data_rooms"]
    assert tender_data_rooms.computed_userset is not None
    assert tender_data_rooms.computed_userset.relation == "member"
    tender_matrix_cells = org.relations["can_manage_tender_matrix_cells"]
    assert tender_matrix_cells.computed_userset is not None
    assert tender_matrix_cells.computed_userset.relation == "member"
    tender_playbooks = org.relations["can_manage_tender_playbooks"]
    assert tender_playbooks.computed_userset is not None
    assert tender_playbooks.computed_userset.relation == "member"
    tender_win_losses = org.relations["can_manage_tender_win_losses"]
    assert tender_win_losses.computed_userset is not None
    assert tender_win_losses.computed_userset.relation == "member"
    tender_consortium_members = org.relations["can_manage_tender_consortium_members"]
    assert tender_consortium_members.computed_userset is not None
    assert tender_consortium_members.computed_userset.relation == "member"
    tender_prospects = org.relations["can_manage_tender_prospects"]
    assert tender_prospects.computed_userset is not None
    assert tender_prospects.computed_userset.relation == "member"
    tender_bid_stances = org.relations["can_manage_tender_bid_stances"]
    assert tender_bid_stances.computed_userset is not None
    assert tender_bid_stances.computed_userset.relation == "member"
    tender_carbon_marks = org.relations["can_manage_tender_carbon_marks"]
    assert tender_carbon_marks.computed_userset is not None
    assert tender_carbon_marks.computed_userset.relation == "member"
    lane_patterns = org.relations["can_manage_lane_patterns"]
    assert lane_patterns.computed_userset is not None
    assert lane_patterns.computed_userset.relation == "member"
    kreptd_licences = org.relations["can_manage_kreptd_licences"]
    assert kreptd_licences.computed_userset is not None
    assert kreptd_licences.computed_userset.relation == "member"
    monitoring_schemes = org.relations["can_manage_monitoring_schemes"]
    assert monitoring_schemes.computed_userset is not None
    assert monitoring_schemes.computed_userset.relation == "member"
    party_documents = org.relations["can_manage_party_documents"]
    assert party_documents.computed_userset is not None
    assert party_documents.computed_userset.relation == "member"
    customer_contracts = org.relations["can_manage_customer_contracts"]
    assert customer_contracts.computed_userset is not None
    assert customer_contracts.computed_userset.relation == "member"
    tenant_contract_keks = org.relations["can_manage_tenant_contract_keks"]
    assert tenant_contract_keks.computed_userset is not None
    assert tenant_contract_keks.computed_userset.relation == "member"
    cash_discounts = org.relations["can_manage_cash_discounts"]
    assert cash_discounts.computed_userset is not None
    assert cash_discounts.computed_userset.relation == "member"
    carbon_methods = org.relations["can_manage_carbon_methods"]
    assert carbon_methods.computed_userset is not None
    assert carbon_methods.computed_userset.relation == "member"
    prediction_ledgers = org.relations["can_manage_prediction_ledgers"]
    assert prediction_ledgers.computed_userset is not None
    assert prediction_ledgers.computed_userset.relation == "member"
    suggestion_ledgers = org.relations["can_manage_suggestion_ledgers"]
    assert suggestion_ledgers.computed_userset is not None
    assert suggestion_ledgers.computed_userset.relation == "member"
    outcome_ledgers = org.relations["can_manage_outcome_ledgers"]
    assert outcome_ledgers.computed_userset is not None
    assert outcome_ledgers.computed_userset.relation == "member"
    interval_scores = org.relations["can_manage_interval_scores"]
    assert interval_scores.computed_userset is not None
    assert interval_scores.computed_userset.relation == "member"
    counterfactual_runs = org.relations["can_manage_counterfactual_runs"]
    assert counterfactual_runs.computed_userset is not None
    assert counterfactual_runs.computed_userset.relation == "member"
    benefit_ledgers = org.relations["can_manage_benefit_ledgers"]
    assert benefit_ledgers.computed_userset is not None
    assert benefit_ledgers.computed_userset.relation == "member"
    suggestion_kinds = org.relations["can_manage_suggestion_kinds"]
    assert suggestion_kinds.computed_userset is not None
    assert suggestion_kinds.computed_userset.relation == "member"
    autonomy_levels = org.relations["can_manage_autonomy_levels"]
    assert autonomy_levels.computed_userset is not None
    assert autonomy_levels.computed_userset.relation == "member"
    plan_snapshots = org.relations["can_manage_plan_snapshots"]
    assert plan_snapshots.computed_userset is not None
    assert plan_snapshots.computed_userset.relation == "member"
    circle_sims = org.relations["can_manage_circle_sims"]
    assert circle_sims.computed_userset is not None
    assert circle_sims.computed_userset.relation == "member"
    lane_kms = org.relations["can_manage_lane_kms"]
    assert lane_kms.computed_userset is not None
    assert lane_kms.computed_userset.relation == "member"
    weather_observations = org.relations["can_manage_weather_observations"]
    assert weather_observations.computed_userset is not None
    assert weather_observations.computed_userset.relation == "member"
    free_time_clocks = org.relations["can_manage_free_time_clocks"]
    assert free_time_clocks.computed_userset is not None
    assert free_time_clocks.computed_userset.relation == "member"
    telematics_connectors = org.relations["can_manage_telematics_connectors"]
    assert telematics_connectors.computed_userset is not None
    assert telematics_connectors.computed_userset.relation == "member"
    erp_connectors = org.relations["can_manage_erp_connectors"]
    assert erp_connectors.computed_userset is not None
    assert erp_connectors.computed_userset.relation == "member"
    exchange_connectors = org.relations["can_manage_exchange_connectors"]
    assert exchange_connectors.computed_userset is not None
    assert exchange_connectors.computed_userset.relation == "member"
    idp_connectors = org.relations["can_manage_idp_connectors"]
    assert idp_connectors.computed_userset is not None
    assert idp_connectors.computed_userset.relation == "member"
    terminal_slot_connectors = org.relations["can_manage_terminal_slot_connectors"]
    assert terminal_slot_connectors.computed_userset is not None
    assert terminal_slot_connectors.computed_userset.relation == "member"
    tower_impacts = org.relations["can_manage_tower_impacts"]
    assert tower_impacts.computed_userset is not None
    assert tower_impacts.computed_userset.relation == "member"
    twin_kinds = org.relations["can_manage_twin_kinds"]
    assert twin_kinds.computed_userset is not None
    assert twin_kinds.computed_userset.relation == "member"
    twin_marks = org.relations["can_manage_twin_marks"]
    assert twin_marks.computed_userset is not None
    assert twin_marks.computed_userset.relation == "member"
    war_room_marks = org.relations["can_manage_war_room_marks"]
    assert war_room_marks.computed_userset is not None
    assert war_room_marks.computed_userset.relation == "member"
    memory_edges = org.relations["can_manage_memory_edges"]
    assert memory_edges.computed_userset is not None
    assert memory_edges.computed_userset.relation == "member"
    executive_marks = org.relations["can_manage_executive_marks"]
    assert executive_marks.computed_userset is not None
    assert executive_marks.computed_userset.relation == "member"
    rank_marks = org.relations["can_manage_rank_marks"]
    assert rank_marks.computed_userset is not None
    assert rank_marks.computed_userset.relation == "member"
    task_templates = org.relations["can_manage_task_templates"]
    assert task_templates.computed_userset is not None
    assert task_templates.computed_userset.relation == "member"
    tender_award_reviews = org.relations["can_manage_tender_award_reviews"]
    assert tender_award_reviews.computed_userset is not None
    assert tender_award_reviews.computed_userset.relation == "member"
    tender_ted_notices = org.relations["can_manage_tender_ted_notices"]
    assert tender_ted_notices.computed_userset is not None
    assert tender_ted_notices.computed_userset.relation == "member"
    tender_rfp_intakes = org.relations["can_manage_tender_rfp_intakes"]
    assert tender_rfp_intakes.computed_userset is not None
    assert tender_rfp_intakes.computed_userset.relation == "member"
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
