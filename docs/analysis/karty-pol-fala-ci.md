# Karty pól — Fala CI (umowy / SLA / strata)

**Kanon:** PLAN § Fala CI. CI9 przed CI1. Pin 2026-09-08c.

## Gwarancja

Treść umowy/SLA: nie Omni, nie support, nie super-admin, nie inny tenant, **nie AI**, nie publiczne. Super-admin: `contracts_count`. Impersonation nie unwrap.

## Tabele

| Tabela | Pola | Uwagi |
|---|---|---|
| `customer_contract` | shipper, their_customer, valid, source_ref, blob_ciphertext, wrapped_dek | wiele umów |
| `sla_clause` | metric, próg, penalty_ciphertext, obligation_ciphertext | wpis ręczny |
| `tenant_contract_kek` | wrap KMS/hasło tenanta | brak plaintext platformy |
| `delay_forecast` | interval, p_late, horizon_h | przed actual late |
| `impact_scenario` | łańcuch stock→EBITDA albo NULL | |
| `remediation_option` | kind, repair_cost, expected_save | S11 |
| `intervention_outcome` | predicted_loss, repair_cost, actual_loss, saved SQL | CI7 |
| `spend_leakage` | FV vs klauzula | ≠ druga marża |

ExtractionService: deny-list `customer_contract`. Demo: tylko fikcyjne umowy.
