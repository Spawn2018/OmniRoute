# Zestaw wykonawczy

Warstwa, której brakowało: gotowe pliki, nie ich opisy.

---

# CZĘŚĆ 0 — CO REALNIE BRAKOWAŁO

Uczciwa ocena stanu dokumentacji przed tym plikiem:

| Element | Stan |
|---|---|
| Strategia, moduły, plan, metodyka | kompletne |
| `AGENTS.md` | kompletny |
| Reguły `.cursor/rules/` | kompletne, 8 plików |
| **Skille (`SKILL.md`)** | **wymienione z nazwy, żaden nie napisany** |
| **Komendy własne** | **wymienione, żadna nie napisana** |
| Hooki | jeden z trzech napisany |
| **Skrypty jakości** | **wywoływane w `justfile`, nie istnieją** |
| **Szablony testów** | jeden przykład, brak reszty |
| **Procedura kompilacji `docs/spec/`** | **opisana jednym zdaniem, a to najbardziej ryzykowny krok** |
| **`GLOSSARY.md` i `ARCHITECTURE.md`** | „napisz sam", bez struktury |
| **Dane seed** | opisane, nie dostarczone |
| Definicja gotowości do startu | brak |
| Procedura wycofania po awarii agenta | brak |
| Przykład przerobiony od początku do końca | brak |

Ten dokument dostarcza wszystkie pozycje oznaczone pogrubieniem.

---

# CZĘŚĆ 1 — KOMENDY WŁASNE

Katalog `.cursor/commands/`. Uruchamiane przez `/` w czacie agenta.

## `.cursor/commands/plaster.md`

```markdown
---
description: Rozpoczyna realizację plastra według procedury
---

Przeczytaj `docs/state/CURRENT.md`.

Wykonaj w kolejności, zatrzymując się po każdym kroku po potwierdzenie:

1. Wypisz w jednym zdaniu, co budujesz i czego NIE budujesz.
2. Uruchom subagenta `lowca-duplikatow` z opisem funkcjonalności.
   Zaczekaj na werdykt ISTNIEJE / PODOBNE / BRAK.
3. Jeśli ISTNIEJE — zaproponuj rozszerzenie zamiast nowego kodu i przerwij.
4. Przeczytaj wyłącznie ten plik ze `spec/`, który wskazuje CURRENT.md.
5. Sprawdź schemat bazy przez MCP Postgres. Nie czytaj modeli.
6. Napisz plan: pliki nowe, pliki zmieniane, kolejność, ryzyka.
   NIE PISZ KODU.

Zatrzymaj się i czekaj na akceptację planu.
```

## `.cursor/commands/testy.md`

```markdown
---
description: Pisze testy z kryteriów akceptacji, bez implementacji
---

Z `docs/deltas/open/<id>.md` weź kryteria akceptacji.

Dla każdego kryterium napisz test, który MUSI FAILOWAĆ przy obecnym kodzie.

Zasady:
- reguły biznesowe → property-based (hypothesis), nie przykładowe wartości
- nowa tabela → test izolacji tenantów wg wzorca z `tests/patterns/`
- nazwa testu to zdanie opisujące regułę
- Postgres przez testcontainers, nigdy SQLite
- bez mockowania własnego kodu

Uruchom `pytest` i pokaż, że wszystkie nowe testy failują.
NIE PISZ IMPLEMENTACJI.
```

## `.cursor/commands/bramka.md`

```markdown
---
description: Pełna weryfikacja plastra
---

Uruchom subagenta `weryfikator` z:
- ścieżką do delta-spec
- listą zmienionych plików (`git diff --name-only main`)

Następnie subagenta `audytor-wydajnosci`, jeśli zmieniły się zapytania.

Zwróć tabelę: kryterium → PRZESZŁO / NIE / NIE DA SIĘ SPRAWDZIĆ.
Przy NIE — dokładny komunikat, bez interpretacji.

Nie naprawiaj niczego w tym kroku.
```

## `.cursor/commands/zamknij.md`

```markdown
---
description: Zamyka plaster i przygotowuje następny
---

1. Uruchom subagenta `kronikarz` w tle.
2. Sprawdź, czy `docs/deltas/open/` jest puste.
3. Utwórz commit wg konwencji: `feat(M-xx): <opis> [plaster <id>]`
   ze stopką `Co-authored-by: Cursor Agent <agent@cursor.sh>`.
4. Zaktualizuj `docs/state/CURRENT.md` na następny plaster z planu.
5. Wypisz jednym zdaniem, co zostało niedokończone albo odłożone.

Po tym kroku otwieram nową rozmowę. Nie kontynuuj.
```

## `.cursor/commands/delta.md`

```markdown
---
description: Tworzy szkielet delta-spec dla plastra
---

Argument: identyfikator plastra z `docs/MODULES.md`.

Utwórz `docs/deltas/open/<id>.md` wg szablonu:

# Plaster <id> · <M-xx> <nazwa modułu>
**Spec źródłowa:** docs/spec/<moduł>.md, sekcje <x–y>
**Zależy od:** <lista plastrów>

## Zakres
<co powstaje — trzy zdania maksimum>

## Poza zakresem
<co świadomie zostaje na później — to jest ważniejsze od zakresu>

## Ustalenia
<decyzje podjęte przed startem, np. która data odniesienia>

## Kryteria akceptacji
- [ ] <sprawdzalne maszynowo>
- [ ] <test izolacji tenantów, jeśli nowa tabela>
- [ ] <budżet wydajności, jeśli ścieżka krytyczna>

Wypełnij tyle, ile wynika ze spec. Puste miejsca oznacz jako DO USTALENIA
i wypisz je na końcu jako pytania do mnie.
```

## `.cursor/commands/refaktor.md`

```markdown
---
description: Slot refaktoryzacyjny z wejściem z metryk
---

Uruchom i zbierz wyniki:
  just complexity   → funkcje powyżej progu 10
  just dup          → duplikacja powyżej 3%
  just dead         → martwy kod
  python scripts/refactor_ratio.py --weeks 4

Zbuduj listę zadań posortowaną po: (liczba wywołań × złożoność).

Dla każdej pozycji zaproponuj konkretną zmianę.
NIE ZMIENIAJ ZACHOWANIA. Testy muszą przejść bez modyfikacji.
Po każdej zmianie uruchom `just test`.

Zatrzymaj się po trzech pozycjach i pokaż wynik.
```

---

# CZĘŚĆ 2 — SKILLE

Katalog `.cursor/skills/`. Ładowane dynamicznie albo przypinane jako Custom Mode.

## `.cursor/skills/nowy-plaster/SKILL.md`

```markdown
---
name: nowy-plaster
description: Pełna procedura pionowego plastra od migracji do komponentu
---

# Pionowy plaster

Kolejność jest obowiązkowa. Nie przeskakuj etapów.

## 1. Migracja
- sprawdź aktualny schemat przez MCP Postgres
- `organization_id`, `created_at`, `updated_at`, `created_by` w każdej tabeli
- polityka RLS
- kwoty: `Numeric(14,4)` + `CHAR(3)` waluta obok
- klucze obce z jawnym `ondelete`, bez kaskad na danych finansowych
- indeks: napisz uzasadnienie w komentarzu migracji
- `just migrate-down` musi przejść

## 2. Model
- SQLAlchemy 2.0, typowanie pełne
- bez logiki biznesowej w modelu

## 3. Repozytorium
- jedyne miejsce dostępu do bazy
- nie zna reguł biznesowych
- filtrowanie i agregacja w SQL (zasada 11)
- ścieżka gorąca → asyncpg i surowy SQL zamiast ORM

## 4. Serwis
- nie zna FastAPI: bez Request, Depends, HTTPException
- wyjątki z `domain/errors.py`
- kwoty jako `Money`, nigdy gołe liczby
- zdarzenia do innych modułów przez outbox

## 5. Endpoint
- walidacja, wywołanie serwisu, mapowanie DTO
- jawna deklaracja uprawnień, brak = odmowa
- idempotencja przy zapisie

## 6. Typy frontendu
- `just api-types` — nigdy ręcznie
- katalog `frontend/src/api/` jest tylko do odczytu

## 7. Komponent
- `features/<moduł>/`, nie w katalogu współdzielonym
- stan serwera przez TanStack Query
- kwoty przez `<Money/>`, nigdy surowy number
- powyżej 500 wierszy wirtualizacja
- stany loading / empty / error / partial jako komponenty

## 8. Test
- reguła biznesowa → hypothesis
- nowa tabela → izolacja tenantów
- ścieżka krytyczna → budżet wydajności

## Definicja ukończenia
`just gate` zielone + tabela od weryfikatora + delta-spec zarchiwizowana.
```

## `.cursor/skills/migracja-rls/SKILL.md`

```markdown
---
name: migracja-rls
description: Dodanie tabeli z izolacją tenantów i testem dowodzącym
---

# Tabela z RLS

## Migracja

```python
op.create_table(
    "nazwa",
    sa.Column("id", UUID, primary_key=True, server_default=sa.text("gen_random_uuid()")),
    sa.Column("organization_id", UUID, sa.ForeignKey("organization.id"), nullable=False),
    # ... kolumny domenowe
    sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    sa.Column("created_by", UUID, sa.ForeignKey("app_user.id")),
)
op.create_index("ix_nazwa_org", "nazwa", ["organization_id"])

op.execute("ALTER TABLE nazwa ENABLE ROW LEVEL SECURITY")
op.execute("ALTER TABLE nazwa FORCE ROW LEVEL SECURITY")
op.execute("""
    CREATE POLICY tenant_isolation ON nazwa
    USING (organization_id = current_setting('app.current_org', true)::uuid)
""")
op.execute("CREATE TRIGGER nazwa_audit AFTER INSERT OR UPDATE OR DELETE ON nazwa "
           "FOR EACH ROW EXECUTE FUNCTION write_audit_log()")
```

`FORCE ROW LEVEL SECURITY` jest istotne — bez tego właściciel tabeli omija politykę.

## Test obowiązkowy

Skopiuj z `tests/patterns/tenant_isolation.py` i podmień nazwę tabeli.
Bez tego testu plaster nie jest ukończony.

## Uwaga przy Citus
Tabela dystrybuowana po `organization_id`. Żadne złączenie nie może
przekraczać granicy tenanta.
```

## `.cursor/skills/adapter-armatora/SKILL.md`

```markdown
---
name: adapter-armatora
description: Dodanie kanału armatorskiego do M-19
---

# Nowy kanał armatorski

Nowy armator to KONFIGURACJA, nie kod. Jeśli piszesz więcej niż mapowanie,
framework jest źle zbudowany — zgłoś to zamiast pisać wyjątek.

## Kroki

1. Wpis w `carrier_channel`: typ (api / aggregator / email / portal), priorytet
2. Mapowanie uwierzytelniania w `integrations/carriers/<nazwa>/auth.yaml`
3. Mapowanie endpointów w `endpoints.yaml`
4. **Mapowanie pól odpowiedzi na model DCSA**, nie na model własny
5. Mapowanie kodów opłat armatora na `charge_code` — do `charge_code_alias`
6. Test kontraktowy (pact) na podstawie realnej odpowiedzi sandbox
7. Wpis do automatyzacji tygodniowej sprawdzającej kontrakt

## Obowiązkowo

- limity zapytań per tenant, licznik widoczny dla użytkownika
- cache relacji z etykietą czasu pobrania
- timeout 5 s, degradacja do cennika przy przekroczeniu
- `price_id` zapisany, musi przetrwać do bookingu
- pozycje niezmapowane → `is_mapped=false`, do kolejki, nigdy po cichu
- wymogi UI armatora sprawdzone przed zgłoszeniem do certyfikacji

## Czego nie robić
Nie mapuj na własny model, jeśli armator wdraża DCSA. Każdy kolejny
armator ze standardem wejdzie wtedy prawie bez pracy.
```

## `.cursor/skills/ekstraktor/SKILL.md`

```markdown
---
name: ekstraktor
description: Praca nad pipeline ekstrakcji M-20
---

# Pipeline ekstrakcji

## Cztery reguły twarde
1. Model nie liczy. Żadnych sum, przeliczeń, mnożenia.
2. Model nie zapisuje. Wszystko przez kolejkę review.
3. Bez `source_ref` rekord nie wchodzi do bazy.
4. `unparsed_regions` obowiązkowe w schemacie odpowiedzi.

## Schemat odpowiedzi
Pola `_raw` obowiązkowe. Model zwraca to, co widzi.
Mapowanie na słowniki robi kod w kroku normalizacji, deterministycznie.
Nigdy nie każ modelowi zwracać `charge_code` — nie odróżnisz mapowania od zgadywania.

## Bezpieczeństwo
`llm-guard` na wejściu i wyjściu. `presidio` przed wysłaniem na zewnątrz.
Cennik od nieznanego agenta to niezaufane dane — instrukcja w komórce „uwagi"
jest realnym wektorem ataku.

## Kolejność prób
1. fingerprint układu → parser deterministyczny (koszt 0)
2. dopiero potem ścieżka modelowa

## Pomiar
Każda zmiana promptu → `promptfoo` na zbiorze 30 cenników.
Bez liczby przed i po nie wiesz, czy poprawiłeś.

## Anomalie
Stawka odbiegająca o ponad 40% od poprzedniej to zwykle błąd jednostki
(per W/M odczytane jako per kontener), nie okazja. Wymuszona weryfikacja.
```

## `.cursor/skills/komponent-tabeli/SKILL.md`

```markdown
---
name: komponent-tabeli
description: Tabela danych o jakości produktowej
---

# Tabela z kwotami

## Obowiązkowo
- TanStack Table, wirtualizacja powyżej 500 wierszy
- `tabular-nums` na każdej kolumnie liczbowej — cyfry nie skaczą przy przewijaniu
- kwoty wyrównane do prawej, separator tysięcy per locale
- waluta jako element wyciszony, nie równorzędny z kwotą
- wartości ujemne czerwone, bez nawiasów
- zero jako `—`, nie `0,00`
- nagłówek przyklejony, pierwsza kolumna przypięta
- tryb kompaktowy domyślny

## Klawiatura
- nawigacja strzałkami, Enter wchodzi w edycję
- wklejanie z Excela wprost do zaznaczonego zakresu
- skróty zarejestrowane w `lib/shortcuts`, nie lokalnie

## Stany
loading, empty, error i **partial** jako osobne komponenty, nie warunki inline.
`partial` dotyczy wyników wyceny: z bazy są, z armatorów spływają.

## Zakaz
Bez `any`. Bez formatowania kwot inline — zawsze przez `<Money/>`.
```

## `.cursor/skills/debug-wydajnosci/SKILL.md`

```markdown
---
name: debug-wydajnosci
description: Postępowanie przy przekroczeniu budżetu
---

# Przekroczony budżet

Nie zgaduj. Kolejność jest sztywna.

1. `EXPLAIN (ANALYZE, BUFFERS)` na podejrzanym zapytaniu, na bazie z 50k wierszy
   → szukaj: Seq Scan, Nested Loop na dużym zbiorze, sortowanie na dysku
2. `just profile <plik>` → py-spy, gdzie faktycznie schodzi czas
3. `pghero` → brakujące indeksy, najwolniejsze zapytania
4. Sprawdź N+1: czy liczba zapytań rośnie z liczbą wierszy

## Kolejność napraw
1. indeks pokrywający
2. przeniesienie logiki z Pythona do SQL (zasada 11)
3. widok materializowany odświeżany zdarzeniem
4. cache w Redisie z kluczem zawierającym `organization_id`
5. dopiero na końcu zmiana algorytmu

## Zakaz
Bez optymalizacji „na wyczucie". Każda zmiana ma mieć pomiar przed i po.
```
---

# CZĘŚĆ 3 — HOOKI

## `.cursor/hooks/post_edit.py`

```python
#!/usr/bin/env python3
"""Uruchamiany po każdej edycji agenta. Zwraca błędy przez followup_message."""
import json, subprocess, sys
from pathlib import Path

payload = json.load(sys.stdin)
path = Path(payload["file_path"])
problems: list[str] = []

# Reguły dobrane pod pięć najczęstszych zapachów w kodzie agentów:
# BLE001 szerokie except · F841 nieużywane zmienne · ARG nieużywane argumenty
# PLW0621 przesłonięte zmienne · SLF001 dostęp do składowych chronionych
RUFF = "E,F,B,BLE,C901,ARG,PLW0621,SLF001,F841"

if path.suffix == ".py":
    subprocess.run(["ruff", "format", str(path)], check=False)
    r = subprocess.run(["ruff", "check", "--select", RUFF, str(path)],
                       capture_output=True, text=True)
    if r.returncode:
        problems.append("ruff:\n" + r.stdout)
    m = subprocess.run(["mypy", "--follow-imports=skip", str(path)],
                       capture_output=True, text=True)
    if m.returncode:
        problems.append("mypy:\n" + m.stdout)

elif path.suffix in {".ts", ".tsx"}:
    subprocess.run(["pnpm", "prettier", "--write", str(path)],
                   cwd="frontend", check=False)
    t = subprocess.run(["pnpm", "tsc", "--noEmit"], cwd="frontend",
                       capture_output=True, text=True)
    if t.returncode:
        problems.append("tsc:\n" + t.stdout[-3000:])

elif path.suffix == ".sql" or "alembic/versions" in str(path):
    s = subprocess.run(["sqlfluff", "lint", str(path)],
                       capture_output=True, text=True)
    if s.returncode:
        problems.append("sqlfluff:\n" + s.stdout)

if problems:
    print(json.dumps({
        "followup_message": (
            "Popraw poniższe zanim przejdziesz dalej. "
            "Nie wyłączaj reguł, nie dodawaj noqa.\n\n" + "\n\n".join(problems)
        )
    }))
```

## `.cursor/hooks/pre_commit.py`

```python
#!/usr/bin/env python3
"""Blokuje commit przy naruszeniu architektury, duplikacji, martwym kodzie."""
import json, subprocess, sys

checks = [
    ("architektura", ["lint-imports"]),
    ("duplikacja",   ["jscpd", "--threshold", "3", "--min-lines", "5",
                      "--reporters", "console", "--silent",
                      "backend/app", "frontend/src"]),
    ("martwy kod",   ["vulture", "backend/app", "--min-confidence", "80"]),
    ("sekrety",      ["trufflehog", "git", "file://.", "--since-commit", "HEAD",
                      "--only-verified", "--fail"]),
]

failures = []
for name, cmd in checks:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        failures.append(f"[{name}]\n{r.stdout or r.stderr}")

if failures:
    print(json.dumps({
        "block": True,
        "followup_message": (
            "Commit zablokowany:\n\n" + "\n\n".join(failures) +
            "\n\nDuplikacja: sprawdź, czy nie powielasz istniejącej funkcji "
            "(zasada 14). Uruchom subagenta lowca-duplikatow."
        )
    }))
```

## `.cursor/hooks/pre_edit.py`

```python
#!/usr/bin/env python3
"""Weto na plikach, których agent nie ma zmieniać."""
import json, subprocess, sys, re
from pathlib import Path

payload = json.load(sys.stdin)
path = str(payload["file_path"])

PROTECTED = [
    (r"frontend/src/api/",        "katalog generowany — użyj `just api-types`"),
    (r"docs/deltas/archived/",    "delta zarchiwizowana — utwórz nową"),
    (r"\.cursor/hooks/",          "zmiana hooków wymaga decyzji człowieka"),
    (r"docs/adr/.*\.md",          "ADR ze statusem przyjęta jest niezmienny"),
]

for pattern, reason in PROTECTED:
    if re.search(pattern, path):
        print(json.dumps({"block": True, "followup_message": f"Odmowa: {reason}"}))
        sys.exit(0)

# migracje już zastosowane na bazie deweloperskiej
if "alembic/versions" in path:
    applied = subprocess.run(["alembic", "current"], capture_output=True, text=True)
    rev = Path(path).stem.split("_")[0]
    if rev and rev in applied.stdout:
        print(json.dumps({
            "block": True,
            "followup_message":
                "Ta migracja jest już zastosowana. Utwórz nową: `just migration <nazwa>`."
        }))
```

---

# CZĘŚĆ 4 — USTAWIENIA

## `.cursor/settings.json`

```json
{
  "autoReview": {
    "enabled": true,
    "allowlist": [
      "just check", "just test", "just arch", "just perf",
      "just migrate", "just migrate-down", "just api-types",
      "just complexity", "just dup", "just dead",
      "ruff *", "mypy *", "pytest *", "alembic upgrade *",
      "pnpm test", "pnpm tsc *", "pnpm lint *",
      "jscpd *", "vulture *", "lint-imports",
      "git status", "git diff *", "git log *"
    ],
    "sandbox": ["python *", "node *", "psql *", "uv *"],
    "requireApproval": [
      "git push *", "git commit *", "docker *", "curl *",
      "rm *", "alembic downgrade *", "just gate"
    ]
  },
  "hooks": {
    "onPostEdit": ".cursor/hooks/post_edit.py",
    "onPreCommit": ".cursor/hooks/pre_commit.py",
    "onPreEdit": ".cursor/hooks/pre_edit.py"
  },
  "context": {
    "maxFilesPerRequest": 12,
    "excludePatterns": [
      "docs/_source/**", "frontend/src/api/**",
      "**/node_modules/**", "**/.venv/**", "**/*.lock"
    ]
  }
}
```

`docs/_source/` w wykluczeniach jest istotne: to tam leżą aneksy przed
kompilacją i nie mogą wpaść do kontekstu.

---

# CZĘŚĆ 5 — SKRYPTY JAKOŚCI

## `scripts/refactor_ratio.py`

Mierzy metrykę nadrzędną z rewizji badawczej: stosunek kodu przenoszonego
do dodawanego. Spadek poniżej 10% oznacza, że kod przestał być refaktoryzowany.

```python
#!/usr/bin/env python3
"""Stosunek kodu przeniesionego do dodanego. Próg alarmowy: 10%."""
import subprocess, sys, argparse
from collections import defaultdict

def analyze(weeks: int) -> dict:
    log = subprocess.run(
        ["git", "log", f"--since={weeks}.weeks", "--numstat", "--format=%H|%an"],
        capture_output=True, text=True).stdout

    added = deleted = 0
    for line in log.splitlines():
        parts = line.split("\t")
        if len(parts) == 3 and parts[0].isdigit():
            added += int(parts[0])
            deleted += int(parts[1])

    # przybliżenie kodu przeniesionego: linie usunięte, które pojawiły się
    # gdzie indziej w tym samym commicie (git -M wykrywa przeniesienia)
    moves = subprocess.run(
        ["git", "log", f"--since={weeks}.weeks", "-M", "--diff-filter=R",
         "--numstat", "--format="],
        capture_output=True, text=True).stdout
    moved = sum(int(p.split("\t")[0]) for p in moves.splitlines()
                if p.split("\t")[0].isdigit())

    total = added + moved
    ratio = (moved / total * 100) if total else 0
    return {"added": added, "deleted": deleted, "moved": moved, "ratio": ratio}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--weeks", type=int, default=4)
    p.add_argument("--fail-under", type=float, default=10.0)
    a = p.parse_args()

    r = analyze(a.weeks)
    print(f"Ostatnie {a.weeks} tyg.")
    print(f"  dodane:      {r['added']:>8}")
    print(f"  przeniesione:{r['moved']:>8}")
    print(f"  stosunek:    {r['ratio']:>7.1f}%   (próg {a.fail_under}%)")
    if r["ratio"] < a.fail_under:
        print("\n⚠ Kod przestał być refaktoryzowany, tylko dokładany.")
        print("  Uruchom slot refaktoryzacyjny: /refaktor")
        sys.exit(1)
```

## `scripts/check_spec_sync.py`

```python
#!/usr/bin/env python3
"""Ostrzega, gdy zmiana w serwisie nie ma odpowiednika w spec."""
import subprocess, re, sys

changed = subprocess.run(["git", "diff", "--name-only", "origin/main...HEAD"],
                         capture_output=True, text=True).stdout.splitlines()

modules_touched = {
    m.group(1) for f in changed
    if (m := re.match(r"backend/app/services/(\w+)/", f))
}
specs_touched = {
    m.group(1) for f in changed
    if (m := re.match(r"docs/spec/(\w+)\.md", f))
}

missing = modules_touched - specs_touched
if missing:
    print("⚠ Zmieniono serwisy bez aktualizacji specyfikacji:")
    for m in sorted(missing):
        print(f"    docs/spec/{m}.md")
    print("\nJeśli zachowanie się nie zmieniło, zignoruj.")
```

## `scripts/complexity_delta.py`

Wykrywa dryf złożoności — sygnał, że agent wstawił logikę inline zamiast
wyodrębnić.

```python
#!/usr/bin/env python3
"""Blokuje PR, w którym złożoność funkcji wzrosła o więcej niż 3."""
import subprocess, json, sys

def complexity(ref: str) -> dict[str, int]:
    subprocess.run(["git", "stash", "push", "-q"], check=False)
    subprocess.run(["git", "checkout", "-q", ref], check=True)
    out = subprocess.run(["radon", "cc", "backend/app", "-j"],
                         capture_output=True, text=True).stdout
    subprocess.run(["git", "checkout", "-q", "-"], check=True)
    subprocess.run(["git", "stash", "pop", "-q"], check=False)
    return {f"{f}:{b['name']}": b["complexity"]
            for f, blocks in json.loads(out).items() for b in blocks}

base, head = complexity("origin/main"), complexity("HEAD")
drift = [(k, base.get(k, 0), v) for k, v in head.items()
         if v - base.get(k, 0) >= 3]

if drift:
    print("⚠ Dryf złożoności — sprawdź, czy logika nie powinna być wyodrębniona:")
    for name, b, h in drift:
        print(f"    {name}: {b} → {h}")
    sys.exit(1)
```

---

# CZĘŚĆ 6 — SZABLONY TESTÓW

## `tests/patterns/tenant_isolation.py`

Wzorzec do skopiowania przy każdej nowej tabeli.

```python
import pytest
from app.db import tenant_context

pytestmark = pytest.mark.tenant_isolation

async def test_ENCJA_isolated_between_tenants(db, org_a, org_b, make_ENCJA):
    """Rekord jednego tenanta jest niewidoczny dla drugiego."""
    async with tenant_context(db, org_a):
        created = await make_ENCJA(organization_id=org_a.id)

    async with tenant_context(db, org_b):
        found = await REPOZYTORIUM(db).get(created.id)
    assert found is None

    async with tenant_context(db, org_b):
        listed = await REPOZYTORIUM(db).list()
    assert created.id not in {r.id for r in listed}

async def test_ENCJA_cannot_be_updated_across_tenants(db, org_a, org_b, make_ENCJA):
    async with tenant_context(db, org_a):
        created = await make_ENCJA(organization_id=org_a.id)
    async with tenant_context(db, org_b):
        with pytest.raises((PermissionError, LookupError)):
            await REPOZYTORIUM(db).update(created.id, {})
```

## `tests/patterns/business_rules.py`

Reguły domenowe testowane własnościowo, nie przykładami.

```python
from decimal import Decimal
from hypothesis import given, strategies as st

# --- waga obliczeniowa LCL ---
@given(
    tonnes=st.decimals(min_value=0, max_value=1000, places=3),
    cbm=st.decimals(min_value=0, max_value=1000, places=3),
    minimum=st.decimals(min_value=1, max_value=5, places=1),
)
def test_chargeable_wm_is_never_below_minimum(tonnes, cbm, minimum):
    r = chargeable_wm(tonnes, cbm, minimum=minimum)
    assert r >= minimum
    assert r >= min(tonnes, cbm) or r == minimum

@given(t=st.decimals(min_value=0, max_value=1000, places=3),
       c=st.decimals(min_value=0, max_value=1000, places=3))
def test_chargeable_wm_takes_higher_of_tonnes_or_cbm(t, c):
    assert chargeable_wm(t, c, minimum=Decimal(0)) == max(t, c)

# --- przeliczenia walutowe ---
@given(amount=st.decimals(min_value=0, max_value=10**6, places=4),
       rate=st.decimals(min_value=Decimal("0.0001"), max_value=Decimal("100"), places=6))
def test_conversion_is_reversible_within_rounding(amount, rate):
    there = convert(Money(amount, "USD"), to="PLN", rate=rate)
    back = convert(there, to="USD", rate=1 / rate)
    assert abs(back.amount - amount) <= Decimal("0.01")

def test_cannot_add_different_currencies():
    with pytest.raises(CurrencyMismatch):
        Money(Decimal(10), "USD") + Money(Decimal(10), "EUR")

# --- kaskada narzutów ---
@given(cost=st.decimals(min_value=1, max_value=10**5, places=2),
       markup=st.decimals(min_value=0, max_value=200, places=2))
def test_markup_and_margin_are_consistent(cost, markup):
    sell = apply_markup(cost, percent=markup)
    margin = margin_pct(cost, sell)
    assert abs(markup_pct(cost, sell) - markup) < Decimal("0.01")
    assert margin < 100

@given(floor=st.decimals(min_value=0, max_value=50, places=2))
def test_markup_never_goes_below_margin_floor(floor):
    sell = apply_markup(Decimal(100), percent=Decimal(0), min_margin_pct=floor)
    assert margin_pct(Decimal(100), sell) >= floor

# --- koszt finansowania ---
@given(amount=st.decimals(min_value=1, max_value=10**6, places=2),
       days=st.integers(min_value=-180, max_value=365),
       rate=st.decimals(min_value=0, max_value=Decimal("0.30"), places=4))
def test_financing_cost_sign_follows_gap_direction(amount, days, rate):
    c = financing_cost(amount, gap_days=days, annual_rate=rate)
    if days > 0 and rate > 0:
        assert c > 0          # finansujesz klienta
    elif days < 0 and rate > 0:
        assert c < 0          # dostawca finansuje ciebie
    else:
        assert c == 0

# --- ważność stawki ---
@given(basis=st.sampled_from(["sailing", "booking", "bl_date", "gate_in"]))
def test_rate_validity_uses_declared_basis(basis, sample_rate, sample_request):
    sample_rate.validity_basis = basis
    ref = reference_date_for(sample_request, basis)
    assert is_valid(sample_rate, ref) == (sample_rate.valid_from <= ref <= sample_rate.valid_to)
```

## `tests/perf/test_budgets.py`

```python
import pytest

pytestmark = pytest.mark.perf

async def test_quote_from_stored_rates_under_300ms(bench, rate_lines_50k, sample_request):
    r = await bench(quote_engine.resolve, sample_request, runs=20)
    assert r.p95_ms < 300, f"budżet 300 ms, zmierzono {r.p95_ms:.0f} ms"

async def test_rate_list_50k_under_500ms(bench, rate_lines_50k):
    r = await bench(rate_repo.list_paginated, page=1, size=100, runs=20)
    assert r.p95_ms < 500

async def test_quote_engine_uses_covering_index(db, rate_lines_50k, sample_request):
    plan = await db.execute(explain(quote_engine.candidates_query(sample_request)))
    text = "\n".join(r[0] for r in plan)
    assert "Seq Scan on rate_line" not in text, f"skan sekwencyjny:\n{text}"
```
---

# CZĘŚĆ 7 — KOMPILACJA DOKUMENTACJI

To jest najbardziej ryzykowny krok całego startu, bo wszystko dalej zależy od
jego jakości. Wcześniej opisałem go jednym zdaniem. Poniżej pełna procedura.

## 7.1 Przygotowanie

```bash
mkdir -p docs/_source docs/spec docs/deltas/{open,archived} docs/adr docs/state
cp SPEC-master.md ANEKS-*.md REJESTR-MODULOW-I-PLAN-v2.md docs/_source/
echo "docs/_source/" >> .cursorignore
```

`.cursorignore` jest istotne — aneksy nie mogą wpaść do kontekstu agenta.

## 7.2 Procedura, moduł po module

**Nie zlecaj kompilacji całości jednym poleceniem.** 71 modułów naraz da wynik,
którego nie zweryfikujesz. Rób partiami po 5–8 modułów, z weryfikacją po każdej.

Użyj **Claude Code**, nie Cursora — to zadanie przez całe repo.

```
Zadanie: skompiluj dokumentację modułów M-01 do M-06.

Źródła w docs/_source/. Rejestr modułów: REJESTR-MODULOW-I-PLAN-v2.md.

Dla każdego modułu utwórz docs/spec/<nazwa>.md wg struktury:

# <M-xx> · <Nazwa>
## Cel
Dwa zdania: po co ten moduł istnieje.
## Obiekty danych
Tabele z kolumnami, w formie SQL-podobnej. Bez opisów prozą.
## Reguły biznesowe
Ponumerowana lista. Każda sprawdzalna. Bez uzasadnień.
## Zależności
Moduły, od których zależy i które od niego zależą.
## Rozstrzygnięcia
Decyzje niepodlegające zmianie, z jednym zdaniem uzasadnienia.
## Kryteria akceptacji modułu
Co musi działać, żeby moduł uznać za ukończony.

Zasady:
- maksymalnie 400 linii na plik; przekroczenie → podziel na <nazwa>-<część>.md
- odsyłacze do innych modułów jako [[M-xx]]
- zero powtórzeń między plikami; wspólne pojęcia → GLOSSARY.md
- nie interpretuj i nie uzupełniaj; brak informacji oznacz jako
  „DO USTALENIA" i wypisz na końcu raportu
- zachowaj wszystkie liczby, progi i nazwy pól dokładnie jak w źródle

Na koniec podaj: listę utworzonych plików z liczbą linii oraz listę
pozycji DO USTALENIA.
```

## 7.3 Weryfikacja po każdej partii

```bash
wc -l docs/spec/*.md | sort -rn | head        # żaden > 400
grep -c "DO USTALENIA" docs/spec/*.md          # przejrzyj każdą
grep -o "\[\[M-[0-9]*\]\]" docs/spec/*.md | sort -u   # czy odsyłacze istnieją
```

Wyrywkowo: weź trzy reguły biznesowe z losowego pliku i sprawdź w źródle,
czy liczby się zgadzają. Jeśli choć jedna nie — powtórz partię.

## 7.4 Po kompilacji

```bash
git mv docs/_source ../_source_archive   # poza repozytorium
```

Aneksy zostają u ciebie jako materiał, ale przestają być częścią projektu.

---

# CZĘŚĆ 8 — SZKIELETY DOKUMENTÓW WŁASNYCH

Te dwa piszesz sam. Agent ich nie napisze, bo to twoja wiedza domenowa.

## `docs/GLOSSARY.md`

Rejestr nazw. Zapobiega temu, żeby ta sama rzecz miała trzy nazwy w kodzie.

```markdown
# Słownik

Zasada: nazwa z tej listy jest jedyną dopuszczalną w kodzie.
Nowe pojęcie → najpierw wpis tutaj, potem kod.

| PL | EN (kod) | Definicja | Nie mylić z |
|---|---|---|---|
| stawka zakupowa | `rate_line` | pojedyncza pozycja cenowa od dostawcy | oferta |
| cennik | `rate_sheet` | jedna dostawa stawek od dostawcy | taryfa |
| oferta | `quotation` | propozycja cenowa dla klienta | zapytanie |
| zapytanie klienta | `rfq` | prośba klienta o wycenę | zapytanie do agenta |
| zapytanie do agenta | `rate_request` | prośba o stawkę wysłana do dostawcy | rfq |
| zlecenie | `shipment` | przyjęte do realizacji | booking |
| opłata | `charge` | pozycja kosztowa z kupnem i sprzedażą | stawka |
| kod opłaty | `charge_code` | pozycja słownika opłat | opłata |
| luka | `quotation_gap` | brakująca pozycja wykryta przy wycenie | błąd |
| waga obliczeniowa | `chargeable_wm` | większa z: tony, CBM; minimum wg cennika | waga brutto |
| przejazd | `tour` | kurs pojazdu jako jednostka kosztowa | zlecenie |
| doładunek | `part_load` | ładunek dokładany do zajętego pojazdu | drobnica |
| tenant | `organization` | firma korzystająca z systemu | klient |
| klient | `party` z rolą `customer` | odbiorca usługi spedycyjnej | tenant |

## Terminy, których nie tłumaczymy
cut-off · rollover · demurrage · detention · free time · incoterm ·
transshipment · blank sailing · GRI · PSS · THC · VGM
```

## `docs/ARCHITECTURE.md`

Mapa dla agenta. Dzięki niej nie przeszukuje repozytorium.

```markdown
# Architektura

## Mapa katalogów
| Ścieżka | Co tam jest | Kto może importować |
|---|---|---|
| `backend/app/api/` | routery, DTO | — |
| `backend/app/workflows/` | Temporal | — |
| `backend/app/services/<moduł>/` | logika domenowa | api, workflows |
| `backend/app/repositories/` | dostęp do danych | services |
| `backend/app/models/` | SQLAlchemy | repositories |
| `backend/app/domain/` | typy, wyjątki, wartości | wszyscy |
| `backend/app/integrations/` | adaptery zewnętrzne | api, workflows |
| `frontend/src/features/<moduł>/` | pion modułu | — |
| `frontend/src/components/ui/` | shadcn, skopiowane | features |
| `frontend/src/api/` | generowane z OpenAPI | features (tylko odczyt) |

## Mapa modułów na katalogi
| Moduł | Backend | Frontend |
|---|---|---|
| M-17, M-18, M-19, M-20 | `services/rates/` | `features/rates/` |
| M-21…M-27 | `services/quotation/` | `features/quotation/` |
| M-28…M-31 | `services/rfq/` | `features/rfq/` |
| M-35…M-39 | `services/shipment/` | `features/shipment/` |
| M-40…M-47 | `services/finance/` | `features/finance/` |
| M-53…M-56 | `services/compliance/` | `features/compliance/` |

## Gdzie czego szukać
| Szukasz | Idź do |
|---|---|
| jak liczy się marża | `services/quotation/margin.py` |
| jak dobierane są stawki | `repositories/rates/candidates.sql` |
| jak mapowane są opłaty | `services/rates/normalization.py` |
| wzorzec testu izolacji | `tests/patterns/tenant_isolation.py` |
| jak dodać armatora | `.cursor/skills/adapter-armatora/` |

## Zakazy strukturalne
- serwis nie importuje z api
- integracja nie importuje z serwisu
- domena nie importuje niczego zewnętrznego
- frontend nie edytuje `src/api/`
```

---

# CZĘŚĆ 9 — DANE POCZĄTKOWE

## `backend/app/seeds/charge_codes.yaml` — fragment wzorcowy

Pełny słownik ma około 60 pozycji w pięciu grupach (`ANEKS-13` i
`spec-wyceny-morskie-ai-stawki.md`). Format:

```yaml
- code: OTHC
  name_pl: Terminal Handling Charge — origin
  name_en: Origin Terminal Handling Charge
  category: local
  side: origin
  default_basis: PER_CONTAINER
  applies_to: [FCL, LCL]
  required_for_incoterms: [FCA, FOB, CFR, CIF, CPT, CIP, DAP, DPU, DDP]
  aliases:
    - THC
    - THC ORIGIN
    - O/THC
    - TERMINAL HANDLING
    - TERMINAL HANDLING CHARGE POL
    - THC AT ORIGIN
    - OPŁATA TERMINALOWA
    - 起运港码头费
    - ORIGIN THC

- code: DEMUR
  name_pl: Demurrage
  name_en: Demurrage
  category: local
  side: destination
  default_basis: PER_CONTAINER_DAY
  applies_to: [FCL]
  has_free_time: true
  aliases: [DEM, DEMURRAGE, PRZESTÓJ KONTENERA, 滞期费]

- code: ETS
  name_pl: Dodatek emisyjny EU ETS
  name_en: EU ETS Surcharge
  category: freight
  side: freight
  default_basis: PER_CONTAINER
  applies_to: [FCL, LCL]
  is_formula: true
  formula_note: faza wdrożenia × emisja relacji × cena EUA
  aliases: [ETS, EU ETS, EMISSION SURCHARGE, ETS SURCHARGE]
```

**Aliasy w czterech językach od startu** — polskim, angielskim, niemieckim
i chińskim. Czekanie, aż nauczą się z korekt, oznacza pierwsze miesiące
z niską skutecznością mapowania.

---

# CZĘŚĆ 10 — DEFINICJA GOTOWOŚCI

Plaster wolno zacząć, gdy delta-spec spełnia wszystkie punkty:

```
□ Zakres opisany w trzech zdaniach albo mniej
□ „Poza zakresem" wypełnione — ważniejsze od zakresu
□ Wskazana sekcja spec źródłowej
□ Zależności od innych plastrów zamknięte
□ Kryteria akceptacji sprawdzalne maszynowo
□ Brak pozycji DO USTALENIA
□ Jeśli nowa tabela — zaplanowany test izolacji
□ Jeśli ścieżka krytyczna — podany budżet
```

Nieukończona delta-spec to najczęstsza przyczyna błądzenia agenta.
Piętnaście minut tutaj oszczędza godziny później.

---

# CZĘŚĆ 11 — GDY COŚ PÓJDZIE ŹLE

## 11.1 Izolacja pracy

```bash
git worktree add ../work-2.4 -b plaster/2.4
cd ../work-2.4
```

Każdy plaster w osobnym drzewie roboczym. Gałąź główna zawsze zielona,
a porzucenie nieudanego plastra to usunięcie katalogu.

## 11.2 Punkty kontrolne w trakcie

```bash
git commit -am "wip: <co działa>" --no-verify
```

Co 30–40 minut pracy agenta. `--no-verify` pomija hooki przy commitach roboczych.
Przed PR: `git rebase -i` i sprzątasz historię do jednego commita.

## 11.3 Kiedy przerwać agenta

Twarde sygnały, przy których zatrzymujesz i zaczynasz od nowa:

| Sygnał | Reakcja |
|---|---|
| Trzecia nieudana próba naprawy tego samego błędu | stop, nowa rozmowa z opisem błędu |
| Agent dotyka plików spoza zakresu | stop, doprecyzuj zakres w delta-spec |
| Wyłącza reguły lintera albo dodaje `noqa` | stop, to jest obchodzenie bramki |
| Zmienia testy, żeby przechodziły | stop, poważne — testy są kontraktem |
| Kontekst przekracza połowę okna | zamknij, przenieś ustalenia do CURRENT.md |

## 11.4 Odzyskiwanie

```bash
git reset --hard HEAD~N            # cofnięcie do ostatniego działającego
git worktree remove ../work-2.4    # porzucenie plastra
just migrate-down                  # cofnięcie migracji
```

Baza: Neon z gałęzią per pull request — reset to usunięcie gałęzi.

---

# CZĘŚĆ 12 — PRZYKŁAD PRZEROBIONY: PLASTER 0.3

Pełny przebieg, od pustego repozytorium do zielonej bramki.

## Krok 1 — delta-spec

`docs/deltas/open/0.3.md`:

```markdown
# Plaster 0.3 · M-01 Wielodostępność
**Spec:** docs/spec/tenancy.md, sekcje 1–3
**Zależy od:** 0.1, 0.2

## Zakres
Tabele `organization`, `app_user`, `role`, `user_role`. Polityki RLS na
poziomie bazy. Kontekst tenanta ustawiany w sesji SQLAlchemy.

## Poza zakresem
OpenFGA i uprawnienia szczegółowe (0.8). Audit log (0.4). Metering (0.4).
Rejestracja i logowanie użytkownika.

## Ustalenia
- `FORCE ROW LEVEL SECURITY`, nie tylko `ENABLE` — bez tego właściciel
  tabeli omija politykę
- kontekst przez `SET LOCAL app.current_org`, nie przez parametr zapytania
- `role.permissions` jako `jsonb`, uszczegółowienie w 0.8

## Kryteria akceptacji
- [ ] Rekord organizacji A niewidoczny w kontekście organizacji B
- [ ] Próba aktualizacji między tenantami kończy się błędem
- [ ] Zapytanie bez ustawionego kontekstu nie zwraca nic
- [ ] `just migrate-down` przechodzi
- [ ] `just arch` przechodzi
```

## Krok 2 — sesja w Cursorze

```
[przypnij tryb: nowy-plaster, Opt+Enter z /]

/goal Plaster 0.3 przechodzi `just gate` i spełnia cztery kryteria
      z docs/deltas/open/0.3.md

/plaster
```

Agent: uruchamia łowcę duplikatów (werdykt: BRAK — pierwsze tabele w repo),
czyta `docs/spec/tenancy.md`, sprawdza schemat przez MCP, przedstawia plan.

Ty: sprawdzasz, czy w planie jest `FORCE ROW LEVEL SECURITY`. Akceptujesz.

## Krok 3 — testy przed implementacją

```
/testy
```

Agent generuje `tests/test_tenant_isolation.py` z czterema testami.
Uruchamia `pytest` — wszystkie failują, bo nie ma tabel.

**Tu wnosisz wiedzę domenową.** Sprawdzasz, czy test „zapytanie bez kontekstu
nie zwraca nic" faktycznie nie ustawia `app.current_org`. To jest przypadek,
który agent pominie, bo wygląda jak brak konfiguracji, a jest regułą
bezpieczeństwa.

## Krok 4 — implementacja

```
Zaimplementuj plan tak, żeby testy przeszły.
```

Hook po każdej edycji uruchamia `ruff` i `mypy`. Agent poprawia bez twojego
udziału. Migracja generuje się z MCP, więc kolumny mają właściwe nazwy.

## Krok 5 — weryfikacja

```
/bramka
```

Weryfikator zwraca:

```
Kryterium                                    Werdykt
─────────────────────────────────────────────────────
Rekord A niewidoczny dla B                   PRZESZŁO
Aktualizacja między tenantami blokowana      PRZESZŁO
Zapytanie bez kontekstu zwraca pustkę        NIE
  → policy pozwala na NULL w current_setting
just migrate-down                            PRZESZŁO
just arch                                    PRZESZŁO
```

Poprawka: `current_setting('app.current_org', true)` zwraca NULL zamiast błędu,
więc polityka przepuszcza. Trzeba `AND current_setting(...) IS NOT NULL`.

To jest dokładnie ten rodzaj błędu, którego nie wyłapałby ani linter, ani
przegląd wzrokowy — a wyłapał test, który sam kazałeś napisać.

## Krok 6 — zamknięcie

```
/zamknij
```

Kronikarz scala deltę do `docs/spec/tenancy.md`, dopisuje linię do
`PROGRESS.md`, tworzy commit. Ty otwierasz nową rozmowę i plaster 0.4.

**Czas: 2–3 godziny. Twojego czasu: około 40 minut** — delta-spec,
weryfikacja planu, sprawdzenie testów, decyzja o poprawce.

---

# CZĘŚĆ 13 — CO INSTALUJESZ, ŻEBY TO DZIAŁAŁO

```bash
uv add --dev ruff mypy pytest pytest-cov pytest-asyncio hypothesis \
             testcontainers schemathesis import-linter vulture radon \
             sqlfluff py-spy memray
npm i -g jscpd knip @size-limit/preset-app
brew install just trufflehog trivy k6
```

Bez `radon` nie zadziała `complexity_delta.py`, bez `jscpd` hook przed commitem,
bez `import-linter` cała warstwa granic modułów.
