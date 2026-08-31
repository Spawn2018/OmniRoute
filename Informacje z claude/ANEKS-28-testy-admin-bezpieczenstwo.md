# Aneks 28 — Testowanie, administracja, bezpieczeństwo, optymalizacja

---

# CZĘŚĆ I — M-210 · TESTOWANIE I DIAGNOSTYKA

## I.1 Co już mamy

`pytest` · `hypothesis` · `testcontainers` · `schemathesis` · `playwright` ·
`k6` · `promptfoo` · `deepeval` · `pact` · testy izolacji tenantów ·
testy budżetów wydajności · `axe`.

To jest solidna baza. Brakuje ośmiu rzeczy.

## I.2 Braki

### Zarządzanie danymi testowymi

```sql
test_scenario
  id, name, description
  entity_graph jsonb,      -- kompletny graf: tenant, klient, stawki, oferta
  is_deterministic bool,
  used_by_tests text[]
```

**Fabryki zamiast utrwalonych plików.** Test tworzy dokładnie to, czego
potrzebuje, i sprząta po sobie.

```python
# tests/factories.py
@factory
def quotation_ready_for_booking(org, *, lanes=1, with_gaps=False):
    """Oferta zaakceptowana, gotowa do konwersji na zlecenie."""
```

**Zbiór scenariuszy domenowych** do testów end-to-end: FCL bez luk, FCL z luką
w opłatach lokalnych, LCL poniżej minimum, ładunek ADR z wcześniejszym cut-offem,
klient po limicie kredytowym, trafienie sankcyjne.

### Anonimizacja danych produkcyjnych

Do diagnozy błędów, których nie da się odtworzyć na danych syntetycznych.

```
scripts/anonymize_dump.py
  → nazwy kontrahentów zastąpione
  → NIP-y wygenerowane poprawne strukturalnie
  → kwoty przeskalowane współczynnikiem
  → adresy mailowe na domenę testową
  → zachowana struktura relacji i rozkłady
```

**Nigdy nie kopiuj danych produkcyjnych bez anonimizacji.** To jest naruszenie
umowy powierzenia, nawet na własnym laptopie.

### Testy mutacyjne

Pokrycie mówi, że linia została wykonana. Nie mówi, że test by zauważył błąd.

```bash
mutmut run --paths-to-mutate backend/app/services/quotation/
```

**Stosuj wyłącznie do rdzenia**: silnik wyceny, kaskada narzutów, waga
obliczeniowa, koszt finansowania, przeliczenia walutowe. Uruchamiane
tygodniowo, nie w każdym commicie.

### Wykrywanie testów niestabilnych

```sql
test_run
  id, test_id, run_at, status, duration_ms, commit_sha
flaky_test
  test_id, failure_rate_30d, quarantined_at, quarantine_reason
```

Test, który failuje losowo, uczy ignorowania czerwonego CI. Automatyczna
kwarantanna po trzech losowych porażkach plus zadanie do naprawy.

### Odtwarzanie żądań produkcyjnych ⚠

To jest funkcja diagnostyczna o największej wartości w twojej domenie.

```sql
request_replay
  id, organization_id, correlation_id
  endpoint, method
  request_snapshot jsonb,       -- wejście z anonimizacją
  db_state_refs jsonb,          -- wersje rekordów użytych w obliczeniu
  response_snapshot jsonb, error
  captured_at, replayed_at, replay_result
```

**Scenariusz:** klient zgłasza, że wycena wyszła zła. Dziś: prosisz o zrzut
ekranu i zgadujesz. Z tym: odtwarzasz to samo obliczenie z tymi samymi danymi
wejściowymi i tymi samymi wersjami stawek — i widzisz, gdzie się rozjechało.

Przechwytywanie włączane per endpoint, z próbkowaniem i krótką retencją.

### Wstrzykiwanie awarii

```python
@pytest.mark.chaos
async def test_quote_degrades_when_carrier_api_down(chaos):
    chaos.fail("carrier.hapag", error=TimeoutError, probability=1.0)
    result = await quote_engine.resolve(request)
    assert result.stored_rates          # tło z bazy zostało
    assert "hapag" in result.unavailable
    assert result.partial is True
```

Scenariusze do pokrycia: padnięcie API armatora, timeout KSeF, brak odpowiedzi
wywiadowni, przepełnienie kolejki, utrata połączenia z bazą, wyczerpanie limitu
zapytań u dostawcy.

### Testy kontraktowe frontend–backend

`schemathesis` sprawdza zgodność API ze specyfikacją. Brakuje sprawdzenia,
czy frontend faktycznie używa API zgodnie z typami.

```bash
just api-types && git diff --exit-code frontend/src/api/
```

Rozjazd typów wywala CI, zanim dojdzie do błędu w przeglądarce.

### Obserwowalność testów

```sql
test_metrics
  period, total, passed, failed, skipped, flaky
  duration_p50_ms, duration_p95_ms
  slowest jsonb, most_failing jsonb
  coverage_pct, mutation_score
```

Zestaw testów rosnący w nieskończoność przestaje być uruchamiany.
Mierz go, żeby wiedzieć, kiedy przyciąć.

## I.3 Strategia testów — piramida

```
                    ╱╲
                   ╱E2E╲          ~20 scenariuszy, tylko ścieżki krytyczne
                  ╱──────╲
                 ╱ Integr. ╲      ~200, testcontainers, prawdziwy Postgres
                ╱────────────╲
               ╱  Jednostkowe ╲   ~2000, reguły biznesowe, hypothesis
              ╱────────────────╲
             ╱ Statyczne: mypy,  ╲ każdy commit, hooki
            ╱  ruff, import-linter╲
```

**Ścieżki krytyczne do pokrycia end-to-end:**
zapytanie → wycena → wysyłka · akceptacja → booking → dokumenty ·
faktura → KSeF → płatność → dopasowanie · ekstrakcja → review → stawka →
użycie w ofercie · trafienie sankcyjne → blokada.

## I.4 Diagnostyka produkcyjna

| Narzędzie | Zastosowanie |
|---|---|
| **Identyfikator korelacji** w każdym logu, odpowiedzi i zdarzeniu | prześledzenie żądania przez wszystkie warstwy |
| **OpenTelemetry** ze śladem przez kolejkę i workery | gdzie schodzi czas |
| **Sentry** z kontekstem tenanta i użytkownika | błąd z pełnym kontekstem |
| **`request_replay`** | odtworzenie obliczenia |
| **`decision_log`** (M-181) | dlaczego system wybrał tę stawkę |
| **`py-spy` na produkcji** | profil bez restartu procesu |
| **Tryb diagnostyczny per tenant** | rozszerzone logowanie na godzinę, włączane z konsoli |

**Nakład M-210: 14 dni.** Plastry 0.13 (fabryki i scenariusze), 0.14
(korelacja i telemetria), 3.7 (odtwarzanie żądań), 6.21 (chaos i mutacje).

---

# CZĘŚĆ II — M-211 · KONSOLA ADMINISTRATORA PLATFORMY

Rozszerzenie M-193 do pełnego narzędzia zarządzania.

## II.1 Hierarchia ustawień

Trzypoziomowa, z jasnym pierwszeństwem.

```
domyślne platformy  →  szablon planu  →  ustawienia tenanta  →  nadpisanie
     (twoje)            (Start/Pro)         (klient)          (twoje, ręczne)
```

```sql
platform_setting
  id, key, value jsonb, value_type
  category, description
  is_tenant_overridable bool
  requires_restart bool
  updated_by, updated_at

plan_template
  id, plan_code, name
  settings jsonb, quotas jsonb, features text[]
  price_monthly, currency, is_active

tenant_setting_override
  id, organization_id, key, value jsonb
  reason, set_by, set_at, expires_at
  -- nadpisanie ręczne przez ciebie, np. czasowe zwiększenie limitu
```

**Każde nadpisanie ma powód i osobę.** Bez tego po roku nie wiesz,
dlaczego jeden klient ma inne ustawienia.

## II.2 Cykl życia tenanta

```sql
tenant_lifecycle_event
  id, organization_id
  event,        -- provisioned | activated | plan_changed | suspended
                -- resumed | migrated | offboarding_started | deleted
  from_state, to_state, reason
  performed_by, performed_at, metadata jsonb
```

| Operacja | Co robi | Zabezpieczenie |
|---|---|---|
| Utworzenie | baza, RLS, słowniki, użytkownik administratora, zaproszenie | — |
| Zmiana planu | limity, funkcje, rozliczenie proporcjonalne | zatwierdzenie przy obniżce |
| Zawieszenie | blokada logowania, dane nietknięte, komunikat | powód obowiązkowy |
| Wznowienie | przywrócenie dostępu | — |
| Migracja | przeniesienie do dedykowanej bazy | okno serwisowe, test odtworzenia |
| Zakończenie | eksport, karencja, usunięcie z uwzględnieniem retencji | dwie pary oczu |

## II.3 Statystyki platformy

```sql
platform_kpi
  period, metric, value
  -- mrr | arr | new_tenants | churned | net_revenue_retention
  -- active_users | dau_mau | trial_conversion
  -- ai_cost_total | infra_cost | gross_margin
  -- support_tickets | median_resolution_hours

tenant_health
  organization_id, computed_at
  activity_score,          -- logowania, operacje, ostatnia aktywność
  adoption_score,          -- ile funkcji faktycznie używa
  value_score,             -- zlecenia, oferty, wolumen
  risk_score,              -- spadek aktywności, zgłoszenia, opóźnienia płatności
  health_status,           -- healthy | at_risk | churning | dormant
  drivers jsonb
```

**`tenant_health` jest najważniejszą tabelą w tym module.** Klient nie odchodzi
nagle — przestaje się logować, przestaje wystawiać oferty, zaczyna zgłaszać
problemy. Wskaźnik ryzyka odejścia z trzymiesięcznym wyprzedzeniem daje ci
czas na reakcję.

### Ekrany

| Ekran | Zawartość |
|---|---|
| **Przegląd** | MRR, przyrost, odejścia, tenanci w ryzyku, koszt AI, marża |
| **Tenanci** | lista z kondycją, planem, zużyciem, ostatnią aktywnością |
| **Tenant** | pełny widok: ustawienia, limity, zużycie, historia, zgłoszenia, faktury |
| **Zużycie** | koszt AI per tenant, wywołania API, storage — do wykrycia nierentownych |
| **Kondycja** | ranking ryzyka odejścia z powodami |
| **Operacje** | kolejka błędów integracji, nieudane workflow, martwe zadania |
| **Wsparcie** | zgłoszenia z kontekstem, sesje impersonacji |
| **Audyt** | wszystkie działania administracyjne |

## II.4 Impersonacja — z twardymi zabezpieczeniami

```sql
impersonation_session
  id, support_user_id
  target_organization_id, target_user_id
  reason, ticket_ref
  consent_type,        -- customer_request | contractual | emergency
  started_at, ends_at,  -- limit czasu wymuszony
  actions_performed jsonb,
  was_readonly bool,
  visible_to_customer bool NOT NULL DEFAULT true
```

**Zasady niepodlegające zmianie:**

```
□ powód i numer zgłoszenia obowiązkowe
□ domyślnie tylko odczyt — zapis wymaga osobnego zatwierdzenia
□ sesja wygasa po 60 minutach
□ klient widzi w swoim audycie, kto i kiedy
□ baner w interfejsie: „sesja wsparcia, użytkownik: X"
□ operacje finansowe zablokowane w trybie impersonacji
□ zrzut wszystkich działań do audytu platformy
```

Impersonacja bez śladu to problem prawny i utrata zaufania jednocześnie.

## II.5 Bezpieczeństwo konsoli

Konsola administratora to najwyżej uprzywilejowana powierzchnia w systemie.

```
□ uwierzytelnianie dwuskładnikowe obowiązkowe, bez wyjątków
□ osobna domena, osobna sesja, brak wspólnego logowania z aplikacją
□ ograniczenie adresów IP
□ brak bezpośredniego dostępu do bazy produkcyjnej — wszystko przez API
□ operacje destrukcyjne wymagają potwierdzenia z drugiego kanału
□ pełny audyt z niemożliwością usunięcia wpisów
□ alert przy każdym logowaniu do konsoli
```

**Nakład M-211: 18 dni.** Plastry 0.15 (hierarchia ustawień), 7.21 (cykl życia),
7.22 (statystyki i kondycja), 7.23 (impersonacja i wsparcie).
---

# CZĘŚĆ III — M-212 · BEZPIECZEŃSTWO

Mieliśmy narzędzia rozproszone po modułach. Brakuje warstwy, która to spina
i — co ważne dla sprzedaży — **udowadnia klientowi, że system jest bezpieczny.**

## III.1 Model zagrożeń per moduł

```sql
threat_model
  id, module_code, version
  assets jsonb,           -- co chronimy
  threats jsonb,          -- STRIDE: spoofing, tampering, repudiation,
                          -- information disclosure, DoS, elevation
  mitigations jsonb,      -- co robimy, gdzie w kodzie
  residual_risk,          -- co zostaje i dlaczego akceptujemy
  reviewed_by, reviewed_at, next_review_at
```

**Obowiązkowy dla ośmiu modułów o podwyższonym ryzyku:** M-01 wielodostępność,
M-19 poświadczenia armatorów, M-20 ekstrakcja z niezaufanych plików,
M-100 widoczność kosztów, M-207 finansowanie, M-209 płatności,
M-211 konsola administratora, M-94 publiczne API.

## III.2 Testowanie bezpieczeństwa w potoku

| Etap | Narzędzie | Blokuje |
|---|---|---|
| Przy edycji (hook) | `trufflehog` | sekrety w kodzie |
| Commit | `gitleaks` | sekrety w historii |
| CI — analiza statyczna | `semgrep`, `bandit`, `ruff S` | wzorce podatne |
| CI — zależności | `pip-audit`, `pnpm audit`, `osv-scanner` | znane podatności |
| CI — kontenery | `trivy` | podatności w obrazie |
| CI — infrastruktura | `checkov` | błędna konfiguracja |
| CI — API | `schemathesis` z profilem bezpieczeństwa | brak autoryzacji na endpoincie |
| Nocnie | `zaproxy` na środowisku testowym | podatności dynamiczne |
| Tygodniowo | `garak` | podatności warstwy AI |
| Kwartalnie | testy penetracyjne zewnętrzne | reszta |

### Testy bezpieczeństwa jako kod

```python
@pytest.mark.security
class TestTenantIsolation:
    async def test_cannot_read_other_tenant_by_id(self, org_a, org_b): ...
    async def test_cannot_enumerate_other_tenant_ids(self): ...
    async def test_api_key_scoped_to_tenant(self): ...
    async def test_export_respects_cost_visibility(self, sales_user): ...

@pytest.mark.security
class TestAuthorization:
    async def test_every_endpoint_declares_permission(self):
        """Endpoint bez jawnej deklaracji uprawnień = błąd."""
        for route in app.routes:
            assert hasattr(route.endpoint, "__permission__"), route.path

@pytest.mark.security
class TestPromptInjection:
    async def test_instruction_in_excel_cell_ignored(self): ...
    async def test_extraction_output_schema_enforced(self): ...
```

**Test „każdy endpoint deklaruje uprawnienie" jest najważniejszy z tej grupy.**
Zapomniana autoryzacja to najczęstsza poważna podatność w aplikacjach
wielodostępnych.

## III.3 Zarządzanie podatnościami

```sql
vulnerability
  id, source,        -- scanner | pentest | bug_bounty | disclosure | internal
  cve_id, component, version_affected
  severity,          -- critical | high | medium | low
  cvss_score, description, affected_modules text[]
  discovered_at, sla_due_at
  status,            -- open | triaged | in_progress | fixed
                     -- accepted_risk | false_positive
  fixed_in_version, fixed_at, verified_by
  customer_notification_required bool
```

**Umowy dotyczące czasu naprawy:**

| Waga | Naprawa | Powiadomienie klientów |
|---|---|---|
| Krytyczna | 24 h | natychmiast, jeśli dotyczy ich danych |
| Wysoka | 7 dni | w podsumowaniu miesięcznym |
| Średnia | 30 dni | w changelogu |
| Niska | 90 dni | — |

## III.4 Reagowanie na incydenty

```sql
security_incident
  id, severity,      -- P1 | P2 | P3 | P4
  category,          -- data_breach | unauthorized_access | availability
                     -- integrity | supply_chain | fraud
  detected_at, detected_by, contained_at, resolved_at
  affected_tenants uuid[], affected_records_estimate
  requires_gdpr_notification bool,
  gdpr_notified_at,              -- 72 h od stwierdzenia
  requires_customer_notification bool, customers_notified_at
  root_cause, corrective_actions jsonb
  postmortem_path
```

**Klasyfikacja i czasy:**

| Poziom | Definicja | Reakcja | Zawiadomienie |
|---|---|---|---|
| **P1** | wyciek danych, dostęp międzytenantowy | 15 min | organ nadzorczy w 72 h, klienci niezwłocznie |
| **P2** | nieuprawniony dostęp bez wycieku, niedostępność | 1 h | klienci w 24 h |
| **P3** | podatność wykorzystywalna, bez dowodu wykorzystania | 4 h | w podsumowaniu |
| **P4** | podatność teoretyczna | 1 dzień roboczy | changelog |

**Scenariusz P1 „klient widzi cudze dane" wymaga runbooka napisanego wcześniej.**
To jest jedyny incydent, który może zakończyć produkt, i jedyny, przy którym
nie będziesz w stanie myśleć spokojnie.

## III.5 Centrum zaufania — to, o co pytałeś ⚠

Publiczna strona z rzetelnymi danymi dla potencjalnych klientów. **Funkcja
sprzedażowa, nie techniczna.**

```
trust.twojadomena.pl

┌─ DOSTĘPNOŚĆ ────────────────────────────────────────┐
│ Ostatnie 90 dni:        99,94%                      │
│ Incydenty:              2 (P3, P4) — szczegóły      │
│ Czas odpowiedzi p95:    142 ms                      │
│ Wykres 90 dni, dane z monitoringu, nie deklaracje   │
└─────────────────────────────────────────────────────┘

┌─ BEZPIECZEŃSTWO ────────────────────────────────────┐
│ Ostatni test penetracyjny:  2026-07-15, [raport]    │
│   ustalenia: 0 krytycznych, 1 wysokie (naprawione)  │
│ Skanowanie zależności:      codziennie              │
│ Otwarte podatności:         0 krytycznych, 2 niskie │
│ SBOM:                       [pobierz CycloneDX]     │
│ Zgłaszanie podatności:      [polityka]              │
└─────────────────────────────────────────────────────┘

┌─ DANE ──────────────────────────────────────────────┐
│ Lokalizacja:            Niemcy (UE)                 │
│ Szyfrowanie w spoczynku: AES-256                    │
│ Szyfrowanie w transporcie: TLS 1.3                  │
│ Kopie zapasowe:         co godzinę, PITR 30 dni     │
│ Ostatni test odtworzenia: 2026-08-25, 14 min        │
│ Podprzetwarzający:      [lista]                     │
│ Umowa powierzenia:      [wzór do pobrania]          │
└─────────────────────────────────────────────────────┘

┌─ SYSTEMY AI ────────────────────────────────────────┐
│ Gdzie używamy AI:       [inwentarz]                 │
│ Klasyfikacja ryzyka:    brak systemów wysokiego     │
│                         ryzyka wg AI Act            │
│ Przetwarzanie lokalne:  dostępne na życzenie        │
│ Dane treningowe:        nie używamy danych klientów │
└─────────────────────────────────────────────────────┘
```

**Ostatni punkt jest istotny handlowo.** Deklaracja, że dane klienta nie służą
do trenowania modeli, zdejmuje najczęstszą obawę przy sprzedaży oprogramowania
z AI.

### Gotowe odpowiedzi na kwestionariusze

```sql
security_questionnaire_answer
  id, standard,      -- caiq | sig_lite | custom | iso27001_soa
  question_ref, question_text, answer, evidence_ref
  last_verified_at, verified_by
```

Pierwszy większy klient przyśle kwestionariusz bezpieczeństwa na 150 pytań.
Odpowiedzi przygotowane wcześniej to różnica między tygodniem a godziną —
i między wrażeniem firmy dojrzałej a improwizującej.

## III.6 Metryki bezpieczeństwa

```sql
security_metric
  period
  vulnerabilities_open_by_severity jsonb
  mean_time_to_remediate_hours jsonb
  failed_login_attempts, blocked_ips
  impersonation_sessions, admin_actions
  security_tests_passed_pct
  dependencies_outdated, sbom_components
  incidents_by_severity jsonb
```

**Nakład M-212: 16 dni.** Plastry 0.16 (skanowanie w CI, testy bezpieczeństwa),
0.17 (SBOM, polityka ujawniania), 7.24 (zarządzanie podatnościami i incydentami),
8.20 (centrum zaufania i kwestionariusze).

---

# CZĘŚĆ IV — ANALIZA OPTYMALIZACYJNA

## IV.1 Konsolidacja — trzy nakładające się moduły

Przy 212 modułach pojawiły się dublety. Znalazłem trzy.

| Konflikt | Rozstrzygnięcie |
|---|---|
| M-13 karta wyników kontrahenta ↔ M-200 ocena przewoźnika | **Scal w M-13** z dyskryminatorem roli. Ta sama logika, inne metryki per rola |
| M-79 załącznik ↔ M-205 wymagalność | **Zostają osobno**, ale `attachment` przejmuje `document_kind` i daty ważności — bez tego checklist nie działa |
| M-193 konsola operatora ↔ M-211 administracja | **Scal w M-211.** M-193 był szkicem |

**Efekt: 212 → 210 modułów.** Warto to zrobić teraz, przed kompilacją
specyfikacji, bo później dwie specyfikacje opisujące to samo się rozjadą.

## IV.2 Przyspieszenia, których jeszcze nie ująłem

| Problem | Rozwiązanie | Zysk |
|---|---|---|
| Odpytywanie tabeli `outbox` w pętli | `LISTEN/NOTIFY` zamiast pollingu | opóźnienie z sekund do milisekund, mniej obciążenia bazy |
| Odświeżanie widoków materializowanych blokuje odczyt | `REFRESH MATERIALIZED VIEW CONCURRENTLY` | brak blokady, wymaga indeksu unikalnego |
| Nadmiar kolumn `jsonb` | Wynieś często filtrowane pola do kolumn | indeksy działają, plany zapytań lepsze |
| Brak puli połączeń per tenant | `PgCat` z routingiem po tenancie | jeden tenant nie wyczerpuje puli |
| Raporty na bazie głównej | Wymuszenie repliki testem architektonicznym | wycena nie zwalnia przy raportowaniu |
| Ekstrakcja w tym samym procesie co API | Osobna kolejka i workery z limitem pamięci | duży cennik nie spowalnia wycen |
| Pełny zestaw testów przy każdym commicie | Testy wybierane po zmienionych plikach | pętla zwrotna z minut do sekund |
| Paczka frontendu jako całość | Podział po `features/<moduł>` z prefetch przy najechaniu | pierwsze wejście szybsze, nawigacja natychmiastowa |
| Brak buforowania promptu | Schemat i instrukcje z cache | rachunek za AI niższy o rząd wielkości |
| Sekwencyjne wywołania armatorów | `asyncio.gather` z limitem czasu — **było w planie, wymaga testu** | pierwszy wynik poniżej sekundy |

## IV.3 Refaktoryzacje do zaplanowania

**R-06 · Wydzielenie warstwy zapytań odczytowych.**
Repozytoria zapisu i odczytu jako osobne klasy. Odczytowe mogą używać
surowego SQL, denormalizacji i repliki bez wpływu na spójność zapisu.

**R-07 · Ujednolicenie wzorca „wartość wyliczana".**
Mamy `FINCOST`, `FXDIFF`, `kpi_measurement`, `tenant_health`, `carrier_rating`,
`eligibility_score` — sześć różnych implementacji tego samego pomysłu.
Jeden wzorzec: definicja, wyzwalacz, przeliczanie, przechowywanie, unieważnianie.

**R-08 · Konsolidacja tabel zdarzeniowych.**
`shipment_event`, `market_event`, `security_incident`, `tenant_lifecycle_event`,
`decision_log`, `audit_log` — wspólna strategia partycjonowania i retencji
zamiast sześciu osobnych.

**R-09 · Ujednolicenie kolejek.**
Temporal, Hatchet, procrastinate i outbox to cztery mechanizmy asynchroniczne.
Spisz jasną zasadę, co gdzie trafia, zanim powstanie piąty.

```
Temporal      → procesy wielogodzinne z timerami i sygnałami
Hatchet       → zadania krótkie ze sprawiedliwością per tenant
procrastinate → zadania cykliczne, harmonogram
outbox        → wyłącznie zdarzenia domenowe między modułami
```

## IV.4 Co pominęliśmy

Trzy rzeczy wyszły przy tym przeglądzie.

**Wersjonowanie API od pierwszego endpointu.** Mamy `/v1/` w planie, ale nie ma
polityki deprecacji ani mechanizmu równoległego działania wersji. Po pierwszej
integracji klienta nie możesz zepsuć kontraktu.

**Limity zapytań per klucz API.** Publiczne API bez ograniczeń to zaproszenie
do wyczerpania zasobów przez jednego integratora.

**Kolejka priorytetowa dla operacji interaktywnych.** Wycena wykonywana przez
użytkownika czekającego na ekranie musi mieć pierwszeństwo przed przetwarzaniem
wsadowym cenników. Dziś obie trafiają do tej samej kolejki.
