# Aneks 6 — Koszt pieniądza i finanse operacyjne

Kategoria, której nie ma w żadnym systemie spedycyjnym w segmencie MŚP.

---

# CZĘŚĆ 1 — SILNIK KOSZTU PIENIĄDZA

## 1.1 Problem

Zlecenie z marżą 12% wygląda tak samo niezależnie od tego, czy pieniądze wracają w 14 czy w 60 dni. A to nie to samo zlecenie.

```
Zlecenie A                          Zlecenie B
przychód  20 000 zł                 przychód  20 000 zł
koszt     17 600 zł                 koszt     17 600 zł
marża      2 400 zł (12,0%)         marża      2 400 zł (12,0%)

agent płatny w  7 dni               agent płatny w 45 dni
klient płaci w 60 dni               klient płaci w 30 dni

luka: 53 dni × 17 600 zł            luka: −15 dni × 17 600 zł
→ finansujesz klienta               → dostawca finansuje ciebie
```

Przy koszcie kapitału na poziomie linii obrotowej te dwa zlecenia różnią się realnym wynikiem o kilkaset złotych. Przy tysiącu zleceń rocznie to jest pozycja, która decyduje o tym, czy firma zarabia.

**Nikt tego nie liczy, bo nikt nie ma w jednym miejscu terminów płatności obu stron i harmonogramu kosztów.** Ty będziesz miał.

## 1.2 Formuła

Dla każdej pozycji kosztowej `i` i przychodu `R`:

```
koszt_finansowania = Σ [ Aᵢ × (t_wpływu − t_zapłatyᵢ) / 365 × r ]

gdzie:
  Aᵢ           kwota pozycji kosztowej i
  t_zapłatyᵢ   dzień faktycznej zapłaty dostawcy
  t_wpływu     dzień faktycznego wpływu od klienta
  r            roczny koszt kapitału organizacji
```

**Znak ma znaczenie.** Gdy `t_wpływu > t_zapłaty` — finansujesz i koszt jest dodatni. Gdy dostawca daje dłuższy termin niż klient — wartość jest ujemna i **powiększa marżę**. To jest realna korzyść, którą dziś nikt nie przypisuje do zlecenia.

Pozycje kosztowe mają różne terminy: armator chce przedpłaty, agent 30 dni, port przy wydaniu, przewoźnik 21 dni. Każdą liczysz osobno, nie od sumy.

## 1.3 Terminy umowne kontra rzeczywiste

To jest różnica, która decyduje o wiarygodności całego modułu.

```sql
party_payment_behavior           -- przeliczane cyklicznie z historii
  party_id, period
  contractual_terms_days,        -- co jest w umowie
  observed_dso_days,             -- ile faktycznie trwa (należności)
  observed_dpo_days,             -- ile faktycznie trwa (zobowiązania)
  payment_delay_avg, payment_delay_p90
  invoices_count, disputes_count
  reliability_score
```

Klient ma umowne 30 dni, płaci średnio w 47. Wyceniasz na 47, nie na 30. Po roku danych ta liczba jest twarda i nie do zakwestionowania w negocjacji — pokazujesz klientowi jego własną historię.

## 1.4 Model danych

```sql
cost_of_capital_config           -- per organizacja
  organization_id
  annual_rate,                   -- parametr konfigurowalny
  method,                        -- overdraft | factoring | wacc | manual
  source_note, valid_from
  -- punkt odniesienia: oprocentowanie twojej linii obrotowej
  -- albo koszt faktoringu; nie zgaduj, wpisz realną liczbę

payment_term_profile             -- terminy per typ dostawcy
  id, organization_id
  party_id NULL, charge_code NULL, party_role NULL
  terms_days,                    -- może być ujemne: przedpłata
  trigger,                       -- invoice_date | vessel_departure
                                 -- delivery | booking | gate_in
  priority

shipment_cash_event              -- harmonogram przepływów
  id, shipment_id
  direction,                     -- out | in
  party_id, charge_code NULL, invoice_id NULL
  amount, currency
  planned_date, actual_date NULL
  status                         -- forecast | committed | settled

shipment_financing               -- wynik obliczeń
  shipment_id
  weighted_gap_days,             -- średnia ważona luka
  capital_employed,              -- ile kapitału zaangażowane
  financing_cost, currency       -- ← ze znakiem
  computed_at, config_version
```

## 1.5 Integracja z istniejącą architekturą

Elegancko wpina się w zasadę 3 z głównej specyfikacji. Koszt pieniądza to **kolejna pozycja `shipment_charge`**, z kodem `FINCOST`:

```
charge_code: FINCOST
  name_pl:    Koszt finansowania
  side:       internal
  is_visible_to_customer: false   ← nigdy nie pokazywany klientowi
  computed:   true                ← wyliczany, nie wprowadzany
```

Dzięki temu wszystkie istniejące raporty rentowności — per zlecenie, klient, relacja, handlowiec — od razu uwzględniają koszt kapitału, bez zmiany ani jednego zapytania. Cała analityka z Aneksu 1 działa dalej.

## 1.6 Wycena z kosztem pieniądza

```
Oferta OF/2026/00913 — Gdynia → Szanghaj, 2×40HC

  Przychód                    24 800 zł
  Koszty bezpośrednie         21 900 zł
  ─────────────────────────────────────
  Marża brutto                 2 900 zł   11,7%
  Koszt finansowania            −310 zł   (52 dni luki)
  ─────────────────────────────────────
  Marża po koszcie kapitału    2 590 zł   10,4%

  ⚠ Termin płatności klienta: umowny 30 dni, faktyczny 47 dni
```

Handlowiec widzi to **przed wysłaniem oferty**. Zmienia decyzję cenową, a nie tylko raport na koniec kwartału.

## 1.7 Termin płatności jako dźwignia handlowa

Tu robi się z tego funkcja sprzedażowa, a nie tylko księgowa.

Klient prosi o rabat. Zamiast schodzić z ceny — negocjujesz termin:

```
Symulacja dla klienta [nazwa], zlecenie 24 800 zł

  Obecnie:  60 dni, marża po kapitale  10,4%
  
  Wariant A: 14 dni + rabat 1,5%
             → marża po kapitale  10,9%   ✓ lepiej dla obu stron
  Wariant B: 30 dni + rabat 0,8%
             → marża po kapitale  10,6%   ✓
  Wariant C: 60 dni + rabat 1,5%
             → marża po kapitale   8,9%   ✗
```

**Rabat za skrócenie terminu jest często korzystniejszy niż utrzymanie ceny przy długim terminie.** Handlowcy tego nie liczą, bo nie mają czym. To jest narzędzie, które daje im nowy argument w negocjacji zamiast odbierać marżę.

## 1.8 Negocjacja z dostawcami — konkret zamiast wyczucia

Ta sama matematyka w drugą stronę, jako materiał na rozmowę roczną z agentem:

```
Agent [nazwa] — analiza roczna
  Obrót:                          1 240 000 zł
  Średni termin płatności:        21 dni (umowny 30, płacisz wcześniej)
  
  Wydłużenie do 45 dni jest warte: 18 400 zł rocznie
  → to jest twój argument negocjacyjny, wyrażony kwotą
```

Spedytorzy negocjują z agentami stawki. Prawie nikt nie negocjuje terminów, bo nie umie ich wycenić.

---

# CZĘŚĆ 2 — RESZTA KATEGORII

Otworzyłeś obszar, w którym jest więcej niż jeden moduł.

## 2.1 Prognoza przepływów pieniężnych

Z otwartych zleceń i harmonogramu `shipment_cash_event` powstaje prognoza kasowa bez żadnej dodatkowej pracy:

```
Tydzień 36:   wypływy 284 000 zł   wpływy  96 000 zł   saldo −188 000
Tydzień 37:   wypływy 112 000 zł   wpływy 341 000 zł   saldo +229 000
Tydzień 38:   wypływy 198 000 zł   wpływy 154 000 zł   saldo  −44 000

⚠ Tydzień 36: zapotrzebowanie przekracza limit linii obrotowej
```

Dla właściciela małej spedycji to jest informacja o wartości większej niż połowa pozostałych funkcji razem wziętych. Dziś powstaje ręcznie w Excelu, w piątek wieczorem, albo wcale.

## 2.2 Decyzja o faktoringu per faktura

```
Faktura FV/2026/0847 — 68 400 zł, termin 60 dni
  Koszt finansowania własnego:     −840 zł
  Koszt faktoringu:              −1 220 zł
  → nie opłaca się

Faktura FV/2026/0851 — 214 000 zł, termin 90 dni, klient DSO 108 dni
  Koszt finansowania własnego:   −4 900 zł
  Koszt faktoringu:              −3 100 zł
  → faktoruj  ✓
```

Decyzja podejmowana dziś hurtowo albo wcale, a powinna być liczona per faktura.

## 2.3 Dynamiczny limit kredytowy

Limit kredytowy jest dziś liczbą wpisaną raz i nieaktualizowaną. Powinien reagować:

```sql
credit_assessment
  party_id, computed_at
  current_exposure,              -- otwarte faktury + niezafakturowane zlecenia
  approved_limit, suggested_limit
  payment_reliability,           -- z party_payment_behavior
  trend,                         -- poprawa | stabilnie | pogorszenie
  external_score NULL,           -- wywiadownia, jeśli klient ma abonament
  alerts jsonb                   -- opóźnienia rosną, ekspozycja > limit
```

Blokada nowego bookingu przy przekroczeniu, z możliwością zwolnienia przez uprawnioną osobę. Chroni przed sytuacją, w której dobry klient staje się złym długiem, a nikt nie zauważył trendu.

## 2.4 Kaucje, depozyty i gwarancje

Pieniądze zamrożone poza obiegiem, których nikt nie pilnuje:

```sql
deposit
  id, party_id, shipment_id NULL
  kind,                          -- container | customs_guarantee
                                 -- carrier_deposit | tender_bond
  amount, currency
  placed_at, expected_return_at, returned_at NULL
  status                         -- placed | overdue | returned | forfeited
```

Depozyty kontenerowe i gwarancje celne potrafią zamrozić poważne kwoty na miesiące. Alert „depozyt 12 000 zł zwrotny 40 dni temu, nie wrócił" to czysty odzysk.

## 2.5 Trójwymiarowa rentowność klienta

Połączenie tego aneksu z kosztem obsługi z Aneksu 5 daje widok, którego nie ma nikt:

```
Klient                Marża brutto   Po koszcie obsługi   Po koszcie kapitału
─────────────────────────────────────────────────────────────────────────────
Alfa Sp. z o.o.           14,2%              11,8%               11,4%
Beta Trading              12,8%               9,1%                6,2%  ⚠
Gamma Logistics            8,4%               7,9%                8,6%  ✓
```

Beta wygląda dobrze w standardowym raporcie i jest prawie nierentowna. Gamma wygląda słabo, a jest najlepszym klientem w portfelu — płaci szybko i nie generuje obsługi.

**To jest raport, który właściciel spedycji zobaczy raz i kupi system.** Bo pokazuje mu coś, o czym wiedział, że nie wie.

---

# CZĘŚĆ 3 — CO ZROBIĆ TERAZ

Sam silnik zbudujesz później, ale **dane muszą się zbierać od pierwszego dnia**, bo wstecz ich nie odtworzysz.

W tygodniach 1–2 dołóż:

1. `payment_term_profile` — terminy per dostawca i typ opłaty, nie jedna liczba na kontrahencie
2. `shipment_cash_event` — harmonogram przepływów generowany przy tworzeniu zlecenia, choćby prognostycznie
3. `cost_of_capital_config` — jedna liczba, twoja realna stawka finansowania
4. Rejestrowanie **faktycznych** dat zapłaty i wpływu, nie tylko terminów

Punkt 4 jest kluczowy. Bez historii rzeczywistych płatności `observed_dso` nie powstanie, a terminy umowne kłamią.

Sam silnik obliczeniowy to potem kilka dni pracy — cała trudność leży w tym, żeby dane były.

## Dlaczego to jest właściwa odpowiedź na „oprogramowanie, którego nie ma"

Wszystkie systemy spedycyjne liczą marżę jako różnicę przychodu i kosztu. Żaden nie pyta, **kiedy** te pieniądze się poruszają.

A spedycja jest biznesem o niskiej marży i wysokim obrocie — czyli dokładnie takim, w którym koszt kapitału jest istotną częścią wyniku, a nie zaokrągleniem. Firma z marżą 3% netto i sześćdziesięciodniową luką finansuje działalność, której realna rentowność jest o jedną trzecią niższa, niż pokazuje jej własny system.

To nie jest funkcja dodatkowa. To jest poprawienie błędu, który cała branża popełnia od trzydziestu lat.
