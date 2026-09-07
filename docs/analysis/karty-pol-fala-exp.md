# Karty pól — Fala EXP (poprawki + pola + silniki)

**Kanon:** PLAN § Fala EXP. Pin 2026-09-08c. Cięcie: pole idzie z `/plan-modul` obiektu, nie 80 kolumn naraz.

## EXP0 — poprawki cienkich fal

EXP0.1 wieża+SLA (CI5). EXP0.2 dwa ETA. EXP0.3 slot≠gwarancja. EXP0.4 zakaz 500k instant. EXP0.5 P0 pierwszy. EXP0.6 named_place+wersja. EXP0.7 role/holding. EXP0.8 CMR deadline. EXP0.9 tunel/segregacja UN. EXP0.10 dwa ledgery. EXP0.11 Demo GPS 7 dni. EXP0.12 impersonate≠unwrap.

## EXP1 — pola (produkcja)

**shipment:** customer_po, customer_release, call_off_no; sold_to/bill_to/ship_to/notify; incoterms_code+version+named_place; freight_term prepaid/collect/third_party; cargo_value+waluta; temperature_setpoint_c, logger_id, temp_min/max; booked_carrier vs actual_haulier; diversion_of_shipment_id; legal_hold; high_value_protocol; payment_terms_id; profit_center, cost_center, project_code; language_code.

**quotation:** valid_until, revision_no, supersedes_id; spot_or_contract; mqc_teu, mqc_window; currency_account vs currency_pay; bid_decision go/no_go/hold.

**party:** legal_form, is_sole_trader; peppol_id, ksef_buyer_ref; aeo_status, known_consignor, ra3; preferred_language; contact_hours, channel_pref; kreptd_licence_no, kreptd_checked_at, licence_kind; parent_party_id; sanctions_screened_at, sanctions_result.

**stop:** timezone; appointment_ref/status, no_show_at; seal_in/out; weigh_in_kg/weigh_out_kg; waiting_free_minutes, waiting_started_at; eta_physical, eta_legal; pod_quality ok/retake/missing.

**container:** iso_size_type, grade; vgm_kg, vgm_method, vgm_cutoff_at; free_time_origin_h, free_time_dest_h; last_survey_at; alliance_service, vessel_imo, voyage; bl_kind original/seawaybill/telex/express; si_cutoff_at, ams_cutoff_at, cy_cutoff_at, cfs_cutoff_at.

**rate_line/charge:** spot_or_contract; index_id (FSC/BAF/CAF); allotment_teu; charge_code waiting/no_show/diversion/stamp + source_ref.

**cargo_claim:** damage_code OS&D; notice_due_at, suit_due_at; evidence_gps/temp/photo; liable_party_id szkic S11.

## EXP2 — silniki

2.1 DSO/cash-at-risk. 2.2 make-or-buy. 2.3 cost allocation. 2.4 cargo_cover. 2.5 sanctions listy oficjalne. 2.6 subcontract_edge. 2.7 schedule_exception. 2.8 cutoffy rozdzielone. 2.9 TIME-TO-FIX. 2.10 what-if. 2.11 cabotage. 2.12 combined transport. 2.13 ferry art. 9. 2.14 fuel card+anomalia. 2.15 fleet cost/CMMS. 2.16 bin-pack OR. 2.17 palety Chep. 2.18 e-CMR/eFTI. 2.19 e-Doręczenia. 2.20 Peppol+MPP. 2.21 import SID. 2.22 Integration Hub. 2.23 webhook outbox. 2.24 giełda partnerska. 2.25 regulatory radar. 2.26 ISO/NIS2 ops. 2.27 retencja+legal hold. 2.28 offboarding ciphertext+wipe.

## EXP3 — korpo 4PL

PO line SKU/plant/batch. JIT/JIS. VDA/Odette. inventory position (nie WMS). line impact gdy dane. fair share. MQC vs actual. ECCN. EUR.1/ATR. phyto/ATA. LC. switch BL/LOI. abandoned/RTO. general average. OTIF split. tender_decline_reason. demand_snapshot. 3-way OpenFGA. CAPA. CSRD.

## EXP4–EXP7

Air RA3/lithium. Rail UIC/CIM/SMGS. Ocean alliance/feeder. ICS2 filer. Local charges. OOG. Reefer. Empty/depot/chassis. EIR. NVOCC. Multi-manning. Posting. Tacho Office. LEZ/zakazy. LABEL parking. DTC→CMMS. Job-metric M-72. A/B+SUS. X7 lejek. Terms AI (nie CI blob). Accept z maila. Widoki ról. RAG tylko SOP. Zakaz copy 8min/15k/500k/Bayer. KREPTD + poll rejestrów + TED + ERRU TO_VERIFY.

## EXP8 — nie budujemy

Własny HW GPS/kamera, Selenium, scrape czatów, BIK, GAN, LLM kary, drugi WMS, Energy EV, Transformation Office, gwarancja slotu świata, wymyślone M-203.
