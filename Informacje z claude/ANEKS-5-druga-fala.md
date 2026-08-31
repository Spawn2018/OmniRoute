# Aneks 5 — Druga fala

Moduły dla spedycji dojrzałej. Nic z tego nie buduje się w pierwszym roku, ale model danych powinien je przewidzieć, żeby dało się je dołożyć bez migracji.

---

## 1. Zarządzanie przetargami

Duzi załadowcy kontraktują przez przetargi na platformach. Po stronie spedytora cały proces żyje w Excelu, a straty biorą się z pomyłek arytmetycznych i przegapionych terminów, nie z niekonkurencyjności.

To jest moduł, którego nie ma w segmencie MŚP w ogóle — a ty znasz ten proces od środka.

```sql
tender
  id, organization_id
  buyer_party_id, platform,        -- transporeon | ticontract | mail | inny
  reference, title
  published_at, questions_due_at, bid_due_at
  contract_from, contract_to
  currency, incoterm_scope
  volume_basis,                    -- deklarowany wolumen roczny
  status,                          -- watching|preparing|submitted|won|lost
  award_share_pct                  -- jaki udział przyznano

tender_lane
  id, tender_id
  pol, pod, mode, container_type
  annual_volume, seasonality jsonb
  required_transit_days, service_requirements jsonb
  incumbent_price NULL,            -- jeśli znane

tender_bid_line
  id, tender_lane_id
  cost_build jsonb,                -- rozbicie kosztu zakupu
  buy_source_id,                   -- z której stawki/oferty agenta
  bid_price, margin_pct
  win_probability,                 -- z historii (Aneks 3)
  is_submitted, submitted_at

tender_outcome
  tender_id, lane_id, result,      -- won|lost|no_award
  winning_price NULL, our_rank NULL
  feedback_text
```

**Funkcje, które robią różnicę:**

- **Budowa oferty z żywej bazy stawek**, nie z przepisanego Excela. Zmiana stawki zakupowej przelicza cały przetarg
- **Kalendarz terminów** z automatycznym przypomnieniem — pytania, oferta wstępna, runda negocjacyjna
- **Analiza wrażliwości**: przy jakiej marży wygrywasz ile relacji, i ile to daje łącznie
- **Ryzyko zobowiązania**: przetarg to deklaracja stawki na 12 miesięcy. Moduł rynkowy z Aneksu 2 wylicza ryzyko, że koszt wzrośnie w tym okresie
- **Historia przetargowa**: przegrywasz systematycznie na relacjach azjatyckich o 6% — to jest wiedza, której dziś nikt nie zbiera

## 2. Kontrakty indeksowane

Coraz więcej kontraktów wiąże cenę z indeksem zamiast ustalać kwotę. Systemy MŚP tego nie obsługują w ogóle.

```sql
contract
  id, party_id, contract_number
  valid_from, valid_to
  pricing_mode,                    -- fixed | index_linked | hybrid
  index_code,                      -- WCI_SHA_RTM, SCFI_COMP
  index_baseline, index_multiplier
  floor_price, ceiling_price,      -- korytarz
  adjustment_frequency,            -- weekly | monthly | quarterly
  mqc_volume,                      -- minimalne zobowiązanie ilościowe
  escalation_clauses jsonb         -- BAF, ETS, GRI: kto ponosi

contract_adjustment               -- historia przeliczeń
  id, contract_id, effective_from
  index_value, computed_price, applied_by
```

Cena przelicza się sama przy publikacji indeksu, w granicach korytarza. Klient dostaje powiadomienie z podstawą wyliczenia. To jest funkcja, po której duży załadowca traktuje cię jak partnera, a nie jak małego pośrednika.

## 3. Alokacja i zobowiązania ilościowe

Kontrakt z armatorem zawiera minimalne zobowiązanie. Niewykorzystanie kosztuje, przekroczenie oznacza brak miejsca.

```sql
allocation
  id, contract_id, pol, pod, period
  committed_teu, used_teu, booked_teu
  utilization_pct, penalty_risk
```

Ekran pokazujący na bieżąco: gdzie jesteś poniżej zobowiązania i ile zostało czasu. Przy wycenie system podpowiada armatora, u którego masz niewykorzystaną alokację — decyzja, która dziś zapada z pamięci albo wcale.

## 4. Ekspozycja walutowa

Kupujesz w dolarach, sprzedajesz w złotych, płacisz za 45 dni. Między wyceną a płatnością kurs się zmienia i zjada marżę, o czym dowiadujesz się po fakcie.

```sql
fx_exposure                       -- widok, nie tabela
  organization_id, currency
  open_quotes_amount,             -- oferty wysłane, jeszcze nieprzyjęte
  booked_unpaid_amount,           -- zlecenia bez rozliczenia
  net_exposure, avg_locked_rate, current_rate
  unrealized_delta
```

Raport „masz otwartą ekspozycję 340 tys. USD, osłabienie złotego o 3% kosztuje cię 41 tys. zł". Dla spedytora rozliczającego się w złotych to jest realna pozycja wynikowa, której nikt nie mierzy.

## 5. Koszt obsługi klienta

Marża brutto kłamie. Klient z 14% marży, który generuje czterdzieści maili na zlecenie i trzy korekty dokumentów, bywa mniej opłacalny niż ten z 8% i zerową obsługą.

```sql
cost_to_serve
  party_id, period
  shipments_count
  operator_minutes,               -- z aktywności w systemie
  emails_handled, document_corrections
  exceptions_count, claims_count
  allocated_overhead, true_margin_pct
```

Dane zbierają się same z aktywności w systemie. Efekt: lista klientów posortowana po **rzeczywistej** rentowności, z których część zaskoczy właściciela. To jest raport, który uzasadnia zakup przed zarządem.

## 6. Procedury operacyjne per klient

Duzi spedytorzy mają SOP dla każdego klienta. Mali trzymają je w głowach dwóch osób, co jest ryzykiem przy urlopie i katastrofą przy odejściu.

```sql
customer_sop
  id, party_id, version
  rules jsonb,                    -- wymagane dokumenty, terminy, odbiorcy
                                  -- specjalne instrukcje, zakazy
  auto_tasks jsonb,               -- zadania generowane przy zleceniu
  approved_by, effective_from
```

SOP nie jest dokumentem do przeczytania — **generuje zadania i walidacje**. Nowy pracownik obsługuje klienta poprawnie od pierwszego dnia, bo system pilnuje reguł zamiast pamięci kolegi.

## 7. Ochrona przed oszustwem płatniczym

Spedycja jest jednym z najczęściej atakowanych sektorów. Schemat: podszycie się pod agenta, mail o zmianie rachunku bankowego, przelew trafia do przestępcy. Kwoty są duże, bo faktury frachtowe są duże.

Zabezpieczenia, które da się zautomatyzować:

- **zmiana rachunku kontrahenta wymaga potwierdzenia innym kanałem** — blokada w systemie, nie procedura na papierze
- **weryfikacja na białej liście VAT** przed każdą płatnością, nie tylko przy zakładaniu
- **wykrywanie podobnych domen** — mail z `agent-shipping.com` zamiast `agentshipping.com`
- **próg kwotowy z zasadą dwóch par oczu**
- **alert przy pierwszej płatności na nowy rachunek**

Żaden system spedycyjny w tym segmencie tego nie ma, a jedno udaremnione oszustwo zwraca kilkuletni abonament.

## 8. Konsolidacja drobnicy morskiej

Odpowiednik twojego silnika alokacji z Aneksu 1, ale dla morza.

```sql
consolidation
  id, container_type, pol, pod
  cutoff_at, sailing_id
  capacity_cbm, capacity_kg
  used_cbm, used_kg, fill_rate
  break_even_fill,                -- próg opłacalności
  cost_total, allocation_mode

consolidation_item
  consolidation_id, shipment_id
  cbm, weight_kg, chargeable_wm, allocated_cost
```

Pytanie operacyjne: „mam kontener w 60%, cut-off za trzy dni — przyjąć tę przesyłkę poniżej cennika czy czekać?". To jest ta sama matematyka kosztu krańcowego co przy doładunku drogowym. Silnik masz, wystarczy podpiąć inne wejście.

## 9. Kompensata rozrachunków z agentami

Z agentem masz zwykle dwustronne rozliczenia — coś jemu, coś tobie. Zestawienie kompensacyjne zamiast przelewów w obie strony:

```sql
netting_statement
  id, party_id, period
  receivables_total, payables_total, net_amount, currency
  status,                         -- draft|sent|agreed|settled
  disputed_items jsonb
```

Mniej przelewów, mniejsza ekspozycja walutowa, mniej pracy księgowej. Standard w dużych sieciach agencyjnych, nieobecny w małych.

---

## Jak to wpiąć bez przepisywania

Żaden z tych modułów nie wymaga zmiany rdzenia — pod warunkiem, że **teraz** przewidzisz cztery rzeczy:

1. **`contract` jako encja** obok `party` — nawet pusta. Kontrakty klientów i armatorów zawiesza się na niej później
2. **`period` jako wymiar** w metrykach — cost-to-serve, alokacja i ekspozycja liczą się okresami
3. **Aktywność użytkownika logowana od początku** — bez tego cost-to-serve nie ma z czego powstać, a danych wstecz nie odtworzysz
4. **`consolidation` i `tour` jako rodzeństwo** — jedno pojęcie „jednostki transportowej dzielonej między przesyłki", dwie implementacje. Wtedy silnik alokacji obsłuży oba

Cztery decyzje, kilka dni pracy w tygodniach 1–2. Bez nich każdy z tych modułów oznacza migrację.

---

## Które trzy warto mieć na radarze najwcześniej

**Przetargi** — bo znasz ten proces lepiej niż ktokolwiek, kogo mógłbyś zatrudnić, i bo to jest moduł, którego naprawdę nie ma. Do tego zbiera dane, na których uczy się reszta systemu.

**Ochrona przed oszustwem** — bo jest tania, a jedno zdarzenie u klienta zmienia was z dostawcy oprogramowania w partnera, któremu zawdzięcza pieniądze.

**Koszt obsługi klienta** — bo dane zbierają się same od pierwszego dnia i po roku masz raport, którego nie da się kupić nigdzie indziej.
