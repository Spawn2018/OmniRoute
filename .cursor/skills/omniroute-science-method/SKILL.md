---
name: omniroute-science-method
description: >-
  Metoda naukowa OmniRoute: model nie liczy; PAL/automation bias tylko z
  cytatu w 25d, VISION albo 05; bliźniak stylu to nie ocena osoby. Używaj
  przy CRPS/MAE, suggestion_ledger, golden, L0–L5, AI Act, STYLE FIDELITY.
---

# Model nie liczy

`CONFIRMED`, `docs/VISION.md` D.3 / B.1: model językowy wyciąga dane, kod je przetwarza. Model nie liczy marży, VAT, kursu, ETA punktowego, osi, km. Kwoty = `Decimal`. CRPS / MAE / Brier — Postgres ze złączenia ledgerów, nie pole wpisane ręką i nie Python na złączeniu, gdy SQL to zrobi.

## PAL i automation bias — tylko cytat

Wolno użyć PAL, GSM-HARD, automation bias, Goddard **wyłącznie** gdy zdanie stoi w:

- `docs/VISION.md`, albo
- `D:\OMNIROUTE-badania\25d-BLIZNIAK-UCZENIE-2026-09-24.md`, albo
- `D:\OMNIROUTE-badania\05-AUDYT-MODELI-AI.md` (albo kopia w `25m`).

Brak cytatu = **„w przeczytanych plikach tego nie ma”**. Nie importuj procentów z pamięci modelu (20,1% vs 61% tylko jeśli VISION/05/25d je podaje).

## Bliźniak stylu ≠ ocena osoby

`CONFIRMED`, VISION B.5: bliźniak osoby modeluje *jak* pisze i czego oczekuje w parze, nigdy *jak dobrze* pracuje. AI Act zał. III pkt 5(b), art. 22 RODO — zakaz narzędzia oceniającego ludzi (VISION A.6).

W kodzie (25d §5): `style_cascade_mark` / `style_fidelity_mark` to katalog HITL. Komentarze i `AGENTS.md`: nie fidelity score, nie ocena osoby, nie wyliczanie 85%. `STYLE FIDELITY SCORE` 85% = `REQUIREMENT` wizji (B.5, E.2 AI8), **nie** runtime.

`twin_mark` przechowuje rodzaj, nie instancję stanu obiektu. Fizyka / circle_sim w tym BC = zakaz.

## Żądanie vs kod

| Warstwa | Przykład |
|---|---|
| Żądanie właściciela | czat / `16-ETAP2-PYTANIA-DO-BLIZNIAKOW.md` (Gdańsk–Oslo, ≥500k kombinacji) |
| Kanon | VISION B.2 cztery tabele; B.4 poziomy 0–5, default 1 |
| Stan kodu | HITL katalog + ledger; silnik L3+ / what-if solver / score 85% = brak albo zakaz w `AGENTS.md` |

Nie zlewaj. HC-04: L0–2 bez zapisu AI; L3–5 w zapisanych granicach + audit; LLM nadal nie liczy.

## Substrat

Cztery tabele wizji: `suggestion_ledger`, `outcome_ledger`, `counterfactual_run`, `benefit_ledger`. Champion / dryf = leftover AI2; detektor auto-champion na 444–446 `REJECTED` (cytuj VISION, nie zgaduj).

Nazwa `learning_scope`: w 25d — zero trafień w `backend/**/*.py` i alembic na datę skanu. XT.0 = `REQUIREMENT` z `12`, nie tabela w kodzie.
