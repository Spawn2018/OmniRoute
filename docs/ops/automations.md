# Automatyzacje fabryki (Cursor / GitHub)

Wspólny kontrakt: **żadna automacja nie commituje, nie merguje, nie edytuje HC, nie akceptuje extractu, nie wysyła maila, nie robi bookingu.** Wynik = komentarz, issue albo draft.

## Już w repo (egzekucja, nie prośba)

| Mechanizm | Co robi | Czego nie robi |
|---|---|---|
| `scripts/githooks/pre-commit` | Odmowa, gdy w drzewie zostają pliki poza commitem (drugi pisarz). Odmowa zmiany kontraktu bez baseline agentlinta | Nie podpisuje kontraktu (`--write`) |
| `scripts/quality/writer_preflight.py` | `/plaster` i `/plan-modul`: stop, gdy `NOC-LIVE` ≠ `stop` | Nie zgaduje drugiego okna Cursora bez nocy |
| `scripts/githooks/pre-push` | `just gate` | `--no-verify` omija — nawyk zakazany |
| job `report-failure` w `gate.yml` | Na PR: który job padł (`gate` / `meta`) | Nie commituje docs-debt |

`just hooks` po clone — inaczej pre-commit nie wisi.

## Do włączenia ręcznie w Cursor Automations (nie YAML w git)

Dopiero gdy dwa piątki z rzędu operator **przeczyta** issue.

| ID | Trigger | Wolno | Zakaz |
|---|---|---|---|
| D1 retro | cron piątek | Issue z checklistą z `friday-retrospective.md` | Edycja AGENTS / GROUNDING / rules |
| D3 jakość | cron poniedziałek | Issue: jscpd, coverage; `refactor_ratio` tylko z adnotacją że bywał fałszywy | `/refaktor` z automatu; progi; blocker merge |
| D4 kartka | push z migracją albo archiwum delty | Komentarz gdy brak linii PROGRESS | Dopisywanie CURRENT; nota 4,4 |
| D5 synth | nie włączać | — | Żywy OpenAI; dane tenanta |

D2 jest w CI, nie w Cursor Automations.

## Uczenie

Karta `docs/_knowledge/` **po** powtórzonym błędzie, ≤80 linii, commit bez agentlinta. Nie generator kart. Puste `rules-catalog` / `skills-catalog` zostają puste.
