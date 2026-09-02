# Automatyzacje fabryki (Cursor / GitHub)

Wspólny kontrakt: **żadna automacja nie commituje, nie merguje, nie edytuje HC, nie akceptuje extractu, nie wysyła maila, nie robi bookingu.**

Operator **nie** jest w pętli. `/plan-modul`, `/plaster`, `/refaktor`, `/noc`, `/zamknij` odpalają `factory_cycle.py`.

## Już w repo (egzekucja, nie prośba)

| Mechanizm | Co robi | Czego nie robi |
|---|---|---|
| `factory_cycle.py --start` | Retrieve kart + podłoga + (poza `/noc`) writer-preflight | Dump całej knowledge |
| `factory_cycle.py --close` | Bench, karta z 3× czerwonego CI, podłoga w górę | GROUNDING / Auto-AGENTS |
| `run_gate.py` | Lokalny gate zbiera KOD i META | Ukrywanie meta za ruffem |
| `quality_floor.py` | Izolacja / bench / promptfoo / HC nie spadają | Obniżanie podłogi |
| `check_agent_refs.py` C2 | Kłamliwy `just` / MCP / skrypt | Edycja kontraktu |
| `pre-commit` | Drugi pisarz / brak baseline | Auto `--write` |
| `report-failure` | Komentarz PR i push na main | Commit docs-debt |
| `noc-preflight.ps1` | `--allow-noc` + `factory_cycle --start noc` | Start przy brudnym git |

`just hooks` po clone.

## Świadomie wyłączone

D1/D3/D4 cron. D5 żywy OpenAI. Auto-merge. `log.jsonl` w git.
