# Aneks 20 — Co jeszcze pominęliśmy

Przegląd pełnego cyklu życia zlecenia. Dziesięć modułów, w tym trzy, których
brak byłby odczuwalny od pierwszego wdrożenia.

---

# M-89 · Booking i dokumentacja przewozowa ⚠

**To jest największa luka.** Mamy ofertę, mamy zlecenie, mamy tracking i
fakturę — a między nimi jest cały proces operacyjny, którego nie zaprojektowaliśmy.

## 20.1 Co się dzieje po akceptacji oferty

```
akceptacja → booking u armatora → potwierdzenie → SI → B/L draft
→ zatwierdzenie draftu → VGM → zgłoszenia (ENS/AMS) → gate-in
→ wypłynięcie → B/L oryginał lub telex → wydanie towaru
```

Każdy z tych kroków ma termin, wersje, korekty i może się nie udać.

```sql
booking
  id, shipment_id, carrier_party_id
  price_id,                        -- z live_offer
  carrier_booking_ref, status,     -- requested | confirmed | amended
                                   -- rolled | cancelled
  requested_at, confirmed_at
  vessel, voyage, etd, eta
  cutoffs jsonb,                   -- gate, doc, vgm, dg, reefer
  amendment_count, previous_booking_id
  rollover_reason

shipping_instruction
  id, booking_id, version
  shipper, consignee, notify, marks_and_numbers
  cargo_description, hs_codes text[]
  freight_terms,                   -- prepaid | collect
  bl_type,                         -- original | seaway | telex
  bl_copies_count
  submitted_at, accepted_at
  correction_of_id, correction_reason

bl_document
  id, booking_id, bl_number, kind, -- master | house
  status,                          -- draft | approved | issued
                                   -- released | surrendered
  draft_sent_at, approved_by_customer_at, approved_by_user_id
  issued_at, release_type, released_at
  file_path

document_courier                   -- śledzenie oryginałów
  id, shipment_id, document_ids uuid[]
  carrier, tracking_number
  sent_at, sent_to_party_id, received_at
```

## 20.2 Dlaczego to jest ważne

**Śledzenie oryginałów B/L to realny problem operacyjny.** Oryginały krążą
kurierem, giną, docierają po statku. Bez rejestru nikt nie wie, gdzie są —
a bez oryginału odbiorca nie odbierze towaru.

**Korekta SI kosztuje.** Każda zmiana po złożeniu instrukcji to opłata
armatora i ryzyko opóźnienia. Wersjonowanie z powodem korekty pokazuje,
kto i dlaczego generuje te koszty.

**Rollover musi być zdarzeniem, nie notatką.** Kontener nie wypłynął —
zmienia się ETA, zaczyna biec detention, klient musi wiedzieć. To wpina się
w M-37 (wyjątki) i M-74 (bliżniak kosztu).

## 20.3 Zlecenia do podwykonawców

```sql
carrier_order                      -- zlecenie do przewoźnika drogowego
  id, shipment_id, carrier_party_id
  order_number, service_type
  pickup jsonb, delivery jsonb,    -- adres, kontakt, okno czasowe
  cargo jsonb, special_instructions
  agreed_price, currency
  status,                          -- sent | accepted | rejected
                                   -- in_progress | completed
  sent_at, accepted_at, driver_name, vehicle_plate

proof_of_delivery
  id, carrier_order_id
  delivered_at, received_by, signature_path
  documents jsonb,                 -- skan CMR, zdjęcia
  remarks, has_damage bool
```

**Awizacja dostawy** — okno czasowe u odbiorcy, potwierdzenie, przypomnienie.
Bez tego kierowca stoi, a postojowe idzie na twój koszt.

---

# M-90 · Rezerwy kosztowe ⚠

**Przez brak tego modułu marża miesięczna kłamie.**

Zamykasz miesiąc. Zlecenie dostarczone, faktura wystawiona klientowi, przychód
zaksięgowany. Ale faktura od agenta przyjdzie za trzy tygodnie. W raporcie
miesiąc wygląda znakomicie, następny fatalnie — a rzeczywistość jest pośrodku.

```sql
cost_accrual
  id, shipment_id, charge_code
  expected_amount, currency
  source,          -- quotation | rate_line | historical_avg | manual
  confidence,      -- wysoka gdy z oferty agenta, niska gdy z historii
  accrued_at, period
  actual_bill_id NULL, actual_amount NULL
  variance, released_at
  status           -- open | partially_matched | closed | written_off
```

**Mechanizm:**

1. Przy zamknięciu zlecenia system tworzy rezerwy na koszty niezafakturowane,
   biorąc kwoty z oferty agenta albo ze średniej historycznej
2. Rezerwa wchodzi do wyniku okresu jako koszt
3. Gdy przychodzi faktura — dopasowanie, różnica jako korekta
4. Rezerwy starsze niż X dni → alert („agent nie wystawił faktury")

**Efekt:** raport rentowności miesiąca jest prawdziwy, a nie zależny od tego,
kiedy agentowi chciało się wystawić fakturę.

**Efekt uboczny, równie cenny:** rezerwy niezamknięte po sześćdziesięciu dniach
to lista kosztów, których nikt nigdy nie zafakturował. Czasem to prezent,
czasem sygnał, że coś się zgubiło.

Wpina się w M-41 (rozliczenie z fakturą) i M-74 (bliźniak kosztu).

---

# M-91 · Fakturowanie zaawansowane

## 20.4 Faktury zbiorcze

Duzi klienci nie chcą trzydziestu faktur miesięcznie. Chcą jednej,
z załącznikiem specyfikacyjnym.

```sql
invoice_batch
  id, organization_id, customer_party_id
  period_from, period_to
  grouping,        -- by_month | by_week | by_lane | by_cost_center
  shipment_ids uuid[]
  invoice_id, specification_file_path
  status
```

Bez tego nie obsłużysz klienta korporacyjnego. To nie jest funkcja
zaawansowana, tylko warunek wejścia do segmentu.

## 20.5 Zaliczki i proformy

```sql
proforma_invoice
  id, quotation_id NULL, shipment_id NULL
  amount, currency, due_date
  paid_at, settled_by_invoice_id
```

Nowy klient bez historii, ładunek wysokiej wartości, relacja ryzykowna —
przedpłata jest standardem. Powiązana z limitem kredytowym z M-14.

## 20.6 Refaktury

Koszt przeniesiony na klienta jeden do jednego, bez marży, z widocznym
dokumentem źródłowym. Częste przy opłatach celnych i podatkach.

```sql
-- rozszerzenie invoice_line
  is_pass_through bool,
  source_bill_id, source_document_path
```

## 20.7 Noty korygujące i anulowanie

Faktura korygująca z powodem, powiązaniem do oryginału i obsługą KSeF.
Anulowanie przed wysłaniem. To jest codzienność księgowa, nie przypadek brzegowy.

---

# M-92 · Cenniki sprzedażowe dla klienta

Odwrotność bazy zakupowej: **twój cennik dla stałego klienta.**

```sql
customer_tariff
  id, organization_id, customer_party_id
  name, valid_from, valid_to, currency
  status,          -- draft | active | expired | superseded
  approved_by, approved_at

customer_tariff_line
  id, tariff_id
  pol, pod, mode, container_type
  charge_code, amount, basis
  min_amount, conditions jsonb
```

**Po co:** klient ze stałym cennikiem nie wymaga liczenia oferty za każdym
razem. Zapytanie wpada, system stosuje cennik, oferta wychodzi w sekundy
albo automatycznie (M-03, tryb `auto`).

Do tego portal klienta pokazuje jego własny cennik — funkcja, którą klienci
korporacyjni traktują jako oczywistą, a mało kto ma.

**Ostrzeżenie:** cennik sprzedażowy musi być pilnowany wobec zmian stawek
zakupowych. Stawka zakupowa rośnie, cennik sprzedażowy stoi — marża znika
po cichu. Alert obowiązkowy, powiązany z M-24.

---

# M-93 · Umowy z klientami

```sql
customer_agreement
  id, organization_id, party_id
  kind,            -- framework | tariff | dpa | nda | sla
  number, signed_at, valid_from, valid_to
  auto_renewal bool, notice_period_days
  file_path, signed_by_us, signed_by_them
  parent_agreement_id              -- aneksy
  status
```

Rejestr umów z terminami wypowiedzenia i automatycznym przedłużeniem.
Alert na trzy miesiące przed wygaśnięciem — bo umowa, która wygasła
niezauważona, to relacja bez podstawy prawnej.

Powiązane z M-16 (SOP klienta) i M-65 (kontrakty indeksowane).

---

# M-94 · Publiczne API i webhooki

Nie jako funkcja techniczna, tylko jako **produkt**.

```sql
api_key
  id, organization_id, name
  key_hash, scopes text[], rate_limit
  created_by, last_used_at, expires_at, revoked_at

webhook_endpoint
  id, organization_id, url, secret
  event_types text[], is_active
  failure_count, last_success_at

webhook_delivery
  id, endpoint_id, event_id
  payload, response_status, attempts
  delivered_at, next_retry_at
```

**Dlaczego to jest produkt, a nie dodatek:**

- klient korporacyjny chce, żeby jego system dostawał statusy automatycznie
- integrator klienta pyta o API na drugim spotkaniu
- webhooki eliminują odpytywanie i są tańsze dla obu stron
- publiczna dokumentacja API to sygnał dojrzałości

**Wersjonowanie od pierwszego dnia.** `/v1/` w ścieżce, polityka deprecacji
z dwunastomiesięcznym wyprzedzeniem. Po pierwszej integracji nie możesz
zepsuć kontraktu.

---

# M-95 · Raporty standardowe

Text-to-SQL z M-59 jest świetny, ale klient oczekuje gotowych raportów
w pierwszym dniu. Lista minimalna:

| Raport | Odbiorca |
|---|---|
| Rentowność wg zleceń | operacje |
| Rentowność wg klientów (trójwymiarowa) | właściciel |
| Rentowność wg relacji | handel |
| Rentowność wg handlowców | właściciel |
| Skuteczność ofert (wygrane/przegrane, powody) | handel |
| Czas do oferty | właściciel |
| Otwarte zlecenia wg statusu | operacje |
| Zlecenia z wyjątkami | operacje |
| Wiekowanie należności | finanse |
| Wiekowanie zobowiązań | finanse |
| Rezerwy niezamknięte | finanse |
| Rozbieżności faktura–wycena | finanse |
| Ekspozycja walutowa | właściciel |
| Prognoza kasowa | właściciel |
| Wygasające stawki | operacje |
| Pokrycie stawkami wg relacji | handel |
| Karta wyników agentów | operacje |
| Wolumen wg armatorów | handel |
| Wykorzystanie alokacji kontraktowej | handel |
| Emisje CO₂ wg klientów | klient |

Do tego **dashboard operacyjny**: co dziś wymaga uwagi — cut-offy w ciągu
48 godzin, dokumenty do zatwierdzenia, zapytania bez odpowiedzi, przekroczone
limity, rezerwy do wyjaśnienia.

---

# M-96 · Ciągłość działania

```sql
backup_verification
  id, backup_id, verified_at
  restore_duration_seconds, rows_verified
  status, notes
```

**Kopia zapasowa, która nie była testowo odtworzona, nie istnieje.**
Automatyczne odtwarzanie na osobnej instancji raz w tygodniu, z weryfikacją
liczby rekordów i czasu odtworzenia.

**Runbooki** w `docs/runbooks/` — co robić, gdy:

```
□ padnie baza
□ padnie API armatora w środku dnia
□ KSeF nie odpowiada przy wystawianiu faktur
□ pipeline ekstrakcji zaczyna zwracać śmieci
□ klient zgłasza, że widzi cudze dane   ← najpoważniejszy scenariusz
□ wyciek klucza API
□ wykryta podatność w zależności
□ tenant przekracza limity i wpływa na innych
```

Każdy runbook: objaw, diagnoza, kroki, kogo powiadomić, jak potwierdzić
rozwiązanie. Piszesz je na spokojnie, używasz w panice.

**RTO i RPO zadeklarowane w SLA** i przetestowane, nie wymyślone.

---

# M-97 · Niezgodności i doskonalenie

Poza reklamacjami od klientów (M-55) — **rejestr własnych błędów**.

```sql
nonconformity
  id, organization_id
  source,          -- internal | customer | agent | audit
  shipment_id NULL, category
  description, cost_impact, currency
  root_cause, corrective_action
  responsible_user_id, due_date, closed_at
```

Kategorie: błąd w dokumencie, przekroczony cut-off, zła stawka w ofercie,
brak zgłoszenia, opóźnienie z naszej winy.

**Wartość:** po pół roku widzisz, że 40% niezgodności to jeden typ błędu na
jednej relacji. To jest wejście do usprawnienia procesu albo do funkcji
w systemie, która go wyeliminuje.

Certyfikaty jakości i AEO wymagają takiego rejestru — a twoi klienci
korporacyjni mogą o nie pytać.

---

# M-98 · Migracja danych przy wdrożeniu

Nie usługa konsultingowa, tylko **narzędzie w produkcie**.

```sql
migration_project
  id, organization_id, source_system
  status, started_at, completed_at

migration_mapping
  id, project_id, entity_type
  source_format, column_mapping jsonb
  transformation_rules jsonb
  validation_errors jsonb
```

Kreator: wgraj plik → system rozpoznaje strukturę → mapujesz kolumny →
podgląd stu wierszy → walidacja → import z raportem błędów → możliwość
wycofania.

Obowiązkowo dla: kontrahentów, kontaktów, stawek, historii zleceń.

**To jest przedłużenie M-75 (wdrożenie w jeden dzień).** Klient przychodzący
z innego systemu ma dane w Excelu — jeśli import zajmie mu godzinę zamiast
tygodnia rozmów z tobą, wdrożenie przestaje być barierą sprzedażową.

---

# PODSUMOWANIE

| Moduł | Nazwa | Faza | Nakład |
|---|---|---|---|
| **M-89** | **Booking i dokumentacja przewozowa** | **6** | **12 dni** |
| **M-90** | **Rezerwy kosztowe** | **6** | **4 dni** |
| M-91 | Fakturowanie zaawansowane | 6 | 7 dni |
| M-92 | Cenniki sprzedażowe dla klienta | 5 | 5 dni |
| M-93 | Umowy z klientami | 5 | 3 dni |
| M-94 | Publiczne API i webhooki | 7 | 6 dni |
| M-95 | Raporty standardowe | 6 | 8 dni |
| M-96 | Ciągłość działania | 0 i 7 | 5 dni |
| M-97 | Niezgodności | 8 | 3 dni |
| M-98 | Migracja danych | 2 | 5 dni |

**58 dni. Rejestr rośnie z 88 do 98 modułów.**

## Trzy, których brak byłby najbardziej odczuwalny

**M-89 — booking i dokumentacja.** Bez tego system kończy się na ofercie
i zaczyna przy fakturze, a między nimi jest cała praca spedytora. To była
najpoważniejsza luka w całym projekcie.

**M-90 — rezerwy kosztowe.** Cztery dni pracy, po których raport miesięczny
przestaje kłamać. Bez tego trójwymiarowa rentowność klienta z M-46 opiera się
na danych, które zależą od tego, kiedy agentowi chciało się wystawić fakturę.

**M-91 — faktury zbiorcze.** Nie funkcja zaawansowana, tylko warunek wejścia
do segmentu klientów korporacyjnych.

## Zmiana w harmonogramie

M-96 wchodzi częściowo w fazie zerowej — weryfikacja kopii zapasowych
i pierwsze runbooki. Reszta w fazie siódmej.

M-98 przed punktem kontrolnym po fazie drugiej, bo migracja danych jest
częścią demo: pokazujesz, że klient jest w systemie w godzinę.

M-89 i M-90 razem z fazą szóstą — bez nich moduł finansowy stoi na
niepełnych danych.
