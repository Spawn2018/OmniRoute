from openfga_sdk import (
    Metadata,
    ObjectRelation,
    RelationMetadata,
    RelationReference,
    TypeDefinition,
    Userset,
    WriteAuthorizationModelRequest,
)


def _member() -> Userset:
    return Userset(computed_userset=ObjectRelation(object="", relation="member"))


def _reviewer() -> Userset:
    return Userset(computed_userset=ObjectRelation(object="", relation="reviewer"))


def _organization_core_relations() -> dict[str, Userset]:
    return {
        "member": Userset(this={}),
        "reviewer": Userset(this={}),
        "can_list_users": _member(),
        "can_manage_table_views": _member(),
        "can_review_extractions": _reviewer(),
        "can_manage_charge_codes": _member(),
        "can_manage_rate_lines": _member(),
        "can_manage_charges": _member(),
        "can_manage_quotations": _member(),
        "can_manage_organization_settings": _member(),
        "can_manage_geography": _member(),
        "can_manage_parties": _member(),
        "can_manage_commodity_codes": _member(),
        "can_manage_nbp_rates": _member(),
        "can_manage_dangerous_goods": _member(),
        "can_manage_networks": _member(),
        "can_manage_inbound_messages": _member(),
        "can_manage_customer_rfqs": _member(),
        "can_manage_operator_decisions": _member(),
        "can_manage_operator_notices": _member(),
        "can_manage_mail_drafts": _member(),
        "can_manage_outbox_events": _member(),
        "can_manage_entity_events": _member(),
        "can_manage_telematics_connectors": _member(),
        "can_manage_erp_connectors": _member(),
        "can_manage_exchange_connectors": _member(),
        "can_manage_visibility_connectors": _member(),
        "can_manage_idp_connectors": _member(),
        "can_manage_terminal_slot_connectors": _member(),
        "can_manage_tower_impacts": _member(),
        "can_manage_twin_marks": _member(),
        "can_manage_war_room_marks": _member(),
        "can_manage_memory_edges": _member(),
        "can_manage_executive_marks": _member(),
        "can_manage_rank_marks": _member(),
    }


def _organization_ops_relations() -> dict[str, Userset]:
    return {
        "can_manage_shipments": _member(),
        "can_manage_tracking": _member(),
        "can_manage_shipment_documents": _member(),
        "can_manage_exceptions": _member(),
        "can_manage_cargo_claims": _member(),
        "can_manage_fraud_flags": _member(),
        "can_manage_edi_messages": _member(),
        "can_manage_sales_invoices": _member(),
        "can_manage_quote_invoice_settlements": _member(),
        "can_manage_bank_payments": _member(),
        "can_manage_money_costs": _member(),
        "can_manage_fx_differences": _member(),
        "can_manage_cash_flows": _member(),
        "can_manage_cost_to_serve": _member(),
        "can_manage_bookkeeping": _member(),
        "can_manage_collective_invoices": _member(),
        "can_manage_gdpr_requests": _member(),
        "can_manage_shipment_legs": _member(),
        "can_manage_groupage_lines": _member(),
        "can_manage_shipment_packages": _member(),
        "can_manage_dock_appointments": _member(),
        "can_manage_cod_instructions": _member(),
        "can_manage_groupage_tariffs": _member(),
    }


def _organization_ops_catalog_relations() -> dict[str, Userset]:
    return {
        "can_manage_ocean_bills": _member(),
        "can_manage_consignments": _member(),
        "can_manage_pallet_balances": _member(),
        "can_manage_document_templates": _member(),
        "can_manage_rate_cards": _member(),
        "can_manage_charge_templates": _member(),
        "can_manage_task_templates": _member(),
        "can_manage_fuel_indexes": _member(),
        "can_manage_local_charges": _member(),
        "can_manage_monitoring_schemes": _member(),
        "can_manage_party_documents": _member(),
        "can_manage_customer_contracts": _member(),
        "can_manage_purchase_orders": _member(),
        "can_manage_otif_marks": _member(),
        "can_manage_sap_connectors": _member(),
        "can_manage_capa_marks": _member(),
        "can_manage_freight_audit_marks": _member(),
        "can_manage_collaboration_marks": _member(),
        "can_manage_routing_guide_enforcements": _member(),
        "can_manage_routing_guide_matches": _member(),
        "can_manage_routing_guides": _member(),
        "can_manage_tenant_contract_keks": _member(),
        "can_manage_cash_discounts": _member(),
        "can_manage_carbon_methods": _member(),
        "can_manage_prediction_ledgers": _member(),
        "can_manage_plan_snapshots": _member(),
        "can_manage_circle_sims": _member(),
        "can_manage_lane_kms": _member(),
        "can_manage_weather_observations": _member(),
        "can_manage_free_time_clocks": _member(),
    }


def _organization_ci_catalog_relations() -> dict[str, Userset]:
    return {
        "can_manage_sla_clauses": _member(),
        "can_manage_delay_forecasts": _member(),
        "can_manage_remediation_options": _member(),
        "can_manage_impact_scenarios": _member(),
        "can_manage_clause_notices": _member(),
        "can_manage_calibration_marks": _member(),
        "can_manage_repair_playbooks": _member(),
        "can_manage_spend_marks": _member(),
        "can_manage_penalty_marks": _member(),
        "can_manage_intervention_outcomes": _member(),
    }


def _organization_g_catalog_relations() -> dict[str, Userset]:
    return {
        "can_manage_crm_leads": _member(),
        "can_manage_lc_checklists": _member(),
        "can_manage_ncts_drafts": _member(),
        "can_manage_oog_marks": _member(),
        "can_manage_load_plan_marks": _member(),
        "can_manage_cmms_marks": _member(),
        "can_manage_legal_hold_marks": _member(),
        "can_manage_company_marks": _member(),
        "can_manage_bonded_marks": _member(),
        "can_manage_filing_scheme_marks": _member(),
        "can_manage_edi_map_marks": _member(),
        "can_manage_aeo_dossier_marks": _member(),
        "can_manage_yard_marks": _member(),
        "can_manage_billing_marks": _member(),
        "can_manage_registry_poll_marks": _member(),
        "can_manage_working_capital_marks": _member(),
        "can_manage_make_or_buy_marks": _member(),
        "can_manage_cost_allocation_marks": _member(),
        "can_manage_cargo_cover_marks": _member(),
        "can_manage_sanctions_marks": _member(),
        "can_manage_subcontract_edge_marks": _member(),
        "can_manage_schedule_exception_marks": _member(),
        "can_manage_cutoff_marks": _member(),
        "can_manage_time_to_fix_marks": _member(),
        "can_manage_what_if_marks": _member(),
        "can_manage_cabotage_marks": _member(),
        "can_manage_combined_transport_marks": _member(),
        "can_manage_ferry_art9_marks": _member(),
        "can_manage_fuel_anomaly_marks": _member(),
        "can_manage_fleet_cost_marks": _member(),
    }


def _organization_exp2_catalog_relations() -> dict[str, Userset]:
    return {
        "can_manage_bin_pack_marks": _member(),
        "can_manage_pallet_pool_marks": _member(),
        "can_manage_e_cmr_marks": _member(),
        "can_manage_e_delivery_marks": _member(),
        "can_manage_peppol_marks": _member(),
        "can_manage_sid_import_marks": _member(),
        "can_manage_integration_hub_marks": _member(),
        "can_manage_webhook_outbox_marks": _member(),
        "can_manage_partner_exchange_marks": _member(),
        "can_manage_regulatory_radar_marks": _member(),
        "can_manage_iso_nis2_marks": _member(),
        "can_manage_offboarding_marks": _member(),
        "can_manage_jit_jis_marks": _member(),
        "can_manage_vda_odette_marks": _member(),
    }


def _organization_tender_relations() -> dict[str, Userset]:
    return {
        "can_manage_tender_quotes": _member(),
        "can_manage_tenders": _member(),
        "can_manage_tender_lots": _member(),
        "can_manage_tender_lanes": _member(),
        "can_manage_tender_rounds": _member(),
        "can_manage_tender_data_rooms": _member(),
        "can_manage_tender_matrix_cells": _member(),
        "can_manage_tender_playbooks": _member(),
        "can_manage_tender_win_losses": _member(),
        "can_manage_tender_consortium_members": _member(),
        "can_manage_tender_prospects": _member(),
        "can_manage_tender_bid_stances": _member(),
        "can_manage_tender_carbon_marks": _member(),
        "can_manage_lane_patterns": _member(),
        "can_manage_kreptd_licences": _member(),
        "can_manage_tender_award_reviews": _member(),
        "can_manage_tender_ted_notices": _member(),
        "can_manage_tender_rfp_intakes": _member(),
    }


def _organization_relations() -> dict[str, Userset]:
    return {
        **_organization_core_relations(),
        **_organization_ops_relations(),
        **_organization_ops_catalog_relations(),
        **_organization_ci_catalog_relations(),
        **_organization_g_catalog_relations(),
        **_organization_exp2_catalog_relations(),
        **_organization_tender_relations(),
    }


def _organization_relation_metadata() -> dict[str, RelationMetadata]:
    user_type = [RelationReference(type="user")]
    return {
        "member": RelationMetadata(directly_related_user_types=user_type),
        "reviewer": RelationMetadata(directly_related_user_types=user_type),
    }


def authorization_model_request() -> WriteAuthorizationModelRequest:
    """Model odpowiadający authz/model.fga — źródło prawdy dla write_authorization_model."""
    return WriteAuthorizationModelRequest(
        schema_version="1.1",
        type_definitions=[
            TypeDefinition(type="user"),
            TypeDefinition(
                type="organization",
                relations=_organization_relations(),
                metadata=Metadata(relations=_organization_relation_metadata()),
            ),
        ],
    )
