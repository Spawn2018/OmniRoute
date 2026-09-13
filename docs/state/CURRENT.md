# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **433.0** AI1.1 HITL `outcome_ledger`

**Etap:** Plan — **AI1.2** / **434.0** (delta zaakceptowana `/noc`, wolno `/plaster`)

**Noc:** `/noc 11` do **2026-09-13T11:00+02**.

**Następny:** **434.0** AI1.2 HITL `counterfactual_run` — run_code + baseline_label + levers_label + result_label.

Park: Graph live · Expo/EAS · GPS live poll · unwrap umów. Nie zgaduj poza 434.0.

**Spec (jedyna na sesję):** [docs/deltas/open/434.0-counterfactual-run.md](../deltas/open/434.0-counterfactual-run.md).

**Kanon:** [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c** + **Fala AI** + **Fala BR**. Wizja: [VISION.md](../VISION.md).

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Impersonate ≠ decrypt. `charge.source_ref` **jest** (129.0 / 072) — nie otwieraj plastra AI0. **AI1.0** i **AI1.1** w kodzie (**432.0**, **433.0**). Następny = **AI1.2** `counterfactual_run`. CRPS zostaje w AI2. Silnik what-if zostaje w AI4.1.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-13:** Plaster **428.0** zamknięty (`/noc`) — HITL `spot_contract_mark`.
**2026-09-13:** Plaster **429.0** zamknięty (`/noc`) — HITL `bid_decision_mark`.
**2026-09-13:** Plaster **430.0** zamknięty (`/noc`) — HITL `quote_currency_mark`.
**2026-09-13:** Plaster **431.0** zamknięty (`/noc`) — HITL `quote_validity_mark`.
**2026-09-13:** Plaster **432.0** zamknięty (`/noc`) — HITL `suggestion_ledger`.
**2026-09-13:** Plaster **433.0** zamknięty (`/noc`) — HITL `outcome_ledger`.
**2026-09-13:** Kanon Fali AI/BR w PLAN; `docs/VISION.md`; HC-04 przepisane (Q1–Q2).
**2026-09-13:** Dump CT (badania `03` B.1–B.3, B.7–B.10) w kanonie VISION + PLAN Fala AI/BR; B.4–B.6 FourKites/BY/Kinaxis nietknięte.
**2026-09-13:** Dump TMS top-10 (badania `04b` A–H × 10) w kanonie VISION + PLAN Fala AI/BR. CargoWise/Qargo/interLAN zostają w `04`.
**2026-09-13:** Cloudflare = bramka publikacji (VISION B.8; PLAN park live public). Access ≠ Auth0 S53. Nie Q `/noc`.
