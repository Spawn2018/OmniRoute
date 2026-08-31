# Analiza kompletności modelu i logiki

Przegląd wzdłuż dwóch osi: schemat bazy i logika obliczeniowa.
Dwadzieścia cztery braki, w większości przekrojowe.

---

# CZĘŚĆ I — WZORCE BAZODANOWE

## 1.1 Typy domenowe zamiast surowego tekstu

**Brak:** NIP, IBAN, UN/LOCODE, kod waluty i kod HS przechowujemy jako `text`.
Walidacja jest w aplikacji, więc dane wprowadzone migracją, importem albo
ręcznie przez SQL ją omijają.

```sql
CREATE DOMAIN nip AS text
    CHECK (VALUE ~ '^[0-9]{10}$');

CREATE DOMAIN iban AS text
    CHECK (VALUE ~ '^[A-Z]{2}[0-9]{2}[A-Z0-9]{11,30}$');

CREATE DOMAIN unlocode AS char(5)
    CHECK (VALUE ~ '^[A-Z]{2}[A-Z2-9]{3}$');

CREATE DOMAIN currency_code AS char(3)
    CHECK (VALUE ~ '^[A-Z]{3}$');

CREATE DOMAIN hs_code AS text
    CHECK (VALUE ~ '^[0-9]{6,10}$');

CREATE DOMAIN un_number AS char(4)
    CHECK (VALUE ~ '^[0-9]{4}$');

CREATE DOMAIN container_number AS char(11)
    CHECK (VALUE ~ '^[A-Z]{4}[0-9]{7}$');

CREATE DOMAIN percentage AS numeric(7,4)
    CHECK (VALUE >= -100 AND VALUE <= 1000);

CREATE DOMAIN money_amount AS numeric(14,4);
```

**Zysk:** niepoprawna dana nie wejdzie do bazy żadną drogą. Domena kontenera
łapie literówkę w numerze, zanim trafi do zgłoszenia celnego.

## 1.2 Klucze główne — rozstrzygnięcie

**Brak:** używamy `gen_random_uuid()`, czyli wersji czwartej. Aneks 18
rekomendował wersję siódmą, ale nigdzie tego nie wymusiliśmy.

```sql
CREATE EXTENSION IF NOT EXISTS pg_uuidv7;

-- wszystkie klucze główne
id uuid PRIMARY KEY DEFAULT uuid_generate_v7()
```

**Dlaczego to ma znaczenie:** identyfikator siódmej wersji jest sortowalny
czasowo. Wstawianie do indeksu odbywa się na końcu drzewa zamiast losowo,
co przy tabelach zdarzeniowych rosnących o miliony wierszy daje zauważalną
różnicę w rozdrobnieniu indeksu i wydajności zapisu.

**Klucze naturalne zostawiamy tam, gdzie są stabilne:** `port.unlocode`,
`currency.code`, `country.code`, `charge_code.code` w obrębie organizacji.

## 1.3 Indeksy prowadzone identyfikatorem tenanta

**Brak:** polityki RLS filtrują po `organization_id`, ale nie wszystkie
indeksy zaczynają się od tej kolumny. Planer wtedy skanuje więcej, niż musi.

**Zasada:** każdy indeks na tabeli z RLS zaczyna się od `organization_id`.

```sql
-- źle
CREATE INDEX ix_rate_lane ON rate_line (pol, pod, mode);

-- dobrze
CREATE INDEX ix_rate_lane ON rate_line (organization_id, pol, pod, mode);
```

Do sprawdzenia testem architektonicznym:

```sql
SELECT tablename, indexname
FROM pg_indexes i
JOIN pg_tables t USING (tablename)
WHERE t.rowsecurity
  AND indexdef NOT LIKE '%(organization_id%'
  AND indexname NOT LIKE '%_pkey';
```

## 1.4 Kolumny generowane

**Brak:** marża, kwoty netto i wagi obliczeniowe liczymy w aplikacji
i zapisujemy. Rozjazd między kolumnami jest wtedy możliwy.

```sql
ALTER TABLE quotation_line
    ADD COLUMN margin_amount money_amount
        GENERATED ALWAYS AS (sell_amount - buy_amount) STORED,
    ADD COLUMN margin_pct percentage
        GENERATED ALWAYS AS (
            CASE WHEN sell_amount = 0 THEN 0
                 ELSE (sell_amount - buy_amount) / sell_amount * 100
            END
        ) STORED;

ALTER TABLE invoice_line
    ADD COLUMN gross_amount money_amount
        GENERATED ALWAYS AS (net_amount + vat_amount) STORED;
```

**Zysk:** marża nie może być niespójna z kwotami, bo nie jest osobno zapisywana.

## 1.5 Ograniczenia wykluczające — zapobieganie kolizjom stawek

**Brak najpoważniejszy w tej części.** Wykrywanie nachodzących okresów
ważności stawek opisaliśmy jako logikę aplikacji. Baza może to wymusić.

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;

ALTER TABLE rate_line
    ADD COLUMN validity daterange
        GENERATED ALWAYS AS (daterange(valid_from, valid_to, '[]')) STORED;

ALTER TABLE rate_line ADD CONSTRAINT no_overlapping_rates
    EXCLUDE USING gist (
        organization_id WITH =,
        source_party_id WITH =,
        pol WITH =,
        pod WITH =,
        mode WITH =,
        charge_code WITH =,
        COALESCE(container_type, '') WITH =,
        validity WITH &&
    ) WHERE (superseded_by IS NULL AND deleted_at IS NULL);
```

**Zysk:** dwie stawki tego samego dostawcy na tę samą relację i opłatę
z nachodzącymi okresami są niemożliwe do zapisania. Kolizja wykrywana
przy wstawianiu, a nie przy wycenie.

To samo dla `port_charge_rule`, `customer_tariff_line`, `markup_rule`
i `contract`.

## 1.6 Indeksy częściowe unikalne

**Brak:** przypadki „tylko jeden aktywny" egzekwujemy w aplikacji.

```sql
-- jeden domyślny rachunek na walutę
CREATE UNIQUE INDEX ux_default_bank_per_currency
    ON organization_bank_account (organization_id, currency)
    WHERE is_default_for_currency AND deleted_at IS NULL;

-- jedna aktywna wersja cennika klienta
CREATE UNIQUE INDEX ux_active_tariff
    ON customer_tariff (organization_id, customer_party_id)
    WHERE status = 'active';

-- jeden otwarty tranzyt na odcinek
CREATE UNIQUE INDEX ux_open_transit
    ON shipment_leg_rail (leg_id)
    WHERE t1_expires_at IS NOT NULL AND import_declaration_id IS NULL;

-- jedna oferta wcześniejszej zapłaty na fakturę
CREATE UNIQUE INDEX ux_open_early_payment
    ON early_payment_offer (bill_id)
    WHERE status IN ('offered', 'accepted');
```

## 1.7 Ograniczenia biznesowe w bazie

**Brak:** niezmienniki domenowe sprawdzamy wyłącznie w aplikacji.

```sql
-- daty
ALTER TABLE rate_line ADD CONSTRAINT chk_validity_order
    CHECK (valid_to IS NULL OR valid_from <= valid_to);

ALTER TABLE shipment_leg ADD CONSTRAINT chk_leg_dates
    CHECK (planned_arrival IS NULL OR planned_departure IS NULL
           OR planned_departure <= planned_arrival);

-- kwoty
ALTER TABLE quotation_line ADD CONSTRAINT chk_amounts_non_negative
    CHECK (buy_amount >= 0 AND sell_amount >= 0);

ALTER TABLE early_payment_offer ADD CONSTRAINT chk_discount_logic
    CHECK (net_amount = original_amount - discount_amount
           AND discount_amount >= 0
           AND offered_payment_date < original_due_date);

-- waluta zawsze z kwotą
ALTER TABLE shipment_charge ADD CONSTRAINT chk_currency_pairs
    CHECK ((buy_amount IS NULL) = (buy_currency IS NULL)
       AND (sell_amount IS NULL) = (sell_currency IS NULL));

-- opłata należy do odcinka albo do zlecenia, nigdy do obu naraz
ALTER TABLE shipment_charge ADD CONSTRAINT chk_charge_scope
    CHECK (leg_id IS NOT NULL OR is_shipment_level);

-- ciągłość odcinków
CREATE FUNCTION check_leg_continuity() RETURNS trigger AS $$
DECLARE prev_dest uuid;
BEGIN
    SELECT destination_location_id INTO prev_dest
    FROM shipment_leg
    WHERE shipment_id = NEW.shipment_id
      AND sequence = NEW.sequence - 1
      AND deleted_at IS NULL;

    IF prev_dest IS NOT NULL AND prev_dest <> NEW.origin_location_id THEN
        RAISE EXCEPTION
            'Odcinek % zaczyna się w innym miejscu niż kończy poprzedni',
            NEW.sequence;
    END IF;
    RETURN NEW;
END $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_leg_continuity
    BEFORE INSERT OR UPDATE ON shipment_leg
    FOR EACH ROW EXECUTE FUNCTION check_leg_continuity();
```

**Ciągłość odcinków jest istotna:** zlecenie z dowozem kończącym się w Gdyni
i frachtem zaczynającym się w Gdańsku to błąd, który bez tego wyzwalacza
wyjdzie dopiero przy bookingu.

## 1.8 Ograniczenia odroczone

**Brak:** operacje wieloetapowe wymagają chwilowej niespójności.

```sql
ALTER TABLE shipment_leg
    ADD CONSTRAINT uq_leg_sequence UNIQUE (shipment_id, sequence)
    DEFERRABLE INITIALLY IMMEDIATE;

-- przy przenumerowaniu odcinków
BEGIN;
SET CONSTRAINTS uq_leg_sequence DEFERRED;
UPDATE shipment_leg SET sequence = sequence + 1 WHERE ...;
COMMIT;
```

## 1.9 Strategia partycjonowania — ujednolicona

**Brak:** partycjonowanie wspomnieliśmy przy trzech tabelach, bez zasady.

| Tabela | Klucz | Okres | Retencja |
|---|---|---|---|
| `audit_log` | `at` | miesiąc | 24 mies., potem anonimizacja |
| `shipment_event` | `event_datetime` | kwartał | bezterminowo |
| `rail_event` | `occurred_at` | kwartał | bezterminowo |
| `inbound_message` | `received_at` | miesiąc | 12 mies. |
| `decision_log` | `decided_at` | miesiąc | 24 mies. |
| `bank_transaction` | `booking_date` | rok | 5 lat |
| `integration_run` | `started_at` | miesiąc | 6 mies. |
| `kpi_measurement` | `period` | rok | bezterminowo |
| `request_replay` | `captured_at` | tydzień | 30 dni |

```sql
-- automatyczne tworzenie i odłączanie partycji
CREATE EXTENSION IF NOT EXISTS pg_partman;
```

## 1.10 Archiwizacja

**Brak całkowity.** Tabele rosną, nic ich nie odchudza.

```sql
CREATE SCHEMA archive;

CREATE TABLE archive.shipment (LIKE public.shipment INCLUDING ALL);

CREATE FUNCTION archive_closed_shipments(older_than interval)
RETURNS integer AS $$
DECLARE moved integer;
BEGIN
    WITH m AS (
        DELETE FROM public.shipment
        WHERE status = 'closed'
          AND updated_at < now() - older_than
          AND NOT EXISTS (SELECT 1 FROM legal_hold
                          WHERE entity_type = 'shipment' AND entity_id = shipment.id
                            AND released_at IS NULL)
        RETURNING *
    )
    INSERT INTO archive.shipment SELECT * FROM m;
    GET DIAGNOSTICS moved = ROW_COUNT;
    RETURN moved;
END $$ LANGUAGE plpgsql;
```

**Blokada z tytułu sporu wstrzymuje archiwizację** — to samo, co przy retencji.

## 1.11 Sumowanie kwot w różnych walutach

**Brak:** agregaty po `shipment_charge` sumują kwoty bez sprawdzenia waluty.
Suma dolarów i złotych jest liczbą bez znaczenia.

```sql
CREATE TYPE money_multi AS (amounts jsonb);   -- {"USD": 1200, "PLN": 4300}

CREATE AGGREGATE sum_by_currency(money_amount, currency_code) (
    SFUNC = money_multi_add,
    STYPE = money_multi,
    INITCOND = '("{}")'
);
```

**Zasada:** agregat zwraca rozbicie na waluty **albo** kwotę przeliczoną
z jawnie podanym kursem i datą. Nigdy gołą sumę.

## 1.12 Wersjonowanie systemowe wybranych tabel

**Brak:** `sqlalchemy-continuum` daje historię encji, ale nie pozwala
zapytać „jak wyglądał cennik 14 sierpnia".

```sql
-- dla tabel, gdzie potrzebna jest odpowiedź na pytanie o stan w przeszłości
ALTER TABLE markup_rule
    ADD COLUMN sys_period tstzrange NOT NULL
        DEFAULT tstzrange(now(), NULL);

CREATE TABLE markup_rule_history (LIKE markup_rule);

CREATE TRIGGER versioning_trigger
    BEFORE INSERT OR UPDATE OR DELETE ON markup_rule
    FOR EACH ROW EXECUTE PROCEDURE
    versioning('sys_period', 'markup_rule_history', true);
```

**Zakres:** `markup_rule`, `charge_code`, `port_charge_rule`,
`customer_tariff_line`, `payment_term_profile`, `cost_of_capital_config`.

To są tabele, których stan w przeszłości trzeba odtworzyć przy sporze
o wysokość wystawionej oferty.
---

# CZĘŚĆ II — BIBLIOTEKA DOMENOWA

## 2.1 Problem

**Największy brak logiczny w całym projekcie.** Obliczenia są rozproszone:
kaskada narzutów w module wyceny, przeliczenia walutowe w kilku miejscach,
waga obliczeniowa osobno dla morza, drogi i kolei, zaokrąglenia wszędzie
inaczej.

Skutek przy 212 modułach: dwie funkcje liczące marżę różnią się o grosz,
a raport nie zgadza się z fakturą.

## 2.2 Rozwiązanie: jeden pakiet obliczeniowy

```
backend/app/domain/calc/
├── money.py            typ Money, arytmetyka, zaokrąglenia
├── currency.py         przeliczenia, kursy, spread
├── weight.py           waga obliczeniowa per gałąź
├── markup.py           kaskada narzutów, narzut kontra marża
├── financing.py        koszt kapitału, dyskonto, stopa efektywna
├── allocation.py       alokacja kosztu: shared, capacity, marginal
├── validity.py         ważność stawki wg validity_basis
├── dates.py            kalendarz roboczy, cut-offy, strefy
└── rounding.py         reguły zaokrągleń per waluta i kontekst
```

**Zasada bezwzględna:** żaden moduł nie liczy sam. Każde obliczenie
domenowe przechodzi przez ten pakiet. Egzekwowane kontraktem `import-linter`.

```ini
[importlinter:contract:obliczenia]
name = Obliczenia tylko przez domain.calc
type = forbidden
source_modules = app.services, app.api, app.repositories
forbidden_modules = decimal
# Decimal wolno importować wyłącznie w app.domain.calc
```

## 2.3 Reguły zaokrągleń — nigdzie nieustalone

**Brak:** nie zdefiniowaliśmy, kiedy zaokrąglamy.

```python
class RoundingPolicy:
    """Kolejność ma znaczenie i musi być jedna w całym systemie."""

    # 1. Przeliczenie waluty: pełna precyzja, bez zaokrąglenia
    # 2. Narzut na pozycji: zaokrąglenie do miejsc waluty docelowej
    # 3. Suma pozycji: suma zaokrąglonych, nie zaokrąglenie sumy
    # 4. Podatek: liczony od sumy zaokrąglonej
    # 5. Prezentacja: bez dalszego zaokrąglania

    MODE = ROUND_HALF_UP        # księgowo, nie bankowo
```

**Punkt trzeci jest źródłem najczęstszych rozbieżności groszowych.**
Suma zaokrąglonych pozycji i zaokrąglona suma różnią się — trzeba wybrać
jedno i trzymać się wszędzie, łącznie z fakturą i raportem.

Liczba miejsc z tabeli `currency`, nigdy na sztywno.

## 2.4 Kalendarz roboczy — brak całkowity

**Brak:** „termin płatności 30 dni" — kalendarzowych czy roboczych?
Święta którego kraju? Cut-off w piątek przed świętem?

```sql
business_calendar
  id, organization_id NULL, country_code, region NULL
  name, is_default

business_calendar_day
  calendar_id, date, day_type,   -- workday | weekend | holiday | half_day
  name, is_banking_day, is_customs_day, is_terminal_day
```

```python
def add_business_days(start, days, calendar, kind='banking'): ...
def is_working_day(date, calendar, kind): ...
def next_working_day(date, calendar, kind): ...
```

**Trzy różne kalendarze na tej samej dacie:** bank może być otwarty,
urząd celny zamknięty, terminal pracować. Bez tego rozróżnienia terminy
liczą się źle kilka razy w roku.

## 2.5 Strefy czasowe w regułach biznesowych

**Brak:** cut-off zapisujemy jako `timestamptz`, ale nie ustaliliśmy,
w czyjej strefie użytkownik go widzi i w czyjej działa reguła.

**Zasada:** cut-off obowiązuje w strefie **lokalizacji, której dotyczy**.
Cut-off bramowy w Gdyni to strefa Gdyni, niezależnie od tego, gdzie siedzi
operator.

```python
def cutoff_local(cutoff_utc, location) -> datetime:
    return cutoff_utc.astimezone(location.timezone)
```

Stąd `port.timezone` i `terminal.timezone` jako pola obowiązkowe.
Interfejs pokazuje obie: lokalną i użytkownika.

## 2.6 Tolerancje

**Brak:** „kwota dokładna" przy dopasowaniu płatności nie istnieje —
są różnice kursowe, prowizje bankowe i zaokrąglenia.

```sql
matching_tolerance
  organization_id
  context,             -- payment_match | invoice_reconcile | weight_check
  absolute_value, absolute_currency,
  relative_pct,
  rule                 -- lesser | greater | either
```

| Kontekst | Tolerancja domyślna |
|---|---|
| Dopasowanie płatności | 0,5% albo 10 zł, mniejsza z nich |
| Rozliczenie faktury z wyceną | 2% albo 50 zł |
| Waga zadeklarowana wobec VGM | 5% albo 100 kg |
| Objętość wobec deklaracji | 5% |

Bez tego dopasowanie automatyczne nie zadziała nigdy albo zadziała błędnie.

## 2.7 Źródło prawdy przy konflikcie danych

**Brak:** waga występuje w pięciu miejscach i bywa różna.

```sql
data_source_priority
  organization_id, field_name, source_type, priority, notes
```

| Pole | Kolejność wiarygodności |
|---|---|
| Waga brutto | VGM → ważenie terminalu → packing list → deklaracja klienta |
| Objętość | pomiar CFS → packing list → deklaracja |
| Kod HS | zgłoszenie celne → faktura → deklaracja |
| Wartość towaru | faktura handlowa → deklaracja |
| Opłata portowa | faktura → API armatora → taryfa → oferta agenta |
| Termin płatności | rzeczywisty DSO → umowa → kontrahent |

**Konflikt nie jest błędem, jest informacją.** System pokazuje rozbieżność,
używa źródła o wyższym priorytecie i zapisuje pozostałe.

## 2.8 Uprawnienia na poziomie pola

**Brak:** mamy `cost_visibility` jako przypadek szczególny. Nie ma mechanizmu
ogólnego.

```sql
field_permission
  role_id, entity_type, field_name
  access,              -- read | write | hidden | masked
  mask_pattern         -- np. ostatnie cztery znaki rachunku
```

Zastosowania poza kosztami: numery rachunków bankowych, dane osobowe
kierowców, warunki umów z agentami, poświadczenia integracji,
kwoty prowizji handlowców.

**Egzekwowane w serializacji DTO**, nie w interfejsie. Pole ukryte nie jest
wysyłane, a nie tylko niewyświetlane.

---

# CZĘŚĆ III — BRAKI LOGICZNE

## 3.1 Kompensacja procesów wieloetapowych

**Brak:** opisaliśmy kompensację tylko przy Temporalu, bez katalogu.

| Operacja | Kompensacja |
|---|---|
| Booking u armatora | anulowanie, powiadomienie, ewentualna opłata |
| Zgłoszenie celne | wniosek o unieważnienie |
| Zlecenie do przewoźnika | odwołanie, rozliczenie kosztu podstawienia |
| Wysłanie faktury do KSeF | faktura korygująca, nie usunięcie |
| Płatność zlecona | odwołanie, jeśli nieodebrana; inaczej zwrot |
| Rezerwacja miejsca na pociągu | zwolnienie, opłata za późne anulowanie |
| Wcześniejsza zapłata podwykonawcy | brak — operacja nieodwracalna |

**Ostatni wiersz jest ważny.** Operacje nieodwracalne wymagają zatwierdzenia
przed wykonaniem, nie kompensacji po.

## 3.2 Walidacja krzyżowa

**Brak:** sprawdzamy pola osobno, nie ich wzajemną zgodność.

```python
CROSS_RULES = [
    # incoterm a zakres opłat
    ("incoterm_charge_scope",
     "DDP wymaga pozycji odprawy importowej i odwozu"),
    # gałąź a typ kontenera
    ("mode_container_match",
     "45HC nie występuje w transporcie morskim"),
    # ADR a trasa
    ("dg_route_acceptance",
     "klasa 5.1 nieakceptowana przez wybrany serwis kolejowy"),
    # waga a typ kontenera
    ("weight_payload_limit",
     "waga przekracza ładowność 20DV"),
    # daty a odcinki
    ("leg_date_continuity",
     "odcinek 2 zaczyna się przed zakończeniem odcinka 1"),
    # incoterm a strona płacąca
    ("freight_payment_incoterm",
     "przy EXW fracht nie może być prepaid po naszej stronie"),
    # kraj a wymagane zgłoszenia
    ("country_filing_required",
     "relacja do USA wymaga ISF i AMS"),
    # waluta a kontrahent
    ("currency_party_match",
     "kontrahent nie akceptuje rozliczeń w tej walucie"),
]
```

Uruchamiane przed wysłaniem oferty i przed bookingiem. Wynik do
`quotation_gap` z typem `validation`.

## 3.3 Stany pośrednie i wycofanie

**Brak:** maszyny stanów opisują ścieżkę pozytywną. Brakuje ścieżek powrotu.

```
BOOKED ──▶ [ANULOWANIE ZAŻĄDANE] ──▶ [ANULOWANE]
                  │
                  └──▶ [ANULOWANIE ODRZUCONE] ──▶ BOOKED

IN_TRANSIT ──▶ [ZAWRÓCONE] ──▶ [ZWRÓCONE DO NADAWCY]

DELIVERED ──▶ [REKLAMACJA] ──▶ [W SPORZE] ──▶ [ZAMKNIĘTE]
```

Każde zlecenie musi mieć ścieżkę zamknięcia bez realizacji, z rozliczeniem
poniesionych kosztów.

## 3.4 Idempotencja odczytów zewnętrznych

**Brak:** idempotencję zdefiniowaliśmy dla zapisów. Odczyty też jej wymagają.

Zapytanie o stawkę spot wykonane dwa razy w ciągu minuty nie powinno zużyć
dwóch wywołań limitu ani zwrócić dwóch różnych cen w tej samej wycenie.

```sql
external_call_cache
  cache_key text PRIMARY KEY,   -- hash: adapter + parametry
  organization_id, adapter,
  response jsonb, fetched_at, expires_at,
  hit_count
```

## 3.5 Kolejność stosowania reguł

**Brak:** mamy kaskady w kilku miejscach, każda z inną logiką rozstrzygania.

**Ujednolicenie:** wszędzie ta sama zasada — wygrywa reguła o najwyższej
specyficzności, przy remisie nowsza, przy dalszym remisie pytanie do człowieka.

```python
def resolve_rule(candidates, context):
    scored = [(specificity(r, context), r.effective_from, r) for r in candidates]
    scored.sort(reverse=True)
    if len(scored) > 1 and scored[0][:2] == scored[1][:2]:
        raise AmbiguousRuleError(scored[0][2], scored[1][2])
    return scored[0][2]
```

Dotyczy: `markup_rule`, `port_charge_rule`, `document_requirement`,
`approval_policy`, `margin_rule`, `field_permission`.

## 3.6 Jednostki miary i przeliczniki

**Brak:** przeliczniki rozproszone.

```sql
unit_conversion
  from_unit, to_unit, factor, context NULL
  -- kg → t: 0.001
  -- cbm → ldm: zależne od typu pojazdu, stąd context
  -- teu: 20DV=1, 40DV=2, 40HC=2, 45HC=2.25
```

**LDM zależy od kontekstu.** Przelicznik metra ładunkowego na objętość
zależy od wysokości przestrzeni ładunkowej pojazdu — dlatego nie jest stałą.

---

# CZĘŚĆ IV — PLAN UZUPEŁNIENIA

| Grupa | Zakres | Dni | Kiedy |
|---|---|---|---|
| **Typy domenowe i klucze v7** | §1.1, 1.2 | 2 | **plaster 0.3, przed pierwszą tabelą** |
| **Biblioteka `domain/calc`** | §2.1–2.3, 2.6 | 6 | **plaster 0.5, przed silnikiem wyceny** |
| Kalendarz roboczy | §2.4 | 3 | plaster 1.4 |
| Strefy czasowe w regułach | §2.5 | 2 | plaster 1.1 |
| Ograniczenia wykluczające | §1.5 | 2 | plaster 2.1 |
| Ograniczenia biznesowe i wyzwalacze | §1.7, 1.8 | 3 | wraz z tabelami |
| Kolumny generowane | §1.4 | 1 | wraz z tabelami |
| Indeksy prowadzone tenantem + test | §1.3 | 2 | plaster 0.7 |
| Źródło prawdy przy konflikcie | §2.7 | 2 | plaster 6.1 |
| Uprawnienia na poziomie pola | §2.8 | 3 | plaster 0.8 |
| Walidacja krzyżowa | §3.2 | 4 | plaster 2.5 |
| Kompensacja i ścieżki powrotu | §3.1, 3.3 | 4 | plaster 6.2 |
| Cache wywołań zewnętrznych | §3.4 | 2 | plaster 7.7 |
| Ujednolicenie kaskad | §3.5 | 2 | plaster 2.6 |
| Jednostki i przeliczniki | §3.6 | 2 | plaster 1.3 |
| Partycjonowanie i archiwizacja | §1.9, 1.10 | 4 | plaster 0.14 |
| Wersjonowanie systemowe | §1.12 | 2 | plaster 2.6 |
| Sumowanie wielowalutowe | §1.11 | 2 | plaster 1.4 |

**Razem 48 dni.**

## Cztery pozycje, które muszą wejść przed jakimkolwiek kodem domenowym

**① Typy domenowe i klucze siódmej wersji** — plaster 0.3. Zmiana typu
kolumny w stu trzydziestu tabelach po fakcie to migracja na godziny
z blokadą zapisu.

**② Biblioteka `domain/calc`** — plaster 0.5. Jeśli pierwsze obliczenie
powstanie poza nią, powstanie ich sto poza nią.

**③ Reguły zaokrągleń** — część biblioteki. Ustalone raz, egzekwowane
wszędzie. Rozbieżność groszowa między raportem a fakturą to najczęstsze
zgłoszenie w systemach finansowych.

**④ Indeksy prowadzone identyfikatorem tenanta z testem** — plaster 0.7.
Test wykrywa naruszenie automatycznie, więc nie trzeba tego pamiętać przy
każdej kolejnej tabeli.

## Trzy najważniejsze zyski

**Ograniczenie wykluczające na stawkach** przenosi wykrywanie kolizji
z aplikacji do bazy. Nachodzące okresy ważności stają się niemożliwe,
a nie tylko wykrywane.

**Biblioteka obliczeniowa** eliminuje rozbieżności między modułami.
Przy 212 modułach to jest różnica między systemem spójnym a takim,
w którym każdy raport pokazuje inną marżę.

**Kalendarz roboczy z trzema rodzajami dni** naprawia klasę błędów
terminowych, które ujawniają się kilka razy w roku i zawsze w najgorszym
momencie.
