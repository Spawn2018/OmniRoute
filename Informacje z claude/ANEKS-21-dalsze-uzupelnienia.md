# Aneks 21 — Dalsze uzupełnienia

Dziesięć modułów. Dwa pierwsze to poważne luki, reszta to uzupełnienia
podnoszące kompletność.

---

# M-99 · Odprawy celne ⚠

**Największa luka domenowa.** Mieliśmy kody opłat `CUST-EXP`, `CUST-IMP` i `T1`,
wspominaliśmy AES, AIS i PUESC — ale nie ma modułu. A znaczna część polskich
spedytorów prowadzi własną agencję celną albo obsługuje odprawy przez partnera.
Bez tego system obsługuje pół procesu.

```sql
customs_declaration
  id, shipment_id, organization_id
  kind,              -- export | import | transit_t1 | transit_t2
                     -- temporary | reexport
  procedure_code,    -- kod procedury celnej
  mrn,               -- numer ewidencyjny zgłoszenia
  office_of_entry, office_of_destination
  declarant_party_id, representation,  -- direct | indirect
  eori_declarant, eori_importer
  status,            -- draft | submitted | accepted | released
                     -- under_control | rejected | cancelled
  submitted_at, released_at
  system,            -- AES | AIS | NCTS2 | ICS2
  guarantee_id NULL

customs_item
  id, declaration_id, item_no
  hs_code, taric_code, description
  origin_country, preferential_origin bool
  gross_weight, net_weight, quantity, unit
  customs_value, currency, statistical_value
  duty_rate, duty_amount
  vat_rate, vat_amount, excise_amount
  documents jsonb            -- świadectwa, faktury, pozwolenia

customs_guarantee
  id, organization_id
  kind,              -- comprehensive | individual
  grn, amount, currency, valid_until
  used_amount, available_amount   -- ← śledzenie wykorzystania

customs_event
  id, declaration_id, event_code, message_type
  received_at, payload jsonb
```

## Funkcje, które robią różnicę

**Śledzenie wykorzystania zabezpieczenia generalnego.** Zabezpieczenie ma limit;
przekroczenie blokuje kolejne odprawy. Operator dowiaduje się o tym w najgorszym
momencie. Alert przy 80% wykorzystania to funkcja tania i bardzo widoczna.

**Kalkulator należności celnych** przed odprawą — kod TARIC, wartość celna,
pochodzenie, preferencje. Klient chce wiedzieć wcześniej, ile zapłaci.

**Powiązanie z sankcjami i podwójnym zastosowaniem** — moduł M-53 sprawdza
strony i statki; tutaj dochodzi towar po kodzie TARIC.

**Terminy i komunikaty.** Zgłoszenie przyjęte, towar pod kontrolą, zwolnienie —
każdy komunikat jako zdarzenie, powiązane z wyjątkami z M-37.

**Archiwum zgłoszeń** — obowiązek przechowywania przez pięć lat, patrz M-104.

**Uwaga:** to jest moduł, który możesz zbudować w wersji pełnej (własna agencja)
albo lekkiej (rejestr odpraw robionych przez partnera, z numerami MRN i kosztami).
Wersja lekka to trzy dni, pełna to trzy tygodnie plus certyfikacja dostępu do
systemów celnych.

---

# M-100 · Widoczność stawek zakupowych ⚠

**Luka przecinająca cały system.** Dodana po fazie drugiej byłaby droga,
bo dotyka każdego ekranu z kwotami.

## Problem

W większości spedycji handlowiec **nie widzi stawek zakupowych**. Widzi cenę
sprzedaży i informację, czy mieści się w progu marży. Operacje widzą jedno
i drugie. Właściciel widzi wszystko.

Powody są dwa i oba poważne: ochrona relacji z agentami przed przejęciem
i ochrona przed odejściem handlowca z bazą kosztową do konkurencji.

W naszym projekcie każdy ekran pokazuje `buy_amount` obok `sell_amount`.

## Rozwiązanie

```sql
-- rozszerzenie role
  cost_visibility,   -- full | margin_only | sell_only | none
  can_see_supplier_names bool,
  can_export_costs bool

-- rozszerzenie quotation_line, shipment_charge
  -- filtrowanie na poziomie serializacji DTO, nie w komponencie
```

**Musi być egzekwowane w warstwie API**, nie ukrywaniem kolumny w interfejsie.
Handlowiec bez uprawnienia nie dostaje pola `buy_amount` w odpowiedzi —
w ogóle, nie ukryte.

| Tryb | Widzi |
|---|---|
| `full` | koszt, marża, nazwy dostawców |
| `margin_only` | cenę sprzedaży i procent marży, bez kwoty kosztu |
| `sell_only` | wyłącznie cenę sprzedaży i próg „mieści się / nie mieści" |
| `none` | tylko dane operacyjne, bez kwot |

**Konsekwencje projektowe:**
- osobne DTO dla każdego trybu, wybierane przez zależność uprawnień
- eksport do Excela respektuje tryb
- raporty respektują tryb
- API publiczne respektuje zakres klucza
- test bezpieczeństwa: użytkownik `sell_only` nie może uzyskać kosztu żadną drogą

To jest ten sam rodzaj decyzji co wielodostępność: łatwa teraz, kosztowna później.
Dopisz jako plaster w fazie 2, razem z silnikiem wyceny.

---

# M-101 · Prowizje handlowców

Spedytorzy płacą handlowcom prowizję od marży. Bez modułu liczy się to
w Excelu, z opóźnieniem i sporami.

```sql
commission_plan
  id, organization_id, name
  basis,             -- gross_margin | net_margin | revenue
  calculation,       -- percent | tiered | flat_per_shipment
  tiers jsonb,       -- progi i stawki
  payout_trigger,    -- on_invoice | on_payment | on_shipment_close
  clawback_days,     -- cofnięcie przy nieopłaconej fakturze
  valid_from, valid_to

commission_assignment
  id, plan_id, user_id, party_id NULL, lane_pattern NULL
  share_pct          -- podział przy wspólnej obsłudze

commission_entry
  id, shipment_id, user_id, plan_id
  base_amount, rate, amount, currency
  status,            -- accrued | approved | paid | clawed_back
  period, approved_by, paid_at
```

**Rozliczenie po zapłacie, nie po fakturze** — to jest właściwy domyślny
wyzwalacz. Prowizja od faktury, której klient nie zapłacił, wraca jako spór
z handlowcem.

**Powiązanie z M-90 (rezerwy) i M-43 (koszt kapitału):** prowizja liczona
od marży brutto jest zawyżona, bo nie uwzględnia kosztu finansowania.
System może liczyć od marży po koszcie kapitału — i to jest argument,
który właściciel doceni.

---

# M-102 · Ubezpieczenie cargo

Mieliśmy kod `INS`, nie mieliśmy procesu. A spedytorzy sprzedają ubezpieczenie
i zarabiają na prowizji.

```sql
cargo_insurance_policy
  id, organization_id
  kind,              -- open_cover | single_shipment
  insurer_party_id, policy_number
  valid_from, valid_to
  max_value_per_shipment, currency
  rate_table jsonb,  -- stawka wg rodzaju towaru i relacji
  deductible

cargo_insurance_certificate
  id, shipment_id, policy_id
  certificate_number
  insured_value, currency, premium, commission
  coverage,          -- ICC_A | ICC_B | ICC_C
  issued_at, file_path

insurance_claim
  id, certificate_id, shipment_id
  reported_at, incident_date, description
  claimed_amount, settled_amount
  status, surveyor, documents jsonb
```

**Kalkulacja składki przy wycenie** — pozycja `INS` liczona automatycznie
z wartości towaru i tabeli stawek, z widoczną prowizją jako przychód (M-22).

**Terminy zgłoszenia szkody są krótkie** i ich przekroczenie kończy roszczenie
niezależnie od zasadności. To samo zastrzeżenie co przy reklamacjach z M-55 —
liczenie automatyczne, alert obowiązkowy.

---

# M-103 · Wiele podmiotów w jednym koncie

Różne od wielodostępności. Jeden klient prowadzi dwie spółki — spedycyjną
i transportową — i chce jednego systemu z rozdzielonym fakturowaniem.

```sql
-- organization_branch z M-80 rozszerzone
legal_entity
  id, organization_id
  legal_name, tax_id, krs
  address jsonb, bank_accounts uuid[]
  numbering_scheme_id, is_default

-- rozszerzenia
shipment.legal_entity_id
invoice.legal_entity_id
```

Plus rozliczenia międzyfirmowe: spółka transportowa fakturuje spedycyjną,
oba dokumenty w jednym systemie, wynik skonsolidowany i osobno.

**To nie jest przypadek brzegowy w Polsce** — rozdzielenie spedycji od
transportu własnego jest częste ze względów podatkowych i licencyjnych.

---

# M-104 · Archiwum i retencja dokumentów

Mieliśmy retencję w kontekście RODO. Tu chodzi o **obowiązek przechowywania**,
który działa w drugą stronę: nie wolno usunąć.

| Kategoria | Okres |
|---|---|
| Dokumenty celne | 5 lat od końca roku |
| Faktury i księgi | 5 lat od końca roku podatkowego |
| Dokumenty przewozowe | wg umowy i przedawnienia roszczeń |
| Dokumenty ADR | wg przepisów |
| Korespondencja przy sporach | do zakończenia sprawy |

```sql
retention_rule
  id, organization_id, entity_type, document_kind
  retain_years, basis,     -- legal | contractual | internal
  legal_reference, action_after   -- delete | anonymize | archive

legal_hold                        -- blokada usunięcia przy sporze
  id, organization_id, entity_type, entity_id
  reason, placed_by, placed_at, released_at
```

**Blokada usunięcia przy sporze** jest ważna: jeśli toczy się reklamacja albo
postępowanie, retencja automatyczna nie może skasować dowodów. Kolizja
obowiązku przechowywania z prawem do usunięcia z RODO rozstrzyga się na korzyść
obowiązku prawnego — ale system musi to rozróżniać.

---

# M-105 · Magazyn i CFS — wersja minimalna

Nie pełny WMS, ale bez tego nie obsłużysz drobnicy ani składowania.

```sql
warehouse_receipt
  id, organization_id, warehouse_id, shipment_id NULL
  party_id, received_at, received_by
  pieces, weight_kg, volume_cbm
  condition_notes, photos jsonb

warehouse_stock
  id, receipt_id, location_code
  pieces_in, pieces_out, pieces_available
  free_storage_until, storage_rate

warehouse_release
  id, receipt_id, released_at, released_to
  pieces, document_ref, gate_pass_number
```

**Naliczanie składowania po okresie darmowym** to ten sam mechanizm co
watchdog free time z M-37 — jeden kod, dwa zastosowania.

---

# M-106 · Kontenery i wymiana sprzętu

```sql
container_movement
  id, container_number, shipment_id NULL
  movement_type,     -- pickup_empty | gate_in | gate_out
                     -- return_empty | repositioning
  location_id, occurred_at
  eir_number, eir_file_path        -- protokół zdawczo-odbiorczy
  condition,         -- sound | damaged
  damage_notes, photos jsonb

container_detention
  id, container_number, shipment_id
  free_days, started_at, returned_at
  chargeable_days, rate, amount, currency
  disputed bool, dispute_reason
```

**Protokół zdawczo-odbiorczy ze zdjęciami** rozstrzyga spory o uszkodzenia
kontenera, które potrafią kosztować tysiące. Zdjęcie przy odbiorze i zwrocie
to funkcja dla aplikacji mobilnej albo dla kierowcy — i jedyny dowód, jaki masz.

**Wyliczanie detention z możliwością sporu** — armatorzy naliczają błędnie
częściej, niż się przyznają. Rejestr z datami i dowodami to podstawa reklamacji.

---

# M-107 · Ładunki specjalne

Rozszerzenie modelu, nie osobny proces.

```sql
-- rozszerzenie shipment_container i quotation_cargo
  is_oog bool,                     -- ponadgabaryt
  oog_dimensions jsonb,            -- przekroczenia w cm na każdej osi
  is_reefer bool,
  temperature_setpoint, temperature_range jsonb
  ventilation, humidity
  requires_genset bool,
  is_flexitank, is_breakbulk
  lashing_required, survey_required
```

**Reefer:** monitorowanie temperatury z zapisem, alarm przy odchyleniu.
Zerwanie łańcucha chłodniczego to szkoda całkowita — a dane z rejestratora
są jedynym dowodem, po czyjej stronie leży wina.

**Ponadgabaryt:** inne stawki, wymagane zezwolenia, ograniczenia tras,
akceptacja armatora przed bookingiem.

---

# M-108 · Zadania i kalendarz operatora

Mieliśmy `shipment_task` przy zleceniu. Brakuje widoku poprzecznego.

```sql
task
  id, organization_id
  entity_type, entity_id NULL,     -- może być niezwiązane ze zleceniem
  title, description
  assignee_user_id, watchers uuid[]
  due_at, priority, status
  source,            -- manual | workflow | sop | exception
  completed_at, completed_by

calendar_sync
  id, user_id, provider,           -- google | microsoft
  credentials_encrypted, sync_direction
  last_sync_at
```

**Widok „mój dzień":** zadania na dziś, cut-offy w ciągu 48 godzin, oferty
wygasające, zapytania bez odpowiedzi, dokumenty do zatwierdzenia.

**Synchronizacja z kalendarzem** — cut-offy i terminy w kalendarzu operatora,
bo tam patrzy rano, a nie w system.

---

# PODSUMOWANIE

| Moduł | Nazwa | Faza | Nakład |
|---|---|---|---|
| **M-99** | **Odprawy celne** | 6 | 3 dni (lekka) / 15 dni (pełna) |
| **M-100** | **Widoczność stawek zakupowych** | **2** | **4 dni** |
| M-101 | Prowizje handlowców | 6 | 4 dni |
| M-102 | Ubezpieczenie cargo | 6 | 5 dni |
| M-103 | Wiele podmiotów | 1 | 3 dni |
| M-104 | Archiwum i retencja | 7 | 3 dni |
| M-105 | Magazyn i CFS | 8 | 6 dni |
| M-106 | Kontenery i EIR | 8 | 4 dni |
| M-107 | Ładunki specjalne | 8 | 3 dni |
| M-108 | Zadania i kalendarz | 3 | 5 dni |

**40–52 dni. Rejestr rośnie z 98 do 108 modułów.**

## Dwa, których nie odkładaj

**M-100 w fazie 2, razem z silnikiem wyceny.** To jest decyzja przecinająca
cały system, jak wielodostępność. Cztery dni teraz, przepisywanie każdego
ekranu i każdego raportu później. Do tego jest to funkcja, o którą klient
zapyta na pierwszym spotkaniu — „czy mój handlowiec zobaczy, ile płacę agentowi".

**M-103 w fazie 1.** Rozdzielenie spółki spedycyjnej od transportowej jest
w Polsce częste. Dołożenie `legal_entity` do schematu na starcie to trzy dni;
później to migracja wszystkich dokumentów i numeracji.

## Uwaga o zakresie

To jest dwudziesty pierwszy aneks i sto ósmy moduł. **Zmieniło się główne
ryzyko projektu.** Wcześniej było nim to, że czegoś nie przewidzieliśmy.
Teraz jest nim to, że zakres przerasta wykonanie.

Rejestr jest kompletny jako mapa. Ale realizacja wszystkiego to około pięciu lat
pracy jednej osoby. **Fazy 0–3 pozostają jedynym, co musi powstać przed
pierwszym klientem** — reszta to katalog, z którego wybierasz na podstawie
tego, co powiedzą klienci, a nie tego, co jest na liście.

Gdybyś zapytał mnie o kolejny aneks, odpowiem tak samo jak teraz: prawdopodobnie
znajdę jeszcze dziesięć modułów, bo domena jest głęboka. Ale wartość
z kolejnego wyliczania jest już mniejsza niż wartość z rozpoczęcia budowy.
