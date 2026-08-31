# System spedycyjny — specyfikacja nadrzędna

Dokument scalający wszystkie ustalenia. Źródło prawdy dla pracy z agentem kodującym.

**Wersja:** 1.0 · **Data:** sierpień 2026
**Autor koncepcji:** Sebastian Bożek, LOGMAR
**Charakter:** produkt wielodostępny na sprzedaż, nie narzędzie wewnętrzne

---

# CZĘŚĆ A — STRATEGIA I ARCHITEKTURA

## A1. Czym to jest

Platforma zarządzania stawkami i ofertowania dla spedycji morskiej, rozwijana w kierunku pełnego ERP. Trzy filary, których nie ma razem żaden system na rynku polskim:

1. **Automatyczne budowanie bazy cen zakupowych** — cennik przychodzi mailem jako Excel, PDF albo treść wiadomości, po minucie jest w systemie jako strukturalne stawki
2. **Bezpośrednia integracja z armatorami** — stawki spot i tracking kontenerów bez otwierania sześciu portali
3. **Warstwa agentowa** — system wystawiony jako narzędzie dla modelu językowego, nie chatbot doklejony obok

## A2. Czym to nie jest (na tym etapie)

Nie jest pełnym ERP. Nie jest systemem księgowym. Nie obsługuje frachtu lotniczego, drogowego ani magazynu. Te moduły mają miejsce w modelu danych, ale nie w kodzie.

**Uzasadnienie:** wymiana ERP to cykl sprzedażowy 6–12 miesięcy i decyzja zarządu. Moduł stawek działający obok istniejącego systemu to 2–6 tygodni i decyzja kierownika działu. Wchodzisz wąsko, zbierasz klientów i informację zwrotną, moduły dobudowujesz w kolejności, którą wskażą.

## A3. Dla kogo

Spedytor morski z własną bazą stawek zakupowych i co najmniej dwiema osobami w ofertowaniu. Główny ból, który rozwiązujesz:

- cenniki od kilkunastu agentów i armatorów, każdy w innym formacie, przepisywane ręcznie do Excela
- oferta liczona 30–40 minut, z ryzykiem pominięcia dopłaty
- brak wiedzy, na której relacji i którym kliencie faktycznie się zarabia
- sześć zakładek przeglądarki rano, żeby sprawdzić, gdzie są kontenery

## A4. Architektura — warstwy

```
┌─────────────────────────────────────────────────────────────┐
│  INTERFEJSY                                                  │
│  React SPA · Portal klienta · Serwer MCP · REST API · Copilot│
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────────┐
│  LOGIKA DOMENOWA                                             │
│  Silnik wyceny · Maszyna stanów zlecenia · Reguły marży      │
│  Kalkulator opłat · Numeracja · Uprawnienia                  │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────────┐
│  ŹRÓDŁA STAWEK — trzy, jeden interfejs                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Cenniki      │  │ API          │  │ Wprowadzone  │       │
│  │ (AI pipeline)│  │ armatorów    │  │ ręcznie      │       │
│  │ PDF/XLS/mail │  │ (live spot)  │  │              │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────────┐
│  INTEGRACJE ZEWNĘTRZNE                                       │
│  Armatorzy (DCSA T&T, Offers, Quick Quotes) · KSeF · GUS     │
│  Biała lista · NBP · Poczta (EmailEngine) · Bank (MT940)     │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────────┐
│  DANE                                                        │
│  PostgreSQL + RLS · MinIO (dokumenty źródłowe) · Redis       │
└─────────────────────────────────────────────────────────────┘
```

## A5. Dziesięć zasad projektowych

Te zasady rozstrzygają większość decyzji, które pojawią się w trakcie. Gdy agent kodujący zaproponuje coś sprzecznego z którąś — zasada wygrywa.

**1. Multi-tenancy od pierwszej migracji.**
`organization_id` w każdej tabeli, RLS wymuszany przez bazę, nie przez kod aplikacji. Doklejenie tego później to przepisanie każdego zapytania i każdego testu.

**2. Konfiguracja jest danymi, nie kodem.**
Kody opłat, szablony dokumentów, statusy zlecenia, reguły marży, numeracja, pola własne — wszystko jako rekordy w bazie, per organizacja. Jeśli nowy klient wymaga zmiany w kodzie, przy piątym utrzymanie zjada cały twój czas.

**3. `Charge` to jedyne miejsce prawdy o marży.**
Kupno i sprzedaż na jednym rekordzie, waluta i kurs zamrożone w momencie księgowania. Cała rentowność — per zlecenie, klient, relacja, handlowiec — liczy się z tej jednej tabeli.

**4. Model językowy wyciąga dane, kod je przetwarza.**
Żadnej arytmetyki, przeliczeń walutowych ani mapowania na słowniki po stronie modelu. Model zwraca surowy tekst z pozycją źródłową, resztę robi deterministyczny kod.

**5. Provenance obowiązkowe.**
Każda stawka wie, skąd pochodzi: plik, arkusz, komórka albo identyfikator odpowiedzi API i moment pobrania. Bez tego nie odpowiesz klientowi, skąd wzięła się cena na fakturze.

**6. Stawki są niemutowalne.**
Zmiana ceny to nowy rekord i oznaczenie starego jako zastąpionego. Musisz umieć odtworzyć, po jakiej stawce liczyłeś ofertę pół roku temu.

**7. Kwoty jako `numeric`, nigdy float. Waluta nierozerwalnie z kwotą.**
Typ `Money`, nie gołe liczby. Przy siedmiu walutach na jednej ofercie błąd jest kwestią czasu.

**8. Nic nie wchodzi do bazy bez akceptacji człowieka.**
Ekstrakcja trafia do kolejki review. Automatyczny zapis wyłącznie dla zweryfikowanych szablonów o pewności powyżej progu.

**9. Poświadczenia armatorów należą do klienta, nie do ciebie.**
Każdy tenant ma własne konta i klucze, system odpytuje w jego imieniu. Nie masz prawa redystrybuować dostępu ani cudzych stawek kontraktowych.

**10. Wszystko, co przychodzi z zewnątrz, jest niezaufane.**
Cennik od nieznanego agenta może zawierać instrukcje dla modelu. Odpowiedź API może być niekompletna. Plik może być zainfekowany. Waliduj, filtruj, loguj.

## A6. Granica: co robi AI, a co deterministyczny kod

| Zadanie | Wykonawca | Dlaczego |
|---|---|---|
| Rozpoznanie, czy załącznik to cennik | Kod (nadawca) → model (fallback) | 90% przypadków rozstrzyga adres nadawcy |
| Odczytanie układu strony i tabel | Docling / Marker | Do tego są zbudowane |
| Wyciągnięcie wartości z tabeli | Model językowy | Nieregularne układy, których nie da się sparsować regułami |
| Mapowanie „THC POL" → `OTHC` | Kod: alias → fuzzy → embedding | Musi być powtarzalne i wyjaśnialne |
| Normalizacja portu na UN/LOCODE | Kod (słownik aliasów) | To jest wyszukiwanie, nie rozumowanie |
| Przeliczenie waluty | Kod (kurs NBP) | Model nie liczy. Nigdy |
| Suma pozycji oferty | Kod | Jak wyżej |
| Wykrycie brakujących dopłat | Kod (reguły per incoterm) | Reguła biznesowa, nie interpretacja |
| Wykrycie kolizji stawek | Kod | Porównanie zakresów dat |
| Odpowiedź na „jaka marża na Azji w Q2" | Model + warstwa semantyczna + walidator SQL | Model planuje, warstwa definiuje pojęcia, walidator sprawdza |
| Decyzja o zapisie do bazy | Człowiek | Zasada 8 |

## A7. Trzy źródła stawek — jeden interfejs

To jest kluczowa decyzja architektoniczna całego systemu. Stawki przychodzą z trzech zupełnie różnych światów, ale silnik wyceny nie może o tym wiedzieć.

| | Cenniki (AI) | API armatorów | Ręczne |
|---|---|---|---|
| Format | Excel, PDF, mail | JSON | Formularz |
| Ważność | okno `valid_from`–`valid_to` | **brak — cena dynamiczna** | okno |
| Aktualność | dni/tygodnie | sekundy | dowolna |
| Kompletność opłat | zwykle pełna | częściowa (patrz C3) | zależna od operatora |
| Koszt pobrania | ~1 zł za cennik | limit zapytań | czas człowieka |
| Identyfikator do bookingu | brak | `price_id` | brak |
| Dostępność | zawsze (w bazie) | zależna od API | zawsze |

**Konsekwencja:** silnik wyceny operuje na abstrakcji `RateCandidate`, a nie na tabeli. Trzy adaptery zwracają ten sam kształt. Stawki z API są pobierane równolegle i mają krótki TTL, stawki z cenników leżą w bazie i stanowią natychmiastowe tło, gdy API nie odpowie.
---

# CZĘŚĆ B — MODEL DANYCH

Wszystkie tabele mają `organization_id`, `created_at`, `updated_at`, `created_by`. Nie powtarzam tego przy każdej.

## B1. Fundament wielodostępności

```sql
organization
  id, name, tax_id, country_code
  plan,                          -- pakiet abonamentowy
  settings jsonb,                -- numeracja, waluta domyślna, język
  is_active

app_user
  id, organization_id, email, name, is_active, last_login_at

role
  id, organization_id, name, permissions jsonb

user_role
  user_id, role_id

-- RLS na każdej tabeli:
-- CREATE POLICY tenant_isolation ON <table>
--   USING (organization_id = current_setting('app.current_org')::uuid);

audit_log
  id, organization_id, entity_type, entity_id, action,
  before jsonb, after jsonb, user_id, ip, at
  -- wypełniany triggerem bazodanowym, nie kodem aplikacji

usage_metric                     -- metering od dnia pierwszego
  id, organization_id, metric,   -- quotes | shipments | sheets_parsed
                                 -- api_calls | active_users
  value, period_start, period_end
```

## B2. Kontrahenci

```sql
party
  id, legal_name, short_name
  tax_id, vat_eu, regon, krs
  country_code, address jsonb
  roles text[],                  -- customer|vendor|agent|carrier
                                 -- shipper|consignee|notify
  payment_terms_days, credit_limit, credit_currency
  default_currency, language
  gus_synced_at, vies_checked_at
  is_active

party_contact
  id, party_id, name, email, phone, position
  is_primary, portal_access, portal_user_id

party_bank_account
  id, party_id, iban, currency, bank_name
  whitelist_status, whitelist_checked_at

party_charge_override           -- stawki dedykowane dla klienta
  id, party_id, charge_code, lane_pattern
  amount, currency, basis, valid_from, valid_to

carrier_profile                 -- rozszerzenie dla armatorów
  party_id, scac_code, is_nvocc
  rate_source_email,
  api_adapter,                  -- maersk|hapag|cma|msc|none
  dcsa_tnt_version
```

## B3. Słowniki — globalne i per organizacja

```sql
port
  unlocode PK,                  -- PLGDY, CNSHA
  name, country_code, lat, lng, is_seaport
  aliases text[]                -- z improved-un-locodes

container_type
  code,                         -- 20DV 40DV 40HC 40RF 20RF 40OT 20FR 45HC
  teu_factor, max_payload_kg, is_reefer, is_special

charge_code                     -- ~60 kodów bazowych, patrz B4
  code, organization_id NULL,   -- NULL = globalny, inaczej własny klienta
  name_pl, name_en, category, side,
  default_basis, default_currency
  applies_to text[],            -- FCL|LCL|BOTH
  is_percentage, percent_of
  required_for_incoterms text[] -- do wykrywania braków

charge_code_alias               -- rośnie sam, patrz C2.6
  id, alias, charge_code, party_id NULL,
  confirmed_by, confirmed_at, confidence

incoterm
  code, named_place_required, cost_boundary
```

## B4. Słownik opłat — pięć grup

Pełna lista w osobnym pliku. Struktura:

| Grupa | `side` | Przykłady |
|---|---|---|
| Pre-carriage | `origin` | DRAY-EXP, PICKUP, WAIT, ADR-ROAD |
| Local POL | `origin` | OTHC, DOCFEE-O, BL-FEE, SEAL, VGM, ISPS-O, CUST-EXP, T1, DG-O, CFS-O |
| Fracht | `freight` | OFR, BAF, CAF, LSS, **ETS**, PSS, GRI, WRS, CANAL-SUEZ, PCS, EBS, CIC, OWS |
| Zgłoszenia | `filing` | ENS, AMS, ISF, ACI, AFR |
| Local POD | `destination` | DTHC, DO-FEE, ISPS-D, CUST-IMP, DEMUR, DETEN, STORAGE, CFS-D, DRAY-IMP |

Każdy kod ma `aliases`. Przykład dla `OTHC`:
`["THC","THC ORIGIN","OTHC","O/THC","TERMINAL HANDLING","TERMINAL HANDLING CHARGE POL","THC AT ORIGIN","OPŁATA TERMINALOWA"]`

## B5. Stawki zakupowe — źródło statyczne

```sql
rate_sheet                      -- jedna dostawa cennika
  id, source_party_id
  source_type,                  -- email|excel|pdf|manual|tender|portal
  source_file_path,             -- MinIO
  source_file_hash,             -- SHA-256, deduplikacja
  received_at, valid_from, valid_to
  status,                       -- ingesting|review|active|superseded|rejected
  extraction_confidence, extraction_model, extraction_cost
  template_id NULL,             -- jeśli sparsowany szablonem
  superseded_by, raw_meta jsonb

rate_line                       -- pozycja cenowa, NIEMUTOWALNA
  id, rate_sheet_id
  mode,                         -- FCL|LCL
  pol, pod, via NULL
  carrier_party_id NULL, service_name NULL, transit_days NULL
  container_type NULL
  charge_code
  amount numeric(14,4), currency char(3)
  basis,                        -- PER_CONTAINER|PER_BL|PER_SHIPMENT|PER_WM
                                -- PER_TON|PER_CBM|PER_TEU|PER_KG|PERCENT|FLAT
  min_amount, max_amount, percent_of
  free_time_days NULL
  valid_from, valid_to
  conditions jsonb,             -- commodity, dg_class, min_qty, contract_no
  source_ref jsonb,             -- {sheet,row,col} ← ZASADA 5
  confidence, is_verified, superseded_by

extraction_template             -- pamięć układów, patrz C2.5
  id, party_id, fingerprint
  layout jsonb, success_count, last_confirmed_at, is_active
```

## B6. Stawki live z API armatorów — źródło dynamiczne

Osobna tabela, bo semantyka jest inna: **brak ważności**, krótki TTL, identyfikator do bookingu.

```sql
carrier_credential              -- ZASADA 9: poświadczenia klienta
  id, organization_id, carrier_party_id
  adapter,                      -- maersk|hapag|cma|msc
  credentials_encrypted bytea,  -- klucz szyfrujący per tenant
  scopes text[], account_ref
  is_active, last_ok_at, last_error, rate_limit_remaining

live_offer                      -- cache odpowiedzi API
  id, organization_id
  adapter, carrier_party_id
  pol, pod, container_type, mode
  requested_at, expires_at,     -- TTL, typowo 15–60 min
  price_id,                     -- ← klucz do bookingu (Maersk, Hapag)
  product_name,                 -- "Maersk Spot", "Quick Quotes Spot"
  vessel_name, voyage, etd, eta, cutoff_doc, cutoff_vgm
  total_amount, currency
  terms_url, terms_text,        -- wymóg armatora: widoczne T&C
  raw_response jsonb            -- ZASADA 5: provenance
  
live_offer_charge               -- rozbicie oferty na opłaty
  id, live_offer_id
  charge_code,                  -- po mapowaniu
  description_raw,              -- co zwróciło API
  amount, currency, basis
  is_mapped bool                -- false = nierozpoznana opłata, do review
```

**Uwagi projektowe:**
- `expires_at` zamiast `valid_to` — cena spot jest dynamiczna i nie ma gwarancji obowiązywania
- `price_id` musi przetrwać do momentu bookingu, nawet po wygaśnięciu cache'u
- `terms_text` przechowywany, bo armatorzy wymagają wyświetlania warunków przy ofercie
- `is_mapped=false` na pozycji oznacza opłatę, której nie znasz — trafia do kolejki, nie znika po cichu

## B7. Wycena

```sql
quotation
  id, quote_number, version
  customer_party_id, salesperson_user_id
  mode, pol, pod, incoterm, named_place
  commodity, hs_code, is_dangerous, imo_class, un_number
  valid_from, valid_to
  status,                       -- draft|sent|accepted|lost|expired
  lost_reason, currency
  fx_rate_source, fx_date       -- kurs zamrożony
  sent_at, decided_at

quotation_cargo
  id, quotation_id
  container_type, qty                              -- FCL
  packages, gross_weight_kg, volume_cbm, chargeable_wm  -- LCL

quotation_variant               -- wariant per dostawca
  id, quotation_id
  supplier_party_id, source_type,  -- sheet|api_live|manual
  transit_days, service_name, vessel, etd, eta
  live_offer_id NULL,           -- jeśli z API
  price_id NULL,                -- do bookingu
  is_selected, total_buy, total_sell, margin_pct

quotation_line
  id, quotation_variant_id
  charge_code, description_override
  basis, qty
  buy_amount, buy_currency
  buy_rate_line_id NULL,        -- ← źródło: cennik
  buy_live_offer_charge_id NULL,-- ← źródło: API
  sell_amount, sell_currency, fx_rate
  margin_amount, margin_pct     -- kolumny wyliczane
  is_visible_to_customer, sort_order

quotation_gap                   -- wykryte braki
  id, quotation_variant_id
  charge_code, reason           -- required_by_incoterm|usual_on_lane|expired_rate
```

`quotation_gap` to tabela, która uratuje najwięcej pieniędzy. Najczęstsza strata w drobnicy morskiej to nie zła stawka, tylko zapomniana dopłata.

## B8. Zlecenie

```sql
shipment
  id, job_number, quotation_id NULL
  customer_party_id, shipper_party_id, consignee_party_id
  notify_party_id, agent_party_id, carrier_party_id
  direction (EXPORT|IMPORT|CROSS), mode (FCL|LCL)
  incoterm, named_place
  pol, pod, place_of_receipt, place_of_delivery
  booking_number, mbl_number, hbl_number
  carrier_booking_ref,          -- z API bookingu
  vessel_name, voyage_number
  etd, eta, atd, ata
  cutoff_doc, cutoff_vgm, cutoff_gate
  status, operator_user_id

shipment_container
  id, shipment_id, container_number, seal_number, container_type
  gross_weight_kg, tare_kg, vgm_kg, vgm_method, vgm_submitted_at
  free_time_until, last_known_location, last_event_at

shipment_charge                 -- ZASADA 3: jedno miejsce prawdy
  id, shipment_id
  charge_code, basis, qty
  buy_amount, buy_currency, buy_party_id
  buy_status,                   -- estimated|confirmed|invoiced|paid
  sell_amount, sell_currency
  sell_status
  fx_rate, fx_date

shipment_event                  -- model zdarzeń DCSA
  id, shipment_id, container_id NULL
  event_type,                   -- EQUIPMENT|TRANSPORT|SHIPMENT
  event_code,                   -- DCSA: GTIN, LOAD, DEPA, ARRI, DISC, GTOT...
  event_classifier,             -- PLN|ACT|EST
  location_unlocode, facility_code
  event_datetime, received_at
  source,                       -- api|manual|edi|email
  carrier_raw jsonb

shipment_task
  id, shipment_id, title, assignee_user_id, due_at, completed_at

shipment_document
  id, shipment_id, doc_type, file_path
  visibility (internal|customer)
  generated_from_template, uploaded_by
```

## B9. Fakturowanie

```sql
invoice                         -- AR
  id, shipment_id NULL, customer_party_id
  invoice_number, issue_date, due_date
  currency, fx_rate, net_amount, vat_amount, gross_amount
  ksef_number, ksef_status, ksef_sent_at
  status

invoice_line
  id, invoice_id, shipment_charge_id NULL
  description, qty, unit_price, vat_rate, net_amount

bill                            -- AP, analogicznie
payment
  id, party_id, amount, currency, value_date
  bank_ref,                     -- z MT940
  matched_invoice_id NULL, match_confidence
```

## B10. Konfiguracja per organizacja — ZASADA 2

```sql
document_template
  id, organization_id, doc_type, name
  engine,                       -- typst|docx|html
  content, is_default

numbering_scheme
  id, organization_id, entity_type   -- quotation|shipment|invoice
  pattern,                      -- "OF/{YYYY}/{seq:5}"
  current_seq, reset_period, last_reset_at

workflow_definition
  id, organization_id, entity_type
  states jsonb, transitions jsonb, auto_tasks jsonb

margin_rule
  id, organization_id
  scope,                        -- global|customer|lane|charge_code
  scope_ref, method,            -- percent|fixed|max_of
  value, min_margin, priority

custom_field
  id, organization_id, entity_type, field_key
  label, data_type, is_required, options jsonb
```
---

# CZĘŚĆ C — PRZEPŁYWY

## C1. Mapa przepływów

```
     MAIL rates@ ─┐
     Excel/PDF   ─┼──► [C2] PIPELINE AI ──► rate_line ──┐
     Treść maila ─┘                                      │
                                                         ├──► [C4] SILNIK
     API armatora ──► [C3] ADAPTERY ──► live_offer ──────┤     WYCENY
                                                         │        │
     Formularz ──────────────────────► rate_line ────────┘        │
                                                                  ▼
                                                            quotation
                                                                  │
                                                                  ▼
     [C5] TRACKING ◄────── shipment ◄──── konwersja ◄──── akceptacja
        DCSA T&T                │
                                ▼
                        shipment_charge ──► faktura ──► KSeF
```

## C2. Pipeline AI — cenniki z maila, Excela i PDF

### C2.1 Etapy

```
[0] INGEST
    EmailEngine → webhook → wyciągnięcie załączników
    hash SHA-256 → deduplikacja → zapis do MinIO
    ↓
[1] CLASSIFY
    mapowanie po nadawcy (deterministyczne, ~90% przypadków)
    fallback: model Haiku → czy cennik? FCL/LCL/local/inland?
    ↓
[2] TEMPLATE?
    fingerprint układu → znany? 
    TAK → parser deterministyczny (koszt 0, pewność wysoka)
    NIE → ścieżka poniżej
    ↓
[3] LAYOUT
    Excel: calamine → inwentarz arkuszy, detekcja nagłówków, scalone komórki
    PDF:   Docling / Marker → warstwa tekstowa lub OCR
    Mail:  HTML → tekst + tabele
    ↓
[4] EXTRACT
    Instructor + schemat Pydantic, chunkowanie per arkusz
    obowiązkowo: pola _raw + source_ref + unparsed_regions
    ↓
[5] NORMALIZE
    porty → UN/LOCODE (aliasy z improved-un-locodes)
    opłaty → charge_code (alias → RapidFuzz → embedding)
    kontenery, waluty, basis, daty ważności
    ↓
[6] VALIDATE
    arytmetyka i reguły w KODZIE
    zakresy sanity, wymagane pola, kolizje z istniejącymi stawkami
    ↓
[7] REVIEW
    kolejka z oceną pewności, diff vs poprzednia wersja relacji
    akceptacja jednym kliknięciem, korekta zasila słownik aliasów
    ↓
[8] COMMIT
    rate_sheet.status = active, poprzednia → superseded
```

### C2.2 Schemat ekstrakcji

```json
{
  "carrier": "string|null",
  "valid_from": "YYYY-MM-DD|null",
  "valid_to": "YYYY-MM-DD|null",
  "currency_default": "EUR",
  "lanes": [{
    "pol_raw": "Gdynia",
    "pod_raw": "Shanghai",
    "via_raw": null,
    "service": "AE7",
    "transit_days": 32,
    "mode": "FCL",
    "charges": [{
      "description_raw": "Ocean Freight 40'HC",
      "container_type_raw": "40HC",
      "amount": 1850.00,
      "currency": "USD",
      "basis_raw": "per container",
      "min_amount": null,
      "free_time_days": 14,
      "remarks": "subject to GRI 01.10",
      "source_ref": {"sheet":"FCL EXPORT","row":47,"col":"H"}
    }]
  }],
  "unparsed_regions": [
    {"sheet":"Notes","reason":"prose remarks, not tabular"}
  ]
}
```

### C2.3 Cztery twarde reguły

1. **Model nie liczy.** Żadnych sum, przeliczeń, mnożenia.
2. **Model nie zapisuje.** Wszystko przez kolejkę review (ZASADA 8).
3. **Bez `source_ref` rekord nie wchodzi** (ZASADA 5).
4. **`unparsed_regions` obowiązkowe.** Milcząco pominięta tabela z dopłatami to najgorszy możliwy błąd — oferta wyjdzie za tanio, dowiesz się przy fakturze.

### C2.4 Bezpieczeństwo wejścia

Cennik od nieznanego agenta to niezaufane dane (ZASADA 10). Wystarczy instrukcja wpisana w kolumnę „uwagi", żeby ekstraktor zaczął zwracać stawki, których w cenniku nie ma.

- `llm-guard` na wejściu i wyjściu, od pierwszego dnia
- `presidio` do wykrycia danych osobowych przed wysłaniem do zewnętrznego API
- przełącznik „przetwarzanie wyłącznie lokalne" per tenant (wymóg części klientów, patrz D3)

### C2.5 Pamięć szablonów — optymalizacja rzędu wielkości

```json
{
  "party_id": "...",
  "fingerprint": "hash nagłówków + nazw arkuszy",
  "sheets": {
    "FCL EXPORT": {
      "header_row": 5,
      "columns": {"POL":"B","POD":"C","20DV":"F","40HC":"H","VALID":"M"},
      "charge_rows": {"OFR":47,"BAF":48,"LSS":49}
    }
  },
  "success_count": 12
}
```

Po kilku miesiącach ~80% cenników idzie ścieżką deterministyczną. Różnica między systemem za kilkanaście złotych miesięcznie a za kilkaset.

### C2.6 Uczenie słownika

Każda korekta w kolejce review zapisuje alias:
```
"TERMINAL HANDLING POL" → OTHC, party_id=X, confirmed_by=user
```
System uczy się słownictwa każdego agenta osobno. `party_id` w aliasie rozwiązuje sytuację, gdy dwóch agentów używa tego samego skrótu na różne opłaty.

### C2.7 Kolizje

Nowa stawka nachodzi na istniejącą (ta sama relacja + kod + kontener + zachodzące okresy):
- nowszy `received_at` → stara dostaje `valid_to = new.valid_from - 1 dzień`
- ten sam okres, inna kwota → **decyzja człowieka**, nigdy automatycznie
- różni dostawcy → obie zostają, wycena porównuje

## C3. Adaptery armatorów

### C3.1 Wzorzec

Każdy armator to osobny adapter implementujący wspólny interfejs. Silnik wyceny nie wie, z kim rozmawia.

```python
class CarrierAdapter(Protocol):
    def get_spot_offers(self, req: OfferRequest) -> list[LiveOffer]: ...
    def get_schedules(self, pol, pod, date_range) -> list[Schedule]: ...
    def get_tracking_events(self, ref: TrackingRef) -> list[DcsaEvent]: ...
    def create_booking(self, price_id, details) -> BookingResult: ...
    def get_coverage(self) -> Coverage: ...   # obsługiwane relacje i kontenery
```

### C3.2 Stan integracji per armator

| Armator | Spot quotes | Tracking | Uwagi |
|---|---|---|---|
| **Hapag-Lloyd** | Quick Quotes + Quick Quotes Spot przez API | DCSA T&T 2.2 + zdarzenia reeferowe | **Zacznij tutaj.** Jedyny z API zwracającym pokrycie: obsługiwane relacje, typy kontenerów i rodzaje ładunku. Eliminuje połowę obsługi błędów. 140+ serwisów, 600 portów, także DG |
| **Maersk** | Offers API — pełna oferta z trasą, harmonogramem, statkiem, deadline'ami i **cenami wraz z dopłatami** | DCSA T&T 2.2, Booking 2.0 beta | Publiczny przewodnik onboardingowy. Wymaga spełnienia wymogów UI (C3.4) |
| **CMA CGM** | Pricing API — **tylko fracht**, bez opłat lokalnych, inland i DDSM; SpotOn osobnym API | DCSA T&T 2.1/2.2 | Braki uzupełniasz z własnej bazy opłat lokalnych |
| **MSC** | Instant Quote w portalu, API mniej dojrzałe | DCSA T&T 1.2 i 2.2 | Tracking tak, wyceny na później |
| **ONE, Evergreen, ZIM, HMM, Yang Ming, PIL** | portale (Green X, eZ Quote), API nierówne | DCSA w różnych wersjach | Tracking bezpośrednio, wyceny przez agregator |
| Reszta (COSCO, feeder) | — | — | Agregator albo ręcznie |

Dziesięciu członków DCSA reprezentuje ~75% globalnego handlu kontenerowego. Sześć integracji da ~80–85% twojego wolumenu.

### C3.3 Semantyka stawek live

**Oferty spot nie mają okresu ważności — cena jest dynamiczna.** To nie jest szczegół, to zmienia model danych (patrz B6):

- `expires_at` = TTL cache'u, nie ważność oferty
- `price_id` musi przetrwać do bookingu
- ponowne odpytanie może zwrócić inną cenę — pokazuj moment pobrania
- oferta w wysłanej klientowi wycenie musi mieć zapisane, że była live w chwili X

### C3.4 Wymogi armatorów wobec twojego interfejsu

Nieoczywiste, ale wiążące. Przewodnik onboardingowy Maerska wymaga między innymi:

- nazwa produktu wyświetlana jako „Maersk Spot"
- **brak pola ważności** (cena dynamiczna)
- widoczne warunki handlowe wraz z karami i opłatami
- `price_id` widoczny przy kwocie — klient używa go do bookingu przez EDI, INTTRA albo booking API
- opłaty D&D i kary pokazane w wynikach wyszukiwania
- wszystkie opcje statków widoczne, żeby dało się porównać daty wypłynięcia

Zaprojektuj ekran wyników z tymi wymogami od początku. Przerabianie po odrzuceniu certyfikacji kosztuje tydzień.

### C3.5 Ograniczenia

- relacje amerykańskie podlegają regulacji FMC, wymagającej specjalnej obsługi ofert spotowych
- pokrycie głównie kontenery dry, część relacji i towarów wyłączona
- limity zapytań per konto — cache i kolejkowanie obowiązkowe
- poświadczenia per tenant (ZASADA 9): stawki są kontraktowe, nie masz prawa ich redystrybuować

### C3.6 Ścieżka przeglądarkowa — ostateczność

`browser-use` na poświadczeniach klienta, do jego własnego konta, za jego pisemną zgodą. Nadal zwykle wbrew regulaminowi portalu, ryzyko: zablokowane konto klienta. Używaj wyłącznie tam, gdzie API nie istnieje, i traktuj jako rozwiązanie tymczasowe.

## C4. Silnik wyceny

```
WEJŚCIE: pol, pod, mode, kontenery/ładunek, incoterm, commodity, DG?

1. RÓWNOLEGLE:
   a) zapytanie do bazy rate_line (natychmiast)
   b) zapytania do adapterów armatorów (2–5 s każde, równolegle)
   
   Pokazuj wyniki w miarę spływania. Nie każ czekać 20 sekund.
   Stawki z bazy stanowią natychmiastowe tło.

2. Grupuj kandydatów po dostawcy → każdy = quotation_variant

3. Dla wariantu zbierz wymagane charge_code wg incoterm:
     EXW/FCA → origin + freight (obcięte po załadunku przy FOB)
     CIF     → origin + freight + insurance
     DAP/DDP → wszystko + destination + odwóz

4. WYKRYJ BRAKI → quotation_gap
     - opłaty wymagane przez incoterm, których nie ma w źródle
     - opłaty zwykle występujące na tej relacji (z historii)
     - stawki wygasłe lub wygasające przed planowanym załadunkiem
     - pozycje z API oznaczone is_mapped=false
     
   System ma krzyczeć: „na tej relacji zwykle jest ISPS i CIC, 
   w tym cenniku ich nie ma"

5. Przelicz waluty: NBP tabela A z dnia roboczego POPRZEDZAJĄCEGO,
   kurs zamrożony na ofercie

6. Nałóż marżę wg margin_rule (priorytet: charge_code > lane > customer > global)

7. ZWRÓĆ: warianty posortowane po cenie + braki + data wygaśnięcia
   najkrótszej stawki + dla wariantów live: price_id i moment pobrania
```

## C5. Tracking

### C5.1 Normalizacja na model DCSA

Standard jest opublikowany, ale adopcja nierówna — jedne linie implementują pełny zestaw zdarzeń, inne podzbiór. Podejście: normalizuj wszystko na model zdarzeń DCSA i uzupełniaj braki z feedów albo agregatorów.

```
Adapter armatora → surowe zdarzenie → mapper → shipment_event (DCSA)
                                                      │
                                          ┌───────────┼───────────┐
                                          ▼           ▼           ▼
                                    aktualizacja  powiadomienie  portal
                                    ETA/statusu   (Novu)         klienta
```

### C5.2 Faza w cyklu życia

Standard organizuje przesyłkę w pięć faz: pre-shipment, pre-ocean, ocean, post-ocean, post-shipment. Mapuj `shipment.status` na te fazy — dostajesz spójny obraz niezależnie od armatora.

### C5.3 Kolejność wdrożenia

Tracking robisz **przed** wycenami z API. Powody: darmowy, samoobsługowe portale deweloperskie z sandboxami u Maerska, CMA CGM i Hapaga, zero ryzyka prawnego, a użytkownik widzi wartość codziennie.

### C5.4 Czego AIS nie da

Dane AIS pokazują pozycję statku, nie kontenera. Wystarczą na mapkę, nie wystarczą na milestone'y i wyliczanie free time.
---

# CZĘŚĆ D — PRODUKT, WDROŻENIE, RYZYKA

## D1. Warstwa agentowa

Cztery zdolności, których nie ma żaden system spedycyjny na rynku polskim. Wdrażane w tej kolejności.

### D1.1 System jako serwer MCP — po fazie 1

Opakowanie API w serwer MCP. Kilkadziesiąt linii, a agent operuje systemem: „wystaw ofertę dla Jurgi na Gdynia–Szanghaj, dwa czterdziestki wysokie". To nie chatbot obok aplikacji — to aplikacja jako narzędzie.

Narzędzia do wystawienia: `search_rates`, `create_quotation`, `get_shipment_status`, `list_expiring_rates`, `explain_charge`. Granulacja i opisy decydują o tym, czy agent użyje ich poprawnie.

**Zabezpieczenia:** narzędzia odczytowe bez ograniczeń, zapisowe wyłącznie w trybie „przygotuj do zatwierdzenia". Agent nie wysyła oferty klientowi bez człowieka.

### D1.2 Copilot w interfejsie — po pierwszych klientach

`CopilotKit`. Użytkownik pisze zdaniem, formularz się wypełnia. Funkcja demonstracyjna — sprzedaje system w pierwszej minucie pokazu.

### D1.3 Raporty bez pisania raportów — po fazie 3

`WrenAI` + `Cube` (warstwa semantyczna) + `sqlglot` (walidator). Warstwa semantyczna definiuje raz, czym jest „marża" i „rentowność relacji". Walidator jest obowiązkowy: zapytanie wygenerowane przez model nie dotyka bazy bez sprawdzenia — w systemie wielodostępnym to kwestia bezpieczeństwa, nie wygody.

### D1.4 Dotrenowany model — po roku danych

`unsloth` na zgromadzonym zbiorze cenników. Tańszy i celniejszy od ogólnego, a zbioru nikt nie skopiuje.

## D2. Wielodostępność i izolacja

Twoi klienci są dla siebie konkurentami. Pierwsze pytanie na każdym spotkaniu handlowym: „kto jeszcze widzi moje stawki". Musisz mieć odpowiedź techniczną, nie deklaratywną.

- RLS wymuszany przez bazę, z zestawem testów dowodzących izolacji
- osobne klucze szyfrujące per tenant dla plików źródłowych i poświadczeń armatorów
- audit log dostępu widoczny dla klienta — kto i kiedy patrzył
- opcja instancji dedykowanej w wyższym pakiecie, ten sam kod
- **eksport wszystkich danych w otwartym formacie, w każdej chwili, bez pytania ciebie o zgodę** — zdejmuje największą obawę przed kupnem od jednoosobowego dostawcy

## D3. Warstwa prawna

### D3.1 Podpowierzenie przetwarzania

Wysyłasz cenniki i dokumenty klienta do zewnętrznego API modelu językowego. To jest podpowierzenie i musi być w umowie powierzenia: nazwa dostawcy, lokalizacja przetwarzania, retencja. Klient, który dowie się po fakcie, ma podstawę do rozwiązania umowy i zgłoszenia naruszenia.

**Konsekwencja architektoniczna:** przełącznik „przetwarzanie wyłącznie lokalne" per tenant. Modele lokalne (`ollama`, `olmocr`) istnieją właśnie po to.

### D3.2 Ograniczenie odpowiedzialności

System liczy ceny. Błąd w stawce to realna szkoda majątkowa. Umowa ogranicza odpowiedzialność do opłat z ostatnich 12 miesięcy i wyłącza szkody pośrednie. Do tego OC działalności IT — kilka tysięcy złotych rocznie, jedna z niewielu pozycji, przy której nie ma sensu oszczędzać.

### D3.3 SLA, którego dotrzymasz

Nie obiecuj 99,9% dostępności będąc jedną osobą. Okno serwisowe, czas reakcji w dni robocze, jasna ścieżka awaryjna. Realny SLA bije ambitny i złamany.

### D3.4 Konflikt interesów

Pracujesz w dziale sprzedaży H&H Logistics, chcesz sprzedawać narzędzie ich konkurencji. Rozmowa do odbycia **przed pierwszą umową**. Warianty: osobny podmiot z pełnym rozdzieleniem, HHL jako partner lub udziałowiec, albo ograniczenie segmentu docelowego. Wpływa na architekturę — jeśli osobny podmiot, dane i infrastruktura rozdzielają się od początku.

## D4. Stack

| Warstwa | Wybór |
|---|---|
| Baza | PostgreSQL 16 + RLS + `pgvector` + `pg_trgm` |
| Backend | FastAPI · SQLAlchemy · Alembic · Pydantic · `uv` · `ruff` · `mypy` |
| Kolejka | `procrastinate` (na Postgresie, bez dodatkowego brokera) |
| Pieniądze | `py-moneyed` · `babel` · `pendulum` |
| Parsowanie | `docling` + `marker` (porównaj) · `pdfplumber` · `calamine` |
| Ekstrakcja | `instructor` + Claude API · `langfuse` · `promptfoo` · `llm-guard` |
| Poczta | `emailengine` |
| Frontend | `refine` · `TanStack/table` · `glide-data-grid` · `shadcn-ui` · `zod` |
| Dokumenty | `typst` |
| Storage | `minio` |
| Obserwowalność | `sentry` · `langfuse` · `posthog` · `uptime-kuma` |
| Jakość danych | `great-expectations` |
| Backup | `pgbackrest` |
| CI | `renovate` · `qodo-ai/pr-agent` · `pre-commit` |
| Dane | `improved-un-locodes` |
| Polska | `smekcio/ksef-client-python` · `bigzbig/regonapi` · `WoLpH/mt940` |
| Agenci | `modelcontextprotocol/python-sdk` · `github/spec-kit` |

Pełny katalog 407 pozycji w osobnym pliku. Powyżej jest to, co instalujesz.

## D5. Roadmapa

| Tydz. | Zakres | Kryterium zaliczenia |
|---|---|---|
| **0** | Oszacowanie rynku na kartce. Rozmowa z HHL o konflikcie interesów. Wniosek o klucz GUS. Rejestracja na portalach deweloperskich Hapaga, Maerska, CMA | Wiesz, czy budujesz produkt |
| **1–2** | Schemat bazy z multi-tenancy i RLS. Słownik `charge_code` z aliasami. Porty z UN/LOCODE. Metering | Testy dowodzą izolacji tenantów |
| **3–4** | Kontrahenci: CRUD, GUS/VIES, kontakty, konta bankowe | Dodajesz klienta po NIP w 5 sekund |
| **5–6** | **Ręczne wprowadzanie stawek.** Bez AI | 200 realnych pozycji z twoich cenników w bazie |
| **7–9** | Silnik wyceny + wykrywanie braków + PDF + wysyłka | **Nagranie demo (Loom) do trzech spedytorów** |
| **10–12** | Tracking: adapter Hapaga, normalizacja DCSA, ekran kontenerów | Widzisz swoje kontenery bez portalu |
| **13–17** | Pipeline AI: ingest → extract → normalize → review | 30 cenników w zbiorze testowym, mierzona skuteczność |
| **18–19** | Pamięć szablonów + uczenie aliasów | 80% cenników parsuje się bez modelu |
| **20–22** | Adapter Hapaga: Quick Quotes + Quick Quotes Spot. Potem Maersk Offers | Wycena z live spot obok stawek z cennika |
| **23–27** | Zlecenie morskie: konwersja z oferty, kontenery, dokumenty, eventy | Pierwsza umowa płatna |
| **28+** | Faktura + KSeF. Serwer MCP. Kolejność dalszych modułów wskazują klienci | — |

**Tydzień 5–6 wygląda na stratę i nią nie jest.** Dopóki nie wprowadzisz ręcznie dwustu realnych pozycji, nie wiesz, czy schemat pasuje do rzeczywistości. Przepisywanie schematu po zbudowaniu pipeline'u kosztuje wielokrotnie więcej.

**Tydzień 7–9 to punkt kontrolny.** Jeśli sam silnik wyceny z ręcznie wprowadzonymi stawkami nie zrobi wrażenia na spedytorze, rozwiązujesz problem, którego nie ma. Dowiesz się o tym trzy miesiące wcześniej i za jedną trzecią kosztu.

## D6. Koszty

| | Budowa | Solo | 5 klientów | 20 klientów |
|---|---|---|---|---|
| Miesięcznie | 300–1 200 zł | ~200 zł | ~650 zł | ~1 900 zł |
| Rocznie | 4–14 tys. zł | 2,4 tys. zł | 7,8 tys. zł | 23 tys. zł |
| Twój czas rocznie | 800–1 000 h | ~150 h | ~350 h | etat + wsparcie |

Koszt sparsowania jednego cennika: ~1 zł, przez Batch API 50 gr, po wdrożeniu pamięci szablonów pięć razy mniej. **AI nie jest kosztem tego systemu.** Nie optymalizuj wyboru modelu pod cenę — bierz ten o najwyższej skuteczności ekstrakcji. Różnica w rachunku to kilkadziesiąt złotych, różnica w błędnej stawce to kilka tysięcy.

Prawdziwy koszt to 800–1 000 godzin, czyli 100–150 tys. zł kosztu alternatywnego, plus 15–20% tego rocznie na utrzymanie.

## D7. Ryzyka

| Ryzyko | Waga | Odpowiedź |
|---|---|---|
| **Wąskie gardło jednej osoby** przy 3–5 klientach: sprzedaż + wdrożenia + wsparcie + rozwój | Wysoka | Wybierz świadomie: wspólnik techniczny, partner wdrożeniowy albo limit klientów. Najgorzej nie wybrać |
| Konflikt z HHL wybucha przy trzecim kliencie | Wysoka | Rozmowa przed pierwszą umową (D3.4) |
| Prompt injection przez cennik | Średnia | `llm-guard` od pierwszego dnia (C2.4) |
| Cicho pominięta tabela dopłat | Średnia | `unparsed_regions` obowiązkowe + `quotation_gap` |
| Zmiana schemy KSeF | Średnia | Warstwa abstrakcji nad KSeF, nie wołania rozsiane po kodzie |
| Wycofanie modelu | Średnia | `promptfoo` + zbiór testowy w `label-studio` — migracja mierzalna |
| Zmiana API armatora | Średnia | Adapter per armator, testy kontraktowe, `wiremock` |
| Utrata bazy | Krytyczna | `pgbackrest` z PITR przed pierwszym klientem |
| Każdy klient wymaga zmian w kodzie | Wysoka | ZASADA 2 — konfiguracja jako dane |
| Odrzucenie certyfikacji przez armatora | Niska | Wymogi UI z C3.4 uwzględnione od początku |

## D8. Decyzje otwarte

Rozstrzygnąć przed odpowiadającą fazą:

1. **Osobny podmiot na produkt?** — przed pierwszą umową
2. **Metryka cenowa** — abonament + per użytkownik + limit cenników; przedział 1 000–2 500 zł dla małego spedytora. Punkt odniesienia dla klienta to koszt etatu (8–12 tys. zł), nie konkurencyjny software
3. **Zasięg geograficzny** — sama Polska czy od razu Czechy, Słowacja, kraje bałtyckie? Wpływa na i18n i na warstwę e-faktury (Peppol, Factur-X)
4. **Księgowość** — potwierdzone: integracja, nie własna implementacja. Wybór dostawcy (Fakturownia / wFirma / Comarch) przed tygodniem 28
5. **Agregator trackingu** — Vizion czy Terminal49 na ogon armatorów, dopiero gdy klienci płacą

## D9. Co jest naprawdę twoje

Po przeszukaniu tagów `freight-forwarding`, `freight-management`, `logistics`, `edifact` i `text2sql` — nie istnieje open-source'owy silnik stawek morskich z pełnym zestawem dopłat, terminami ważności i rozwiązywaniem kolizji cenników.

Tabele `charge_code`, `rate_sheet`, `rate_line`, `live_offer` i logika z C4 to jedyna część tego systemu, której nie skopiujesz z GitHuba — i której konkurencja nie skopiuje od ciebie. Cała reszta to składanie klocków, które już istnieją.

Tam powinna trafić większość twojego czasu i cała twoja wiedza domenowa.
