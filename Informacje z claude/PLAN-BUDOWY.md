# Plan budowy — backlog plastrów

Format przeznaczony do użycia z agentem. Każdy plaster ma identyfikator,
zależności, zakres i definicję ukończenia. Realizujesz po jednym, w kolejności.

**Sposób użycia:** kopiujesz treść plastra do `docs/state/CURRENT.md`,
otwierasz nową rozmowę, prompt: *„Przeczytaj docs/state/CURRENT.md
i docs/spec/<moduł>.md. Zaplanuj realizację. Nie pisz kodu."*

---

## FAZA 0 — FUNDAMENT (tydzień 1–2)

### F0.1 · Szkielet i bramki
**Zależności:** brak
**Zakres:** szablon FastAPI, Docker Compose (Postgres, Redis, MinIO, Mailpit),
`justfile`, CI z ruff/mypy/pytest/import-linter, `.cursor/rules/`, `AGENTS.md`
**Ukończone gdy:** `just check && just test && just arch` przechodzi na pustym repo

### F0.2 · Kompilacja dokumentacji
**Zależności:** F0.1
**Zakres:** aneksy → `docs/spec/*.md`, `ARCHITECTURE.md`, `GLOSSARY.md`
**Ukończone gdy:** żaden plik w `spec/` nie przekracza 400 linii, mapa modułów gotowa

### F0.3 · Wielodostępność
**Zależności:** F0.2 · **Spec:** `tenancy.md`
**Zakres:** `organization`, `app_user`, `role`, RLS na poziomie bazy,
kontekst tenanta w sesji, `audit_log` na triggerze, `usage_metric`
**Ukończone gdy:** test izolacji przechodzi, audit log zapisuje się bez udziału kodu
**Krytyczne:** to jest jedyny plaster, którego nie da się dorobić później

### F0.4 · Słowniki
**Zależności:** F0.3 · **Spec:** `charges.md`
**Zakres:** `port` z UN/LOCODE (`improved-un-locodes`), `container_type`,
`incoterm`, `charge_code` z ~60 kodami i aliasami wielojęzycznymi,
`charge_code_alias`, seed
**Ukończone gdy:** normalizacja „Gdingen"/„GDN"/„Gdynia Port" → `PLGDY` działa

### F0.5 · Pieniądz i czas
**Zależności:** F0.3 · **Spec:** `finance.md` sekcja 1
**Zakres:** typ `Money`, `fx_rate` z pobieraniem NBP, `payment_term_profile`,
`cost_of_capital_config`, `shipment_cash_event` (schemat, bez logiki)
**Ukończone gdy:** testy property-based na przeliczeniach przechodzą
**Uwaga:** schemat teraz, silnik później — danych wstecz nie odtworzysz

---

## FAZA 1 — OFERTOWANIE (tydzień 3–9)

### F1.1 · Kontrahenci
**Zależności:** F0.4 · **Spec:** `parties.md`
**Zakres:** `party` z rolami, kontakty, rachunki, `party_email_domain`,
integracja GUS/REGON (sandbox bez klucza), VIES, biała lista
**Ukończone gdy:** dodanie kontrahenta po NIP zajmuje pięć sekund

### F1.2 · Stawki — schemat i wprowadzanie ręczne
**Zależności:** F1.1 · **Spec:** `rates-sheets.md`
**Zakres:** `rate_sheet`, `rate_line` z `validity_basis` i `bracket_*`,
niemutowalność, `superseded_by`, formularz, import CSV
**Ukończone gdy:** 200 realnych pozycji z twoich cenników jest w bazie
**Uwaga:** wygląda na stratę czasu, nie jest. Bez tego nie wiesz, czy schemat pasuje

### F1.3 · Opłaty portowe warunkowe
**Zależności:** F1.2 · **Spec:** `port-charges.md`
**Zakres:** `port_charge_rule` z warunkami i `is_applicable`,
rozstrzyganie przez specyficzność
**Ukończone gdy:** reguła „CIC nie dotyczy kontenerów z Europy" działa jako reguła zerowa

### F1.4 · Silnik wyceny — rdzeń
**Zależności:** F1.3 · **Spec:** `quotation.md`
**Zakres:** `quotation`, warianty, pozycje, dobór stawek na
`expected_gate_cutoff`, wykrywanie luk (`quotation_gap`), reguły marży
**Ukończone gdy:** wycena z bazy poniżej 300 ms p95, luki wykrywane poprawnie

### F1.5 · Narzuty
**Zależności:** F1.4 · **Spec:** `charges.md` sekcja narzuty
**Zakres:** `markup_rule`, kaskada siedmiu poziomów, narzut kontra marża,
zaokrąglanie, tryby prezentacji, `buy_source: customer_contract`
**Ukończone gdy:** widać, która reguła zadziałała na każdej pozycji

### F1.6 · Waluty w ofercie
**Zależności:** F1.5 · **Spec:** `finance.md` sekcja 2
**Zakres:** tryby `original`/`converted`/`hybrid`, klauzula walutowa,
spread jako pozycja marży, kurs i data przy pozycji
**Ukończone gdy:** oferta wielowalutowa generuje się w obu trybach ryzyka

### F1.7 · Dokument oferty i wysyłka
**Zależności:** F1.6
**Zakres:** szablon w `typst`, dwa układy (rozbity i all-in), wysyłka
z firmowej skrzynki użytkownika przez Graph/Gmail, podpis, `Message-ID`
**Ukończone gdy:** oferta wychodzi z twojej skrzynki i widzisz ją w „Wysłanych"

### 🎯 PUNKT KONTROLNY PO F1.7
Nagraj demo (Loom), wyślij trzem spedytorom. **Jeśli nie robi wrażenia —
zatrzymaj się i przemyśl zakres.** Trzy miesiące wcześniej i za jedną trzecią kosztu.

---

## FAZA 2 — TRACKING (tydzień 10–12)

### F2.1 · Adaptery armatorów — szkielet
**Zależności:** F1.1 · **Spec:** `rates-live.md`
**Zakres:** `CarrierChannel`, `carrier_credential` szyfrowane per tenant,
`carrier_channel`, obsługa limitów, mapowanie konfiguracją nie kodem
**Ukończone gdy:** dodanie drugiego armatora to konfiguracja, nie nowy kod

### F2.2 · Hapag-Lloyd: tracking i pokrycie
**Zależności:** F2.1 · **Spec:** `tracking.md`
**Zakres:** DCSA T&T, `shipment_event`, API pokrycia → `carrier_service`
**Ukończone gdy:** widzisz swoje kontenery bez otwierania portalu

### F2.3 · Zarządzanie wyjątkami
**Zależności:** F2.2
**Zakres:** rollover, poślizg ETA, **watchdog free time**, cut-off VGM,
powiadomienia przez `novu`
**Ukończone gdy:** dostajesz alert o demurrage zanim naliczy się pierwsza doba
**Uwaga:** najszybszy zwrot w całym systemie

---

## FAZA 3 — EKSTRAKCJA (tydzień 13–19)

### F3.1 · Wejście pocztowe
**Zależności:** F1.1 · **Spec:** `rfq.md`
**Zakres:** EmailEngine, odczyt własnych wątków po `conversationId`,
folder na cenniki niezamówione, `inbound_message`
**Ukończone gdy:** system nie ma dostępu do skrzynki poza wątkami, które założył

### F3.2 · Zbiór testowy
**Zależności:** F3.1
**Zakres:** 30 realnych cenników w `label-studio`, anotacja, `promptfoo`, `langfuse`
**Ukończone gdy:** masz liczbę skuteczności, nie wrażenie
**Uwaga:** przed pipeline'em, nie po

### F3.3 · Pipeline ekstrakcji
**Zależności:** F3.2 · **Spec:** `rates-sheets.md`
**Zakres:** docling/marker → `instructor` ze schematem → normalizacja
(aliasy → RapidFuzz → embedding) → walidacja w kodzie → kolejka review.
`llm-guard` od pierwszego commita
**Ukończone gdy:** skuteczność mierzona, `unparsed_regions` zgłaszane,
nic nie wchodzi bez akceptacji

### F3.4 · Pamięć szablonów i uczenie aliasów
**Zależności:** F3.3
**Zakres:** `extraction_template`, fingerprint, parser deterministyczny,
korekty zasilające `charge_code_alias`
**Ukończone gdy:** powtórzony cennik tego samego agenta parsuje się bez modelu

### F3.5 · Automatyczne kontakty
**Zależności:** F3.1 · **Spec:** `parties.md`
**Zakres:** dopasowanie po domenie, kontekst wątku, ekstrakcja podpisu,
kolejka weryfikacji, **wykrywanie podobnych domen jako ostrzeżenie**
**Ukończone gdy:** `andes-cargo.com` przy znanym `andescargo.com` daje alert, nie sugestię

---

## FAZA 4 — PĘTLA ZAPYTAŃ (tydzień 20–26)

### F4.1 · Zapytania od klientów
**Zależności:** F3.3 · **Spec:** `rfq.md`
**Zakres:** filtr po domenach klientów, klasyfikator wieloklasowy,
skrzynka propozycji z progami, parsowanie dat gotowości (zakres + precyzja)
**Ukończone gdy:** fałszywe pozytywy poniżej kilku procent

### F4.2 · Wykrywanie akceptacji oferty
**Zależności:** F4.1
**Zakres:** klasa `quote_acceptance`, alert, przygotowanie bookingu
**Ukończone gdy:** „ok, proszę bookować" w piątek o 16:50 nie ginie
**Uwaga:** zrób wcześniej, niż wynika z kolejności

### F4.3 · Katalog agentów i sieci
**Zależności:** F1.1 · **Spec:** `rfq.md`
**Zakres:** `network`, `network_member` per tenant, import przez pipeline,
deduplikacja, wzbogacanie z historii
**Ukończone gdy:** ten sam agent w trzech sieciach to jeden rekord

### F4.4 · Zapytania do agentów
**Zależności:** F4.3
**Zakres:** `rate_request`, okno wyboru z rankingiem, personalizacja
czterowarstwowa, wysyłka indywidualna z rozłożeniem, tokeny per odbiorca,
kaskada dopasowania odpowiedzi, przypomnienia
**Ukończone gdy:** odpowiedź agenta z innego adresu trafia do właściwego zapytania

### F4.5 · Porównanie i karta wyników
**Zależności:** F4.4
**Zakres:** widok porównawczy z wykrywaniem braków, `party_scorecard`
**Ukończone gdy:** agent bez D/O fee jest oznaczony jako niepełny, nie najtańszy

---

## FAZA 5 — ZLECENIA I PIENIĄDZE (tydzień 27–36)

### F5.1 · Zlecenie morskie
**Zależności:** F1.7, F2.2 · **Spec:** `shipment.md`
**Zakres:** konwersja z oferty z zamrożeniem kwot, kontenery, maszyna
stanów, zadania, dokumenty z szablonów

### F5.2 · Fakturowanie i KSeF
**Zależności:** F5.1 · **Spec:** `finance.md`
**Zakres:** `invoice`, `bill`, `smekcio/ksef-client-python`, wizualizacja PDF

### F5.3 · Rozliczenie wyceny z fakturą
**Zależności:** F5.2 · **Spec:** `finance.md`
**Zakres:** `cost_variance`, wykrywanie rozbieżności, **zapisywanie reguł
opłat portowych z faktur**
**Ukończone gdy:** miesięczny raport rozbieżności działa
**Uwaga:** najmocniejsza pojedyncza funkcja w systemie

### F5.4 · Koszt pieniądza i różnice kursowe
**Zależności:** F5.2 · **Spec:** `finance.md`
**Zakres:** `FINCOST` i `FXDIFF` jako pozycje wyliczane, ekspozycja netto
per zlecenie pokazywana przy wycenie, `observed_dso`
**Ukończone gdy:** oferta pokazuje marżę po koszcie kapitału

### F5.5 · Serwer MCP
**Zależności:** F5.1
**Zakres:** narzędzia odczytowe bez ograniczeń, zapisowe w trybie
„przygotuj do zatwierdzenia"
**Ukończone gdy:** możesz wystawić ofertę zdaniem w Claude

---

## FAZA 6 — ROZSZERZENIA

Kolejność wskazują klienci, nie plan.

| ID | Zakres | Spec |
|---|---|---|
| F6.1 | Moduł drogowy: `tour`, alokacja, doładunki | `road.md` |
| F6.2 | LCL: W/M, próg opłacalności FCL | `lcl.md` |
| F6.3 | Kolej dowozowa, porównanie z emisją | `rail.md` |
| F6.4 | Wyceny spot: Hapag, Maersk, CMA | `rates-live.md` |
| F6.5 | Sankcje z automatyczną aktualizacją | `compliance.md` |
| F6.6 | Wywiadownie i Wirtualny CFO | `finance.md` |
| F6.7 | Dane rynkowe, warstwa deterministyczna | `market.md` |
| F6.8 | Portal klienta | — |
| F6.9 | Kolej z Chin (po F6.5, wymaga sankcji trasy) | `rail.md` |

---

## ZASADY PROWADZENIA PLANU

**Jeden plaster to jedna rozmowa.** Po zamknięciu — nowa sesja. Ciągnięcie wątku
przez tydzień oznacza, że każdy prompt niesie historię, której agent nie potrzebuje.

**Nie zaczynaj plastra bez planu.** Tryb planowania, akceptacja, potem kod.

**`PROGRESS.md` po każdym plastrze.** Jedna linia: identyfikator, data, co powstało,
co odłożone. To jest pamięć projektu między sesjami.

**Refaktoryzacja jest częścią plastra, nie osobnym zadaniem.** Jeśli po trzecim
powtórzeniu widzisz wzorzec — wyodrębnij od razu. Backlog „do posprzątania"
nigdy się nie opróżnia.

**Budżet wydajności to warunek ukończenia.** Plaster przekraczający próg nie jest
gotowy, niezależnie od tego, czy testy przechodzą.

**Punkt kontrolny po F1.7 jest realny.** Jeśli demo nie robi wrażenia na trzech
spedytorach, dalsza budowa nie naprawi produktu — naprawi go zmiana zakresu.
