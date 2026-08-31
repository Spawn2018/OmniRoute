# PLAN GŁÓWNY

Dokument nadrzędny. Konsoliduje wszystkie ustalenia z prac projektowych:
specyfikację, 16 aneksów, rewizję stosu, rewizję badawczą, konfigurację Cursora.

**Wersja:** 1.0 · sierpień 2026 · **Autor koncepcji:** Sebastian Bożek, LOGMAR

---

# CZĘŚĆ 0 — DECYZJE, KTÓRE JUŻ ZAPADŁY

Nie wracamy do nich bez nowych danych.

| # | Decyzja | Uzasadnienie |
|---|---|---|
| D-01 | Produkt na sprzedaż, nie narzędzie wewnętrzne | wybór właściciela |
| D-02 | **Wejście modułem stawek, nie pełnym ERP** | cykl sprzedaży 2–6 tyg. zamiast 6–12 mies. |
| D-03 | Wielodostępność od pierwszej migracji | nie da się dorobić |
| D-04 | Konfiguracja jako dane, nie kod | inaczej piąty klient blokuje rozwój |
| D-05 | Księgowość: integracja, nie własna implementacja | odpowiedzialność i czas |
| D-06 | Silnik wyceny w SQL, nie w Pythonie | budżet 300 ms nieosiągalny inaczej |
| D-07 | Pętla RFQ na Temporalu, nie na cronie | timery, sygnały, odporność na restart |
| D-08 | Outbox i idempotencja od pierwszej migracji | działasz w imieniu klienta |
| D-09 | Poświadczenia zewnętrzne należą do tenanta | prawo i brak redystrybucji |
| D-10 | Metodyka: przepływ z limitem 1 + delta-spec + XP | Scrum bezprzedmiotowy przy jednej osobie |
| D-11 | **Wzorzec agentowy: orkiestrator + efemeryczne subagenty** | debata person degraduje wynik i mnoży koszt |
| D-12 | Duplikacja to zagrożenie nr 1, nie złożoność | dane: +81% duplikacji, refaktoryzacja 21%→3,8% |
| D-13 | Środowisko: lokalnie + Oracle Always Free do pierwszego klienta | 0 zł, przejście na Hetzner przy pierwszej umowie |
| D-14 | Agregatorzy dopiero po pierwszych klientach | zasięg mniejszy niż marketing sugeruje |

---

# CZĘŚĆ I — PRODUKT

## I.1 Czym to jest

Platforma zarządzania stawkami zakupowymi i ofertowania dla spedycji morskiej
i drogowej, rozwijana w kierunku pełnego ERP.

**Trzy filary, których nie ma razem żaden system w segmencie:**

1. **Automatyczna baza cen zakupowych** — cennik z maila, Excela albo PDF
   jest w systemie po minucie, ze śladem pochodzenia
2. **Kanałowa integracja z armatorami** — API u największych, agregator
   u średnich, **mail automatyczny u całej reszty świata**
3. **Zamknięta pętla** — od maila klienta przez zapytanie do agentów po
   rozliczenie faktury i koszt kapitału

## I.2 Profil klienta

Spedytor morski z własną bazą stawek i co najmniej dwiema osobami w ofertowaniu.
Ból: cenniki w Excelu, oferta liczona 40 minut, zapomniane dopłaty, brak wiedzy
o rzeczywistej rentowności, sześć zakładek przeglądarki rano.

**Do policzenia w tygodniu 0:** ile takich firm jest w Polsce i regionie.
To rozstrzyga, czy budujesz produkt, czy bardzo dobre narzędzie dla siebie.

## I.3 Model biznesowy

| Element | Ustalenie |
|---|---|
| Metryka | abonament bazowy + per użytkownik + limit cenników |
| Poziom | 1 000–2 500 zł/mies. dla małego spedytora |
| Punkt odniesienia dla klienta | koszt etatu (8–12 tys. zł), nie konkurencyjny software |
| Wariant dodatkowy | prowizja od odzysku z modułu rozliczeń faktur |
| Koszt krańcowy klienta | 60–95 zł/mies. |
| Marża brutto | powyżej 90% |

## I.4 Argument sprzedażowy

Nie „automatyzacja" i nie „AI". Dwie liczby:
- godziny miesięcznie na wprowadzanie cenników i liczenie ofert
- wartość jednej pominiętej dopłaty razy częstotliwość

Plus metryka `time_to_quote` zmierzona przed i po.

## I.5 Trzy sprawy do załatwienia przed pierwszą umową

**Konflikt interesów z H&H Logistics.** Sprzedajesz narzędzie ich konkurencji.
Rozmowa przed, nie po. Wpływa na architekturę, jeśli produkt ma być w osobnym
podmiocie.

**Umowa powierzenia z ujawnieniem podpowierzenia.** Wysyłasz cenniki klienta
do zewnętrznego API modelu. Musi być w umowie z nazwą dostawcy i lokalizacją.
Plus przełącznik przetwarzania wyłącznie lokalnego.

**Ograniczenie odpowiedzialności i OC IT.** System liczy ceny. Błąd to szkoda
majątkowa. Odpowiedzialność do wysokości opłat z 12 miesięcy, szkody pośrednie
wyłączone.

---

# CZĘŚĆ II — ARCHITEKTURA

## II.1 Czternaście zasad

Wygrywają z każdą inną sugestią, także z sugestią agenta.

1. `organization_id` w każdej tabeli. RLS wymuszany przez bazę.
2. Konfiguracja jest danymi, nie kodem.
3. `charge` to jedyne miejsce prawdy o marży.
4. Model wyciąga dane. Kod je przetwarza. **Model nigdy nie liczy.**
5. Każda stawka ma `source_ref`.
6. Stawki niemutowalne. Zmiana to nowy rekord i `superseded_by`.
7. Kwoty jako `Decimal`. Waluta nierozerwalnie z kwotą.
8. Nic z ekstrakcji nie wchodzi bez akceptacji człowieka.
9. Poświadczenia zewnętrzne należą do tenanta, szyfrowane jego kluczem.
10. Wszystko z zewnątrz jest niezaufane.
11. **Nie licz w Pythonie tego, co Postgres policzy z indeksem.**
12. **Żadne zapytanie nie sięga po dane więcej niż jednego tenanta.**
13. **Każde wywołanie zewnętrzne idempotentne. Każde zdarzenie przez outbox.**
14. **Zanim napiszesz funkcję, sprawdź, czy istnieje.**

## II.2 Stos

```
DANE
  PostgreSQL 16 + RLS + pgvector + pg_trgm
  Citus              ścieżka shardingu po organization_id
  PgCat/Supavisor    pooling świadomy tenantów
  Replika odczytu    raporty, analityka, text-to-SQL
  Redis              cache stawek, sesje, limity
  MinIO              dokumenty źródłowe

PROCESY
  Temporal           pętla RFQ, ekstrakcja, booking
  Hatchet            zadania krótkie ze sprawiedliwością per tenant
  procrastinate      cykliczne: NBP, sankcje, wygasające stawki
  outbox             gwarancja dostarczenia

API
  FastAPI + granian · SSE do strumieniowania wycen
  OpenFGA · idempotencja na każdym wywołaniu

AI
  instructor + Claude API · router modeli · prompt caching + Batch
  llm-guard · presidio · langfuse · promptfoo · label-studio

FRONTEND
  Aplikacja wewnętrzna: Vite SPA + TanStack + shadcn + Tailwind v4 (OKLCH)
  Portal klienta:       osobna aplikacja SSR
  openapi-ts:           typy generowane, katalog api/ tylko do odczytu

OBSERWOWALNOŚĆ
  OpenTelemetry jako jedyna warstwa instrumentacji
  → Sentry · Grafana/SigNoz · PostHog · Langfuse
```

## II.3 Warstwy i granice

```
api → services → repositories → models
workflows → services
integrations → domain     (nigdy do services)
domain → (nic zewnętrznego)
```

Egzekwowane przez `import-linter` z czterema kontraktami. Naruszenie wywala CI.

Moduły domenowe niezależne: `rates`, `quotation`, `shipment`, `finance`,
`compliance`, `extraction`.

## II.4 Trzy źródła stawek, jeden interfejs

| | Cenniki (AI) | API armatorów | Ręczne |
|---|---|---|---|
| Ważność | okno `valid_from`–`valid_to` | **brak, TTL** | okno |
| Aktualność | dni/tygodnie | sekundy | dowolna |
| Kompletność | zwykle pełna | częściowa | zależna |
| Do bookingu | — | `price_id` | — |

Silnik operuje na abstrakcji `RateCandidate`. Stawki z bazy to natychmiastowe
tło, live spływa przez SSE przyrostowo.

## II.5 Data odniesienia — poprawiona

```
gotowość + dowóz do portu ≤ cut-off bramowy
cut-off DG wypada 5–10 dni wcześniej niż bramowy
```

Pole `validity_basis` na `rate_line`: `sailing | booking | bl_date | gate_in`.
Różni armatorzy różnie definiują, co decyduje o ważności — ekstraktor to wychwytuje.

## II.6 Granica AI i kodu

| Zadanie | Wykonawca |
|---|---|
| Rozpoznanie typu załącznika | kod (nadawca) → model (fallback) |
| Odczyt układu strony | docling / marker |
| Wyciągnięcie wartości | model |
| Mapowanie na `charge_code` | kod: alias → fuzzy → embedding |
| Normalizacja portu | kod (słownik) |
| Każde przeliczenie | **kod** |
| Wykrycie braków wg incoterm | kod (reguła) |
| Decyzja o zapisie | **człowiek** |
---

# CZĘŚĆ III — REJESTR MODUŁÓW

71 modułów, ~130 obiektów. Pełny rejestr z repozytoriami:
`REJESTR-MODULOW-I-PLAN-v2.md`. Tu skrót z kluczowymi rozstrzygnięciami.

## Domena A — Fundament

| Kod | Moduł | Rozstrzygnięcia niepodlegające zmianie |
|---|---|---|
| M-01 | Wielodostępność | RLS w bazie, ścieżka do Citus i bazy dedykowanej, zero zapytań międzytenantowych |
| M-02 | Niezawodność zdarzeń | outbox w tej samej transakcji, idempotencja na każdym wywołaniu |
| M-03 | Konfiguracja per organizacja | numeracja, szablony, workflow, `margin_rule`, pola własne, polityki automatyzacji |
| M-04 | Uprawnienia | OpenFGA, dwie pary oczu powyżej progu |

## Domena B — Dane referencyjne

| Kod | Moduł | Rozstrzygnięcia |
|---|---|---|
| M-05 | Geografia | `improved-un-locodes` jako podstawa, World Port Index, `terminal` obsługuje port i terminal lądowy, strefy pocztowe per organizacja |
| M-06 | Słownik opłat | ~60 kodów w 5 grupach, aliasy w 4 językach, uczenie z korekt, aliasy per kontrahent |
| M-07 | Waluty i czas | NBP D-1 roboczy, **trzy kursy: podatkowy, zarządczy, faktyczny**, typ `Money` |
| M-08 | Towary niebezpieczne | z publicznych załączników ADR; **system waliduje, nie klasyfikuje**; `carrier_dg_acceptance` |
| M-09 | Kody towarowe | HS, powiązanie z kontrolą eksportu |

## Domena C — Kontrahenci

| Kod | Moduł | Rozstrzygnięcia |
|---|---|---|
| M-10 | Kontrahenci | role tablicą, GUS/VIES/biała lista, `party_email_domain` |
| M-11 | Automatyczne kontakty | **domena podobna = ostrzeżenie, nigdy sugestia dodania** |
| M-12 | Sieci i stowarzyszenia | **`network_member` per tenant**, import własnego eksportu, deduplikacja |
| M-13 | Karta wyników | odpowiedzi, czas, konkurencyjność, zgodność oferty z fakturą |
| M-14 | Wywiadownie | **KRS API i RDF darmowe, sprawozdania w XML**, upoważnienie dla JDG |
| M-15 | Wirtualny CFO | scoring deterministyczny, **decyzja zawsze przez człowieka (RODO art. 22)** |
| M-16 | SOP klienta | generuje zadania i walidacje, nie dokument do czytania |

## Domena D — Stawki zakupowe

| Kod | Moduł | Rozstrzygnięcia |
|---|---|---|
| M-17 | Stawki statyczne | niemutowalność, `validity_basis`, przedziały wagowe i LDM, `origin_context` |
| M-18 | Opłaty portowe | 11 wymiarów warunkowych, **`is_applicable=false` jako wiedza negatywna**, rozstrzyganie przez specyficzność, **uczenie z faktur** |
| M-19 | Stawki live i kanały | framework: nowy armator = konfiguracja; **kanał mailowy dla reszty świata**; wymogi UI armatora; limity per tenant |
| M-20 | Pipeline ekstrakcji | 9 etapów, `source_ref` i `unparsed_regions` obowiązkowe, pamięć szablonów, `llm-guard` od pierwszego commita |

## Domena E — Wycena

| Kod | Moduł | Rozstrzygnięcia |
|---|---|---|
| M-21 | Silnik wyceny | **w SQL**, dobór na cut-off, DG osobno, SSE, `quotation_gap` |
| M-22 | Narzuty | kaskada 7 poziomów, narzut vs marża razem, **`buy_source: customer_contract`**, tryby prezentacji |
| M-23 | Waluty w ofercie | 3 tryby, klauzula walutowa, **spread jako pozycja przychodu** |
| M-24 | Ryzyko oferty | stawka probabilistyczna, marża zagrożona, optymalna ważność, ekspozycja netto |
| M-25 | Negocjacja i wynik | próg minimalnej marży, **krzywa elastyczności cenowej** |
| M-26 | Dokument oferty | typst, dwa układy, „dlaczego ta cena" |
| M-27 | Pokrycie | mapa białych plam zestawiona z zapytaniami klientów |

## Domena F — Zapytania

| Kod | Moduł | Rozstrzygnięcia |
|---|---|---|
| M-28 | Zapytania klientów | filtr po domenach klientów, **klasyfikator wieloklasowy (8 klas)**, skrzynka propozycji, daty jako zakres + precyzja, notatka głosowa |
| M-29 | Akceptacja oferty | **najdroższa pomyłka operacyjna — zrób wcześnie** |
| M-30 | Zapytania do agentów | **Temporal**, personalizacja 4 warstwy, **token per odbiorca**, kaskada 4 poziomów dopasowania, uprzedzanie wygasających |
| M-31 | Porównanie | **wykrywanie braków ważniejsze niż suma** |

## Domena G — Poczta

| Kod | Moduł | Rozstrzygnięcia |
|---|---|---|
| M-32 | Integracja pocztowa | **wysyłka z firmowej skrzynki użytkownika**, odczyt tylko własnych wątków + jeden folder |
| M-33 | Dodatek do Outlooka | uzupełnienie, nie fundament |
| M-34 | Powiadomienia | **push z akceptacją jednym dotknięciem** |

## Domena H — Zlecenia i tracking

| Kod | Moduł | Rozstrzygnięcia |
|---|---|---|
| M-35 | Zlecenie | konwersja z zamrożeniem kwot i kursu, dyskryminator gałęzi |
| M-36 | Tracking | normalizacja na DCSA niezależnie od formatu armatora |
| M-37 | Wyjątki | **watchdog free time — najszybszy zwrot w systemie** |
| M-38 | Dokumenty | walidacja krzyżowa B/L ↔ booking ↔ VGM ↔ faktura |
| M-39 | EDI | IFTMIN, IFTSTA, AS2 |

## Domena I — Finanse

| Kod | Moduł | Rozstrzygnięcia |
|---|---|---|
| M-40 | Faktury i KSeF | KSeF 2.0, wizualizacja XML→PDF |
| M-41 | Rozliczenie wyceny z fakturą | **najmocniejsza pojedyncza funkcja**, zasila M-18 |
| M-42 | Bank | MT940, dopasowanie płatności |
| M-43 | Koszt pieniądza | **`FINCOST` jako pozycja `shipment_charge`**, DSO/DPO rzeczywiste, termin jako dźwignia handlowa |
| M-44 | Różnice kursowe | **`FXDIFF` jako pozycja**, ekspozycja netto przy wycenie |
| M-45 | Przepływy | prognoza kasowa, faktoring per faktura, kaucje |
| M-46 | Koszt obsługi | **trójwymiarowa rentowność klienta** |
| M-47 | Księgowość | integracja, warstwa abstrakcji |

## Domena J — Gałęzie transportu

| Kod | Moduł | Rozstrzygnięcia |
|---|---|---|
| M-48 | Drogowy | **alokacja shared/capacity/marginal**, koszt krańcowy doładunku, pętla zwrotna do marż |
| M-49 | Kolej intermodalna | kanał mailowy, porównanie droga/kolej z emisją |
| M-50 | Kolej z Chin | **sprawdzanie trasy wobec sankcji, nie tylko stron** |
| M-51 | Drobnica morska | W/M liczone kodem, **próg opłacalności LCL vs FCL** |
| M-52 | Ślad węglowy | GLEC / ISO 14083 |

## Domena K — Zgodność

| Kod | Moduł | Rozstrzygnięcia |
|---|---|---|
| M-53 | Sankcje | **przeskanowanie wszystkich przy zmianie listy**, statki po IMO, `list_versions` jako wymóg audytowy |
| M-54 | Oszustwa | zmiana rachunku z potwierdzeniem innym kanałem |
| M-55 | Reklamacje | terminy zawite liczone automatycznie |
| M-56 | RODO | rejestr, retencja, eksport tenanta, przełącznik lokalny |

## Domena L — AI i analityka

| Kod | Moduł | Rozstrzygnięcia |
|---|---|---|
| M-57 | Serwer MCP | odczyt bez ograniczeń, zapis w trybie „przygotuj do zatwierdzenia" |
| M-58 | Copilot | funkcja demonstracyjna |
| M-59 | Raporty językiem naturalnym | **walidacja SQL obowiązkowa**, replika do odczytu |
| M-60 | Cyfrowi współpracownicy | sześciu agentów z bramkami i mierzalnym wynikiem |
| M-61 | Dane rynkowe | **warstwa 1 deterministyczna to 80% wartości**, warstwa 3 nigdy nie daje liczby, backtesting przeciw random walk |
| M-62 | Graf wiedzy | rośnie z wolumenem — jedyny mechanizm działający na twoją korzyść z czasem |
| M-63 | Symulacja portfela | narzędzie dla właściciela |

## Domena M — Sprzedaż i kontrakty

| Kod | Moduł | Rozstrzygnięcia |
|---|---|---|
| M-64 | Przetargi | znasz proces od środka, nikt tego nie ma w segmencie |
| M-65 | Kontrakty | indeksowane z korytarzem, MQC z alertem |
| M-66 | Portal klienta | **osobna aplikacja SSR** |
| M-67 | Subskrypcje | model prowizji od odzysku |

## Domena N — Platforma

| Kod | Moduł |
|---|---|
| M-68 | Obserwowalność |
| M-69 | Jakość i wydajność |
| M-70 | Wdrożenie |
| M-71 | **Metryki jakości kodu** — stosunek refaktoryzacji, duplikacja, dryf złożoności, przeżywalność problemów |
---

# CZĘŚĆ IV — METODYKA

## IV.1 Wybór i uzasadnienie

**Przepływ z limitem prac w toku równym jeden + delta-spec + praktyki XP.**

Nie Scrum: punkty historyjkowe tracą sens, gdy AI generuje w dwie godziny to,
co zajmowało dwa dni; ceremonie koordynują ludzi, których nie masz.

Nie maksymalistyczne podejście specyfikacyjne z personami: dane pokazują, że
przy pracy iteracyjnej w pojedynkę wygrywa tryb planowania plus dobre testy.

Ale specyfikacja jest niezbędna: słaba dyscyplina wymagań wiąże się z wyższym
długiem — złożonością, duplikacją i degradacją pokrycia. Rygorystyczna
dokumentacja daje ten sam trzy- do pięciokrotny wzrost tempa przy znacznie
mniejszym koszcie jakościowym.

## IV.2 Delta-spec zamiast pełnej specyfikacji

Dokumentujesz zmianę, nie moduł. Cykl: **zaproponuj → zastosuj → zarchiwizuj**.

```
docs/
├── spec/<moduł>.md              źródło prawdy, aktualne
└── deltas/
    ├── open/<id>.md             bieżąca zmiana
    └── archived/<id>.md         scalone do spec
```

## IV.3 Rytm

| Kiedy | Co | Czas |
|---|---|---|
| Poniedziałek | Wybór plastrów, `CURRENT.md` | 30 min |
| Codziennie | Pętla plastra, jeden na raz | — |
| Piątek | **Raport metryk M-71** | 30 min |
| Piątek | Retrospektywa → poprawka w regułach albo hookach | 15 min |
| Co 4 tygodnie | Slot refaktoryzacyjny z wejściem z metryk | 1 dzień |

Jeśli agent trzeci raz popełnił ten sam błąd, to jest brak reguły, nie jego wina.

## IV.4 Wzorzec agentowy — rozstrzygnięcie

**Orkiestrator z efemerycznymi subagentami.** Jeden agent posiada pełny kontekst,
uruchamia subagenty z czystym kontekstem, każdy zwraca jedno podsumowanie.
Brak kanału peer-to-peer, brak współdzielonego stanu.

**Odrzucone: zespół person (CEO, CFO, PM, programiści).** Dowody: pojedynczy
agent dorównuje wielagentowemu przy równym budżecie tokenów; debata bywa
degradująca, bo agenci zgadzają się odruchowo zamiast kwestionować; błąd raz
wprowadzony jest wzmacniany przez kolejnych. W badaniu z inżynierii wymagań
poprawa była rzędu tysięcznych punktu przy wielokrotnym koszcie.

**Uratowane z tego pomysłu:** krytyk asymetryczny (subagent tylko szukający
dziur, bez prawa do zgody), perspektywy jako listy kontrolne w szablonie PR,
plany równoległe przy decyzjach architektonicznych.

---

# CZĘŚĆ V — KONFIGURACJA CURSORA

## V.1 Struktura

```
AGENTS.md                 ← 14 zasad, nawigacja, budżety. Limit 130 linii
justfile
.importlinter
.cursor/
├── rules/
│   ├── context.mdc       alwaysApply
│   ├── no-slop.mdc       alwaysApply
│   ├── backend.mdc       globs
│   ├── database.mdc      globs
│   ├── frontend.mdc      globs
│   ├── testing.mdc       globs
│   ├── performance.mdc   globs
│   └── workflows.mdc     globs
├── skills/               ← używane też jako Custom Modes
├── subagents/
├── hooks/
├── plans/
├── mcp.json
└── settings.json         ← auto-review allowlist
docs/
├── ARCHITECTURE.md · MODULES.md · GLOSSARY.md
├── spec/ (71 plików, każdy < 400 linii)
├── deltas/{open,archived}/
├── adr/
└── state/{CURRENT.md, PROGRESS.md}
```

## V.2 Hooks — mechanizm najważniejszy

`onPostEdit` uruchamia po każdej edycji `ruff --select E,F,B,C901,ARG,PLW0621,SLF001`
i `mypy`, zwracając błędy agentowi przez `followup_message`. Reguły dobrane pod
pięć najczęstszych zapachów z badania na 302 tys. commitów AI.

`onPreCommit` blokuje przy naruszeniu `import-linter`, `jscpd` powyżej 3%,
martwym kodzie.

`onPreEdit` weto na: migracjach zastosowanych, `frontend/src/api/` (generowany),
ADR-ach ze statusem „przyjęta".

## V.3 Subagenty

| Subagent | Rola |
|---|---|
| **`lowca-duplikatow`** | **obowiązkowy przed implementacją** — czysty kontekst, jedno zadanie: czy to już istnieje |
| `weryfikator` | uruchamia bramkę, sprawdza kryteria z delta-spec, raportuje tabelę |
| `testolog` | testy z kryteriów akceptacji, muszą failować |
| `audytor-wydajnosci` | EXPLAIN na nowych zapytaniach, py-spy przy przekroczeniu |
| `kronikarz` (tło) | scala deltę do spec, PROGRESS.md, api-types, szkic ADR |
| `migrator` | migracje z MCP Postgres |
| `krytyk` | tylko szuka dziur, bez prawa do zgody |

## V.4 Custom Modes i `/goal`

Skill przypięty jako tryb na całą sesję (Opt+Enter z `/`). `/goal` nadaje cel
długoterminowy. Razem zastępują powtarzanie instrukcji w każdym prompcie.

## V.5 Automations

| Automatyzacja | Wyzwalacz |
|---|---|
| Strażnik bramki | PR otwarty/zmieniony |
| Recenzent z listą kontrolną | PR otwarty |
| Raport jakości (M-71) | piątek |
| Triage zależności | PR od Renovate |
| Strażnik budżetów | nocny |
| **Kontrakty armatorów** | tygodniowy — wykrywa zmianę API zanim zepsuje produkcję |

**Reguła bezpieczeństwa:** automatyzacje mające kontakt z M-20 mają **pamięci
wyłączone**. Przetwarzasz niezaufane cenniki; zatruta pamięć trwała jest trudna
do wykrycia i wpływa na przyszłe uruchomienia.

## V.6 MCP

Postgres (schemat bez zgadywania) · Context7 (aktualna dokumentacja bibliotek)
· GitHub · Playwright.

## V.7 Model

Auto domyślnie (nie zużywa puli) · Composer do plastrów rutynowych i subagentów
· model czołowy do architektury i refaktoryzacji wielopikowej · plany równoległe
przy decyzjach z ADR.

## V.8 Pętla plastra

```
① DELTA-SPEC            piszesz sam, 15 min
② TRYB + /goal          przypięty `plaster`, cel z kryteriów
③ ŁOWCA DUPLIKATÓW      obowiązkowo przed kodem
④ PLAN                  tryb planowania; przy decyzji — plany równoległe
⑤ TESTOLOG              testy muszą failować  ← TU WNOSISZ WIEDZĘ DOMENOWĄ
⑥ IMPLEMENTACJA         hooki poprawiają na bieżąco
⑦ WERYFIKATOR           bramka + kryteria → tabela
⑧ AUDYTOR WYDAJNOŚCI    EXPLAIN
⑨ KRONIKARZ (tło)       dokumentacja
⑩ PR + AUTOMATYZACJE    → NOWA ROZMOWA
```

Twoja rola: kroki ①, ⑤ i decyzja w ④. Reszta to nadzór.

---

# CZĘŚĆ VI — JAKOŚĆ

## VI.1 Dane, na których to stoi

| Zjawisko | Liczba |
|---|---|
| Duplikacja bloków | +81% od 2023, najwyższa w historii pomiarów |
| Kopiuj-wklej w commicie | 9,4% (2022) → 15,7% (2026) |
| **Kod refaktoryzowany** | **21% (2022) → 3,8% (2026)** |
| Konstrukcje maskujące błędy | +47% |
| Commity AI z ≥1 problemem | ponad 15% |
| Problemy przeżywające | 22,7% |
| Recenzenci wobec kodu AI | **łagodniejsi mimo gorszej jakości projektowej** |

Wniosek: obroną nie jest ograniczanie AI, tylko jego oprzyrządowanie.

## VI.2 Bramki

| Mechanizm | Blokuje |
|---|---|
| `import-linter` | naruszenie warstw i granic |
| `ruff C901` | złożoność > 10, delta +3 na funkcję w PR |
| `jscpd` próg 3% | duplikację — w hooku, nie tylko w CI |
| `vulture` / `knip` | martwy kod |
| `mypy --strict` | brak typów |
| `pytest --cov-fail-under=80` | brak testów |
| test izolacji tenantów | każda nowa tabela |
| `just perf` | przekroczenie budżetu |
| `size-limit` | rozrost paczki |
| `schemathesis` | niezgodność z OpenAPI |
| `pact` | zmianę API armatora |
| BugBot + `pr-agent` | brak przeglądu |

## VI.3 Metryka nadrzędna

**Stosunek kodu przeniesionego do dodanego.** Próg alarmowy: poniżej 10%.
Spadek oznacza, że kod przestał być refaktoryzowany, tylko dokładany —
i dowiesz się o tym z liczby, zanim stanie się nieodwracalne.

## VI.4 Lista kontrolna przeglądu

Bo intuicja zawodzi w udokumentowany sposób, a ty jesteś autorem i recenzentem
jednocześnie.

```
□ Czy ta logika już gdzieś istnieje?
□ Czy nowa funkcja mogła być rozszerzeniem istniejącej?
□ Czy obsługa błędów jest konkretna, czy maskująca?
□ Czy złożoność którejś funkcji wzrosła o więcej niż 3?
□ Czy testy sprawdzają regułę biznesową, czy implementację?
□ Czy da się to napisać krócej?
□ Jaki to ma wpływ na koszt utrzymania i czas do przychodu?
```

## VI.5 Budżety wydajności

| Operacja | Próg |
|---|---|
| Wycena ze stawek w bazie (50k) | p95 < 300 ms |
| Pierwszy wynik z kanałów | < 1 s |
| Endpoint API, mediana | < 150 ms |
| Lista 50k wierszy | p95 < 500 ms |
| LCP aplikacji wewnętrznej | < 1,5 s |
| Paczka JS gzip | < 250 kB |

Przekroczenie blokuje merge.

## VI.6 Wygląd

Tailwind v4 z tokenami OKLCH · shadcn/ui kopiowane do repo · Geist/Inter ·
paleta poleceń `Cmd+K` · tryb kompaktowy domyślny · pełna ścieżka bez myszy ·
wklejanie z Excela do siatki.

**Szczegół decydujący:** `tabular-nums` w każdej tabeli z kwotami, wyrównanie
do prawej, waluta wyciszona, zero jako myślnik. Spedytor patrzy na kolumny kwot
osiem godzin dziennie.

**Stan `partial` jako komponent pierwszej klasy** — wyniki z bazy są, z armatorów
spływają.

Kontrola: Storybook · Playwright ze zrzutami · axe w CI · tryb ciemny równolegle.
---

# CZĘŚĆ VII — HARMONOGRAM

96 plastrów w 10 fazach. Pełne opisy z warunkami ukończenia:
`REJESTR-MODULOW-I-PLAN-v2.md`.

## Faza 0 · Platforma (tydz. 1–3)

`0.1` szkielet + granian + CI · `0.2` kompilacja aneksów do `docs/spec/` ·
`0.3` wielodostępność + RLS · `0.4` audit log + metering · **`0.5` outbox +
idempotencja** · `0.6` OpenTelemetry + Sentry + Langfuse + PostHog ·
`0.7` bramki jakości + M-71 · `0.8` OpenFGA · `0.9` numeracja i szablony

## Faza 1 · Dane i kontrahenci (tydz. 4–6)

`1.1` porty · `1.2` World Port Index + strefy · `1.3` słownik opłat ·
`1.4` waluty i NBP · `1.5` kontrahenci · `1.6` GUS/VIES/biała lista ·
`1.7` kody HS · `1.8` ADR

## Faza 2 · Stawki i wycena (tydz. 7–14)

`2.1` `rate_line` + `validity_basis` · `2.2` przedziały · `2.3` opłaty portowe
warunkowe · **`2.4` silnik w SQL** · `2.5` `quotation_gap` · `2.6` kaskada
narzutów · `2.7` kontrakt klienta jako źródło · `2.8` waluty w ofercie ·
`2.9` PDF w dwóch układach · `2.10` wysyłka z firmowej skrzynki ·
`2.11` mapa pokrycia

### 🎯 PUNKT KONTROLNY — nagranie demo dla trzech spedytorów

Jeśli sam silnik wyceny na ręcznie wprowadzonych stawkach nie robi wrażenia,
dalsza budowa tego nie naprawi. Dowiesz się trzy miesiące wcześniej i za
jedną trzecią kosztu.

## Faza 3 · Tracking (tydz. 15–18)

`3.1` framework kanałów · `3.2` Hapag: pokrycie · `3.3` DCSA T&T ·
**`3.4` watchdog free time** · `3.5` push z akceptacją · `3.6` mapa i link

## Faza 4 · Ekstrakcja (tydz. 19–26)

`4.1` wejście pocztowe · **`4.2` zbiór testowy przed pipeline'em** ·
`4.3` porównanie parserów · `4.4` instructor + provenance · `4.5` llm-guard ·
`4.6` normalizacja · `4.7` walidacja i anomalie · `4.8` kolejka review ·
`4.9` pamięć szablonów · `4.10` uczenie aliasów · `4.11` automatyczne kontakty

## Faza 5 · Pętla zapytań (tydz. 27–34)

`5.1` filtr domen klientów · `5.2` klasyfikator · **`5.3` akceptacja oferty** ·
`5.4` daty · `5.5` wiele relacji, załączniki, leady · `5.6` notatka głosowa ·
`5.7` katalog sieci · `5.8` deduplikacja · **`5.9` Temporal** ·
`5.10` personalizacja · `5.11` wysyłka z tokenami · `5.12` kaskada dopasowania ·
`5.13` porównanie · `5.14` karta wyników · `5.15` uprzedzanie

## Faza 6 · Zlecenia i pieniądze (tydz. 35–46)

`6.1` konwersja · `6.2` maszyna stanów · `6.3` dokumenty · `6.4` KSeF ·
**`6.5` rozliczenie z fakturą** · **`6.6` uczenie opłat portowych z faktur** ·
`6.7` MT940 · `6.8` `FINCOST` · `6.9` `FXDIFF` · `6.10` przepływy ·
`6.11` koszt obsługi · `6.12` marża zagrożona · `6.13` elastyczność cenowa

## Faza 7 · Zgodność i automatyzacja (tydz. 47–56)

`7.1` listy sankcyjne · `7.2` screening · **`7.3` przeskanowanie przy zmianie** ·
`7.4` statki po IMO · `7.5` ochrona przed oszustwem · `7.6` RODO ·
`7.7` Hapag spot · `7.8` Maersk Offers · `7.9` CMA CGM · `7.10` SSE ·
`7.11` kanał mailowy armatorów · `7.12` polityki automatyzacji ·
`7.13` `auto_quote_policy`

## Faza 8 · Gałęzie (tydz. 57–72)

`8.1–8.4` drogowy: `tour`, alokacja, tryb marginal, or-tools ·
`8.5–8.7` LCL: W/M, próg FCL, konsolidatorzy · `8.8` kolej ·
`8.9` emisje · `8.10` porównanie gałęzi · `8.11` kolej z Chin ·
`8.12` EDI · `8.13` reklamacje · `8.14` SOP

## Faza 9 · AI i sprzedaż (tydz. 73+)

`9.1` MCP · `9.2` text-to-SQL · `9.3` copilot · `9.4` cyfrowi współpracownicy ·
`9.5` wywiadownie · `9.6` Wirtualny CFO · `9.7–9.8` dane rynkowe ·
`9.9` przetargi · `9.10` kontrakty indeksowane · `9.11` portal ·
`9.12` dodatek Outlook · `9.13` graf wiedzy · `9.14` symulacja ·
`9.15` subskrypcje · `9.16` księgowość

**Fazy 0–3 to 18 tygodni i produkt sprzedawalny.** Fazy 8 i 9 to zbiór gotowych
do podjęcia, nie sekwencja. Kolejność wskazują klienci.

---

# CZĘŚĆ VIII — ŚRODOWISKO I KOSZTY

## VIII.1 Faza budowy — zero złotych poza drobiazgami

**Lokalnie:** Docker Compose z Postgresem, Redisem, MinIO, Mailpitem, Langfuse.
Tu dzieje się 90% pracy przez pierwsze pół roku.

**W chmurze:** Oracle Always Free, **region Frankfurt** (wybór nieodwracalny),
Ampere A1 z 2 OCPU i 12 GB po redukcji z czerwca 2026, 200 GB storage.

**Darmowe:** GitHub · Cloudflare (Tunnel do demo z laptopa) · Neon (gałąź bazy
per PR) · Sentry · PostHog · Langfuse · Better Stack · Loom · Linear

**Darmowe API:** KSeF · GUS BIR (sandbox bez klucza) · biała lista · VIES ·
NBP · KRS · RDF · portale deweloperskie armatorów

## VIII.2 Koszty

| | Budowa | Solo | 5 klientów | 20 klientów |
|---|---|---|---|---|
| Miesięcznie | 300–1 200 zł | ~200 zł | ~650 zł | ~1 900 zł |
| Twój czas rocznie | 800–1 000 h | ~150 h | ~350 h | etat |

Sparsowanie cennika: ~1 zł, przez Batch API 50 gr, po pamięci szablonów
pięć razy mniej. **AI nie jest kosztem tego systemu.** Nie optymalizuj wyboru
modelu pod cenę — bierz najskuteczniejszy.

Prawdziwy koszt: 100–150 tys. zł kosztu alternatywnego twojego czasu,
plus 15–20% tego rocznie na utrzymanie.

## VIII.3 Moment przejścia na płatne

**Pierwszy płacący klient zewnętrzny.** Nie wcześniej (strata pieniędzy),
nie później (umowa powierzenia, SLA, backup poza dostawcą).

Docelowo Hetzner CPX31 za ~60 zł, dane w UE, plus `pgbackrest` z PITR.

---

# CZĘŚĆ IX — RYZYKA

| Ryzyko | Waga | Odpowiedź |
|---|---|---|
| **Wąskie gardło jednej osoby przy 3–5 klientach** | wysoka | wybierz świadomie: wspólnik, partner wdrożeniowy albo limit klientów |
| Konflikt z HHL | wysoka | rozmowa przed pierwszą umową |
| Duplikacja kodu | wysoka | łowca duplikatów + jscpd w hooku + metryka refaktoryzacji |
| Prompt injection przez cennik | średnia | llm-guard od pierwszego commita, pamięci wyłączone |
| Cicho pominięta tabela dopłat | średnia | `unparsed_regions` + `quotation_gap` |
| Zmiana schemy KSeF | średnia | warstwa abstrakcji |
| Zmiana API armatora | średnia | testy kontraktowe, automatyzacja tygodniowa |
| Wycofanie modelu | średnia | promptfoo + zbiór w label-studio |
| Utrata bazy | krytyczna | pgbackrest przed pierwszym klientem |
| Każdy klient wymaga zmian w kodzie | wysoka | zasada 2 |

## Decyzje otwarte

| # | Decyzja | Termin |
|---|---|---|
| O-01 | Osobny podmiot na produkt? | przed pierwszą umową |
| O-02 | Zasięg: Polska czy od razu region? | przed fazą 2 (i18n, Peppol) |
| O-03 | **Morze czy droga jako pierwszy rynek?** | przed fazą 2 |
| O-04 | Dostawca księgowości | przed 6.4 |
| O-05 | Agregator trackingu | gdy klienci płacą |
| O-06 | Benchmark rynkowy w zakresie? | wymaga subskrypcji klienta |

**O-03 zasługuje na uwagę.** Rynek drogowy w Polsce jest wielokrotnie większy,
a tam masz działający, zwalidowany silnik rentowności z gotowym argumentem
sprzedażowym. W morzu zaczynasz od zera, ale ból z cennikami agentów jest
ostrzejszy. Pytanie dotyczy kolejności faz, nie architektury — wspólny model
danych jest właściwy niezależnie od odpowiedzi.

---

# CZĘŚĆ X — PIERWSZE DZIESIĘĆ DNI

| Dzień | Zadanie |
|---|---|
| **0** | Oszacowanie rynku na kartce. Rozmowa z HHL o konflikcie. Wniosek o klucz GUS. Rejestracja w portalach Hapaga, Maerska, CMA CGM |
| **1** | Szkielet: szablon FastAPI, granian, Docker Compose, `justfile`, `AGENTS.md`, `.cursor/rules/`, `.importlinter`. CI pusty, zielony |
| **2** | Konto Oracle (Frankfurt), Cloudflare, Neon. MCP: Postgres, Context7, GitHub |
| **3** | Kompilacja aneksów do `docs/spec/` przez Claude Code. `MODULES.md` z rejestru |
| **4** | `ARCHITECTURE.md` i `GLOSSARY.md` — piszesz sam, to twoja wiedza |
| **5** | `.cursor/hooks/` i `.cursor/subagents/`. Test: czy hook zwraca błędy agentowi |
| **6** | Plaster 0.3: `organization`, RLS, **test izolacji jako wzorzec** |
| **7** | Plastry 0.4–0.5: audit log, outbox, idempotencja |
| **8** | Plaster 0.6–0.7: telemetria i bramki, M-71 |
| **9** | Pierwszy pion od końca do końca: migracja → repozytorium → serwis → endpoint → typ → komponent → test |
| **10** | Retrospektywa: co w regułach i hookach poprawić po pierwszym tygodniu |

Po dziesiątym dniu masz cykl, który powtarzasz dziewięćdziesiąt sześć razy.

---

# ZAMIAST PODSUMOWANIA — SIEDEM RZECZY, KTÓRE DECYDUJĄ

**① Wejdź wąsko.** Moduł stawek jako dodatek do tego, co klient ma. Pełne ERP
przed pierwszym klientem to najczęstszy sposób, w jaki takie projekty umierają.

**② Multi-tenancy i outbox w pierwszym tygodniu.** Jedyne rzeczy, których nie
da się dorobić bez przepisania systemu.

**③ Silnik wyceny w SQL.** Zasada 11 jest najważniejsza w całym `AGENTS.md`.

**④ Łowca duplikatów przed każdą implementacją.** Dane pokazują duplikację
jako zagrożenie numer jeden, a przyczyną jest ograniczone okno kontekstu.
Subagent z czystym kontekstem usuwa przyczynę.

**⑤ Punkt kontrolny po fazie 2 jest realny.** Demo dla trzech spedytorów.
Jeśli nie robi wrażenia, zmień zakres, nie buduj dalej.

**⑥ Testy reguł biznesowych piszesz z głowy.** To jedyna część, której agent
nie zrobi za ciebie, i jedyna, która decyduje, czy system liczy poprawnie.

**⑦ Rozliczenie wyceny z fakturą to twoja najmocniejsza funkcja.** Finansuje
się w pierwszym miesiącu, zasila bazę opłat portowych i buduje kartę wyników
agentów. Trzy rzeczy z jednego mechanizmu, którego nie ma nikt.
