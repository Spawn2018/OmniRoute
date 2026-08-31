# Aneks 22 — Uzupełnienia podatkowe, flotowe i zarządcze

Dziesięć modułów. Trzy pierwsze to obszary z realną odpowiedzialnością prawną,
o których nie było mowy ani razu.

---

# M-109 · Podatek u źródła i certyfikaty rezydencji ⚠

**Pułapka podatkowa, na której wykłada się wielu spedytorów.**

Płacisz zagranicznemu agentowi za usługi. Część takich płatności podlega
podatkowi u źródła — i jeśli nie masz aktualnego certyfikatu rezydencji
podatkowej kontrahenta, obowiązek poboru spoczywa na tobie. Odkrywa się to
przy kontroli, razem z odsetkami.

```sql
tax_residency_certificate
  id, party_id
  country, tax_id_foreign
  issued_at, valid_from, valid_to
  file_path, verified_by, verified_at
  status              -- valid | expiring | expired | missing

wht_assessment
  id, bill_id, party_id
  service_type,       -- transport | doradztwo | licencje | inne
  is_wht_applicable bool
  gross_amount, wht_rate, wht_amount
  treaty_rate,        -- stawka z umowy o unikaniu podwójnego opodatkowania
  certificate_id NULL
  exemption_basis, assessed_by, assessed_at

wht_declaration
  id, organization_id, period
  entries uuid[], total_amount
  filed_at, reference
```

## Funkcje, które zapobiegają problemowi

**Blokada płatności bez certyfikatu.** Faktura od zagranicznego agenta,
brak ważnego certyfikatu, usługa potencjalnie objęta podatkiem → ostrzeżenie
przed zatwierdzeniem przelewu.

**Alert o wygasających certyfikatach.** Certyfikat ma ograniczoną ważność.
Przypomnienie na sześćdziesiąt dni przed to jeden e-mail do agenta zamiast
korekty deklaracji.

**Klasyfikacja usługi.** Nie każda płatność podlega podatkowi u źródła —
sam fracht zwykle nie, doradztwo i licencje tak. System sygnalizuje, decyduje
człowiek albo księgowość. To ta sama zasada co przy ADR: **walidujesz,
nie klasyfikujesz za klienta.**

## Powiązane obowiązki podatkowe

```
□ Biała lista jako konsekwencja podatkowa — płatność na rachunek spoza wykazu
  powyżej progu oznacza brak możliwości zaliczenia do kosztów. Mieliśmy
  weryfikację (M-10), brakowało ostrzeżenia o skutku
□ Mechanizm podzielonej płatności — obowiązkowy dla części transakcji
□ JPK_V7M — generowanie z danych fakturowych
□ Transakcje wewnątrzwspólnotowe — VAT-UE, informacja podsumowująca
```

---

# M-110 · Monitoring przewozu towarów wrażliwych (SENT)

Wspominałem raz przy polskiej specyfice, nigdy nie zamodelowałem.
Przewóz towarów objętych systemem monitorowania bez zgłoszenia to kary
administracyjne — i to na przewoźnika, spedytora i odbiorcę.

```sql
sent_notification
  id, shipment_id, organization_id
  role,               -- sender | carrier | recipient
  reference_number,   -- numer referencyjny SENT
  goods_cn_code, goods_description
  quantity, unit, gross_weight
  vehicle_plate, trailer_plate, driver_name
  loading_place, unloading_place
  planned_start, planned_end
  geolocator_id,      -- lokalizator GPS
  status,             -- draft | sent | active | closed | expired
  submitted_at, closed_at
  puesc_reference
```

**Automatyczne rozpoznanie po kodzie CN.** Towar wpisany na zlecenie z kodem
objętym monitorowaniem → system sygnalizuje obowiązek zgłoszenia przed
rozpoczęciem przewozu, blokuje zamknięcie zlecenia bez numeru referencyjnego.

To jest funkcja, która chroni klienta przed karą — i argument sprzedażowy
dla każdego, kto wozi paliwa, oleje, alkohol czy susz tytoniowy.

---

# M-111 · Flota własna i kierowcy

Dotyczy cię, jeśli LOGMAR wykonuje transport własnymi pojazdami.
Obszar z gęstą regulacją i realnymi karami.

```sql
vehicle
  id, organization_id, legal_entity_id
  plate, vin, kind,   -- ciągnik | naczepa | solówka | bus
  make, model, year
  gvw_kg, payload_kg, ldm_capacity, pallet_capacity
  euro_class, has_adr_certificate, adr_classes text[]
  is_reefer, has_tail_lift
  status              -- active | service | sold

vehicle_document
  id, vehicle_id, kind,  -- przegląd | OC | AC | licencja
                         -- wypis | ADR | tachograf | zezwolenie
  number, valid_from, valid_to, file_path
  reminder_days_before

driver
  id, organization_id, user_id NULL
  name, license_number, license_categories text[]
  license_valid_to
  qualification_card_valid_to     -- świadectwo kwalifikacji
  medical_valid_to, psychological_valid_to
  adr_certificate_valid_to
  driver_card_number, driver_card_valid_to

driver_working_time
  id, driver_id, date
  driving_minutes, other_work_minutes, availability_minutes
  daily_rest_minutes, weekly_rest_taken
  source,             -- tachograph | manual | telematics
  violations jsonb    -- przekroczenia czasu prowadzenia

driver_posting                     -- Pakiet Mobilności
  id, driver_id, country
  declaration_reference,           -- zgłoszenie w systemie IMI
  valid_from, valid_to
  applicable_minimum_wage, currency
  documents jsonb
```

## Dlaczego to jest poważne

**Czas pracy kierowcy** podlega przepisom unijnym z twardymi limitami
dziennego i tygodniowego prowadzenia oraz odpoczynku. Naruszenia to kary
zarówno dla kierowcy, jak i dla przewoźnika, wykrywane przy kontroli drogowej
i przy kontroli w siedzibie.

**Delegowanie kierowców** wymaga zgłoszenia w systemie IMI przed rozpoczęciem
przewozu w danym państwie i wypłaty wynagrodzenia według stawek kraju
delegowania. Dokumentacja musi być dostępna dla kontroli.

**Terminy dokumentów.** Przegląd, ubezpieczenie, wypis z licencji, badania
kierowcy, świadectwo kwalifikacji, karta kierowcy — każdy z osobną datą
ważności. Jazda bez ważnego dokumentu to kara i utrata ochrony ubezpieczeniowej.

**Alert wyprzedzający na wszystko powyżej** jest funkcją tanią i chroniącą
przed konsekwencjami nieproporcjonalnie dużymi wobec kosztu jej zbudowania.

## Koszty eksploatacji

```sql
vehicle_cost
  id, vehicle_id, kind,   -- paliwo | serwis | opony | myto
                          -- ubezpieczenie | leasing | kierowca
  amount, currency, occurred_at
  odometer_km, source     -- karta paliwowa | faktura | ręcznie
```

Zasila silnik alokacji z M-48: koszt przejazdu przestaje być stawką ryczałtową,
a staje się wyliczeniem z rzeczywistych kosztów pojazdu.

---

# M-112 · Uprawnienia i certyfikaty organizacji

Osobno od dokumentów pojazdów — uprawnienia firmy i ludzi.

```sql
company_certification
  id, organization_id, kind,
  -- licencja spedycyjna | licencja transportowa | AEO
  -- agencja celna | ISO 9001 | ISO 14001 | GDP
  number, issuer, valid_from, valid_to
  scope, file_path, reminder_days_before

employee_qualification
  id, user_id, kind,
  -- DGSA (doradca ADR) | agent celny | ADR | operator wózka
  -- uprawnienia IATA | szkolenie RODO | szkolenie AI Act
  number, valid_from, valid_to, file_path
```

**Doradca do spraw bezpieczeństwa przewozu towarów niebezpiecznych** jest
wymagany, jeśli firma uczestniczy w przewozie ADR powyżej progów. Brak doradcy
to naruszenie, a nie niedopatrzenie organizacyjne.

**Szkolenie z kompetencji w zakresie AI** wynika z AI Act i obowiązuje
od lutego 2025 — dobrze mieć rejestr, kto i kiedy je przeszedł. To jedno pole,
a przy kontroli albo audycie klienta ma znaczenie.

---

# M-113 · Przyjęcie i umowy z agentami

Mieliśmy kartę wyników agenta i katalog sieci. Brakowało procesu przyjęcia
i strony umownej.

```sql
agent_onboarding
  id, party_id, organization_id
  status,             -- prospect | verifying | approved | rejected | suspended
  checks jsonb,       -- KYC, sankcje, licencje, ubezpieczenie, referencje
  insurance_policy_number, insurance_valid_to, insurance_limit
  network_membership_verified bool
  approved_by, approved_at, review_due_at

agent_agreement
  id, party_id
  kind,               -- ramowa | agencyjna | poufności | DPA
  number, valid_from, valid_to
  commission_terms jsonb
  payment_terms_days, credit_limit_granted
  liability_cap, jurisdiction, governing_law
  file_path
```

**Weryfikacja ubezpieczenia agenta z alertem wygaśnięcia** jest istotna:
agent bez ważnej polisy to twoje ryzyko przy szkodzie. Wielu spedytorów sprawdza
to raz, przy nawiązaniu współpracy, i nigdy więcej.

**Okresowy przegląd** — data następnej weryfikacji, alert. Agent sprawdzony
trzy lata temu nie jest sprawdzony.

---

# M-114 · Budżet i plan wobec wykonania

Narzędzie właściciela, nieobecne w projekcie.

```sql
budget
  id, organization_id, year, version
  status,             -- draft | approved | superseded
  approved_by, approved_at

budget_line
  id, budget_id
  dimension,          -- lane | customer | salesperson
                      -- mode | branch | legal_entity
  dimension_ref, period,   -- miesiąc albo kwartał
  revenue_target, margin_target, volume_target
  currency

budget_variance                  -- widok
  budget_line_id, period
  actual_revenue, actual_margin, actual_volume
  variance_amount, variance_pct, trend
```

**Cel handlowca zestawiony z wykonaniem** zasila prowizje z M-101 i rozmowę
roczną. **Cel na relacji** pokazuje, gdzie plan się rozjeżdża, zanim skończy
się kwartał.

Powiązane z prognozą z M-72 (pipeline) — plan, prognoza i wykonanie na jednym
ekranie to standardowe pytanie właściciela, na które dziś odpowiada Excel.

---

# M-115 · Windykacja twarda i zabezpieczenie należności

Przedłużenie windykacji miękkiej z M-87.

```sql
debt_case
  id, organization_id, party_id
  invoices uuid[], principal, interest, costs, currency
  stage,              -- internal | prelegal | external_agency
                      -- court | enforcement | written_off
  handler,            -- wewnętrzny albo firma windykacyjna
  handed_over_at, recovered_amount, recovered_at
  limitation_date     -- ← termin przedawnienia
  documents jsonb

receivables_insurance
  id, organization_id, insurer_party_id
  policy_number, valid_from, valid_to
  covered_parties uuid[], limits jsonb
  notification_deadline_days      -- termin zgłoszenia opóźnienia
```

**Termin przedawnienia liczony automatycznie** — roszczenia z umowy spedycji
przedawniają się szybko, a przekroczenie terminu kończy sprawę niezależnie od
zasadności. To ta sama logika co przy reklamacjach z M-55.

**Ubezpieczenie należności ma własny termin zgłoszenia opóźnienia** — niezgłoszona
w terminie faktura wypada spod ochrony. Alert obowiązkowy.

---

# M-116 · Fracht lotniczy

Świadomie odłożony, ale powinien być w rejestrze — bo model danych musi być
na niego przygotowany, nawet jeśli kodu nie piszesz.

```sql
-- rozszerzenie shipment
shipment_air
  shipment_id
  awb_number, hawb_number
  airline_party_id, flight_number
  departure_airport, arrival_airport   -- IATA
  chargeable_weight_kg,                -- max(waga, objętość / 6000)
  volumetric_ratio,                    -- zwykle 1:6, ale bywa inaczej
  uld_type, pieces
  security_status,                     -- SPX | SCO | znany nadawca
  screening_method
  cutoff_acceptance, cutoff_security
```

**Waga obliczeniowa lotnicza to inny wzór niż morska** — objętość dzielona
przez współczynnik zamiast porównania ton i metrów sześciennych. Jeśli
`chargeable_weight` zaprojektujesz jako funkcję zależną od gałęzi, dołożenie
lotnictwa będzie rozszerzeniem, nie przepisaniem.

**Status bezpieczeństwa i znany nadawca** to wymóg regulacyjny w lotnictwie,
bez odpowiednika w morzu.

---

# M-117 · Zarządzanie zmianami cen wobec klientów

Stawka zakupowa rośnie. Co dalej?

```sql
price_change_notice
  id, organization_id
  trigger,            -- gri | pss | bunker | ets | contract_review
  affected_lanes jsonb, affected_customers uuid[]
  effective_from, notice_period_days
  old_amount, new_amount, currency, charge_code
  status,             -- draft | sent | acknowledged | disputed | applied
  sent_at, applied_at
  linked_market_event_id           -- z M-61
```

**Automatyczne wyznaczenie kręgu klientów.** GRI ogłoszony na relacji →
system wskazuje, których klientów dotyczy, jakie mają cenniki i umowy, i
generuje projekty powiadomień.

**Termin wypowiedzenia z umowy** — jeśli umowa przewiduje trzydziestodniowe
uprzedzenie, system pilnuje, żeby zmiana nie weszła wcześniej.

To zamyka pętlę: moduł rynkowy wykrywa zdarzenie, moduł cennikowy wskazuje
ekspozycję, ten moduł generuje komunikację. Dziś to jest kilka godzin pracy
przy każdym GRI.

---

# M-118 · Rozliczenia podatkowe i sprawozdawcze

Zebranie rozproszonych obowiązków w jeden moduł.

| Obowiązek | Co robi system |
|---|---|
| JPK_V7M | generowanie z danych fakturowych, walidacja przed wysyłką |
| VAT-UE | informacja podsumowująca dla transakcji wewnątrzwspólnotowych |
| Mechanizm podzielonej płatności | oznaczenie faktur objętych obowiązkiem |
| Biała lista | ostrzeżenie o skutku podatkowym płatności poza wykazem |
| Podatek u źródła | patrz M-109 |
| Kursy do przeliczeń | NBP D-1 roboczy, patrz M-07 |
| Odwrotne obciążenie | reguły stosowania per typ usługi i kontrahenta |
| Stawka 0% na transport międzynarodowy | **warunki dokumentacyjne i kontrola kompletu** |

**Ostatnia pozycja zasługuje na uwagę.** Stawka zerowa na transport
międzynarodowy wymaga posiadania określonych dokumentów. Ich brak przy kontroli
oznacza doszacowanie podatku. System, który pilnuje kompletu i blokuje
zastosowanie stawki bez dokumentów, chroni klienta przed realną kwotą.

---

# PODSUMOWANIE

| Moduł | Nazwa | Faza | Nakład |
|---|---|---|---|
| **M-109** | **Podatek u źródła i certyfikaty** | 6 | 4 dni |
| **M-110** | **SENT** | 7 | 3 dni |
| **M-111** | **Flota i kierowcy** | 8 | 10 dni |
| M-112 | Uprawnienia i certyfikaty | 1 | 2 dni |
| M-113 | Przyjęcie i umowy z agentami | 5 | 3 dni |
| M-114 | Budżet i wykonanie | 9 | 5 dni |
| M-115 | Windykacja twarda | 6 | 3 dni |
| M-116 | Fracht lotniczy | 9 | 12 dni |
| M-117 | Zmiany cen wobec klientów | 9 | 4 dni |
| M-118 | Rozliczenia podatkowe | 6 | 6 dni |

**52 dni. Rejestr rośnie z 108 do 118 modułów.**

## Trzy o realnej odpowiedzialności prawnej

**M-109 — podatek u źródła.** Płacisz zagranicznym agentom. Brak certyfikatu
rezydencji oznacza obowiązek poboru po twojej stronie. Wychodzi przy kontroli,
z odsetkami.

**M-110 — SENT.** Przewóz towaru objętego monitorowaniem bez zgłoszenia to kary
administracyjne dla wszystkich stron. Automatyczne rozpoznanie po kodzie CN
chroni klienta.

**M-111 — czas pracy kierowców i delegowanie.** Jeśli LOGMAR jeździ własnymi
pojazdami, to nie jest funkcja wygody, tylko wymóg z kontrolą i karami.

## Jedno pole, które warto dodać już teraz

W M-112: rejestr szkoleń z kompetencji w zakresie AI. Obowiązek z AI Act
działa od lutego 2025, a wpis to jeden wiersz. Przy audycie klienta
korporacyjnego albo kontroli ma znaczenie nieproporcjonalne do kosztu.

## O zakresie

Sto osiemnaście modułów. Domena jest głęboka i prawdopodobnie znalazłbym
kolejne dziesięć — celne procedury szczególne, przewozy ponadnormatywne,
obsługa portowa, agencja morska.

Ale rejestr przekroczył już punkt, w którym jest mapą. Teraz jest atlasem.
**Fazy 0–3 nie zmieniły się od dziesięciu aneksów** — i to one decydują,
czy powstanie cokolwiek.
