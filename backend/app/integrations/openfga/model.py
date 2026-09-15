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
        "can_manage_telematics_devices": _member(),
        "can_manage_erp_connectors": _member(),
        "can_manage_exchange_connectors": _member(),
        "can_manage_visibility_connectors": _member(),
        "can_manage_idp_connectors": _member(),
        "can_manage_terminal_slot_connectors": _member(),
        "can_manage_tower_impacts": _member(),
        "can_manage_twin_kinds": _member(),
        "can_manage_twin_marks": _member(),
        "can_manage_war_room_marks": _member(),
        "can_manage_memory_edges": _member(),
        "can_manage_executive_marks": _member(),
        "can_manage_rank_marks": _member(),
    }


def _organization_ops_relations() -> dict[str, Userset]:
    return {
        "can_manage_shipments": _member(),
        "can_manage_shipper_like_marks": _member(),
        "can_manage_shipper_round_marks": _member(),
        "can_manage_shipper_tender_marks": _member(),
        "can_manage_tracking": _member(),
        "can_manage_tracking_consents": _member(),
        "can_manage_shipment_documents": _member(),
        "can_manage_exceptions": _member(),
        "can_manage_cargo_claims": _member(),
        "can_manage_fraud_flags": _member(),
        "can_manage_edi_messages": _member(),
        "can_manage_sales_invoices": _member(),
        "can_manage_sales_lanes": _member(),
        "can_manage_quote_invoice_settlements": _member(),
        "can_manage_bank_payments": _member(),
        "can_manage_factoring_connectors": _member(),
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
        "can_manage_plan_snapshots": _member(),
        "can_manage_circle_sims": _member(),
        "can_manage_lane_kms": _member(),
        "can_manage_weather_observations": _member(),
        "can_manage_free_time_clocks": _member(),
    }


def _organization_ai_catalog_relations() -> dict[str, Userset]:
    return {
        "can_manage_prediction_ledgers": _member(),
        "can_manage_suggestion_ledgers": _member(),
        "can_manage_outcome_kinds": _member(),
        "can_manage_outcome_ledgers": _member(),
        "can_manage_interval_scores": _member(),
        "can_manage_version_scores": _member(),
        "can_manage_version_windows": _member(),
        "can_manage_counterfactual_runs": _member(),
        "can_manage_benefit_ledgers": _member(),
        "can_manage_suggestion_kinds": _member(),
        "can_manage_autonomy_levels": _member(),
        "can_manage_allocation_keys": _member(),
        "can_manage_allocation_levels": _member(),
    }


def _organization_ci_catalog_relations() -> dict[str, Userset]:
    return {
        "can_manage_sla_clauses": _member(),
        "can_manage_delay_forecasts": _member(),
        "can_manage_remediation_options": _member(),
        "can_manage_impact_scenarios": _member(),
        "can_manage_clause_notices": _member(),
        "can_manage_calibration_marks": _member(),
        "can_manage_campaign_marks": _member(),
        "can_manage_groupage_dispatcher_marks": _member(),
        "can_manage_load_order_marks": _member(),
        "can_manage_repair_playbooks": _member(),
        "can_manage_spend_marks": _member(),
        "can_manage_penalty_marks": _member(),
        "can_manage_intervention_outcomes": _member(),
    }


def _organization_br_catalog_relations() -> dict[str, Userset]:
    return {
        "can_manage_oog_permit_marks": _member(),
        "can_manage_lcl_console_marks": _member(),
        "can_manage_nac_marks": _member(),
        "can_manage_silk_corridor_marks": _member(),
        "can_manage_po_financing_marks": _member(),
        "can_manage_wms_flow_marks": _member(),
        "can_manage_rfid_marks": _member(),
        "can_manage_inventory_finance_marks": _member(),
        "can_manage_inventory_collateral_marks": _member(),
        "can_manage_ops_room_marks": _member(),
        "can_manage_line_impact_layer_marks": _member(),
        "can_manage_product_ticket_marks": _member(),
        "can_manage_risk_register_marks": _member(),
        "can_manage_automation_bias_marks": _member(),
        "can_manage_l3_gate_marks": _member(),
        "can_manage_style_cascade_marks": _member(),
        "can_manage_style_fidelity_marks": _member(),
        "can_manage_quality_descent_marks": _member(),
        "can_manage_field_confidence_marks": _member(),
        "can_manage_compliance_program_marks": _member(),
    }


def _organization_crm_sales_relations() -> dict[str, Userset]:
    return {
        "can_manage_crm_leads": _member(),
        "can_manage_crm_opportunities": _member(),
        "can_manage_crm_activities": _member(),
        "can_manage_crm_pipeline_marks": _member(),
        "can_manage_crm_dedup_marks": _member(),
        "can_manage_crm_link_marks": _member(),
        "can_manage_sales_bind_marks": _member(),
        "can_manage_shipper_bind_marks": _member(),
        "can_manage_shipper_award_marks": _member(),
        "can_manage_extraction_prompt_marks": _member(),
    }


def _organization_g_catalog_relations() -> dict[str, Userset]:
    return {
        **_organization_crm_sales_relations(),
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
        "can_manage_cost_category_marks": _member(),
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
        "can_manage_ferry_booking_marks": _member(),
        "can_manage_fuel_anomaly_marks": _member(),
        "can_manage_fleet_cost_marks": _member(),
    }


def _organization_exp2_catalog_relations() -> dict[str, Userset]:
    return {
        "can_manage_bin_pack_marks": _member(),
        "can_manage_pallet_pool_marks": _member(),
        "can_manage_e_cmr_marks": _member(),
        "can_manage_e_delivery_marks": _member(),
        "can_manage_e_doreczenia_marks": _member(),
        "can_manage_peppol_marks": _member(),
        "can_manage_sid_import_marks": _member(),
        "can_manage_integration_hub_marks": _member(),
        "can_manage_webhook_outbox_marks": _member(),
        "can_manage_partner_exchange_marks": _member(),
        "can_manage_regulatory_radar_marks": _member(),
        "can_manage_iso_nis2_marks": _member(),
        "can_manage_offboarding_marks": _member(),
        "can_manage_jit_jis_marks": _member(),
        "can_manage_job_metric_marks": _member(),
        "can_manage_vda_odette_marks": _member(),
        "can_manage_inventory_position_marks": _member(),
        "can_manage_fair_share_marks": _member(),
        "can_manage_mqc_marks": _member(),
        "can_manage_eccn_marks": _member(),
        "can_manage_eur1_atr_marks": _member(),
        "can_manage_phyto_ata_marks": _member(),
        "can_manage_switch_bl_loi_marks": _member(),
        "can_manage_abandoned_rto_marks": _member(),
        "can_manage_general_average_marks": _member(),
        "can_manage_tender_decline_reasons": _member(),
        "can_manage_demand_snapshot_marks": _member(),
        "can_manage_demo_gps_marks": _member(),
        "can_manage_demo_sim_marks": _member(),
        "can_manage_demo_wipe_marks": _member(),
        "can_manage_po_plant_marks": _member(),
        "can_manage_po_sku_marks": _member(),
        "can_manage_impersonate_guard_marks": _member(),
        "can_manage_fuel_card_marks": _member(),
        "can_manage_csrd_marks": _member(),
        **_organization_exp4_catalog_relations(),
    }


def _organization_exp4_catalog_relations() -> dict[str, Userset]:
    # Split: craft_style ≤40 linii na funkcję (słownik relacji rośnie z HITL).
    return {
        **_organization_exp4_mode_catalog_relations(),
        **_organization_exp1_shipment_catalog_relations(),
    }


def _organization_exp4_mode_catalog_relations() -> dict[str, Userset]:
    return {
        "can_manage_air_ra3_marks": _member(),
        "can_manage_rail_cim_marks": _member(),
        "can_manage_rail_uic_marks": _member(),
        "can_manage_ocean_alliance_marks": _member(),
        "can_manage_ocean_feeder_marks": _member(),
        "can_manage_reefer_marks": _member(),
        "can_manage_chassis_marks": _member(),
        "can_manage_line_impact_marks": _member(),
        "can_manage_three_way_marks": _member(),
        "can_manage_empty_depot_marks": _member(),
        "can_manage_po_batch_marks": _member(),
        "can_manage_un_segregation_marks": _member(),
        "can_manage_nvocc_marks": _member(),
        "can_manage_multi_manning_marks": _member(),
        "can_manage_posting_marks": _member(),
        "can_manage_position_events": _member(),
        "can_manage_tacho_office_marks": _member(),
        "can_manage_tacho_plan_marks": _member(),
        "can_manage_lez_marks": _member(),
        "can_manage_label_parking_marks": _member(),
        "can_manage_ab_sus_marks": _member(),
        "can_manage_funnel_marks": _member(),
        "can_manage_terms_ai_marks": _member(),
        "can_manage_mail_accept_marks": _member(),
        "can_manage_role_view_marks": _member(),
        "can_manage_rag_sop_marks": _member(),
        "can_manage_copy_ban_marks": _member(),
        "can_manage_route_plan_marks": _member(),
        "can_manage_erru_marks": _member(),
        "can_manage_mobile_client_marks": _member(),
    }


def _organization_exp1_shipment_catalog_relations() -> dict[str, Userset]:
    return {
        "can_manage_dual_ledger_marks": _member(),
        "can_manage_named_place_marks": _member(),
        "can_manage_slot_guarantee_marks": _member(),
        "can_manage_freight_term_marks": _member(),
        "can_manage_customer_po_marks": _member(),
        "can_manage_profit_center_marks": _member(),
        "can_manage_high_value_marks": _member(),
        "can_manage_payment_terms_marks": _member(),
        "can_manage_language_code_marks": _member(),
        "can_manage_haulier_role_marks": _member(),
        "can_manage_diversion_marks": _member(),
        "can_manage_spot_contract_marks": _member(),
        "can_manage_bid_decision_marks": _member(),
        "can_manage_quote_currency_marks": _member(),
        "can_manage_quote_validity_marks": _member(),
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
        **_organization_ai_catalog_relations(),
        **_organization_ci_catalog_relations(),
        **_organization_br_catalog_relations(),
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
