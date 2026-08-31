# M-50 · Kolej Chiny–Europa (Nowy Jedwabny Szlak)

Pełna specyfikacja modułu. FCL i LCL, z odwozami drogowymi wynikającymi
z incoterms.

**Pozycja w modelu:** przewóz kolejowy to `shipment_leg` z `mode = RAIL`.
Odwóz drogowy do klienta to kolejny odcinek. Zgodnie z korektą modelu.

---

# 1. KORYTARZE

## 1.1 Trzy trasy, trzy profile ryzyka

| Korytarz | Trasa | Tranzyt | Profil |
|---|---|---|---|
| **Północny** | Chiny → Kazachstan/Mongolia → Rosja → Białoruś → Polska | 12–20 dni | najszybszy, najtańszy, **najwyższe ryzyko sankcyjne** |
| **Środkowy** | Chiny → Kazachstan → Morze Kaspijskie → Azerbejdżan → Gruzja → Turcja/Morze Czarne → UE | 25–40 dni | omija Rosję, więcej przeładunków, droższy, mniej przewidywalny |
| **Południowy** | Chiny → Azja Środkowa → Iran/Turcja → UE | zmienny | ograniczona przepustowość, ryzyko regulacyjne |

**Wybór korytarza jest decyzją handlową i prawną, nie tylko cenową.**
System musi ją wspierać, nie podejmować.

## 1.2 Przejścia z przeładunkiem szerokotorowym

Rozstaw szyn zmienia się dwukrotnie na korytarzu północnym. Każda zmiana
to przeładunek, czas i koszt.

| Przejście | Kraje | Rozstaw | Uwagi |
|---|---|---|---|
| **Alashankou / Dostyk** | Chiny / Kazachstan | 1435 → 1520 | najruchliwsze, zatory sezonowe |
| **Khorgos / Altynkol** | Chiny / Kazachstan | 1435 → 1520 | nowsze, większa przepustowość |
| **Erenhot / Zamyn-Üüd** | Chiny / Mongolia | 1435 → 1520 | trasa mongolska |
| **Manzhouli / Zabajkalsk** | Chiny / Rosja | 1435 → 1520 | bezpośrednio do Rosji |
| **Brest / Małaszewicze** | Białoruś / Polska | 1520 → 1435 | **główne wejście do UE**, wąskie gardło |
| **Sławków (LHS)** | — | 1520 do wnętrza Polski | linia szerokotorowa bez przeładunku na granicy |
| **Kaliningrad / Braniewo** | Rosja / Polska | 1520 → 1435 | alternatywa przy zatorach w Brześciu |

**Sławków zasługuje na uwagę.** Linia szerokotorowa sięga w głąb Polski,
więc przeładunek następuje dopiero tam, a nie na granicy. Przy części
ładunków to oszczędność kilku dni.

## 1.3 Platformy nadania w Chinach

Każde duże miasto ma spółkę platformową operującą pociągami, często
z dofinansowaniem lokalnym.

| Platforma | Charakterystyka |
|---|---|
| Xi'an | największy wolumen, najczęstsze odjazdy |
| Chengdu | silna pozycja, dobre połączenia do Polski i Niemiec |
| Chongqing | pierwsza historycznie, stabilne rozkłady |
| Zhengzhou | dobra obsługa drobnicy |
| Wuhan, Yiwu, Suzhou, Changsha, Jinan, Hefei, Shenyang, Harbin, Qingdao | mniejsze wolumeny, bywają tańsze |

## 1.4 Terminale w Europie

| Kraj | Terminale |
|---|---|
| **Polska** | Małaszewicze, Sławków, Łódź (Olechów), Warszawa, Poznań, Gliwice, Kutno, Brzeg Dolny, Gądki |
| Niemcy | Duisburg, Hamburg, Norymberga, Lipsk |
| Holandia | Rotterdam, Tilburg |
| Czechy | Praga, Ostrawa |
| Węgry | Budapeszt (Fényeslitke, terminal szerokotorowy) |
| Hiszpania | Madryt |
| Włochy | Mediolan |
| Francja | Lyon, Duisburg jako punkt przeładunkowy |

---

# 2. MODEL DANYCH

## 2.1 Infrastruktura

```sql
rail_corridor
  id, code,                    -- northern | middle | southern
  name_pl, name_en
  transit_countries char(2)[], -- ← podstawa sprawdzania sankcji
  typical_transit_days_min, typical_transit_days_max
  reliability_score,           -- z własnej historii opóźnień
  is_active, risk_notes
  effective_from, effective_to

rail_border_crossing
  id, code
  country_from, country_to
  location_id,                 -- odwołanie do location (M-05)
  gauge_from, gauge_to,        -- 1435 | 1520 | 1668
  requires_transshipment bool,
  typical_dwell_hours,
  typical_dwell_hours_p90,     -- ← realistyczny bufor, nie średnia
  customs_office_code,
  max_daily_capacity_teu,
  is_active

rail_terminal                  -- rozszerzenie terminal z M-05
  terminal_id PK
  gauge,                       -- 1435 | 1520 | oba
  handles_fcl, handles_lcl, handles_reefer, handles_dg bool,
  accepted_rid_classes text[],
  has_customs_office, customs_office_code,
  has_bonded_warehouse,
  genset_available bool,
  max_container_length,        -- 45' na kolei jest częste
  free_storage_days,
  storage_rate_after_free, currency
  operating_hours jsonb,
  contact_party_id

rail_platform_company          -- spółki platformowe w Chinach
  party_id PK,
  city, city_cn,
  subsidy_available bool,
  subsidy_notes,               -- warunki i wygasanie
  departure_terminals uuid[]
```

## 2.2 Serwisy i rozkłady

```sql
rail_service
  id, organization_id
  operator_party_id,
  corridor_id,
  service_name,                -- np. "Xi'an – Małaszewicze XA-MAL"
  origin_terminal_id, destination_terminal_id
  border_crossings uuid[],     -- kolejność przejść
  departure_days smallint[],   -- {1,3,5} = pon/śr/pt
  transit_days_planned,
  transit_days_actual_avg,     -- ← z własnych zleceń
  capacity_teu_per_train,
  accepts_fcl, accepts_lcl, accepts_reefer, accepts_dg bool,
  accepted_rid_classes text[],
  accepted_container_types text[],   -- 20DV, 40DV, 40HC, 45HC, 40RF
  booking_cutoff_days,         -- typowo 5–7 dni przed odjazdem
  documents_cutoff_days,
  is_active, valid_from, valid_to

rail_departure                 -- konkretny odjazd
  id, organization_id, service_id
  train_number, departure_date
  cutoff_booking_at, cutoff_documents_at, cutoff_cargo_at
  capacity_total_teu, capacity_booked_teu, capacity_available_teu
  status,                      -- announced | open | closing | closed
                               -- departed | cancelled | delayed
  actual_departure_at,
  eta_destination, eta_updated_at,
  delay_hours, delay_reason
  source,                      -- operator_email | portal | manual | api
  synced_at
```

## 2.3 Stawki — ze specyfiką dofinansowania

```sql
rail_rate
  id, organization_id
  operator_party_id, service_id NULL, corridor_id
  origin_terminal_id, destination_terminal_id
  mode,                        -- FCL | LCL
  container_type,              -- dla FCL
  -- stawka
  amount numeric(14,4), currency char(3),
  basis,                       -- PER_CONTAINER | PER_WM | PER_CBM | PER_TON
  min_charge,
  -- dofinansowanie platformy chińskiej
  subsidy_amount numeric(14,4),
  subsidy_currency char(3),
  subsidy_conditions jsonb,    -- minimalna liczba kontenerów, rodzaj towaru
  subsidy_valid_to date,       -- ⚠ dofinansowania wygasają
  net_after_subsidy numeric(14,4),
  -- warunki
  includes jsonb,              -- co w cenie: THC origin, przeładunek, T1
  excludes jsonb,
  free_time_destination_days,
  commodity_restrictions text[],
  min_quantity, max_quantity,
  validity_basis,              -- departure | booking | bl_date
  valid_from, valid_to,
  source_ref jsonb, confidence, is_verified
```

**Dofinansowanie modeluj jawnie, ale nie opieraj na nim oferty bez daty
ważności.** Programy wsparcia platform chińskich są zmienne i wygasają.
Oferta oparta na dofinansowaniu, które przestało obowiązywać, to strata
przy fakturze.

## 2.4 Odcinek kolejowy

```sql
shipment_leg_rail
  leg_id PK REFERENCES shipment_leg(id)
  service_id, departure_id
  train_number, wagon_numbers text[],
  corridor_id,
  origin_terminal_id, destination_terminal_id
  -- dokumenty przewozowe
  consignment_note_type,       -- cim | smgs | cim_smgs_unified
  consignment_note_number,
  consignment_note_path,
  is_electronic bool,
  -- przeładunki
  transshipments jsonb,        -- [{crossing_id, planned_at, actual_at,
                               --   dwell_hours, cost, currency}]
  -- odprawy
  export_declaration_mrn,      -- Chiny
  transit_declaration_mrn,     -- T1 przy wjeździe do UE
  t1_expires_at,               -- ⚠ termin zakończenia tranzytu
  import_declaration_id,       -- powiązanie z M-99
  -- czas
  planned_departure, actual_departure
  planned_arrival, eta_current, actual_arrival
  free_time_until,
  -- specjalne
  is_reefer, temperature_setpoint, genset_number,
  is_dg, rid_classes text[], dg_approval_ref
```

## 2.5 Zdarzenia i śledzenie

```sql
rail_event
  id, organization_id, leg_id, container_id NULL
  event_code,
  -- BOOKED | SPACE_CONFIRMED | CARGO_READY | GATE_IN_ORIGIN
  -- CUSTOMS_EXPORT_CLEARED | LOADED | DEPARTED
  -- BORDER_ARRIVED | TRANSSHIPMENT_START | TRANSSHIPMENT_DONE
  -- BORDER_DEPARTED | EU_ENTRY | T1_OPENED | TERMINAL_ARRIVED
  -- CUSTOMS_IMPORT_CLEARED | AVAILABLE_FOR_PICKUP
  -- GATE_OUT | DELIVERED | EMPTY_RETURNED
  location_id, occurred_at, recorded_at
  source,                      -- operator_email | portal | manual | edi
  raw_payload jsonb,
  confidence,
  created_source, is_manually_overridden, override_reason
```

**Zdarzenia wprowadzane ręcznie są normą, nie wyjątkiem.** Operatorzy
kolejowi rzadko mają API — status przychodzi mailem albo z portalu.
Wzorzec ręcznej korekty obowiązkowy.
---

# 3. PRZEBIEG PROCESU

## 3.1 Maszyna stanów odcinka kolejowego

```
 zapytanie
    │
    ▼
[QUOTED] ──── oferta zawiera odcinek kolejowy
    │
    ▼
[SPACE_REQUESTED] ── zapytanie o miejsce do operatora
    │                  automat: mail z parametrami
    ▼
[SPACE_CONFIRMED] ── operator potwierdził miejsce na konkretnym odjeździe
    │                  ⚠ blokada: sankcje trasy, RID, dokumenty
    ▼
[BOOKED] ─────────── rezerwacja potwierdzona, numer nadany
    │
    ▼
[DOCS_PENDING] ───── kompletowanie dokumentów przed cut-off
    │                  blokada: brak kompletu = brak załadunku
    ▼
[CARGO_READY] ────── ładunek gotowy w terminalu nadania
    │
    ▼
[EXPORT_CLEARED] ─── odprawa eksportowa w Chinach
    │
    ▼
[LOADED] ─────────── załadunek na wagon
    │
    ▼
[DEPARTED] ───────── odjazd pociągu
    │
    ├──▶ [AT_BORDER] ──▶ [TRANSSHIPMENT] ──▶ [BORDER_CLEARED]
    │      (dla każdego przejścia z przeładunkiem)
    │
    ▼
[EU_ENTRY] ───────── wjazd do UE, otwarcie tranzytu T1
    │                  ⚠ zegar T1 rusza — termin zakończenia
    ▼
[AT_DESTINATION_TERMINAL]
    │                  ⚠ zegar free time rusza
    ▼
[IMPORT_CLEARED] ─── odprawa importowa
    │
    ▼
[AVAILABLE] ──────── gotowy do odbioru
    │
    ▼
[GATE_OUT] ───────── wydany, przekazanie do odcinka drogowego
    │
    ▼
[COMPLETED]
```

## 3.2 Blokady przejść

| Przejście | Warunek |
|---|---|
| → SPACE_CONFIRMED | brak trafienia sankcyjnego na trasie i stronach |
| → SPACE_CONFIRMED | klasa RID akceptowana przez serwis i terminale |
| → BOOKED | kontrahent w limicie kredytowym |
| → CARGO_READY | komplet dokumentów wg `document_requirement` |
| → LOADED | list przewozowy wystawiony i podpisany |
| → GATE_OUT | odprawa zakończona, opłaty terminalowe rozliczone |

---

# 4. DOKUMENTY

## 4.1 Komplet wymagany

| Dokument | Kto wystawia | Kiedy | Uwagi |
|---|---|---|---|
| **List przewozowy CIM/SMGS** | operator | przed załadunkiem | ujednolicony dla całej trasy, eliminuje przepisywanie na granicy |
| List przewozowy SMGS | operator | alternatywnie | odcinek wschodni |
| List przewozowy CIM | operator | alternatywnie | odcinek UE |
| Faktura handlowa | nadawca | przed odprawą | |
| Packing list | nadawca | jw. | |
| Świadectwo pochodzenia | izba w Chinach | jw. | preferencje taryfowe |
| Deklaracja eksportowa | agent w Chinach | przed załadunkiem | |
| **Zgłoszenie tranzytowe T1** | ty albo agent | przy wjeździe do UE | ⚠ termin zakończenia |
| Świadectwo fumigacji ISPM 15 | nadawca | przy opakowaniach drewnianych | |
| Dokumenty RID | nadawca | przy ADR | patrz §6 |
| Certyfikat temperatury | operator | przy reeferach | zapis z rejestratora |
| Potwierdzenie dostawy | przewoźnik | przy odwozie | odcinek drogowy |

## 4.2 Podpisywanie elektroniczne

```sql
document_signature
  id, organization_id
  document_id, document_type
  signer_party_id, signer_name, signer_role
  signature_type,       -- qualified | advanced | simple | wet_scan
  signed_at, certificate_ref
  signature_path, verification_status, verified_at
  ip_address, audit_trail jsonb
```

**Obieg podpisu listu przewozowego:**

```
operator wystawia projekt → ty sprawdzasz → klient akceptuje w portalu
→ podpis elektroniczny → operator finalizuje → wersja podpisana w systemie
```

Warstwa techniczna: `MatthiasValvekens/pyHanko` do podpisu PDF w standardzie
PAdES, `documenso` albo `docuseal` do obiegu akceptacji.

**Uwaga praktyczna:** elektroniczny list przewozowy jest wdrażany stopniowo
i nie wszyscy operatorzy oraz nie wszystkie odcinki go akceptują. Model
przewiduje `is_electronic` — przy wartości fałsz obieg działa na skanach
z podpisem odręcznym, a system śledzi oryginały jak przy konosamencie (M-89).

---

# 5. SANKCJE TRASY — NAJWAŻNIEJSZY MECHANIZM ⚠

Korytarz północny przebiega przez terytoria objęte reżimami sankcyjnymi.
**Sprawdzenie stron transakcji nie wystarczy.**

```sql
route_compliance_check
  id, organization_id
  leg_id NULL, quotation_id NULL
  corridor_id, transit_countries char(2)[]
  border_crossings uuid[]
  operators_involved uuid[],       -- także przewoźnicy kolejowi na trasie
  cargo_hs_codes text[]
  -- wynik
  restricted_countries char(2)[],
  restricted_entities jsonb,       -- operator objęty sankcjami
  restricted_goods jsonb,          -- towar zakazany w tranzycie
  dual_use_flag bool,
  risk_level,                      -- clear | review | blocked
  list_versions jsonb,             -- ⚠ wersje list użyte przy sprawdzeniu
  checked_at, checked_by
  decision, decided_by, decision_rationale
```

## 5.1 Co sprawdzamy

```
□ kraje tranzytu wobec reżimów sankcyjnych
□ operator kolejowy i przewoźnicy na każdym odcinku
□ terminal przeładunkowy i jego operator
□ kod HS towaru wobec wykazów zakazanych w tranzycie
□ podwójne zastosowanie towaru
□ strony transakcji (standardowo, przez M-53)
```

## 5.2 Zasady

**Sprawdzenie przy wycenie i ponownie przed bookingiem.** Lista mogła się
zmienić między jedną a drugą czynnością.

**Ponowne sprawdzenie wszystkich otwartych zleceń przy aktualizacji listy.**
Zlecenie w drodze, którego trasa stała się objęta ograniczeniami, wymaga
natychmiastowej decyzji.

**Poziom `blocked` blokuje wystawienie oferty.** Zwolnienie wyłącznie przez
zatwierdzenie z uzasadnieniem, zapisane w audycie.

**`list_versions` obowiązkowe.** Pytanie kontrolera brzmi „na jakiej wersji
listy sprawdzaliście to zlecenie" — musisz umieć odpowiedzieć.

## 5.3 Prezentacja przy wycenie

```
Xi'an → Łódź · 2×40HC · meble

  Korytarz północny    2 850 USD   16 dni
    ⚠ tranzyt przez terytoria objęte ograniczeniami
    ⚠ wymaga potwierdzenia zgodności przed bookingiem
    → sprawdzone 29.08, lista UE wersja 2026-08-28: brak trafień

  Korytarz środkowy    4 120 USD   31 dni
    ✓ bez tranzytu przez terytoria objęte ograniczeniami
    ⚠ trzy przeładunki, większa zmienność terminu
```

**Pokazuj oba warianty z jawnym uzasadnieniem różnicy.** To jest decyzja
klienta, podejmowana świadomie, a twoja rola to dostarczenie podstawy.

---

# 6. TOWARY NIEBEZPIECZNE

Kolej podlega **RID** w Europie i przepisom SMGS na odcinku wschodnim.
To nie są te same wykazy co IMDG.

```sql
rail_dg_acceptance
  id, service_id NULL, corridor_id NULL, terminal_id NULL
  accepted_rid_classes text[],
  excluded_un_numbers text[],
  requires_pre_approval bool,
  pre_approval_lead_days,       -- często 10–14 dni
  max_quantity_per_train,
  special_conditions jsonb
```

**Ograniczenia praktyczne:**

- część korytarzy nie przyjmuje ładunków niebezpiecznych w ogóle
- terminale przeładunkowe mają własne wykazy klas
- wcześniejsza zgoda wymagana z dużym wyprzedzeniem
- cut-off dla ADR wypada znacznie wcześniej niż zwykły
- przeładunek szerokotorowy przy niektórych klasach wymaga procedury specjalnej

Sprawdzenie akceptacji odbywa się **przed pokazaniem serwisu w wycenie** —
oferta na trasę, która nie przyjmie tego ładunku, jest gorsza niż brak oferty.

---

# 7. DROBNICA KOLEJOWA

## 7.1 Specyfika

```sql
rail_lcl_rate
  id, organization_id, consolidator_party_id
  origin_cfs_terminal_id, destination_cfs_terminal_id
  corridor_id
  rate_per_wm numeric(14,4), currency,
  wm_ratio numeric(6,3),        -- ile CBM na tonę, bywa inne niż 1:1
  min_charge, min_wm,
  frequency,                     -- np. tygodniowo, wtorek
  transit_days,
  cutoff_cfs_days,               -- ⚠ wcześniejszy niż dla FCL
  max_single_piece_kg, max_dimensions jsonb,
  accepts_dg bool, accepted_rid_classes text[],
  valid_from, valid_to

rail_consolidation
  id, organization_id
  departure_id, container_number
  origin_cfs_id, destination_cfs_id
  capacity_cbm, capacity_kg
  used_cbm, used_kg, fill_rate
  cutoff_at, cost_total, currency
  allocation_mode                -- shared | capacity | marginal
```

**Waga obliczeniowa liczona kodem, nigdy modelem:**

```
chargeable_wm = max(waga_w_tonach, objętość_cbm / wm_ratio)
jeśli chargeable_wm < min_wm → min_wm
```

`wm_ratio` bywa inne niż jeden — dlatego jest polem, nie stałą.

## 7.2 Konsolidacja

Ten sam silnik alokacji co przy drobnicy drogowej (M-48) i morskiej (M-51).
Trzy tryby: proporcjonalny, pojemnościowy i krańcowy przy doładunku.

**Decyzja o doładunku przed cut-offem CFS** to ta sama matematyka kosztu
krańcowego: kontener jedzie tak czy inaczej, pytanie brzmi, czy przychód
z dodatkowej przesyłki przekracza koszt jej obsługi.

## 7.3 Próg opłacalności

```
Ładunek 21 CBM, 5 200 kg, Xi'an → Łódź

  LCL   21 W/M × 165 USD = 3 465 USD + lokalne 280 = 3 745 USD   24 dni
  FCL   40HC                          all-in       = 3 420 USD   19 dni

  → FCL tańszy i szybszy. Próg na tej relacji: 19,4 W/M
```

Automatyczne pokazanie progu przy każdym zapytaniu drobnicowym.

---

# 8. ODWOZY DROGOWE WEDŁUG INCOTERMS

To wynika z korekty modelu: odwóz to kolejny `shipment_leg`.

## 8.1 Reguła

```sql
incoterm_leg_requirement
  incoterm, mode
  requires_pre_carriage bool,
  requires_on_carriage bool,
  cost_boundary,          -- do którego punktu koszty po naszej stronie
  risk_boundary
```

| Incoterm | Odcinek dowozowy | Odcinek odwozowy | Kto płaci odwóz |
|---|---|---|---|
| EXW | tak, od drzwi nadawcy | tak | kupujący, ale organizujemy |
| FCA terminal | nie | tak | kupujący |
| CPT / CIP terminal | nie | nie | — |
| CPT / CIP drzwi | nie | **tak** | sprzedający |
| **DAP** | zależnie | **tak, do drzwi** | sprzedający |
| **DPU** | zależnie | **tak, z rozładunkiem** | sprzedający |
| **DDP** | zależnie | **tak, po odprawie** | sprzedający |

## 8.2 Automatyczne tworzenie odcinka

```
przy wycenie:
  incoterm = DAP, miejsce = Poznań
  terminal kolejowy docelowy = Łódź Olechów
        ↓
  system tworzy odcinek: RAIL Xi'an → Łódź
                         ROAD Łódź → Poznań   ← automatycznie
        ↓
  dobór stawki dla odcinka drogowego:
    cennik przewoźnika → zapytanie do przewoźników → luka w quotation_gap
```

**Przy DDP dochodzi jeszcze odprawa importowa** jako pozycja kosztowa
i powiązanie z modułem celnym (M-99).

## 8.3 Koordynacja terminów

Odwóz drogowy planowany od momentu dostępności kontenera, nie od przyjazdu
pociągu. Między jednym a drugim jest rozładunek i odprawa.

```
przyjazd pociągu → rozładunek (1–2 dni) → odprawa (1–3 dni)
→ dostępność → free time bieży → odwóz
```

**Strażnik free time działa tu tak samo jak przy morzu.** Terminale kolejowe
mają zwykle krótszy okres bezpłatnego składowania niż porty — tym bardziej
warto pilnować.
---

# 9. AUTOMATYZACJE

## 9.1 Katalog

| # | Automatyzacja | Wyzwalacz | Działanie |
|---|---|---|---|
| 1 | **Synchronizacja rozkładów** | cron, codziennie 6:00 | pobranie odjazdów od operatorów, aktualizacja `rail_departure` |
| 2 | **Zapytanie o miejsce** | odcinek w stanie QUOTED, klient akceptuje | mail do operatorów z parametrami, kanał z M-19 |
| 3 | **Parsowanie potwierdzenia miejsca** | odpowiedź operatora | ekstrakcja numeru odjazdu, wagonu, terminów |
| 4 | **Przypomnienie o cut-off dokumentów** | 48 h przed | powiadomienie operatora i klienta o brakach |
| 5 | **Aktualizacja statusu z maila operatora** | mail na skrzynkę | klasyfikacja, ekstrakcja zdarzenia, dopisanie do `rail_event` |
| 6 | **Przeliczenie prognozy przybycia** | każde zdarzenie | ETA z historii tego korytarza, nie z rozkładu |
| 7 | **Alert opóźnienia** | ETA przesunięta powyżej progu | powiadomienie operatora i klienta, korekta prognozy marży |
| 8 | **Monitorowanie przeładunku** | zdarzenie na przejściu | pomiar czasu postoju, alert przy przekroczeniu percentyla |
| 9 | **Zegar tranzytu T1** | otwarcie tranzytu | alert 48 h przed terminem zakończenia |
| 10 | **Strażnik free time** | przybycie do terminalu | alert przed pierwszą dobą płatną |
| 11 | **Planowanie odwozu** | dostępność kontenera | utworzenie zlecenia do przewoźnika, propozycja terminu |
| 12 | **Ponowne sprawdzenie sankcji** | aktualizacja listy | przeskanowanie wszystkich otwartych odcinków |
| 13 | **Wygasanie dofinansowania** | 30 dni przed `subsidy_valid_to` | alert, przegląd ofert opartych na tej stawce |
| 14 | **Wykrywanie zatorów** | mediana postoju rośnie | korekta buforów w prognozie ETA |

## 9.2 Prognoza przybycia z własnych danych

Rozkład operatora podaje czas planowany. Rzeczywistość odbiega.

```
eta = odjazd_faktyczny
    + mediana_tranzytu(korytarz, ostatnie 90 dni)
    + suma_postojów(przejścia, percentyl 75)
    + bufor_sezonowy(chiński nowy rok, szczyt przedświąteczny)
```

**Percentyl 75 zamiast średniej przy postojach.** Rozkład czasu przeładunku
jest skośny — średnia zaniża, a klient pamięta opóźnienia, nie terminowość.

Po roku danych prognoza z własnej historii bije rozkład operatora.

---

# 10. WIZUALIZACJA NA MAPIE

## 10.1 Warstwy

```
① Korytarze          linie tras z rozróżnieniem północny/środkowy/południowy
② Terminale          punkty z ikoną zależną od funkcji (FCL/LCL/reefer/DG)
③ Przejścia          punkty przeładunku szerokotorowego, z czasem postoju
④ Pozycja przesyłki  ostatnie zdarzenie, nie GPS
⑤ Prognoza           odcinek pozostały do przebycia, przerywany
⑥ Zatory             kolor przejścia wg aktualnego czasu postoju
```

## 10.2 Ważne zastrzeżenie

**Kolej nie daje pozycji w czasie rzeczywistym.** Nie ma odpowiednika AIS.
Pozycja jest interpolowana między ostatnim zdarzeniem a następnym punktem
kontrolnym.

```
Ostatnie zdarzenie:  Dostyk, przeładunek zakończony, 21.09 14:30
Następny punkt:      Brześć, prognoza 27.09
Pozycja pokazana:    interpolacja na trasie, z adnotacją
                     „ostatnia potwierdzona lokalizacja: Dostyk, 5 dni temu"
```

**Adnotacja jest obowiązkowa.** Pokazanie kropki bez informacji o wieku danych
sugeruje precyzję, której nie ma — i przy pierwszym pytaniu klienta „gdzie
dokładnie jest teraz" tracisz wiarygodność.

## 10.3 Warstwa techniczna

`maplibre-gl-js` z kafelkami wektorowymi. Trasy jako geometrie w bazie:

```sql
rail_corridor_geometry
  corridor_id, segment_order
  from_location_id, to_location_id
  geometry geography(LINESTRING, 4326),
  distance_km
```

Publiczny link śledzenia dla klienta — ta sama mapa, bez danych kosztowych.

---

# 11. INTEGRACJE

## 11.1 Stan faktyczny

**Operatorzy korytarza Chiny–Europa nie mają publicznych API.**
Kanały dostępne:

| Kanał | Kto | Jak |
|---|---|---|
| **Mail** | większość operatorów | mechanizm z M-30 bez zmian |
| Portal | część większych | `browser-use` na poświadczeniach klienta |
| Plik | niektórzy | rozkłady i statusy w Excelu, cyklicznie |
| EDI | rzadko | komunikaty kolejowe |

**Twój mechanizm zapytań do agentów obsługuje operatorów kolejowych bez
jednej linijki nowego kodu.** Operator to kolejny wpis w `carrier_channel`
z typem `email`.

## 11.2 Parsowanie statusów z maili

Operatorzy wysyłają statusy w formatach nieregularnych — treść maila, tabela,
załącznik Excel. Pipeline ekstrakcji z M-20 obsługuje to z osobnym schematem:

```json
{
  "train_number": "XA-MAL-2609",
  "events": [{
    "container_raw": "TCNU1234567",
    "event_raw": "loaded on wagon at Alashankou",
    "location_raw": "Alashankou",
    "datetime_raw": "21/09/2026 14:30",
    "source_ref": {"line": 12}
  }],
  "unparsed_regions": []
}
```

Mapowanie `event_raw` na kod zdarzenia przez słownik aliasów — ten sam
mechanizm co przy kodach opłat, z uczeniem z korekt.

---

# 12. WSKAŹNIKI MODUŁU

| Wskaźnik | Po co |
|---|---|
| Terminowość per korytarz | który korytarz realnie dowozi na czas |
| Mediana i percentyl 90 tranzytu | podstawa prognozy i obietnicy dla klienta |
| Czas postoju per przejście | wykrywanie zatorów |
| Wykorzystanie miejsca per odjazd | negocjacje z operatorem |
| Marża per korytarz i relacja | gdzie zarabiasz |
| Udział dofinansowania w cenie | ryzyko przy wygaśnięciu |
| Wypełnienie kontenera drobnicowego | efektywność konsolidacji |
| Liczba przekroczeń free time | koszt z przeoczenia |
| Odsetek zdarzeń wprowadzonych ręcznie | jakość automatyzacji |
| Odchylenie ETA prognozowanej od rzeczywistej | jakość prognozy |

---

# 13. PLAN WDROŻENIA

| Plaster | Zakres | Dni | Zależy |
|---|---|---|---|
| **8.21** | Infrastruktura: korytarze, przejścia, terminale, platformy | 3 | M-05 |
| **8.22** | `rail_service`, `rail_departure`, synchronizacja rozkładów | 4 | 8.21 |
| **8.23** | `rail_rate` z dofinansowaniem, dobór w silniku wyceny | 4 | 8.22, 2.4 |
| **8.24** | `shipment_leg_rail`, maszyna stanów, blokady przejść | 5 | korekta odcinków |
| **8.25** | **Sprawdzanie sankcji trasy** | 4 | M-53 |
| **8.26** | Zapytania o miejsce, parsowanie potwierdzeń | 3 | M-30 |
| **8.27** | Zdarzenia: parsowanie maili, słownik aliasów, korekta ręczna | 4 | M-20 |
| **8.28** | Prognoza ETA z własnych danych, alerty opóźnień | 3 | 8.27 |
| **8.29** | Dokumenty: CIM/SMGS, komplet, T1, zegar tranzytu | 4 | M-205 |
| **8.30** | Podpis elektroniczny i obieg akceptacji | 3 | M-84 |
| **8.31** | RID: akceptacja serwisów i terminali, blokady | 2 | M-08 |
| **8.32** | Drobnica: stawki W/M, konsolidacja, próg FCL | 4 | M-51 |
| **8.33** | Odwozy drogowe wg incoterms, automatyczne odcinki | 3 | korekta odcinków |
| **8.34** | Mapa: korytarze, terminale, pozycja z adnotacją | 4 | — |
| **8.35** | Wskaźniki modułu | 2 | M-202 |

**Razem 52 dni.**

## Kolejność w obrębie modułu

**8.25 przed 8.26.** Nie wysyłaj zapytania o miejsce na trasę, której
zgodność nie została sprawdzona.

**8.27 przed 8.28.** Prognoza z własnych danych wymaga danych — najpierw
zbieranie zdarzeń, potem model.

**8.30 może poczekać.** Podpis elektroniczny jest wygodny, ale obieg na
skanach działa i nie blokuje uruchomienia.

---

# 14. TRZY RZECZY, KTÓRE DECYDUJĄ

**① Sankcje trasy, nie tylko stron.** To jest jedyny element tego modułu,
w którym błąd ma konsekwencje karne dla klienta. Sprawdzanie przy wycenie,
ponownie przed bookingiem i ponownie przy każdej aktualizacji listy —
z zapisem wersji listy jako dowodem.

**② Prognoza z własnej historii, nie z rozkładu operatora.** Rozkład podaje
czas planowany. Klient pamięta opóźnienia. Po roku danych mediana i percentyl
z twoich zleceń dają obietnicę, której dotrzymasz — a to jest przewaga nad
konkurencją, która powtarza za operatorem.

**③ Adnotacja o wieku danych na mapie.** Kolej nie daje pozycji w czasie
rzeczywistym. Kropka bez informacji „ostatnia potwierdzona lokalizacja
sprzed pięciu dni" sugeruje precyzję, której nie ma, i kosztuje wiarygodność
przy pierwszym pytaniu klienta.

---

# 15. CZEGO ŚWIADOMIE NIE MA

**Integracji z systemami kolei państwowych.** Nie są dostępne komercyjnie
dla spedytora. Kanał mailowy pozostaje podstawą.

**Śledzenia GPS kontenera.** Wymagałoby własnych lokalizatorów na kontenerach
— to osobny produkt i osobny koszt. Możliwe jako rozszerzenie, gdy klient
o to poprosi i za to zapłaci.

**Automatycznego wyboru korytarza.** System pokazuje warianty z uzasadnieniem,
decyzję podejmuje człowiek. Przy trasie o wymiarze prawnym automatyzacja
decyzji byłaby przeniesieniem odpowiedzialności na oprogramowanie.

**Rezerwacji miejsca przez API.** Nie istnieje. Rezerwacja to wymiana maili
z potwierdzeniem, którą system porządkuje i parsuje.
