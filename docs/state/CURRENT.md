# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **442.0** AI1.4 leftover FK `outcome_ledger` → `outcome_kind`

**Etap:** Plan — **AI2.0** CRPS / Brier / MAE liczone ze złączenia `suggestion_ledger` × `outcome_ledger`

**Noc:** `/noc 20` do **2026-09-13T20:00+02**.

**Następny:** **AI2.0** CRPS, Brier, MAE **liczone** ze złączenia AI1.0 × AI1.1. Wzorzec: Postgres liczy, model nie.

Park: `data_source` (licencja, AI5) · Graph live · Expo/EAS · GPS live poll · unwrap umów. Nie zgaduj poza AI2.0. Nie otwieraj AI0.

**Spec (jedyna na sesję):** brak — **AI2.0** wymaga planu.

**Kanon:** [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c** + **Fala AI** + **Fala BR**. Wizja: [VISION.md](../VISION.md).

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Impersonate ≠ decrypt. `charge.source_ref` **jest** (129.0 / 072) — nie otwieraj plastra AI0. **AI1.0–AI1.4** (słowniki + FK ledgeru, `twin_mark`, `outcome_ledger`) w kodzie. `data_source` = AI5. CRPS = **AI2.0**.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-13:** Plaster **428.0** zamknięty (`/noc`) — HITL `spot_contract_mark`.
**2026-09-13:** Plaster **429.0** zamknięty (`/noc`) — HITL `bid_decision_mark`.
**2026-09-13:** Plaster **430.0** zamknięty (`/noc`) — HITL `quote_currency_mark`.
**2026-09-13:** Plaster **431.0** zamknięty (`/noc`) — HITL `quote_validity_mark`.
**2026-09-13:** Plaster **432.0** zamknięty (`/noc`) — HITL `suggestion_ledger`.
**2026-09-13:** Plaster **433.0** zamknięty (`/noc`) — HITL `outcome_ledger`.
**2026-09-13:** Plaster **434.0** zamknięty (`/noc`) — HITL `counterfactual_run`.
**2026-09-13:** Plaster **435.0** zamknięty (`/noc`) — HITL `benefit_ledger`.
**2026-09-13:** Plaster **436.0** zamknięty (`/noc`) — HITL `suggestion_kind`.
**2026-09-13:** Plaster **437.0** zamknięty (`/noc`) — HITL `twin_kind`.
**2026-09-13:** Plaster **438.0** zamknięty (`/noc`) — HITL `autonomy_level`.
**2026-09-13:** Plaster **439.0** zamknięty (`/noc`) — FK `suggestion_ledger` → `suggestion_kind`.
**2026-09-13:** Plaster **440.0** zamknięty (`/noc`) — FK `twin_mark` → `twin_kind`.
**2026-09-13:** Plaster **441.0** zamknięty (`/noc`) — HITL `outcome_kind`.
**2026-09-13:** Plaster **442.0** zamknięty (`/noc`) — FK `outcome_ledger` → `outcome_kind`.
**2026-09-13:** Kanon Fali AI/BR w PLAN; `docs/VISION.md`; HC-04 przepisane (Q1–Q2).
**2026-09-13:** Dump CT (badania `03` B.1–B.3, B.7–B.10) w kanonie VISION + PLAN Fala AI/BR; B.4–B.6 FourKites/BY/Kinaxis nietknięte.
**2026-09-13:** Dump TMS top-10 (badania `04b` A–H × 10) w kanonie VISION + PLAN Fala AI/BR. CargoWise/Qargo/interLAN zostają w `04`.
**2026-09-13:** Cloudflare = bramka publikacji (VISION B.8; PLAN park live public). Access ≠ Auth0 S53. Nie Q `/noc`.
