# Rewizja stosu — co bym zmienił

Krytyczny przegląd własnych rekomendacji pod kątem docelowej skali:
wielu tenantów, wielu użytkowników, ruch produkcyjny.

---

# CZĘŚĆ 1 — SIEDEM POPRAWEK

## 1.1 Silnik wyceny musi być SQL-owy, nie aplikacyjny ⚠ krytyczne

**Co zaproponowałem:** kaskada reguł i dobór stawek w warstwie serwisów Pythona.

**Dlaczego to błąd:** dobór stawek to filtrowanie i sortowanie po kilkudziesięciu
tysiącach wierszy z siedmioma wymiarami dopasowania. To jest zadanie bazy danych.
Wciągnięcie tego do Pythona oznacza przesłanie tysięcy wierszy przez sieć i
przetworzenie ich w języku, który jest w tym wolny. Przy dwudziestu tenantach i
kilkuset wycenach dziennie przekroczysz budżet 300 ms i zaczniesz optymalizować
coś, czego nie trzeba było tak pisać.

**Poprawka:**

```sql
-- dobór kandydatów: jedno zapytanie, nie pętla w Pythonie
CREATE INDEX idx_rate_lookup ON rate_line
  (organization_id, pol, pod, mode, charge_code, container_type)
  INCLUDE (amount, currency, basis, valid_from, valid_to)
  WHERE superseded_by IS NULL;

-- kaskada narzutów: rozstrzygana funkcją SQL po specificity_score,
-- nie siedmioma zapytaniami z warstwy aplikacji

-- widok materializowany na najczęstsze relacje per tenant,
-- odświeżany przy zmianie cennika, nie przy zapytaniu
```

**Zasada do wpisania w `AGENTS.md`:** *nie licz w Pythonie tego, co Postgres
policzy z indeksem.* Python orkiestruje, waliduje i formatuje. Nie filtruje
dziesiątek tysięcy wierszy.

## 1.2 Pętla RFQ to trwały workflow, nie zadania w cronie ⚠ krytyczne

**Co zaproponowałem:** `procrastinate` plus zadania cykliczne do przypomnień.

**Dlaczego to błąd:** proces „wyślij do pięciu agentów, czekaj do 48 h, po 24 h
przypomnij tym, którzy milczą, po terminie zamknij i porównaj" to workflow z
timerami, ponowieniami i człowiekiem w środku. Realizowany krokami w kolejce plus
cron oznacza własną implementację maszyny stanów rozsypanej po tabelach — i utratę
zadań przy każdym restarcie.

**Poprawka: `temporalio/temporal`.** To jest podręcznikowe zastosowanie: workflow
żyjący dobę, z timerami, sygnałami z zewnątrz (odpowiedź agenta jako sygnał),
ponowieniami i pełną historią wykonania. Restart procesu nie gubi stanu.

```python
@workflow.defn
class RateRequestWorkflow:
    @workflow.run
    async def run(self, req: RateRequest) -> Comparison:
        await workflow.execute_activity(send_to_agents, req)

        await workflow.wait_condition(
            lambda: self.all_responded,
            timeout=req.deadline / 2,
        )
        if not self.all_responded:
            await workflow.execute_activity(send_reminders, self.pending)

        await workflow.wait_condition(
            lambda: self.all_responded,
            timeout=req.deadline / 2,
        )
        return await workflow.execute_activity(build_comparison, req)

    @workflow.signal
    def agent_responded(self, agent_id: str, sheet_id: str) -> None:
        self.responses[agent_id] = sheet_id
```

Ta sama technologia obsłuży pipeline ekstrakcji z kolejką akceptacji i proces
bookingu z kompensacją. `procrastinate` zostaje do zadań prostych i cyklicznych.

## 1.3 Kolejka musi być świadoma tenantów

**Czego nie przewidziałem:** jeden tenant wrzuca pięćset cenników do przetworzenia
i zajmuje wszystkie procesy robocze. Pozostali czekają. Przy modelu SaaS to jest
awaria, nie niedogodność.

**Poprawka:** kolejka z kluczami współbieżności per tenant. `Hatchet` obsługuje to
natywnie (limity współbieżności z kluczem grupującym), Temporal przez oddzielne
kolejki zadań. Minimum: limit równoległych zadań per `organization_id` i
kolejkowanie sprawiedliwe, nie FIFO globalne.

## 1.4 Ścieżka wyjścia z jednej bazy — zaprojektuj teraz, użyj później

**Co zaproponowałem:** wspólny schemat z RLS. To jest dobry wybór domyślny.

**Czego brakowało:** planu na moment, gdy duży klient zażąda własnej bazy albo
gdy jeden tenant urośnie nieproporcjonalnie.

**Poprawka — trzy poziomy, ten sam kod:**

| Poziom | Kiedy | Jak |
|---|---|---|
| Wspólny schemat + RLS | domyślnie | jak dziś |
| Sharding po `organization_id` | przy dużym wolumenie | `citusdata/citus`, tabele dystrybuowane kluczem tenanta |
| Osobna baza | klient korporacyjny, wymóg umowny | routing połączenia po tenancie |

Warunek, żeby to było możliwe bez przepisywania: **żadne zapytanie w systemie
nigdy nie sięga po dane więcej niż jednego tenanta.** Zero zapytań
agregujących ponad tenantami — nawet w raportach wewnętrznych. Jeśli tego
pilnujesz od pierwszej migracji, przeniesienie tenanta do osobnej bazy jest
zmianą konfiguracji.

Pooler: zamiast `pgbouncer` rozważ `PgCat` albo `Supavisor` — oba lepiej radzą
sobie z pulami per tenant i routingiem.

## 1.5 Wzorzec outbox i idempotencja — brakowało całkowicie

**Czego nie było:** gwarancji, że wysłany mail, wywołanie API armatora albo
booking nie zginą przy awarii i nie wykonają się dwa razy.

W systemie, który wysyła zapytania w cudzym imieniu i rezerwuje miejsce na
statku, to nie jest szczegół.

```sql
outbox
  id, organization_id
  aggregate_type, aggregate_id
  event_type, payload jsonb
  created_at, published_at, attempts, last_error
  -- zapisywany w tej samej transakcji co zmiana stanu
  -- publikowany osobnym procesem

idempotency_key
  key, organization_id, endpoint
  request_hash, response jsonb, created_at
  -- każde wywołanie zewnętrzne i każdy zapis przez API
```

Bez outboxa scenariusz „zapisaliśmy zlecenie, ale mail nie wyszedł, bo padł
proces" zdarzy się w pierwszym miesiącu produkcji.

## 1.6 Repliki do odczytu i rozdzielenie ścieżek

**Czego nie przewidziałem:** raporty analityczne na bazie produkcyjnej. Raport
struktury marży za dwanaście miesięcy przy dwudziestu tenantach potrafi zablokować
wyceny.

**Poprawka:**
- replika do odczytu dla raportów, analityki i text-to-SQL
- `duckdb` na wyeksportowanych paczkach dla ciężkiej analityki historycznej
- routing na poziomie repozytorium: `@read_replica` na metodach raportowych
- twarda zasada: żadne zapytanie z warstwy raportowej nie idzie na bazę główną

## 1.7 Strumieniowanie wyników wyceny — nie określiłem transportu

**Czego brakowało:** napisałem „wyniki spływają w miarę odpowiedzi armatorów",
ale nie powiedziałem czym.

**Poprawka: Server-Sent Events.** Prostsze od WebSocketów, wystarczające dla
jednokierunkowego strumienia, działa przez zwykły HTTP i proxy.

```
GET /api/quotations/{id}/stream
→ event: rates_from_db     (natychmiast)
→ event: carrier_result    (Hapag, 1,8 s)
→ event: carrier_result    (Maersk, 3,1 s)
→ event: complete
```

Frontend renderuje przyrostowo. To jest różnica między „system wolno działa"
a „system pokazuje wyniki od razu".

---

# CZĘŚĆ 2 — CO ZOSTAJE

Żeby było jasne, co przeglądam, a czego nie zmieniam:

| Wybór | Werdykt |
|---|---|
| PostgreSQL jako jedyna baza | **Zostaje.** Kolejka, wektory, wyszukiwanie pełnotekstowe, JSON — jeden system zamiast pięciu. Przy jednoosobowym zespole to argument decydujący |
| FastAPI | **Zostaje.** Litestar jest szybszy i ma lepsze wstrzykiwanie zależności, ale ekosystem i znajomość u modeli językowych przeważają. Zmiana nie zwróci się |
| SQLAlchemy 2.0 | **Zostaje**, ale z zastrzeżeniem z 1.1: ścieżki gorące na `asyncpg` i surowym SQL |
| React + TanStack + shadcn | **Zostaje.** Dla gęstych danych to najlepszy zestaw w 2026 |
| Alembic | **Zostaje**, choć `atlasgo/atlas` daje czytelniejsze różnice schematu. Rozważ, jeśli migracje zaczną boleć |
| `uvicorn` | **Wymień na `granian`** — serwer ASGI w Rust, zauważalnie szybszy, zgodny interfejs |
| Meilisearch | **Usuń na razie.** Postgres z `pg_trgm` i indeksem GIN wystarczy do wyszukiwania stawek i kontrahentów. Jeden komponent mniej |

---

# CZĘŚĆ 3 — ZREWIDOWANY STOS

```
WARSTWA DANYCH
  PostgreSQL 16 + RLS + pgvector + pg_trgm
  Citus            — sharding po organization_id, gdy zajdzie potrzeba
  PgCat/Supavisor  — pooling świadomy tenantów
  Replika odczytu  — raporty, analityka, text-to-SQL
  Redis            — cache stawek per relacja, sesje, limity
  MinIO            — dokumenty źródłowe, provenance

WARSTWA PROCESÓW
  Temporal         — pętla RFQ, ekstrakcja, booking: workflow trwałe
  Hatchet          — zadania krótkie ze sprawiedliwością per tenant
  procrastinate    — zadania cykliczne (kursy NBP, sankcje, wygasające stawki)
  outbox           — gwarancja dostarczenia zdarzeń

WARSTWA API
  FastAPI + granian
  SSE              — strumieniowanie wyników wyceny
  OpenFGA          — uprawnienia w modelu relacyjnym
  Idempotencja     — na każdym wywołaniu zewnętrznym i zapisie

WARSTWA AI
  instructor + Claude API
  router modeli    — Haiku do klasyfikacji, mocniejszy do ekstrakcji
  prompt caching + Batch API
  llm-guard        — filtr wejścia i wyjścia
  langfuse         — telemetria

FRONTEND
  Aplikacja wewnętrzna:  Vite SPA + TanStack + shadcn
  Portal klienta:        osobna aplikacja SSR — inne wymagania, inne SLA
  openapi-ts             — typy generowane z OpenAPI

OBSERWOWALNOŚĆ
  OpenTelemetry jako jedyna warstwa instrumentacji
  → eksport do Sentry / Grafana / SigNoz
  PostHog — analityka produktowa
```

Rozdzielenie aplikacji wewnętrznej i portalu klienta to poprawka, której
wcześniej nie zrobiłem. Mają inne wymagania wydajnościowe, inne ryzyko i inny
cykl wydawniczy. Wspólny jest tylko backend.

---

# CZĘŚĆ 4 — REPOZYTORIA, KTÓRYCH NIE PODAŁEM

| Repo | Po co |
|---|---|
| `temporalio/temporal` + `temporalio/sdk-python` | Trwałe workflow. **Najważniejszy dodatek na tej liście** |
| `hatchet-dev/hatchet` | Kolejka ze sprawiedliwością per tenant |
| `citusdata/citus` | Sharding po tenancie — podniesione z przypisu |
| `postgresml/pgcat` | Pooler świadomy tenantów |
| `supabase/supavisor` | Alternatywa, pooling per tenant |
| `emmett-framework/granian` | Serwer ASGI w Rust zamiast uvicorna |
| `ariga/atlas` | Migracje deklaratywne z czytelnym diffem |
| `tembo-io/pgmq` | Kolejka jako rozszerzenie Postgresa |
| `grafana/k6` | Testy obciążeniowe w scenariuszach wielotenantowych |
| `pact-foundation/pact-python` | Testy kontraktowe API armatorów — wykrywają zmianę u nich, zanim zepsuje produkcję |
| `open-telemetry/opentelemetry-python` | Podniesione z dodatku do fundamentu |
| `dbos-inc/dbos-transact-py` | Alternatywa dla Temporala, lżejsza, oparta na Postgresie |

---

# CZĘŚĆ 5 — WPŁYW NA PLAN

Zmiany dotyczą trzech plastrów. Reszta bez zmian.

**F0.1 — szkielet.** Dołóż: `granian` zamiast uvicorna, OpenTelemetry od
początku, `outbox` i `idempotency_key` w pierwszej migracji.

**F0.3 — wielodostępność.** Dołóż twardą regułę i test architektoniczny:
żadne zapytanie nie sięga po dane więcej niż jednego tenanta. To jest kontrakt
w `import-linter` i osobny test.

**F1.4 — silnik wyceny.** Przepisz jako SQL-owy od początku. Indeks pokrywający,
funkcja rozstrzygająca kaskadę, widok materializowany na częste relacje.
Test wydajnościowy na 50 tysiącach wierszy jako warunek ukończenia.

**F4.4 — zapytania do agentów.** Zrealizuj na Temporalu, nie na cronie.

Do `AGENTS.md` dopisz trzy zasady:

> 11. Nie licz w Pythonie tego, co Postgres policzy z indeksem.
> 12. Żadne zapytanie nie sięga po dane więcej niż jednego tenanta.
> 13. Każde wywołanie zewnętrzne jest idempotentne. Każde zdarzenie przez outbox.

---

# CZĘŚĆ 6 — CZEGO NIE ZMIENIAM MIMO POKUSY

**Nie przechodzę na mikroserwisy.** Przy jednej osobie to mnożenie problemów
operacyjnych bez korzyści. Modularny monolit z granicami wymuszanymi przez
`import-linter` daje tę samą dyscyplinę bez kosztu rozproszenia. Podział na
serwisy ma sens, gdy masz zespoły, nie gdy masz moduły.

**Nie przechodzę na Rust ani Go.** Kuszące dla wydajności, zabójcze dla tempa.
Jeśli po roku profil wskaże jedną gorącą ścieżkę, wyodrębnisz ją wtedy —
wiedząc, którą.

**Nie dokładam Kafki.** Outbox na Postgresie obsłuży twój wolumen przez lata.
Kafka to komponent, który trzeba utrzymywać, monitorować i rozumieć.

**Nie buduję własnego uwierzytelniania.** OpenFGA plus gotowy dostawca tożsamości.
Uwierzytelnianie napisane samodzielnie to najczęstsze źródło poważnych podatności
w produktach jednoosobowych.

---

# PODSUMOWANIE — TRZY ZMIANY, KTÓRE MAJĄ ZNACZENIE

1. **Silnik wyceny w SQL, nie w Pythonie.** Bez tego nie utrzymasz budżetu
   wydajności i będziesz refaktoryzował rdzeń systemu pod presją.

2. **Temporal do pętli RFQ.** Bez tego napiszesz własną, gorszą maszynę stanów
   i będziesz gubił zapytania przy każdym wdrożeniu.

3. **Outbox i idempotencja od pierwszej migracji.** Bez tego duplikaty bookingów
   i zgubione maile — w systemie, który działa w imieniu klienta.

Pozostałe cztery poprawki są ważne, ale dają się dorobić. Te trzy dotykają
fundamentów.
