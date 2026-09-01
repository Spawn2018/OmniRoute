# Nocna zmiana (kod bez Ciebie przy klawiaturze)

Operator przyjął ryzyko: **noc może pisać kod**. HITL produktowe (akceptacja ekstrakcji do bazy) **nie** znika. Znika tylko czekanie na Ciebie przy już zaplanowanym plasterze.

To nie jest drugi plan produktu. Kolejka nadal jest w [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md). Ten plik = jak agent ma się zachować, gdy Cię nie ma.

## Co wolno tej nocy

| CURRENT.md Etap | Noc robi | Noc nie robi |
|---|---|---|
| Delta zaakceptowana / wolno `/plaster` | Jeden plaster: `/plaster` → `/testy` (czerwone) → kod → gate → `/zamknij` | Następnego plastra kodu. 4.2, Q2, M-02, Auth0 |
| Etap: Plan / brak delty | Plan z **rekomendowanymi** opcjami (niżej), zapis delty, stop | Kod nowego zakresu w tej samej nocy |
| Niejasne / DO USTALENIA w delcie | Stop. Zostaw pytanie w CURRENT | Zgadywanie poza listą rekomendowaną |

**Limit: jeden plaster kodu na noc.** Po zamknięciu 4.1 CURRENT skacze na Plan 4.2 — rano `/plan-modul`, nie 4.2 w tym samym biegu.

Cloud Agent zwykle **nie pushuje na `main`**. Robi gałąź + PR. Rano merge, gdy CI zielone. To jest pożądane: zły nocny diff nie ląduje od razu na origin/main.

Lokalny agent (Windows, `pg_ctl`) może pushować na `main` tylko gdy `just gate` przechodzi i hook `scripts/githooks` jest włączony. Czerwony gate = stop, nie `--no-verify`.

## Opcje w Planie (to, co zawsze wyskakuje)

Cursor w trybie Plan pokazuje wybór. Operator: **zawsze bierz to, co jest oznaczone jako rekomendowane.**

Gdy etykiety nie ma:

1. Opcja zgodna z kolejką Q i z już zapisaną deltą / spec z CURRENT.
2. Opcja węższa (mniej tabel, mniej UI) zamiast szerszej.
3. Stop i pytanie w CURRENT, jeśli żadna nie jest oczywista.

Nie wymyślaj czwartej drogi. Nie otwieraj M-02, Auth0, 70 pustych modułów, Temporal, Infisical.

## Twarde stop (nawet o 3 w nocy)

- HITL: nic z ekstrakcji LLM do bazy bez akceptacji człowieka.
- LLM nie liczy. `charge` = jedyna prawda o marży. Decimal, nie float.
- ExtractionService nie importuje rates.
- WIP=1 — nie zaczynaj drugiego plastra kodu.
- Brak `organization_id` / RLS / testu izolacji = nie merge.
- Nie cofaj hotfixów CI (lista w HANDOFF).
- Gate czerwony po dwóch naprawach = zostaw PR otwarty, nie sil.

## Cloud 5

Odpalasz **Cloud Agent** (cursor.com/agents albo Agents → Cloud), najmocniejszy dostępny model — u Ciebie: **Cloud 5 / Claude 5**, nie fast/Composer.

VM w chmurze **nie ma** Twojego `tools\pgdata`. Żeby testy RLS 4.1 nie były teatrem, środowisko Cloud musi mieć Postgres 16 (Docker w setupie agenta) albo agent ma napisać migrację + testy i zostawić w PR adnotację, że integracja RLS nie była odpalona lokalnie w VM — wtedy **nie** twierdź, że izolacja jest udowodniona, dopóki CI z PG nie przejdzie.

Wklejka: [HANDOFF-BUILDING-AGENT.md](../state/HANDOFF-BUILDING-AGENT.md) albo komenda `/noc`.
