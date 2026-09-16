# FACTORY-PULSE-2026-W38

Pierwsze liczby SH-R16-12 (P-R). Wypełnione z `gh run list` + PROGRESS 2026-09-16.  
Szablon: [FACTORY-PULSE.md](../szablony/FACTORY-PULSE.md). Nie pasmo „elite” — ogłasza tylko człowiek.

- Okno: **2026-09-09 – 2026-09-16** (7 dni UTC)
- Deploye fabryki n = **patrz tabela** (push `origin/main` + workflow `gate` = `success`)
- Źródła: `gh run list --workflow gate --branch main` · [PROGRESS.md](../../state/PROGRESS.md) · post-plaster 527.0–535.0

## Pięć analogów

| ID | Liczba / ułamek | Pasmo |
|---|---|---|
| `factory_df` | n = **13** zielonych `gate` / 7 dni (40 runów: 13 success, 0 failure, 27 cancelled) | unmeasured → high-factory po drugiej P-Y |
| `factory_lt` | HITL/plaster: lokalny pre-push ~8–11 min; CI mediana **32,9** min · avg 40,2 · max 96,3 | nie karć silnika |
| `factory_recover` | brak `failure` w oknie 7d; recover = N/A (nie było czerwonego) | |
| `factory_cfr` | (0 failure + 0 revert) / 13 ≈ **0** | n≥8 |
| `factory_rework` | 0 | cel 0 |

### Snapshot `gh` (7 dni UTC do 2026-09-16)

- runs = 40 · success = 13 · failure = 0 · cancelled = 27 (`cancel-in-progress`)
- success duration: median ≈ 32,9 min · avg ≈ 40,2 min · max ≈ 96,3 min
## Twarde zera

| Zero | Liczba | Spalenie? |
|---|---|---|
| Kolizje × `/noc` | 0 (ten tydzień) | nie |
| Echo/STUB jako DONE | 0 w 527–535 | nie |
| Event PII | 0 | nie |
| `--no-verify` / force-push | 0 | nie |

## Jedno ograniczenie

1. Baseline: pierwsze liczby — ten plik.
2. Tarcie: długi CI (~40 min) + `cancel-in-progress` utrudnia czytanie historii success.
3. Jedna zmiana: nic w kodzie; kolejna P-Y powtórzy liczby WoW.
4. Data check: następna IDLE-SESJA / P-Y.

## CEO (90 s)

Pierwszy pomiar fabryki z `gh` jest. Pasmo ogłasza człowiek. Agent nie wpisuje „elite” do PROGRESS.
