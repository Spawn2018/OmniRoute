# K0 — inwentaryzacja nazw (żywy rejestr)

Źródło: docs/MODULES.md + katalogi ackend/app/services/. Bez dump archiwum Claude.

Wiersze MODULES: **93**. Katalogi BC w kodzie: **203**.

## Rejestr MODULES (ID | nazwa | jedna linia)

| ID | Nazwa | Jedna linia |
|---|---|---|
| M-01 | Wielodostępność / tenancy | 0.3 RLS + 0.4 OpenFGA + 0.12 JWT + 0.15 hasła |
| M-20 | Ekstrakcja dokumentów | 0.7–0.14 HITL + T0 + 0.18 live HTTP PG + 1.3 accept→rate_line + U-art50 + U-pdf-spans + 2.1–2.2 · 66.0 z `inbound_messag |
| M-02 | Outbox / idempotencja | 79.0 `outbox_event` · 264.0 `task_template_saved` |
| M-03 | Konfiguracja jako dane | 3.0 `organization_setting` · 71.0 prefiks/szablon |
| M-06 | charge_code + aliasy | 1.0 katalog |
| M-07 | rate_line (stawka kupna) | 1.1 immutable + source_ref |
| M-08 | charge (buy+sell, marża) | 1.2 jeden wiersz · 129.0 `source_ref` |
| M-21 | Silnik wyceny (SQL) | 2.0 INSERT…SELECT z `rate_line` · 5.1 POL/POD + `party_id` · 16.0 odczyt `nbp_rate` · 20.0 wsad kodów · 68.0 `customer_r |
| M-05 | Geografia | 4.0 `port` + 4.1 `location`/strefy + 4.2 `terminal`/WPI |
| M-10 | Kontrahenci | 5.0 `party` + 131.0 ID · 132.0 role/JDG/parent |
| M-09 | Kody towarowe | 5.2 `commodity_code` · 70.0 FK na RFQ/wycenie |
| M-52 | Towary niebezpieczne | 7.0 `dangerous_good` · 122.0 FK · 192.0 tunel ADR + SG |
| M-23 | Kurs NBP | 6.0 `nbp_rate` · 16.0 odczyt przy `quotation` |
| M-11 | Automatyczne kontakty | 8.0 `resolve_email` |
| M-12 | Sieci i stowarzyszenia | 9.0 `network` · 82.0 `network_member` · 130.0 `party_id` |
| M-13 | Karta wyników kontrahenta | 10.0 `party_scorecard` · 120.0 decyzje oferty |
| M-16 | Procedury operacyjne klienta | 11.0 `customer_sop` · 73.0 `blocks_auto` |
| M-18 | Opłaty portowe warunkowe | 12.0 `port_surcharge` · 69.0 matching `applies_when` |
| M-19 | Stawki live i kanały | 13.0 `channel_quote` |
| M-14 | Ocena kredytowa | 14.0 `credit_review` · 88.0 `bureau_attachment_ref` |
| M-15 | Wirtualny Dyrektor Finansowy | 15.0 `finance_board` · 106.0 FV · 117.0 narracja |
| M-24 | Ryzyko oferty | 17.0 `offer_risk` · 87.0 wskazanie |
| M-25 | Negocjacja i wynik | 18.0 `offer_negotiation` · 85.0 wskazanie |
| M-26 | Dokument oferty | 19.0 `offer_document` · 72.0 `document_number` |
| M-27 | Wycena wsadowa | 20.0 `quotation_batch` |
| M-28 | Zapytania od klientów | 21.0 `customer_inquiry` · 67.0 `customer_rfq` |
| M-29 | Wykrywanie akceptacji | 22.0 `offer_acceptance` · 86.0 S11 |
| M-30 | Zapytania do agentów/armatorów | 23.0 ślad · 83.0 `carrier_inquiry` |
| M-31 | Porównanie odpowiedzi | 24.0 ślad · 84.0 `charge` |
| M-32 | Integracja pocztowa | 64.0 `inbound_message` · 66.0 extract HITL · 78.0 ingest `graph://` · 80.0 ingest `imap://` |
| M-33 | Dodatek do Outlooka | 26.0 `mail_client` · 81.0 dispatch `mailto:` |
| M-34 | Powiadomienia | 27.0 tablica · 75.0 tabela · 123.0 filtr pending |
| M-35 | Zlecenie | 90.0 `shipment` |
| M-36 | Tracking | 91.0 `tracking_event` |
| M-37 | Wyjątki | 93.0 `operational_exception` |
| M-38 | Dokumenty zlecenia | 92.0 `shipment_document` |
| M-39 | EDI | 95.0 `edi_message` |
| M-40 | Fakturowanie i KSeF | 33.0 tablica · 96.0 `sales_invoice` · 97.0 `ksef_ref` |
| M-41 | Rozliczenie wyceny z fakturą | 34.0 tablica · 98.0 `quote_invoice_settlement` |
| M-42 | Bank i płatności | 35.0 tablica · 99.0 `bank_payment` |
| M-43 | Koszt pieniądza | 36.0 tablica · 100.0 `money_cost` |
| M-44 | Różnice kursowe | 37.0 tablica · 101.0 `fx_difference` |
| M-45 | Przepływy | 38.0 tablica · 102.0 `cash_flow` |
| M-46 | Koszt obsługi klienta | 39.0 tablica · 103.0 `cost_to_serve` |
| M-47 | Księgowość (integracja) | 40.0 tablica · 104.0 `bookkeeping` |
| M-91 | Zbiorcza faktura | 105.0 `collective_invoice` |
| M-48 | Transport drogowy | 41.0 `road_transport` · 108.0 `shipment_leg` |
| M-49 | Kolej intermodalna | 42.0 `intermodal_rail` · 109.0 `shipment_leg` rail |
| M-50 | Kolej z Chin | 43.0 `china_rail` · 110.0 `shipment_leg` china_rail |
| M-51 | Drobnica morska | 44.0 `ocean_lcl` · 111.0 `shipment_leg` ocean_lcl |
| M-53 | Sankcje | 45.0 `sanctions` · 89.0 `sanctions_list_ref` |
| M-54 | Oszustwo | 114.0 `fraud_flag` |
| M-55 | Reklamacja ładunku | 191.0 `cargo_claim` |
| M-56 | RODO | 46.0 `gdpr` · 107.0 `gdpr_request` |
| M-57 | Copilot AI | 47.0 `ai_copilot` · 76.0 `mail_draft` · 116.0 wieża · 118.0 SOP |
| M-68 | Obserwowalność | 48.0 `observability` · 119.0 park |
| M-69 | Jakość | 49.0 `extraction_quality` |
| M-70 | Wdrożenie | 50.0 `tenant_rollout` |
| M-71 | Szyna decyzji operatora | 74.0 `operator_decision` · 77.0 lock · 121.0 `changed` |
| B0b | Ledger predykcji | 193.0 `prediction_ledger` · 265.0 `plan_snapshot` |
| G2.20 | Kółko HITL | 266.0 `circle_sim` |
| G2.21 | Km ładowny HITL | 267.0 `lane_km` |
| F9 | Konektor Optima HITL | 268.0 `erp_connector` |
| T8 | Konektor slotu HITL | 269.0 `terminal_slot_connector` |
| S53 | Konektor IdP HITL | 270.0 `idp_connector` |
| S55 | Konektor giełdy HITL | 271.0 `exchange_connector` |
| CI9 | Umowa klienta HITL | 272.0–273.0 `customer_contract` · 274.0 `tenant_contract_kek` |
| CI1 | Klauzula SLA HITL | 313.0 `sla_clause` |
| CI4 | Prognoza opóźnienia HITL | 314.0 `delay_forecast` |
| CI6 | Opcja naprawy HITL | 315.0 `remediation_option` |
| CI6 | Scenariusz skutku HITL | 316.0 `impact_scenario` |
| CI3 | Powiadomienie klauzuli HITL | 317.0 `clause_notice` |
| CI7 | Znacznik kalibracji HITL | 318.0 `calibration_mark` |
| CI8 | Playbook naprawy HITL | 319.0 `repair_playbook` |
| CI2 | Znacznik wycieku HITL | 320.0 `spend_mark` |
| CI5 | Znacznik kary HITL | 321.0 `penalty_mark` |
| CT7 | Konektor widoczności HITL | 275.0 `visibility_connector` |
| CT1 | Zamówienie zakupu HITL | 276.0 `purchase_order` · 277.0 `po_line` · 278.0 `asn` |
| CT4 | Przewodnik routingu HITL | 279.0 `routing_guide`; 285.0 `routing_guide_enforcement`; 286.0 ASN 409 |
| CT3 | Znacznik OTIF HITL | 280.0 `otif_mark` |
| CT6 | Konektor SAP/Oracle HITL | 281.0 `sap_connector` |
| CT10 | Znacznik audytu frachtu HITL | 283.0 `freight_audit_mark` |
| CT11 | Znacznik współpracy 3 stron HITL | 284.0 `collaboration_mark` |
| CT12 | Znacznik CAPA HITL | 282.0 `capa_mark` |
| V2 | Pogoda HITL | 194.0 `stop` ETA · 195.0 `weather_observation` |
| V3 | Zegar D&D HITL | 196.0 `free_time_clock` |
| V5 | Konektor GPS HITL | 197.0 `telematics_connector` |
| V6 | Impact wieży HITL | 198.0 `tower_impact` |
| W1 | Bliźniak HITL | 199.0 `twin_mark` |
| W2 | Sala kryzysowa HITL | 200.0 `war_room_mark` |
| W3 | Krawędź pamięci HITL | 201.0 `memory_edge` |
| W4 | Pytanie zarządu HITL | 202.0 `executive_mark` |
| W5 | Oś rankingu HITL | 203.0 `rank_mark` |

## BC w kodzie (ackend/app/services/)

| Katalog BC |
|---|
| ab_sus_marks |
| abandoned_rto_marks |
| aeo_dossier_marks |
| air_ra3_marks |
| bank_payments |
| billing_marks |
| bin_pack_marks |
| bonded_marks |
| booking_instructions |
| bookkeeping |
| cabotage_marks |
| calibration_marks |
| capa_marks |
| carbon_methods |
| cargo_claims |
| cargo_cover_marks |
| carrier_inquiries |
| cash_discounts |
| cash_flows |
| channel_quotes |
| charge_codes |
| charge_templates |
| charges |
| circle_sims |
| clause_notices |
| cmms_marks |
| cod_instructions |
| collaboration_marks |
| collective_invoices |
| combined_transport_marks |
| commodity_codes |
| company_marks |
| consignments |
| containers |
| copy_ban_marks |
| cost_allocation_marks |
| cost_to_serve |
| crm_leads |
| csrd_marks |
| customer_contracts |
| customer_rfqs |
| cutoff_marks |
| dangerous_goods |
| delay_forecasts |
| demand_snapshot_marks |
| dock_appointments |
| document_checklist_rules |
| document_dispatch_rules |
| document_templates |
| e_cmr_marks |
| e_delivery_marks |
| eccn_marks |
| edi_map_marks |
| edi_messages |
| empty_depot_marks |
| entity_events |
| erp_connectors |
| erru_marks |
| eur1_atr_marks |
| exchange_connectors |
| executive_marks |
| extraction |
| fair_share_marks |
| ferry_art9_marks |
| field_carry_forwards |
| filing_scheme_marks |
| fleet_cost_marks |
| fraud_flags |
| free_time_clocks |
| freight_audit_marks |
| fuel_anomaly_marks |
| fuel_indexes |
| funnel_marks |
| fx_differences |
| gdpr_requests |
| general_average_marks |
| geography |
| groupage_lines |
| groupage_tariffs |
| idp_connectors |
| impact_scenarios |
| inbound_messages |
| incoterm_responsibilities |
| integration_hub_marks |
| intervention_outcomes |
| inventory_position_marks |
| iso_nis2_marks |
| jit_jis_marks |
| kreptd_licences |
| label_parking_marks |
| lane_kms |
| lane_patterns |
| lc_checklists |
| legal_hold_marks |
| lez_marks |
| load_plan_marks |
| local_charges |
| mail_accept_marks |
| mail_drafts |
| make_or_buy_marks |
| memory_edges |
| mobile_client_marks |
| money_costs |
| monitoring_schemes |
| mqc_marks |
| multi_manning_marks |
| nbp_rates |
| ncts_drafts |
| networks |
| nvocc_marks |
| ocean_alliance_marks |
| ocean_bills |
| offboarding_marks |
| oog_marks |
| operational_exceptions |
| operator_decisions |
| operator_notices |
| organization_calendars |
| organization_settings |
| otif_marks |
| outbox_events |
| pallet_balances |
| pallet_pool_marks |
| parties |
| partner_exchange_marks |
| party_documents |
| penalty_marks |
| peppol_marks |
| phyto_ata_marks |
| plan_snapshots |
| port_surcharges |
| posting_marks |
| prediction_ledgers |
| purchase_orders |
| quotations |
| quote_invoice_settlements |
| rag_sop_marks |
| rail_cim_marks |
| rank_marks |
| rate_cards |
| rate_lines |
| reefer_marks |
| registry_poll_marks |
| regulatory_radar_marks |
| remediation_options |
| repair_playbooks |
| resources |
| role_view_marks |
| routing_guide_enforcements |
| routing_guide_matches |
| routing_guides |
| sales_invoices |
| sanctions_marks |
| sap_connectors |
| schedule_exception_marks |
| shipment_documents |
| shipment_legs |
| shipment_packages |
| shipment_stakeholders |
| shipments |
| sid_import_marks |
| sla_clauses |
| spend_marks |
| stops |
| subcontract_edge_marks |
| switch_bl_loi_marks |
| tacho_office_marks |
| task_templates |
| telematics_connectors |
| tenancy |
| tenant_contract_keks |
| tender_award_reviews |
| tender_bid_stances |
| tender_carbon_marks |
| tender_consortium_members |
| tender_data_rooms |
| tender_decline_reasons |
| tender_lanes |
| tender_lots |
| tender_matrix_cells |
| tender_playbooks |
| tender_prospects |
| tender_quotes |
| tender_rfp_intakes |
| tender_rounds |
| tender_ted_notices |
| tender_win_losses |
| tenders |
| terminal_slot_connectors |
| terms_ai_marks |
| time_to_fix_marks |
| tower_impacts |
| tracking_events |
| trips |
| twin_marks |
| vda_odette_marks |
| visibility_connectors |
| war_room_marks |
| weather_observations |
| webhook_outbox_marks |
| what_if_marks |
| working_capital_marks |
| yard_marks |

## Skip świadomy

- Puste ID M-71…M-212 spoza żywego rejestru — nie inventaryzować (zakaz 70 stubów).
- Informacje z claude/ — magazyn, nie SoT (AGENTS).

