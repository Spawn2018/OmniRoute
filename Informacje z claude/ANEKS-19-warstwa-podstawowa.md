# Aneks 19 — Warstwa podstawowa

Rzeczy oczywiste, których nie było w rejestrze. Pojedynczo trywialne,
razem decydują, czy produkt wygląda na skończony.

**Szacowany udział w nakładzie: 25–30%.** To jest część, którą się pomija
przy planowaniu i która potem opóźnia wdrożenie o miesiąc.

---

# M-80 · Ustawienia organizacji

Bez tego nie wystawisz ani jednego dokumentu.

```sql
organization_profile
  organization_id
  legal_name, trade_name
  tax_id, regon, krs, nip_eu
  share_capital, registry_court        -- wymagane na fakturach spółek
  address jsonb, correspondence_address jsonb
  phone, email, website
  default_currency, default_language, timezone
  fiscal_year_start_month

organization_asset                      -- logo i grafiki
  id, organization_id
  kind,      -- logo_color | logo_mono | logo_dark | favicon
             -- stamp | signature | letterhead | email_banner
  file_path, width, height

organization_bank_account
  id, organization_id
  bank_name, iban, swift, currency
  is_default_for_currency, show_on_invoice

organization_branch                     -- oddziały własne
  id, organization_id, name, code
  address jsonb, phone, email
  numbering_prefix                      -- osobna seria numeracji
  is_active

organization_credential                 -- to, o co pytają klienci
  id, organization_id
  kind,      -- forwarder_license | aeo | oc_insurance
             -- customs_agency | iata | fiata
  number, issuer, valid_from, valid_to
  show_on_documents bool
```

**`organization_credential` zasługuje na uwagę.** Numer polisy OC spedytora
i certyfikat AEO to rzeczy, o które klienci pytają przy pierwszej ofercie,
i które umieszcza się w stopce dokumentów. Bez tego oferta wygląda
nieprofesjonalnie.

## Warunki handlowe

```sql
organization_terms
  id, organization_id
  kind,      -- opws | own_terms | payment_terms | privacy
  language, title, content, version
  is_default, valid_from
  attach_to_documents text[]     -- quotation | invoice | booking_confirmation
```

W Polsce standardem są Ogólne Polskie Warunki Spedycyjne. Oferta bez odwołania
do nich albo do własnych warunków jest niekompletna prawnie. To pole musi być
w ustawieniach, a treść dołączana do PDF.

---

# M-81 · Ustawienia użytkownika

```sql
user_profile
  user_id
  display_name, position, phone, mobile
  avatar_path
  email_signature_html                  -- do wysyłek z M-32
  language, timezone, date_format, number_format
  density,        -- compact | comfortable
  theme           -- light | dark | system

user_notification_preference
  user_id, event_type, channel, is_enabled
  quiet_hours_from, quiet_hours_to

user_delegation                         -- zastępstwo na urlop
  id, organization_id
  from_user_id, to_user_id
  valid_from, valid_to, scope text[]
  -- zlecenia i zapytania nieobecnego trafiają do zastępcy

user_saved_view                         -- zapisane filtry i układy kolumn
  id, user_id, entity_type, name
  filters jsonb, columns jsonb, sort jsonb
  is_default, is_shared

user_favorite                           -- ulubione i ostatnio używane
  id, user_id, entity_type, entity_id, kind
```

**Zastępstwo na urlop to funkcja, o której nikt nie pamięta przy projektowaniu
i której wszyscy potrzebują w lipcu.** Zapytanie wysłane ze skrzynki handlowca
na urlopie musi trafić do kogoś.

---

# M-82 · Słowniki podstawowe

Wszystkie z możliwością dodania własnych pozycji per organizacja.

| Słownik | Przykłady | Uwaga |
|---|---|---|
| `packaging_type` | paleta EUR, paleta przemysłowa, karton, skrzynia, big bag, bęben, luzem | z wymiarami domyślnymi |
| `unit_of_measure` | kg, t, m³, LDM, szt., paleta, W/M | z przelicznikami |
| `vat_rate` | 23%, 8%, 5%, 0%, NP, ZW, odwrotne obciążenie | **reguła 0% na transport międzynarodowy** |
| `payment_term` | przedpłata, 7, 14, 21, 30, 45, 60 dni | powiązane z M-43 |
| `payment_method` | przelew, gotówka, karta, kompensata | |
| `loss_reason` | cena, tranzyt, harmonogram, brak miejsca, klient zrezygnował | do M-25 |
| `contact_role` | ofertowanie, operacje, księgowość, decydent | |
| `industry` | branża klienta | do segmentacji |
| `service_type` | door-door, port-port, door-port, port-door | |
| `document_type` | B/L, CMR, faktura, packing list, SAD, DGD, świadectwo | |
| `country` | z kodami ISO, strefą celną UE/poza UE, walutą | |
| `holiday_calendar` | dni wolne per kraj | **wpływa na cut-offy i terminy** |
| `working_hours` | godziny pracy organizacji i oddziałów | do liczenia SLA |

**Kalendarz świąt jest niedoceniany.** Cut-off w piątek przed świętem oznacza
inną datę gotowości niż cut-off w zwykły piątek. Bez tego system liczy daty
błędnie kilka razy w roku, i to zwykle wtedy, kiedy najbardziej boli.

**Stawki VAT z regułami**, nie same procenty. Transport międzynarodowy ma
stawkę 0% pod warunkami dokumentacyjnymi — system musi wiedzieć, kiedy ją
zastosować i jakie dokumenty są wymagane.

---

# M-83 · Wprowadzanie i edycja ręczna

Twój drugi punkt. Automat jest świetny, ale musi istnieć droga obok niego.

## Pozycje ad-hoc

```sql
-- rozszerzenie quotation_line i shipment_charge
  is_ad_hoc bool,              -- pozycja spoza cennika
  ad_hoc_description text,     -- wolny tekst zamiast charge_code
  created_manually_by
```

Handlowiec musi móc dopisać pozycję, której nie ma w słowniku, bez czekania
na administratora. System proponuje potem dodanie jej jako stałego kodu.

## Szybkie dodanie kodu opłaty

Podczas wyceny, bez wychodzenia z ekranu: nazwa, podstawa naliczenia, strona.
Reszta atrybutów uzupełniana później. Nowy kod trafia do kolejki
„do uporządkowania" dla administratora.

## Ręczne stawki i opłaty

```sql
-- rate_line z source_type = 'manual' już to obsługuje
-- port_charge_rule z source = 'manual' też
```

Potrzebne są **ekrany**, nie tylko model: formularz stawki, formularz opłaty
portowej z podpowiedziami wymiarów warunkowych, edycja masowa.

## Szablony

```sql
quotation_template
  id, organization_id, name
  lane_pattern, mode
  lines jsonb,                 -- typowy zestaw pozycji
  markup_rule_override jsonb
  usage_count, created_by
```

Typowy zestaw pozycji dla relacji, którą obsługujesz co tydzień. Jedno
kliknięcie zamiast wypełniania dziesięciu wierszy.

## Kopiowanie

Duplikowanie oferty, zlecenia i kontrahenta jako punkt startowy.
Trywialne w implementacji, oszczędza godziny tygodniowo.

## Import z pliku

`data_import` z M-79 z mapowaniem kolumn i podglądem przed zatwierdzeniem.
Obowiązkowo dla: kontrahentów, stawek, portów własnych, kontaktów.

---

# M-84 · Wydruki i szablony dokumentów

```sql
document_layout
  id, organization_id, doc_type
  header jsonb,      -- logo, dane firmy, numer, data
  footer jsonb,      -- dane rejestrowe, rachunek, licencje, strona X z Y
  body_template,     -- typst
  terms_page bool,   -- warunki na osobnej stronie
  language, paper_size, margins jsonb
  show_qr bool,      -- link do śledzenia albo weryfikacji
  watermark          -- DRAFT | KOPIA | brak
  signature_asset_id, stamp_asset_id
  is_default
```

**Co musi być na każdym wydruku:**

```
Nagłówek:  logo · nazwa · numer dokumentu · data · ważność
Ciało:     pozycje · sumy · waluta z kursem · uwagi
Stopka:    dane rejestrowe (NIP, KRS, kapitał, sąd)
           rachunek bankowy właściwy dla waluty
           numer polisy OC spedytora
           odwołanie do warunków handlowych
           numeracja stron
           dane osoby wystawiającej + podpis
```

**Wielojęzyczność wydruków** to nie jest tłumaczenie interfejsu. Oferta dla
niemieckiego klienta ma być po niemiecku, łącznie z nazwami pozycji z
`charge_code.name_de`. Struktura `translation` z M-79 to obsługuje, ale
szablony muszą ją wykorzystywać od początku.

---

# M-85 · Praca z listami i danymi

Warstwa, która decyduje o codziennym odbiorze produktu.

| Funkcja | Uwaga |
|---|---|
| Konfigurowalne kolumny | użytkownik wybiera i porządkuje, zapis w `user_saved_view` |
| Zapisane filtry | nazwane, opcjonalnie współdzielone z zespołem |
| Eksport widoku do Excela | **z uwzględnieniem aktywnych filtrów**, nie całej tabeli |
| Operacje masowe | zmiana statusu, przypisanie operatora, dodanie znacznika |
| Wyszukiwarka globalna | jedno pole, wyniki pogrupowane po typie encji |
| Historia zmian dla użytkownika | czytelna, nie surowy audit log |
| Kosz i cofnięcie usunięcia | 30 dni, potem trwałe |
| Cofnij ostatnią operację | przynajmniej dla operacji masowych |
| Drukowanie listy | bo ktoś zawsze chce |

**Eksport z filtrami zamiast całej tabeli** to drobiazg, który odróżnia produkt
przemyślany od zbudowanego naprędce. Użytkownik widzi na ekranie dwadzieścia
wierszy i oczekuje dwudziestu w pliku.

---

# M-86 · Administracja i bezpieczeństwo konta

```sql
user_invitation
  id, organization_id, email, role_id
  token, expires_at, accepted_at, invited_by

user_session
  id, user_id, ip, user_agent, created_at, last_seen_at
  revoked_at

login_attempt
  id, email, ip, success, at, failure_reason

security_policy
  organization_id
  mfa_required bool
  password_min_length, password_expiry_days
  session_timeout_minutes
  allowed_ip_ranges cidr[]        -- opcjonalne, dla klientów korporacyjnych
```

Plus ekrany: lista użytkowników, zapraszanie mailem, dezaktywacja,
resetowanie hasła, uwierzytelnianie dwuskładnikowe, przegląd aktywnych sesji
z możliwością wylogowania zdalnego, historia logowań.

**Uwierzytelnianie dwuskładnikowe i ograniczenie adresów IP** to pozycje
z kwestionariuszy bezpieczeństwa, które dostaniesz od pierwszego większego
klienta. Taniej wbudować teraz niż dorabiać pod presją sprzedaży.

---

# M-87 · Windykacja miękka

Brakowało tego w module finansowym, a jest codziennością.

```sql
dunning_policy
  id, organization_id, name
  steps jsonb,     -- [{days_overdue: 3, action: reminder_soft},
                   --  {days_overdue: 14, action: reminder_firm},
                   --  {days_overdue: 30, action: notice_before_action},
                   --  {days_overdue: 45, action: block_new_bookings}]
  is_default

dunning_run
  id, invoice_id, step, sent_at, channel
  response, promised_payment_date

interest_note                    -- nota odsetkowa
  id, organization_id, party_id
  invoices uuid[], amount, rate_basis
  issued_at, paid_at
```

Automatyczne upomnienia według harmonogramu, z eskalacją i blokadą nowych
bookingów po przekroczeniu progu. Powiązane z limitem kredytowym z M-14.

---

# M-88 · Pomoc w produkcie

| Element | Uwaga |
|---|---|
| Podpowiedzi kontekstowe | przy polach nieoczywistych: `validity_basis`, W/M, incoterm |
| Przewodnik przy pierwszym uruchomieniu | powiązany z M-75 |
| Baza wiedzy | `mkdocs` osadzony w aplikacji |
| „Co nowego" | changelog widoczny w produkcie, powiązany z M-76 |
| Kontakt do wsparcia | z automatycznym kontekstem: tenant, ekran, wersja |
| Zgłoszenie błędu z ekranu | zrzut + logi + identyfikator sesji |

---

# PODSUMOWANIE ZMIAN

| Moduł | Nazwa | Faza | Nakład |
|---|---|---|---|
| M-80 | Ustawienia organizacji | 1 | 4 dni |
| M-81 | Ustawienia użytkownika | 1 | 3 dni |
| M-82 | Słowniki podstawowe | 1 | 4 dni |
| M-83 | Wprowadzanie ręczne | 2 | 5 dni |
| M-84 | Wydruki i szablony | 2 | 5 dni |
| M-85 | Praca z listami | 2 | 6 dni |
| M-86 | Administracja i bezpieczeństwo | 1 | 4 dni |
| M-87 | Windykacja miękka | 6 | 3 dni |
| M-88 | Pomoc w produkcie | 3 | 3 dni |

**Razem 37 dni roboczych.** Rejestr rośnie z 79 do 88 modułów.

## Umiejscowienie w harmonogramie

M-80, M-82 i M-86 **muszą wejść w fazie 1**, przed silnikiem wyceny.
Bez danych firmy, słownika opakowań i stawek VAT nie wystawisz oferty,
a bez zarządzania użytkownikami nie pokażesz systemu nikomu.

M-84 wchodzi razem z plastrem 2.9 (dokument oferty) — to jest ta sama praca.

M-83 i M-85 przed punktem kontrolnym po fazie 2. Demo bez konfigurowalnych
kolumn i eksportu do Excela wygląda na prototyp, a nie na produkt.

## Trzy rzeczy, których nikt nie przewiduje

**Kalendarz świąt per kraj.** Wpływa na wyliczanie cut-offów i terminów
płatności. Bez niego system myli daty kilka razy w roku.

**Zastępstwo na urlop.** Zapytania i zlecenia osoby nieobecnej muszą trafiać
do kogoś. Odkrywa się to w pierwszym lipcu po wdrożeniu.

**Numer polisy OC spedytora i AEO na dokumentach.** Pierwsza rzecz, o którą
pyta poważny klient. Trywialne pole, którego brak psuje wrażenie.
