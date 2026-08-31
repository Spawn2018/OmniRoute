# Aneks 25 — Audyt funkcjonalny i nowe obszary

---

# CZĘŚĆ I — AUDYT WZDŁUŻ ZADANYCH WYMIARÓW

## 1.1 Załączniki — stan i braki

Mamy generyczny `attachment` w M-79. **Brakuje warstwy wymagalności i kontroli
kompletności.** Załącznik, którego nie ma, jest niewidoczny — a to właśnie
jego brak blokuje operację.

### M-205 · Wymagalność i komplet dokumentów

```sql
document_requirement
  id, organization_id
  entity_type,          -- shipment | party | carrier_order | customs_declaration
  condition jsonb,      -- kiedy wymagany: mode=SEA, is_dg=true, country=US
  document_kind, is_mandatory
  blocks,               -- booking | departure | invoicing | closing | assignment
  valid_period_days,    -- dla dokumentów z ważnością
  reminder_days_before
  responsible_party     -- customer | carrier | us | agent

document_checklist            -- widok wyliczany per encja
  entity_type, entity_id
  required_count, provided_count, missing jsonb, expired jsonb
  is_complete, blocks_what text[]
```

**Zestawy wymagań, które trzeba zdefiniować:**

| Kontekst | Dokumenty |
|---|---|
| Zlecenie od klienta | zlecenie pisemne, packing list, faktura handlowa, instrukcje |
| Transport morski | booking, SI, B/L, VGM, świadectwo pochodzenia |
| Ładunek ADR | DGD, karta charakterystyki, certyfikat pakowania |
| Odprawa celna | faktura, packing list, świadectwa, upoważnienie |
| Przewoźnik drogowy | licencja, wypis, OCP, OC pojazdu, ADR kierowcy |
| Agent zagraniczny | licencja, ubezpieczenie, certyfikat rezydencji |

**Blokady, nie ostrzeżenia.** Zlecenie bez kompletu nie przechodzi do statusu
gotowości. Przewoźnik z wygasłym OCP nie da się przypisać do zlecenia.

---

## 1.2 Zgodność przewoźników i podwykonawców

### M-200 · Zgodność podwykonawcy ⚠

**To jest luka z realnym ryzykiem finansowym.** Zlecasz przewóz podwykonawcy
z wygasłym ubezpieczeniem odpowiedzialności cywilnej przewoźnika. Dochodzi
do szkody. Ubezpieczyciel odmawia, przewoźnik nie ma majątku, roszczenie
idzie do ciebie jako spedytora.

```sql
carrier_compliance
  id, party_id, organization_id
  document_kind,
  -- licencja_wspólnotowa | wypis_z_licencji | ocp | oc_pojazdu
  -- ubezpieczenie_kabotażowe | adr | certyfikat_kompetencji
  -- zaświadczenie_zus | zaświadczenie_us | gwarancja
  number, issuer, insured_sum, currency
  scope,                -- zakres terytorialny, rodzaj przewozów
  valid_from, valid_to
  file_path, verified_by, verified_at
  status,               -- valid | expiring | expired | missing | rejected
  blocks_assignment bool

carrier_vehicle             -- pojazdy podwykonawcy
  id, party_id, plate, kind
  adr_certificate_valid_to, inspection_valid_to
  is_approved, approved_at

carrier_rating
  party_id, period
  on_time_pickup_pct, on_time_delivery_pct
  damage_incidents, claim_amount
  document_completeness_pct, response_time_hours
  price_competitiveness_rank
  overall_score
```

**Mechanizm blokujący:** przypisanie zlecenia do przewoźnika sprawdza komplet
dokumentów. Wygasłe OCP blokuje przypisanie. Zwolnienie blokady wymaga
zatwierdzenia z M-179 i zostaje w audycie.

**Weryfikacja okresowa:** przewoźnik sprawdzony rok temu nie jest sprawdzony.
Data następnej weryfikacji, alert, automatyczne zawieszenie po przekroczeniu.

---

## 1.3 Integracje — obecny stan jest niewystarczający

Mamy publiczne API i webhooki (M-94). To pokrywa integratorów technicznych.
**Nie pokrywa klientów, którzy chcą wymiany danych bez programisty.**

### M-201 · Hub integracyjny

```sql
integration_connection
  id, organization_id, name
  direction,            -- inbound | outbound | bidirectional
  transport,            -- rest | webhook | sftp | email | edi
                        -- ftp | s3 | database | manual_upload
  format,               -- json | xml | csv | excel | edifact | fixed_width
  schedule,             -- realtime | cron | on_event | manual
  entity_types text[]
  mapping_id, credentials_encrypted
  is_active, last_run_at, last_status

integration_mapping
  id, organization_id, name
  source_schema jsonb, target_schema jsonb
  field_mappings jsonb,      -- w tym transformacje
  validation_rules jsonb
  sample_payload jsonb
  version, is_active

integration_run
  id, connection_id, started_at, finished_at
  records_in, records_ok, records_failed
  errors jsonb, file_path
```

**Kanały, które muszą być dostępne bez pisania kodu po stronie klienta:**

| Kanał | Zastosowanie |
|---|---|
| REST + OpenAPI | integratorzy techniczni |
| Webhooki | zdarzenia w czasie rzeczywistym |
| **SFTP z harmonogramem** | **najczęstszy sposób wymiany w spedycji** |
| Skrzynka mailowa z załącznikiem | klienci bez IT |
| Eksport zaplanowany | raport wysyłany codziennie o 6:00 |
| Import z pliku z mapowaniem | jednorazowe i cykliczne |
| EDI | M-39 |
| Łączniki iPaaS | Zapier, Make, n8n — pokrywa długi ogon |

**Kreator mapowania:** klient wgrywa przykładowy plik, system rozpoznaje kolumny,
klient mapuje przeciągnięciem, podgląd na stu wierszach, zapis jako połączenie
cykliczne. To jest różnica między integracją na tydzień a na godzinę.

**Katalog gotowych łączników** dla systemów, które pojawią się u wielu klientów:
Comarch, Symfonia, enova, Subiekt, wFirma, Fakturownia. Każdy zbudowany raz,
używany wielokrotnie.

### Udostępnianie własnych danych

```sql
data_share
  id, organization_id, party_id      -- komu udostępniamy
  scope,               -- own_shipments | own_invoices | tracking_only
  transport, schedule, format
  filters jsonb, field_whitelist text[]
  api_key_id, is_active
```

Klient chce swoje dane u siebie. Zamiast eksportu ręcznego — połączenie,
które wysyła je codziennie w uzgodnionym formacie.

---

## 1.4 Pomiary i KPI — brak frameworku

Metryki są rozproszone po modułach. **Nie ma warstwy, która je definiuje,
mierzy i porównuje z celem.**

### M-202 · Framework pomiarowy

```sql
kpi_definition
  id, organization_id NULL,        -- NULL = systemowa
  code, name, description
  category,            -- customer | quote | shipment | carrier
                       -- agent | employee | financial | operational | quality
  formula,             -- wyrażenie SQL nad warstwą semantyczną
  unit, direction,     -- higher_better | lower_better | target_range
  aggregation, dimensions text[]
  refresh_frequency, is_active

kpi_target
  id, kpi_id, dimension_ref NULL, period
  target_value, threshold_warning, threshold_critical
  set_by, approved_by

kpi_measurement
  id, kpi_id, dimension_ref, period
  value, target_value, variance_pct
  status, trend, computed_at

kpi_dashboard
  id, organization_id, role_id NULL, user_id NULL
  name, layout jsonb, kpi_ids uuid[], filters jsonb
```

### Katalog wskaźników do zdefiniowania

**Klienci**
przychód · marża brutto · marża po koszcie obsługi · marża po koszcie kapitału ·
DSO rzeczywisty vs umowny · liczba zleceń · wskaźnik wygranych ofert · udział
w portfelu · koncentracja ryzyka · liczba reklamacji · wskaźnik retencji ·
czas obsługi zapytania · wartość życiowa klienta

**Wyceny**
czas do oferty (mediana i p90) · liczba ofert na zapytanie · wskaźnik konwersji ·
średnia marża oferowana vs zrealizowana · rozrzut cenowy (CV) · liczba luk
wykrytych · odsetek ofert wymagających zatwierdzenia · odsetek ofert
automatycznych · przyczyny przegranych

**Zlecenia**
liczba wg gałęzi i relacji · terminowość odbioru i dostawy · liczba rolloverów ·
liczba wyjątków wg typu · średni czas realizacji vs planowany · koszt demurrage
i detention · marża planowana vs zrealizowana · odchylenie kosztu

**Armatorzy**
udział w wolumenie · terminowość · wskaźnik rolloverów · konkurencyjność cenowa ·
wykorzystanie alokacji kontraktowej · czas odpowiedzi API · dostępność integracji ·
liczba rozbieżności fakturowych

**Agenci**
wskaźnik odpowiedzi · mediana czasu odpowiedzi · konkurencyjność wg relacji ·
zgodność oferty z fakturą · liczba i wartość rozbieżności · terminowość
dokumentów · reklamacje · ocena łączna

**Przewoźnicy i podwykonawcy**
terminowość podstawienia i dostawy · szkody · kompletność dokumentów ·
czas reakcji na zlecenie · odsetek odrzuceń · cena vs rynek · zgodność
dokumentów zgodnościowych

**Pracownicy**
liczba obsłużonych zapytań i zleceń · czas do oferty · wskaźnik wygranych ·
marża wygenerowana · marża po koszcie kapitału · liczba błędów i niezgodności ·
czas reakcji · wykorzystanie automatyzacji · realizacja celu z budżetu

**Finansowe**
przychód · marża w trzech ujęciach · rotacja należności i zobowiązań ·
cykl konwersji gotówki · ekspozycja walutowa · odzysk z rozbieżności ·
wartość rezerw otwartych · wiekowanie · koszt kapitału

**Jakość i platforma**
skuteczność ekstrakcji · odsetek fałszywych pozytywów klasyfikacji ·
dostępność systemu · czas odpowiedzi p95 · liczba błędów · koszt AI na tenanta ·
wykorzystanie funkcji · stosunek refaktoryzacji kodu

**Warstwa semantyczna z Cube (M-59) definiuje te wskaźniki raz.** Wtedy
dashboard, raport, text-to-SQL i eksport liczą to samo. Bez niej trzy narzędzia
podadzą trzy różne marże i stracisz zaufanie.

---

## 1.5 Definiowanie wydruków — uzupełnienie

M-84 opisuje układ dokumentu. Brakuje **edytora dostępnego dla klienta**.

```sql
document_template_editor
  -- edytor wizualny: bloki przeciągane, podgląd na żywo
  -- biblioteka pól: {{quotation.number}}, {{party.name}}, {{lines}}
  -- warunki: {{#if is_dg}}...{{/if}}
  -- pętle po pozycjach z formatowaniem kwot
  -- wersjonowanie z możliwością cofnięcia
  -- podgląd na realnych danych przed zapisem
```

Klient, który nie może sam zmienić układu oferty, będzie o to prosił przy
każdym drobiazgu. To jest koszt wsparcia, nie funkcja.
---

# CZĘŚĆ II — PORTAL PRZEWOŹNIKA

## M-199 · Portal przewoźnika i podwykonawcy

Trzeci portal obok wewnętrznego i klienckiego. Inna grupa użytkowników,
inne potrzeby, inny poziom zaufania.

```sql
carrier_portal_user
  id, party_id, email, name, role
  -- dispatcher | driver | owner | accounting
  is_active, last_login_at

carrier_portal_invitation
  id, party_id, email, token, expires_at, accepted_at
```

## Co przewoźnik robi w portalu

| Funkcja | Wartość dla ciebie |
|---|---|
| **Przyjęcie lub odrzucenie zlecenia** | koniec z telefonami i mailami |
| Podanie kierowcy i pojazdu | dane wprost do systemu, bez przepisywania |
| Aktualizacja statusu | podstawienie, załadunek, w drodze, rozładunek |
| **Wgranie skanu CMR i zdjęć** | potwierdzenie dostawy natychmiast |
| Wgranie dokumentów zgodnościowych | licencja, OCP — sam pilnuje ważności |
| Podgląd swoich zleceń i rozliczeń | mniej pytań do księgowości |
| **Wystawienie faktury z danymi ze zlecenia** | eliminuje błędy w fakturach |
| Podgląd oceny (M-200) | motywuje do poprawy |
| Zgłoszenie problemu | z kontekstem zlecenia |

## Rzeczy, które zmieniają najwięcej

**Wgrywanie dokumentów zgodnościowych przez przewoźnika.** Dziś ktoś u ciebie
zbiera skany OCP od trzydziestu przewoźników i pilnuje dat. Po przeniesieniu
tego do portalu: przewoźnik dostaje przypomnienie, wgrywa sam, system weryfikuje
i odblokowuje przypisywanie zleceń.

**Potwierdzenie dostawy ze zdjęciem z telefonu.** Portal jako aplikacja
progresywna działa na telefonie kierowcy bez instalacji. Zdjęcie towaru przy
odbiorze i dostawie rozstrzyga spory o szkody — a dziś nie ma go wcale.

**Faktura wystawiana z danych zlecenia.** Przewoźnik nie wpisuje kwoty
z pamięci, tylko akceptuje wyliczoną. Eliminuje najczęstsze źródło rozbieżności
w rozliczeniach.

## Portal agenta

Ta sama infrastruktura, inne funkcje: odpowiadanie na zapytania (M-30),
wgrywanie cenników (M-73), podgląd zleceń, rozliczenia, ocena.

---

# CZĘŚĆ III — FAKTORING I FINANSOWANIE ŁAŃCUCHA DOSTAW

To jest najciekawszy pomysł z twojej listy i jednocześnie ten, przy którym
muszę postawić ostrzeżenie, zanim przejdę do projektu.

## 3.1 Ostrzeżenie regulacyjne ⚠

**Faktoring wykonywany przez ciebie oznacza status instytucji obowiązanej
w rozumieniu przepisów o przeciwdziałaniu praniu pieniędzy.**

Konsekwencje, których nie da się obejść:

```
□ wewnętrzna procedura AML z zatwierdzeniem
□ wyznaczenie osoby odpowiedzialnej na poziomie zarządu
□ identyfikacja i weryfikacja klienta oraz beneficjenta rzeczywistego
□ bieżące monitorowanie transakcji
□ raportowanie do Generalnego Inspektora Informacji Finansowej
□ przechowywanie dokumentacji przez określony okres
□ szkolenia pracowników
□ audyt wewnętrzny
□ odpowiedzialność karna i administracyjna za zaniechania
```

Do tego, jeśli finansujesz z własnych środków: kapitał obrotowy, ryzyko
kredytowe, wycena ryzyka, rezerwy na należności nieściągalne.

Do tego problem prawny specyficzny dla Polski: **umowy spedycyjne i transportowe
często zawierają zakaz cesji wierzytelności.** Faktoring bez zgody dłużnika
jest wtedy nieskuteczny.

**Dla jednoosobowej firmy budującej oprogramowanie to jest osobny biznes,
nie funkcja produktu.**

## 3.2 Trzy modele — od najlżejszego do najcięższego

### Model A — pośrednictwo *(rekomendowany na start)*

Nie finansujesz. Łączysz klienta z instytucją faktoringową, przekazujesz dane
o fakturach i zleceniach, zarabiasz prowizję od pośrednictwa.

```sql
factoring_partner
  id, organization_id NULL,      -- NULL = partner platformy
  name, api_endpoint, credentials_encrypted
  product_types text[], min_invoice, max_invoice
  advance_rate_pct, fee_structure jsonb
  countries text[], currencies text[]

factoring_offer                   -- oferta od partnera
  id, invoice_id, partner_id
  requested_at, advance_amount, fee, net_to_client
  decision, decided_at, expires_at
  our_commission

factoring_transaction
  id, offer_id, invoice_id
  disbursed_at, disbursed_amount
  repaid_at, status
  assignment_notified_at         -- powiadomienie dłużnika o cesji
```

**Bez statusu instytucji obowiązanej, bez kapitału, bez ryzyka.**
Przychód: prowizja od uruchomionej transakcji.

**Twoja przewaga nad bankiem:** widzisz zlecenie, dokumenty przewozowe,
potwierdzenie dostawy i historię płatniczą dłużnika. Faktor widzi tylko
fakturę. To znacząco lepsza ocena ryzyka — i to jest realny argument
przy negocjowaniu prowizji z partnerem faktoringowym.

### Model B — dynamiczne dyskonto *(to, co opisujesz dla podwykonawców klienta)*

**To nie jest faktoring i nie podlega tym samym obowiązkom.**

Klient płaci swojemu podwykonawcy wcześniej, z własnych środków, w zamian za
rabat. Nie ma cesji wierzytelności, nie ma finansowania przez osobę trzecią,
nie ma statusu instytucji obowiązanej. Jest wcześniejsza zapłata z upustem.

```sql
early_payment_program
  id, organization_id,            -- klient, który program prowadzi
  name, is_active
  eligible_supplier_ids uuid[]
  discount_formula,               -- np. 0,05% za każdy dzień przyspieszenia
  min_days_early, max_days_early
  daily_budget, currency
  auto_approve_below, requires_approval_above

early_payment_offer
  id, program_id, bill_id, supplier_party_id
  original_due_date, offered_payment_date
  original_amount, discount_amount, net_amount
  offered_at, expires_at
  status,                         -- offered | accepted | rejected | expired | paid
  accepted_at, paid_at

early_payment_settlement
  id, offer_id
  discount_realized, effective_annual_rate
  benefit_to_buyer, benefit_to_supplier
```

**Jak to działa w portalu podwykonawcy:**

```
Faktura FV/2026/00847 · 48 200 zł · termin 14.10 (za 45 dni)

  Zapłata za 3 dni     47 105 zł   (–1 095 zł)
  Zapłata za 10 dni    47 350 zł   (–  850 zł)
  Zapłata za 20 dni    47 715 zł   (–  485 zł)

  [ Wybierz termin ]
```

**Dla twojego klienta:** zwrot z wolnej gotówki znacznie wyższy niż na lokacie,
przy zerowym ryzyku kredytowym — płaci za coś, co i tak jest jego zobowiązaniem.
**Dla podwykonawcy:** gotówka bez faktoringu i bez cesji.
**Dla ciebie:** opłata za moduł albo udział w zrealizowanym dyskoncie.

To jest model, który polecam wdrożyć **pierwszy**. Jest lekki regulacyjnie,
technicznie prosty i tworzy wartość dla obu stron.

### Model C — faktoring własny *(dopiero po decyzji strategicznej)*

Finansujesz z własnych albo pozyskanych środków. Wymaga wszystkiego z punktu
3.1 plus kapitału. **Osobna spółka, osobna licencja operacyjna, osobny zespół.**

Nie wcześniej niż przy stu klientach i po analizie z prawnikiem oraz
doradcą finansowym.

## 3.3 Co zbudować w produkcie niezależnie od modelu

```sql
receivable_health                 -- ocena wierzytelności
  invoice_id
  debtor_credit_score,            -- z M-14
  debtor_payment_history,         -- z M-43
  document_completeness,          -- z M-205: czy jest POD, CMR, B/L
  dispute_flag,                   -- czy jest spór
  assignment_allowed,             -- czy umowa dopuszcza cesję ⚠
  eligibility_score
```

**Pole `assignment_allowed` jest krytyczne.** Zakaz cesji w umowie z klientem
uniemożliwia faktoring tej faktury. System musi to wiedzieć z rejestru umów
(M-93) i wykluczać takie faktury z ofert automatycznie.

Ta ocena jest wartościowa sama w sobie, niezależnie od finansowania: pokazuje,
które należności są zdrowe, a które ryzykowne.

---

# CZĘŚĆ IV — SILNIK PREDYKCYJNY: WERYFIKACJA

Sprawdziłem, czy mamy to, o co pytasz.

## Co jest

**M-61 — trzy warstwy.** Deterministyczna (ogłoszone GRI, PSS, blank sailings,
BAF ze wzoru, ETS), statystyczna (prognoza kierunku z przedziałem ufności,
z obowiązkowym backtestingiem przeciw modelowi naiwnemu) i kontekstowa
(zdarzenia, nigdy nie generuje liczby).

**M-24 — stawka jako obiekt probabilistyczny.** Zmienność relacji, marża
zagrożona, ryzyko wygaśnięcia marży w okresie ważności oferty.

**M-77 — warstwa drogowa.** Ceny paliwa jako 25–35% kosztu przejazdu,
publikowane codziennie.

## Czego świadomie nie ma

**Nie ma obietnicy przewidzenia ceny.** To była decyzja projektowa, nie
przeoczenie. Stawki spot mają grube ogony i napędzają je decyzje kilkunastu
armatorów — prognoza punktowa rozjedzie się i zniszczy zaufanie do całego
systemu.

Zamiast tego: **wiesz wcześniej i wiesz dlaczego.** Osiemdziesiąt procent
wartości leży w warstwie deterministycznej, która nie wymaga modelu — GRI jest
ogłoszeniem, nie prognozą.

## Co warto dodać

**M-206 · Prognoza stawki na relacji z własnych danych**

```sql
lane_rate_forecast
  id, organization_id, pol, pod, mode, container_type
  horizon_days, generated_at
  point_estimate, ci_low, ci_high, confidence_level
  drivers jsonb,          -- co składa się na prognozę
  model_version, backtest_mape, beats_naive bool
  data_points_used
```

**Warunki wdrożenia, które muszą zostać dotrzymane:**
- minimum dwanaście miesięcy własnych danych na relacji
- backtesting przeciw modelowi naiwnemu, publikowany wynik
- prognoza pokazywana wyłącznie z przedziałem, nigdy jako liczba
- widoczna zmierzona skuteczność: „nasze prognozy dwutygodniowe mylą się
  średnio o X%"
- brak prognozy przy zbyt małej liczbie obserwacji — komunikat, nie zgadywanie

To jest sprzedawalne. Obietnica przewidywania cen nie jest.
---

# CZĘŚĆ V — WYDAJNOŚĆ I REFAKTORYZACJA

Przegląd pod kątem tego, gdzie system zwolni przy realnym obciążeniu.

## 5.1 Miejsca, które zwolnią pierwsze

| Miejsce | Przyczyna | Rozwiązanie |
|---|---|---|
| Dobór stawek | 50k+ wierszy × 7 wymiarów | indeks pokrywający + widok materializowany per relacja |
| Lista zleceń z wyjątkami | wyliczanie wyjątków w locie | wyliczanie zdarzeniem, kolumna `has_exceptions` |
| Raport rentowności | agregacja po `shipment_charge` | tabela agregatów odświeżana przy zamknięciu zlecenia |
| Karta wyników agenta | liczenie z całej historii | przeliczanie cykliczne, nie na żądanie |
| Wyszukiwarka globalna | LIKE po wielu tabelach | `pg_trgm` z indeksem GIN, potem Meilisearch |
| Ekspozycja walutowa | suma po otwartych pozycjach | widok materializowany, odświeżanie zdarzeniem |
| Kolejka review ekstrakcji | JOIN po `rate_line` i `rate_sheet` | denormalizacja pól prezentacyjnych |
| Dashboard KPI | kilkanaście zapytań agregujących | tabela `kpi_measurement` liczona w tle |

## 5.2 Zasada, która to porządkuje

**Nic, co użytkownik widzi na liście, nie jest liczone w momencie otwarcia listy.**

Liczby na dashboardach, statusy zbiorcze, wyniki punktowe i agregaty
są wyliczane zdarzeniem albo cyklicznie i zapisywane. Ekran czyta gotowe.

```sql
-- wzorzec dla każdej wartości wyliczanej i prezentowanej
  computed_value, computed_at, computed_from_version
  is_stale bool           -- oznaczane zdarzeniem, przeliczane w tle
```

## 5.3 Refaktoryzacje warte zaplanowania

**R-01 · Rozdzielenie odczytu od zapisu w module wyceny.**
Model zapisu (normalizowany, z ograniczeniami) i model odczytu (denormalizowany,
zoptymalizowany pod ekran). Synchronizacja zdarzeniem. To nie jest pełne CQRS,
tylko rozdzielenie dwóch reprezentacji.

**R-02 · Wydzielenie ekstrakcji do osobnego procesu.**
Parsowanie dokumentów zjada pamięć i procesor. Osobna kolejka, osobne workery,
osobne limity — żeby duży cennik nie spowalniał wycen.

**R-03 · Warstwa cache z jawnym unieważnianiem.**
Nie TTL na wszystkim, tylko klucz zawierający wersję danych źródłowych.
Zmiana cennika unieważnia cache relacji, a nie czeka na wygaśnięcie.

**R-04 · Partycjonowanie tabel zdarzeniowych po czasie.**
`shipment_event`, `audit_log`, `decision_log`, `inbound_message` rosną
najszybciej. Partycje miesięczne z automatycznym odłączaniem starych.

**R-05 · Wyniesienie raportów na replikę.**
Wszystko z warstwy analitycznej na replikę odczytu. Dziś zaplanowane,
warto wymusić testem architektonicznym.

## 5.4 Pomiar wydajności jako produkt

Klient korporacyjny zapyta o czasy odpowiedzi. Miej odpowiedź:

```sql
performance_metric
  organization_id, endpoint, period
  p50_ms, p95_ms, p99_ms, error_rate
  request_count
```

Publiczna strona statusu (M-76) z historycznymi czasami odpowiedzi
to sygnał dojrzałości, którego konkurencja nie ma.

---

# CZĘŚĆ VI — PODSUMOWANIE

## Nowe moduły

| Kod | Moduł | Faza | Nakład |
|---|---|---|---|
| **M-199** | **Portal przewoźnika i podwykonawcy** | 8 | 12 dni |
| **M-200** | **Zgodność podwykonawców** | 8 | 5 dni |
| **M-201** | **Hub integracyjny** | 7 | 15 dni |
| **M-202** | **Framework KPI** | 6 | 10 dni |
| M-205 | Wymagalność dokumentów | 2 | 5 dni |
| M-206 | Prognoza stawki na relacji | 9 | 8 dni |
| M-207 | Faktoring — model pośrednictwa | 9 | 8 dni |
| **M-208** | **Dynamiczne dyskonto** | 9 | 10 dni |

**73 dni. Rejestr: 208 modułów.**

## Cztery rekomendacje

**① Dynamiczne dyskonto zamiast faktoringu — na start.**
To, co opisujesz dla podwykonawców twoich klientów, jest wcześniejszą zapłatą
z upustem, nie faktoringiem. Nie wymaga statusu instytucji obowiązanej, kapitału
ani zgody na cesję. Wdrażasz jako moduł, klient zarabia na własnej gotówce,
ty bierzesz udział w dyskoncie. **Zbuduj to pierwsze, faktoring dopiero potem
i w modelu pośrednictwa.**

**② Zgodność podwykonawców przed portalem przewoźnika.**
Przypisanie zlecenia przewoźnikowi z wygasłym OCP to ryzyko, które przy jednej
szkodzie kosztuje więcej niż cały moduł. Pięć dni pracy.

**③ Hub integracyjny z SFTP i mapowaniem — wcześniej niż planowałem.**
Wymiana plików przez SFTP z harmonogramem to najczęstszy sposób integracji
w spedycji, a kreator mapowania zamienia integrację z tygodnia na godzinę.
To jest funkcja sprzedażowa, nie techniczna.

**④ Framework KPI z warstwą semantyczną, nie osobne raporty.**
Definiujesz wskaźnik raz w warstwie semantycznej. Dashboard, raport, eksport
i zapytanie językiem naturalnym liczą to samo. Bez tego trzy narzędzia podadzą
trzy różne marże — i to jest błąd, po którym klient przestaje ufać wszystkim
liczbom w systemie.

## Odpowiedź na pytanie o silnik predykcyjny

**Mamy go i jest zaprojektowany konserwatywnie — celowo.** Warstwa
deterministyczna daje 80% wartości bez modelu, bo GRI jest ogłoszeniem.
Warstwa statystyczna wymaga roku danych i obowiązkowego backtestingu.
Prognozy punktowej bez przedziału nie będzie, bo pierwsza rozjechana
zniszczyłaby zaufanie do całego systemu.

Dodaję M-206: prognoza na twoich własnych relacjach, z twoich danych,
z publikowaną zmierzoną skutecznością. To jest sprzedawalne. Obietnica
przewidywania rynku nie jest.
