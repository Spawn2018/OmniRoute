# Podręcznik pracy z Cursorem

---

# 1. TRYB PRACY — ROZSTRZYGNIĘCIE

## 1.1 Kiedy co

| Sytuacja | Tryb | Dlaczego |
|---|---|---|
| Nowy plaster | **Plan → Agent** | Plan czytasz i poprawiasz zanim powstanie kod |
| Refaktoryzacja wielu plików | **Agent** | Potrzebuje całego zakresu |
| Poprawka w jednym pliku | **Inline (Cmd+K)** | Najtańsze, zero ładowania kontekstu |
| Pytanie o kod | **Ask** | Bez uprawnień zapisu |
| Migracja bazy | **Agent + Postgres MCP** | Musi widzieć aktualny schemat |
| Trudny błąd | **Ask z hipotezami** → inline | Agent „naprawia" objaw, nie przyczynę |
| Zadanie przez całe repo | **Claude Code**, nie Cursor | Cursor gubi kontekst przy 20+ plikach |
| Generowanie typów, migracje | **`just`**, nie agent | Deterministyczne, nie potrzebuje modelu |

## 1.2 Pętla plastra — sześć kroków

```
① PLAN
   Tryb: Plan
   Prompt: "Przeczytaj docs/state/CURRENT.md i docs/spec/quotation.md
            sekcje 3–5. Zaplanuj realizację plastra 2.4.
            Wypisz: pliki do utworzenia, pliki do zmiany, kolejność,
            ryzyka. Nie pisz kodu."
   → czytasz plan, poprawiasz, akceptujesz

② SCHEMAT
   Tryb: Agent + Postgres MCP
   Prompt: "Utwórz migrację według punktu 1 planu.
            Sprawdź aktualny schemat przez MCP przed napisaniem."
   → just migrate-down

③ TEST
   Tryb: Agent
   Prompt: "Napisz testy do reguł z planu. Bez implementacji.
            Testy mają failować."
   → weryfikujesz, czy testy opisują właściwe reguły
     TO JEST NAJWAŻNIEJSZY MOMENT — tu wnosisz wiedzę domenową

④ IMPLEMENTACJA
   Tryb: Agent
   Prompt: "Zaimplementuj tak, żeby testy przeszły. Zgodnie z planem."

⑤ BRAMKA
   just gate
   → jeśli czerwone, wracasz do ④ z konkretnym błędem

⑥ ZAMKNIĘCIE
   Prompt: "Dopisz linię do PROGRESS.md. Zaktualizuj CURRENT.md
            na plaster 2.5."
   → NOWA ROZMOWA
```

**Krok szósty decyduje o koszcie.** Ciągnięcie jednego wątku przez tydzień
oznacza, że każdy prompt niesie historię, której agent nie potrzebuje.

## 1.3 Wzorce promptów

**Plan:**
> Przeczytaj `docs/state/CURRENT.md`. Zaplanuj. Nie pisz kodu.

**Implementacja:**
> Zaimplementuj punkt 3 planu. Tylko ten punkt.

**Poprawka po bramce:**
> `just arch` zgłasza: `app.repositories.rates` importuje
> `app.services.quotation`. Napraw bez zmiany zachowania.

**Refaktoryzacja:**
> W `services/quotation/engine.py` funkcja `resolve_candidates` ma
> złożoność 14. Podziel. Testy muszą przejść bez zmian.

**Czego nie robić:**
> ~~„Zbuduj moduł wyceny"~~ — za szeroki zakres, agent zgadnie granice
> ~~„Popraw to"~~ — bez kryterium
> ~~„Dodaj obsługę błędów"~~ — dostaniesz `try/except Exception` wszędzie

---

# 2. OSZCZĘDZANIE TOKENÓW

Pięć mechanizmów, w kolejności skuteczności:

**① Reguły z `globs`.** Reguła frontendowa nie ładuje się przy migracji.
Tylko `context.mdc` i `no-slop.mdc` mają `alwaysApply`.

**② Jeden plaster = jedna rozmowa.** Największa oszczędność. Nowy plaster,
nowy czat.

**③ Spec rozbita na pliki < 400 linii.** Agent czyta jeden, nie szesnaście
aneksów.

**④ MCP Postgres zamiast czytania modeli.** Zapytanie o schemat kosztuje
kilkadziesiąt tokenów, przeczytanie katalogu `models/` kilkanaście tysięcy.

**⑤ `CURRENT.md` jako brief.** Agent nie musi rekonstruować kontekstu z
rozmowy — dostaje go w jednym pliku, który sam napisałeś.

**Antywzorce:** wklejanie plików zamiast `@ścieżka` · „przeczytaj całe repo
i powiedz mi" · trzymanie jednej rozmowy przez tydzień · pytanie o to samo
dwa razy zamiast zapisania w `DECISIONS.md`.

---

# 3. DŁUG TECHNOLOGICZNY — BLOKOWANY MASZYNOWO

Dyscyplina nie działa. Działa CI, który nie przepuszcza.

| Mechanizm | Blokuje |
|---|---|
| `import-linter` | naruszenie warstw i granic modułów |
| `ruff --select C901` | złożoność > 10 |
| `vulture` / `knip` | martwy kod |
| `jscpd` | duplikacja > 3% |
| `mypy --strict` | brak typów |
| `pytest --cov-fail-under=80` | brak testów |
| `size-limit` | rozrost paczki frontendu |
| `pip-audit` / `pnpm audit` | podatności |
| `renovate` | zaległości w zależnościach |
| `qodo-ai/pr-agent` | brak przeglądu |

## 3.1 Reguła trzech i refaktoryzacja w plastrze

**Trzecie powtórzenie uzasadnia wyodrębnienie. Drugie nie.**

Refaktoryzacja jest **częścią plastra**, nie osobnym zadaniem. Backlog
„do posprzątania" nigdy się nie opróżnia — to jest empiryczne, nie moralne.

Jeśli podczas plastra widzisz, że funkcja przekroczyła złożoność albo powtórzyła
się trzeci raz, poprawiasz w tym samym commicie. CI i tak nie przepuści.

## 3.2 Slot refaktoryzacyjny

Jeden dzień co cztery tygodnie, z konkretnym wejściem:

```
just complexity   → funkcje powyżej progu
just dead         → martwy kod
just dup          → duplikacja
pghero            → brakujące indeksy, wolne zapytania
py-spy            → gorące ścieżki
```

Bez tego wejścia to jest błądzenie po kodzie. Z nim — lista zadań na dzień.

---

# 4. WYDAJNOŚĆ JAKO WARUNEK, NIE ETAP

## 4.1 Test wydajnościowy w każdym plastrze krytycznym

```python
@pytest.mark.perf
async def test_quote_engine_under_budget(bench, rate_lines_50k):
    r = await bench(quote_engine.resolve, sample_request, runs=20)
    assert r.p95_ms < 300, f"budżet 300ms, jest {r.p95_ms}"
```

## 4.2 EXPLAIN w przeglądzie

Każde nowe zapytanie do tabeli powyżej 10 tysięcy wierszy wymaga
`EXPLAIN ANALYZE` w opisie PR. Sekwencyjne skanowanie na `rate_line`
to blokada, nie uwaga.

## 4.3 Profil zamiast zgadywania

Przekroczony budżet → `py-spy record` → widzisz gdzie. Nigdy
„zoptymalizujmy tę pętlę, wygląda podejrzanie".

## 4.4 Frontend

- `size-limit` w CI, budżet 250 kB gzip na paczkę początkową
- Lighthouse CI z progami
- Podział paczek per `features/<moduł>`
- Wirtualizacja obowiązkowa powyżej 500 wierszy

---

# 5. DOKUMENTACJA POWSTAJĄCA SAMA

| Warstwa | Narzędzie | Wyzwalacz |
|---|---|---|
| API | FastAPI → OpenAPI → `scalar` | z kodu |
| Typy frontendu | `hey-api/openapi-ts` | `just api-types` |
| Schemat bazy | `azimutt` | `just erd` |
| Kod | `mkdocs-material` + `mkdocstrings` | z docstringów |
| Decyzje | ADR | reguła: decyzja architektoniczna = ADR |
| Zmiany | `release-please` | z commitów |
| Postęp | `PROGRESS.md` | po każdym plastrze |

**Docstring piszesz tylko tam, gdzie wnosi informację** — reguła biznesowa,
niebanalny algorytm, ograniczenie zewnętrzne. Nie na getterach.

---

# 6. SYSTEM PROJEKTOWY — WYGLĄD NA POZIOMIE

To była najsłabsza część poprzedniej wersji. Konkrety.

## 6.1 Fundament

- **Tailwind v4** z `@theme`, tokeny w **OKLCH** — spójna percepcyjnie jasność
  między odcieniami, poprawne przejścia w trybie ciemnym
- **shadcn/ui** kopiowane do repo i modyfikowane u siebie
- **Geist** albo **Inter Variable** dla interfejsu
- **cmdk** — paleta poleceń, jeden skrót do wszystkiego

## 6.2 Liczby — to jest ten szczegół, który widać

```tsx
// components/ui/money.tsx
<span className="tabular-nums text-right font-medium">
  {formatMoney(amount, currency, locale)}
</span>
```

- `font-variant-numeric: tabular-nums` w każdej tabeli z kwotami — cyfry
  nie skaczą przy przewijaniu
- wyrównanie do prawej, separator tysięcy per locale
- waluta jako element wyciszony, nie równorzędny z kwotą
- wartości ujemne czerwone, nie w nawiasach
- zero jako `—`, nie `0,00`

Spedytor patrzy na kolumny kwot osiem godzin dziennie. To decyduje o odbiorze
jakości produktu bardziej niż cokolwiek innego w interfejsie.

## 6.3 Gęstość i klawiatura

- Tryb kompaktowy jako domyślny dla widoków tabelarycznych
- Pełna ścieżka zapytanie → wycena → wysyłka bez dotykania myszy
- Paleta poleceń: `Cmd+K`
- Wklejanie z Excela wprost do siatki pozycji
- Rejestr skrótów w `lib/shortcuts`, wyświetlany pod `?`

## 6.4 Stany jako komponenty pierwszej klasy

Loading, empty, error i **partial** to osobne komponenty, nie warunki inline.
`partial` jest specyficzny dla twojego produktu: wyniki z bazy są, wyniki z
armatorów jeszcze spływają.

```tsx
<QuoteResults
  stored={storedRates}
  streaming={carrierStream}
  onComplete={...}
/>
```

## 6.5 Ruch

Subtelny, funkcjonalny, `prefers-reduced-motion` respektowany. Animujesz
pojawienie się wyniku z kanału armatorskiego — nie ozdabiasz przycisków.

## 6.6 Kontrola jakości wizualnej

- **Storybook** — komponenty w izolacji, wszystkie stany
- **Playwright** ze zrzutami — regresja wizualna w CI
- **axe** — dostępność jako test, nie dobra wola
- Tryb ciemny testowany równolegle, nie „kiedyś"

---

# 7. NARZĘDZIA PONAD CURSOREM

| Narzędzie | Do czego |
|---|---|
| **Claude Code** | Zadania przez całe repo: migracja wzorca, refaktoryzacja warstwy, kompilacja aneksów do `spec/` |
| **`github/spec-kit`** | Development sterowany specyfikacją — `docs/spec/` jako źródło prawdy |
| **`qodo-ai/pr-agent`** | Automatyczny recenzent. Piszesz sam, nie masz kto cię sprawdzić |
| **Neon** | Gałąź bazy per PR — migracja testowana na realnych danych |
| **`azimuttapp/azimutt`** | Wizualizacja schematu przy 130 tabelach |
| **Storybook** | Katalog komponentów |
| **`PatrickJS/awesome-cursorrules`** | Reguły do adaptacji |
| **`x1xhlol/system-prompts...`** | Nauka konstrukcji promptu na działających przykładach |

---

# 8. PIERWSZE PIĘĆ DNI

**Dzień 1** — szkielet: szablon FastAPI, granian, Docker Compose,
`justfile`, `AGENTS.md`, `.cursor/rules/`, `.importlinter`. CI pusty, zielony.

**Dzień 2** — kompilacja dokumentacji. Aneksy do `docs/_source/`,
zadanie dla Claude Code: rozbicie na 70 plików `docs/spec/`.
`MODULES.md` z rejestru. `ARCHITECTURE.md` i `GLOSSARY.md` piszesz sam —
to twoja wiedza, nie do wygenerowania.

**Dzień 3** — MCP: Postgres, Context7, GitHub. Pierwszy plaster (0.3):
`organization`, RLS, test izolacji. Ten test jest wzorcem dla wszystkich kolejnych.

**Dzień 4** — outbox, idempotencja, OpenTelemetry. Warstwa, której później
nie dołożysz.

**Dzień 5** — pierwszy pion od końca do końca: migracja → repozytorium →
serwis → endpoint → typ → komponent → test. Nieważne jak prosty. Ważne,
żeby cała pętla przeszła raz i żebyś ją znał.

Po piątym dniu masz cykl, który powtarzasz dziewięćdziesiąt sześć razy.

---

# 9. ZASADY, KTÓRE UTRZYMAJĄ TEMPO

**Nie zaczynaj plastra bez `CURRENT.md`.** Piętnaście minut na brief oszczędza
godziny błądzenia agenta.

**Nie akceptuj kodu, którego nie rozumiesz.** Za pół roku będziesz go
debugował o drugiej w nocy.

**Testy reguł biznesowych piszesz z głowy, nie z implementacji.** To jest
jedyna część, której agent nie zrobi za ciebie — i jedyna, która decyduje,
czy system liczy poprawnie.

**Punkt kontrolny po fazie 2 jest realny.** Demo dla trzech spedytorów.
Jeśli nie robi wrażenia, dalsza budowa tego nie naprawi.
