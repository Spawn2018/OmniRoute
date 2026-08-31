# Moduł wycen morskich + zleceń + kontrahentów + AI rate ingestion
## Specyfikacja techniczna do budowy w Cursorze

---

## 0. Zakres

**W zakresie:**
- Kontrahenci (klienci, agenci, przewoźnicy, shipper/consignee)
- Baza stawek zakupowych FCL + LCL wraz z pełnym zestawem dodatków
- AI ingestion: mail/Excel/PDF od linii i agentów → strukturalna baza cen
- Wycena (quotation): buy → margin → sell, PDF, wysyłka, wersjonowanie
- Zlecenie morskie (job file): konwersja z oferty, legi, kontenery, dokumenty, statusy

**Poza zakresem (świadomie):**
Księgowość, magazyn, EDI, track & trace, transport lotniczy i drogowy. Model danych ma być na nie przygotowany, ale nie budujesz ich teraz.

---

## 1. Model danych

### 1.1 Kontrahenci

```sql
party
  id, organization_id
  legal_name, short_name
  tax_id (NIP), vat_eu, regon, krs
  country_code, address_json
  roles: text[]        -- customer | vendor | agent | carrier | shipper | consignee | notify
  payment_terms_days, credit_limit, credit_currency
  default_currency
  is_active, created_at

party_contact
  id, party_id, name, email, phone, role, is_primary, portal_access

party_bank_account
  id, party_id, iban, currency, whitelist_checked_at, whitelist_status

carrier                       -- rozszerzenie party dla linii żeglugowych
  party_id, scac_code, is_nvocc, rate_source_email
```

Uwagi:
- `roles` jako tablica, nie osobne tabele. Ten sam podmiot bywa jednocześnie klientem i agentem.
- Autouzupełnianie po NIP: GUS/REGON API + VIES. Biała lista VAT — osobny cron, wynik cache'owany.

### 1.2 Słowniki

```sql
port                          -- UN/LOCODE jako klucz naturalny
  unlocode (PK, np. PLGDN), name, country_code, is_seaport, lat, lng, aliases text[]

container_type
  code (20DV, 40DV, 40HC, 40RF, 20RF, 40OT, 20FR, 45HC), description,
  teu_factor, max_payload_kg, is_reefer, is_special

charge_code                   -- SERCE SYSTEMU, patrz sekcja 2
  code, name_pl, name_en, category, default_basis, default_currency,
  applies_to text[],          -- FCL | LCL | BOTH
  side,                       -- origin | freight | destination | filing | other
  is_percentage, aliases text[]

incoterm
  code (EXW, FCA, FOB, CFR, CIF, CPT, CIP, DAP, DPU, DDP), named_place_required
```

### 1.3 Stawki zakupowe

```sql
rate_sheet                    -- dokument źródłowy, jedna dostawa cennika
  id, organization_id
  source_party_id             -- linia albo agent
  source_type,                -- email | excel | pdf | manual | tender | portal
  source_file_path, source_file_hash
  received_at, valid_from, valid_to
  status,                     -- ingesting | review | active | superseded | rejected
  extraction_confidence numeric,
  superseded_by uuid,
  raw_meta jsonb

rate_line                     -- pojedyncza pozycja cenowa
  id, rate_sheet_id, organization_id
  mode,                       -- FCL | LCL
  pol unlocode, pod unlocode
  via unlocode null,          -- transshipment jeśli podany
  carrier_party_id null
  service_name null,          -- nazwa serwisu/stringu
  transit_days int null
  container_type null,        -- dla FCL
  charge_code
  amount numeric(14,4), currency char(3)
  basis,                      -- PER_CONTAINER | PER_BL | PER_SHIPMENT | PER_WM |
                              -- PER_TON | PER_CBM | PER_TEU | PER_KG | PERCENT | FLAT
  min_amount numeric null, max_amount numeric null
  percent_of null,            -- jeśli basis=PERCENT: kod opłaty bazowej
  free_time_days int null,    -- detention/demurrage
  valid_from date, valid_to date
  conditions jsonb,           -- {commodity, dg_class, min_qty, contract_no, remarks}
  source_ref jsonb,           -- {sheet:"FCL EXP", row:47, col:"H"} ← provenance
  confidence numeric,
  is_verified bool
```

**Zasady krytyczne:**
- `rate_line` jest **niemutowalny**. Zmiana ceny = nowy rekord + `superseded_by` na starym. Musisz umieć odtworzyć, po jakiej stawce liczyłeś ofertę pół roku temu.
- `source_ref` obowiązkowo. Gdy klient kwestionuje cenę, wskazujesz plik, arkusz i komórkę.
- `amount` zawsze `numeric`, nigdy float.

### 1.4 Wycena

```sql
quotation
  id, organization_id, quote_number, version int
  customer_party_id, salesperson_user_id
  mode (FCL|LCL), pol, pod, incoterm, named_place
  commodity, hs_code null, is_dangerous, imo_class null, un_number null
  valid_from, valid_to
  status,                     -- draft | sent | accepted | lost | expired
  lost_reason null, currency, fx_rate_source, fx_date
  created_at, sent_at, decided_at

quotation_cargo
  id, quotation_id
  container_type null, qty int          -- FCL
  packages int null, gross_weight_kg, volume_cbm, chargeable_wm  -- LCL

quotation_line
  id, quotation_id
  charge_code, description_override null
  basis, qty numeric
  buy_amount, buy_currency, buy_rate_line_id null   -- link do źródła stawki
  sell_amount, sell_currency
  fx_rate numeric
  margin_amount, margin_pct                          -- kolumny wyliczane
  is_visible_to_customer bool,       -- pozycje ukryte/zwinięte na PDF
  sort_order int
```

`buy_rate_line_id` to najważniejszy klucz obcy w systemie. Dzięki niemu widzisz, która oferta z której dostawy cennika wynikała, i możesz automatycznie oznaczyć oferty oparte o wygasłe stawki.

### 1.5 Zlecenie morskie

```sql
shipment
  id, organization_id, job_number
  quotation_id null            -- skąd powstało
  customer_party_id, shipper_party_id, consignee_party_id, notify_party_id
  agent_party_id null, carrier_party_id
  direction (EXPORT|IMPORT|CROSS), mode (FCL|LCL)
  incoterm, named_place
  pol, pod, place_of_receipt null, place_of_delivery null
  booking_number, mbl_number, hbl_number
  vessel_name, voyage_number
  etd, eta, atd, ata, cutoff_doc, cutoff_vgm, cutoff_gate
  status,                      -- booked | docs_pending | gate_in | sailed |
                               -- in_transit | arrived | delivered | closed
  operator_user_id

shipment_container
  id, shipment_id, container_number, seal_number, container_type
  gross_weight_kg, tare_kg, vgm_kg, vgm_method (1|2), vgm_submitted_at
  free_time_until

shipment_charge               -- kopiowane z quotation_line przy konwersji
  id, shipment_id
  charge_code, basis, qty
  buy_amount, buy_currency, buy_party_id, buy_status (estimated|confirmed|invoiced)
  sell_amount, sell_currency, sell_status
  fx_rate, fx_date

shipment_event
  id, shipment_id, event_code, planned_at, actual_at, source (manual|api|email), remarks

shipment_document
  id, shipment_id, doc_type, file_path, visibility (internal|customer),
  generated_from_template null, uploaded_by, uploaded_at

shipment_task
  id, shipment_id, title, assignee_user_id, due_at, completed_at, workflow_step_id null
```

Konwersja `quotation → shipment` kopiuje pozycje kosztowe **z zamrożonymi kwotami i kursem**. Późniejsza zmiana cennika nie może ruszyć otwartego zlecenia.

---

## 2. Słownik opłat (charge_code) — kompletny dla morza

To jest fundament. Jeśli źle zaprojektujesz słownik, cała reszta się sypie, bo każdy agent nazywa to samo inaczej.

### 2.1 Pre-carriage / dowóz (side = origin)
| Kod | Nazwa | Basis |
|---|---|---|
| `DRAY-EXP` | Dowóz kontenera do portu | PER_CONTAINER |
| `PICKUP` | Podjazd / odbiór pustego | PER_CONTAINER |
| `WAIT` | Postojowe kierowcy | PER_HOUR |
| `ADR-ROAD` | Dodatek ADR w transporcie drogowym | PER_CONTAINER |
| `DEADFR` | Dead freight / puste przejechanie | FLAT |

### 2.2 Local charges POL (side = origin)
| Kod | Nazwa | Basis |
|---|---|---|
| `OTHC` | Terminal Handling Charge — origin | PER_CONTAINER |
| `DOCFEE-O` | Opłata dokumentacyjna origin | PER_BL |
| `BL-FEE` | Wystawienie B/L | PER_BL |
| `SEAL` | Plomba | PER_CONTAINER |
| `VGM` | Zgłoszenie VGM | PER_CONTAINER |
| `WEIGH` | Ważenie | PER_CONTAINER |
| `ISPS-O` | ISPS / security origin | PER_CONTAINER |
| `PORT-DUES-O` | Opłaty portowe origin | PER_CONTAINER |
| `GATE-IN` | Wjazd na terminal | PER_CONTAINER |
| `CLEAN` | Mycie / czyszczenie kontenera | PER_CONTAINER |
| `CUST-EXP` | Odprawa eksportowa (AES/SAD) | PER_SHIPMENT |
| `T1` | Tranzyt T1 / NCTS | PER_SHIPMENT |
| `DG-O` | Dodatek DG origin | PER_CONTAINER |
| `REEF-PLUG-O` | Podłączenie reefera origin | PER_CONTAINER_DAY |
| `CFS-O` | Obsługa CFS (LCL) | PER_WM |
| `CONSOL` | Opłata konsolidacyjna (LCL) | PER_WM |

### 2.3 Fracht morski (side = freight)
| Kod | Nazwa | Basis |
|---|---|---|
| `OFR` | Ocean freight — stawka bazowa | PER_CONTAINER / PER_WM |
| `BAF` / `FAF` | Bunker Adjustment Factor | PER_CONTAINER |
| `CAF` | Currency Adjustment Factor | PERCENT (of OFR) |
| `LSS` | Low Sulphur Surcharge | PER_CONTAINER |
| `ETS` | EU ETS — dodatek emisyjny | PER_CONTAINER |
| `PSS` | Peak Season Surcharge | PER_CONTAINER |
| `GRI` | General Rate Increase | PER_CONTAINER |
| `WRS` | War Risk Surcharge | PER_CONTAINER |
| `CANAL-SUEZ` | Dodatek za Kanał Sueski | PER_CONTAINER |
| `CANAL-PAN` | Dodatek za Kanał Panamski | PER_CONTAINER |
| `PCS` | Port Congestion Surcharge | PER_CONTAINER |
| `EBS` | Emergency Bunker Surcharge | PER_CONTAINER |
| `CIC` | Container Imbalance Charge | PER_CONTAINER |
| `OWS` | Overweight Surcharge | PER_CONTAINER |
| `DG-SEA` | Dodatek DG — fracht | PER_CONTAINER |
| `REEF-SEA` | Dodatek reefer — fracht | PER_CONTAINER |

### 2.4 Zgłoszenia / filing (side = filing)
| Kod | Nazwa | Basis |
|---|---|---|
| `ENS` | Entry Summary Declaration (UE) | PER_BL |
| `AMS` | Automated Manifest System (US) | PER_BL |
| `ISF` | Importer Security Filing (US) | PER_BL |
| `ACI` | Advance Commercial Info (CA) | PER_BL |
| `AFR` | Advance Filing Rules (JP) | PER_BL |
| `MANIFEST` | Korekta manifestu | PER_BL |

### 2.5 Local charges POD (side = destination)
| Kod | Nazwa | Basis |
|---|---|---|
| `DTHC` | Terminal Handling Charge — destination | PER_CONTAINER |
| `DOCFEE-D` | Opłata dokumentacyjna destination | PER_BL |
| `DO-FEE` | Delivery Order | PER_BL |
| `ISPS-D` | ISPS destination | PER_CONTAINER |
| `CUST-IMP` | Odprawa importowa | PER_SHIPMENT |
| `DEMUR` | Demurrage (po free time) | PER_CONTAINER_DAY |
| `DETEN` | Detention (po free time) | PER_CONTAINER_DAY |
| `STORAGE` | Składowanie | PER_CONTAINER_DAY |
| `CFS-D` | Obsługa CFS destination (LCL) | PER_WM |
| `DRAY-IMP` | Odwóz od portu | PER_CONTAINER |

### 2.6 Pozostałe
`INS` (ubezpieczenie cargo, PERCENT of value), `AGENCY` (opłata agencyjna), `HANDLING` (opłata manipulacyjna), `AMEND` (zmiana dokumentu), `TELEX` (telex release), `SWITCH-BL` (switch B/L), `CERT-ORIG` (świadectwo pochodzenia), `FUMIG` (fumigacja), `SURVEY` (inspekcja).

**Aliasy** — każdy kod ma `aliases text[]`. Przykład dla `OTHC`:
`["THC", "THC ORIGIN", "OTHC", "TERMINAL HANDLING", "TERMINAL HANDLING CHARGE POL", "THC AT ORIGIN", "O/THC", "OPŁATA TERMINALOWA"]`

Ta tabela rośnie sama — patrz sekcja 3.6.

---

## 3. Moduł AI: automatyczna budowa bazy cen zakupowych

### 3.1 Problem

Cenniki przychodzą jako: Excel bez dwóch takich samych layoutów, PDF (czasem skan), treść maila, tabela w treści maila, ZIP z pięcioma plikami. Każda linia i każdy agent robi to inaczej, a ten sam agent zmienia format co kwartał. Ręczne przepisywanie to kilka godzin tygodniowo i główne źródło błędów w ofertach.

### 3.2 Architektura pipeline'u

```
[0] INGEST      → dedykowana skrzynka rates@, watcher IMAP/Graph
                  wyciągnięcie załączników, hash SHA-256, deduplikacja
                  ↓
[1] CLASSIFY    → czy to cennik? od kogo? FCL/LCL/local/inland?
                  najpierw mapowanie po nadawcy (deterministyczne),
                  LLM tylko jako fallback
                  ↓
[2] TEMPLATE?   → czy znam layout tego nadawcy? (patrz 3.5)
                  TAK → parser deterministyczny, koszt ~0, pewność wysoka
                  NIE → ścieżka LLM poniżej
                  ↓
[3] LAYOUT      → Excel: openpyxl → inwentarz arkuszy, detekcja nagłówków,
                     merged cells, zakresy danych
                  PDF: warstwa tekstowa → jeśli brak, OCR
                  Mail: HTML → tekst + tabele
                  ↓
[4] EXTRACT     → LLM ze ścisłym schematem JSON, chunkowanie per arkusz/sekcja
                  zwraca też współrzędne komórek źródłowych
                  ↓
[5] NORMALIZE   → porty → UN/LOCODE
                  opłaty → charge_code (alias → fuzzy → embedding)
                  typy kontenerów, waluty, basis, daty ważności
                  ↓
[6] VALIDATE    → arytmetyka i reguły w KODZIE, nie w LLM
                  zakresy sanity, wymagane pola, kolizje z istniejącymi stawkami
                  ↓
[7] REVIEW      → kolejka z oceną pewności, diff vs. poprzednia wersja tej relacji
                  akceptacja jednym kliknięciem, korekta zasila słownik aliasów
                  ↓
[8] COMMIT      → rate_sheet.status = active, poprzednia = superseded
```

### 3.3 Schemat ekstrakcji (structured output)

```json
{
  "carrier": "string | null",
  "valid_from": "YYYY-MM-DD | null",
  "valid_to": "YYYY-MM-DD | null",
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
      "source_ref": {"sheet": "FCL EXPORT", "row": 47, "col": "H"}
    }]
  }],
  "unparsed_regions": [
    {"sheet": "Notes", "reason": "prose remarks, not tabular"}
  ]
}
```

**Pola `_raw` są obowiązkowe.** LLM zwraca to, co widzi. Mapowanie na słowniki robi kod w kroku [5], deterministycznie i rozliczalnie. Nigdy nie każ modelowi od razu zwracać `charge_code` — nie będziesz wiedział, czy zmapował, czy zgadł.

### 3.4 Twarde reguły

1. **LLM nie liczy.** Żadnych sum, przeliczeń walutowych, mnożenia przez ilość. Model wyciąga liczby, kod je przetwarza.
2. **LLM nie decyduje o zapisie.** Ekstrakcja zawsze ląduje w `status = review`. Auto-commit dopuszczalny wyłącznie dla zweryfikowanych szablonów (3.5) z pewnością > 0.95.
3. **Provenance zawsze.** Bez `source_ref` rekord nie wchodzi do bazy.
4. **`unparsed_regions` obowiązkowe.** Model musi zgłosić, czego nie ogarnął. Milczące pominięcie tabeli z dopłatami to najgorszy możliwy błąd — oferta wyjdzie za tanio i dowiesz się o tym przy fakturze.

### 3.5 Pamięć szablonów — kluczowa optymalizacja

Po pierwszym udanym sparsowaniu cennika danego nadawcy zapisz mapę layoutu:

```json
{
  "party_id": "...",
  "fingerprint": "hash nagłówków + nazw arkuszy",
  "sheets": {
    "FCL EXPORT": {
      "header_row": 5,
      "columns": {"POL": "B", "POD": "C", "20DV": "F", "40HC": "H", "VALID": "M"},
      "charge_rows": {"OFR": 47, "BAF": 48, "LSS": 49}
    }
  },
  "success_count": 12,
  "last_confirmed_at": "..."
}
```

Przy kolejnej dostawie: dopasuj fingerprint → parsuj deterministycznie → LLM tylko do weryfikacji różnic. Po kilku miesiącach 80% cenników idzie ścieżką bez modelu. To jest różnica między systemem, który kosztuje kilkaset złotych miesięcznie, a takim, który kosztuje kilka tysięcy.

### 3.6 Uczenie się słownika

Każda ręczna korekta w kolejce review zapisuje się jako alias:

```
korekta: "TERMINAL HANDLING POL" → OTHC
zapis:   charge_code_alias (alias, charge_code, party_id, confirmed_by, confirmed_at)
```

Następnym razem mapowanie jest deterministyczne. System dosłownie uczy się słownictwa każdego agenta z osobna — a `party_id` w aliasie pozwala obsłużyć sytuację, gdy dwóch agentów używa tego samego skrótu na dwie różne opłaty.

### 3.7 Wykrywanie kolizji

Przy commicie sprawdź, czy nowa stawka nie nachodzi na istniejącą (ta sama relacja + charge_code + typ kontenera + zachodzące okresy ważności). Warianty:
- Nowszy `received_at` → stara dostaje `valid_to = new.valid_from - 1 dzień`
- Ten sam okres, inna kwota → **do decyzji człowieka**, nigdy automatycznie
- Różni dostawcy na tej samej relacji → obie zostają, wycena wybiera najtańszą albo pokazuje porównanie

---

## 4. Silnik wyceny

```
wejście: POL, POD, mode, typ+ilość kontenerów, incoterm, commodity, DG?

1. Znajdź kandydatów: rate_line WHERE pol, pod, mode, valid dziś, is_verified
2. Pogrupuj po dostawcy → każdy dostawca = jeden wariant oferty
3. Dla wariantu zbierz wymagane charge_code wg incoterm:
     EXW/FCA → tylko origin + freight (jeśli sprzedajesz FOB, obetnij po ładunku)
     CIF     → origin + freight + insurance
     DAP/DDP → wszystko + destination + odwóz
4. Oznacz braki: opłaty, których nie ma w cenniku, a incoterm ich wymaga
5. Przelicz waluty: kurs NBP tab. A z dnia poprzedzającego, zamrożony na ofercie
6. Nałóż marżę: reguła per klient / per relacja / per charge_code
     (procent, kwota stała, albo minimum z dwóch)
7. Zwróć: warianty posortowane po cenie + lista braków + data ważności najkrótszej stawki
```

Krok 4 jest ważniejszy, niż wygląda. Najczęstsza strata na drobnicy morskiej to nie zła stawka, tylko **zapomniana dopłata**. System ma krzyczeć: „na tej relacji zwykle jest ISPS i CIC, w tym cenniku ich nie ma".

---

## 5. Stack i kolejność

**Stack:**
PostgreSQL 16 (+ `pg_trgm` do fuzzy matchingu aliasów, `pgvector` do embeddingów opisów opłat) · FastAPI · SQLAlchemy + Alembic · Celery/RQ na pipeline · React + TanStack Table · openpyxl / pdfplumber / Tesseract · Claude API na ekstrakcję.

**Kolejność (nie zmieniaj):**

| Tydz. | Zakres |
|---|---|
| 1–2 | Schemat bazy, multi-tenancy + RLS, słowniki: porty (UN/LOCODE), kontenery, charge_code z aliasami |
| 3–4 | Kontrahenci: CRUD, GUS/VIES, kontakty, konta bankowe |
| 5–6 | Ręczne wprowadzanie stawek + widok bazy cen. **Zanim zbudujesz AI, musisz mieć gdzie zapisywać wyniki i musisz to przeklikać ręcznie.** |
| 7–9 | Silnik wyceny + PDF oferty + wysyłka |
| 10–13 | Pipeline AI: ingest → classify → extract → normalize → review queue |
| 14–15 | Pamięć szablonów + uczenie aliasów |
| 16–19 | Zlecenie morskie: konwersja z oferty, kontenery, eventy, taski, dokumenty |

Tygodnie 5–6 wyglądają na stratę czasu i nie są. Jeśli zbudujesz AI, zanim ręcznie wprowadzisz 200 stawek, zaprojektujesz schemat, który nie pasuje do rzeczywistości.

---

## 6. Co przetestować ręcznie (LLM tego nie napisze za ciebie)

Reguły biznesowe wymagają testów pisanych z wiedzy domenowej:

- Chargeable weight LCL: W/M — max(waga w tonach, objętość w CBM), minimum 1 W/M
- Przeliczenie kursowe: NBP tab. A z **dnia roboczego poprzedzającego**, nie z dnia bieżącego
- `basis = PERCENT`: podstawa naliczenia, kolejność, czy nakłada się na inne procenty
- Free time: liczony od rozładunku ze statku czy od gate-out — zależy od linii
- Incoterm → zestaw opłat: 10 wariantów, każdy osobno
- Kolizja stawek: dwa cenniki, ten sam okres, różne kwoty
- Numeracja ofert: transakcyjna, bez dziur, per rok, per organizacja
- Wygaśnięcie stawki w trakcie ważności oferty: co się dzieje z wysłaną ofertą
