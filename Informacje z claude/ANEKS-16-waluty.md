# Aneks 16 — Waluty: prezentacja i wpływ na wynik

---

# CZĘŚĆ 1 — WALUTA OFERTY

## 1.1 Trzy tryby prezentacji

```sql
quotation
  ...
  currency_mode,          -- original | converted | hybrid
  display_currency,       -- waluta prezentacji przy converted/hybrid
  fx_source,              -- nbp_a | ecb | carrier | manual
  fx_date,                -- dzień notowania
  fx_spread_pct,          -- narzut na kurs, patrz 1.4
  fx_clause               -- fixed | recalculate_at_invoice
```

**`original` — każda pozycja w walucie źródłowej**

```
Ocean freight             2 340 USD
DTHC Callao                 310 USD
Odprawa celna Peru        1 240 PEN
Odwóz Lima                  890 PEN
Dowóz Poznań–Gdynia       1 240 PLN
```

Uczciwe i przejrzyste, ale klient nie wie, ile zapłaci łącznie. Stosowane przy dużych klientach z własnym działem finansowym.

**`converted` — wszystko w jednej walucie**

```
Ocean freight             2 340 USD
DTHC Callao                 310 USD
Odprawa celna Peru          331 USD   (1 240 PEN @ 3,745)
Odwóz Lima                  238 USD   (  890 PEN @ 3,745)
Dowóz Poznań–Gdynia         309 USD   (1 240 PLN @ 4,015)
─────────────────────────────────────
RAZEM                     3 528 USD
```

Najczęstszy wybór. Wymaga pokazania kursu i daty notowania przy każdej przeliczonej pozycji — inaczej klient nie zweryfikuje, a przy sporze nie masz się na co powołać.

**`hybrid` — reguła per rodzaj opłaty**

Typowy układ w praktyce: fracht i dopłaty morskie w dolarach, opłaty lokalne w walucie kraju, transport krajowy w złotych. Zdefiniowane regułą, nie ręcznie:

```sql
currency_display_rule
  id, organization_id
  scope_type,             -- charge_code | charge_side | mode
  scope_ref
  target_currency,        -- albo NULL = zostaw oryginalną
  priority
```

## 1.2 Wybór jest per oferta i per klient

Domyślny tryb zapisany na kontrahencie, nadpisywalny w konkretnej ofercie. Niemiecki klient chce EUR, chiński USD, polski producent mebli złote — i to się nie zmienia z oferty na ofertę.

```sql
party
  ...
  preferred_currency, preferred_currency_mode
```

## 1.3 Kto ponosi ryzyko — dwa modele umowne

To jest decyzja handlowa o realnych konsekwencjach finansowych i musi być jawna w systemie.

**`fixed` — kurs zamrożony.** Wyceniasz w złotych, kwota jest ostateczna. **Ryzyko kursowe bierzesz na siebie.** Klient to lubi, ty płacisz za to zmiennością wyniku.

**`recalculate_at_invoice` — klauzula walutowa.** Oferta w dolarach, faktura przeliczana po kursie z dnia poprzedzającego fakturowanie. **Ryzyko przechodzi na klienta.**

Treść klauzuli generowana automatycznie do oferty:

> Ceny wyrażone w USD. Faktura zostanie wystawiona w PLN według kursu średniego NBP (tabela A) z ostatniego dnia roboczego poprzedzającego dzień wystawienia faktury.

Przy trybie `fixed` system musi liczyć **koszt ryzyka** i pokazywać go handlowcowi — o tym w części 2.

## 1.4 Spread walutowy jako przychód

Rzecz, o której mało kto mówi wprost, a robi ją większość spedytorów: przeliczasz klientowi po kursie NBP powiększonym o marżę.

```
Odprawa celna Peru   1 240 PEN
  kurs NBP                       3,745
  kurs zastosowany (+1,5%)       3,801
  kwota dla klienta            331,5 USD
  koszt po kursie NBP          331,1 USD
  → przychód ze spreadu          4,9 USD
```

Jeśli tego nie modelujesz, spread znika w zaokrągleniach i nie wiesz, ile na nim zarabiasz. Jeśli modelujesz — to osobna pozycja marży, widoczna w raporcie struktury z Aneksu 12.

```sql
-- rozszerzenie quotation_line
  fx_rate_cost,           -- kurs kosztowy (NBP)
  fx_rate_applied,        -- kurs zastosowany klientowi
  fx_spread_amount        -- różnica jako przychód
```

Ustawiane regułą per klient, z widełkami i progiem wymagającym akceptacji.

## 1.5 Zaokrąglanie

Reguła per waluta: USD i EUR do pełnych jednostek, PLN do dziesięciu groszy, JPY bez części ułamkowej. Zaokrąglenie zawsze na korzyść, nigdy w dół — i zawsze **po** przeliczeniu, nigdy przed.

## 1.6 Co musi znaleźć się na PDF

- kurs i data notowania przy każdej przeliczonej pozycji
- źródło kursu, wprost: „NBP tabela A z dnia…"
- klauzula walutowa, jeśli tryb `recalculate_at_invoice`
- data ważności oferty i informacja, czy kurs jest w niej zamrożony

Bez tego przy wahnięciu kursu masz spór, w którym nie masz argumentów.

---

# CZĘŚĆ 2 — RÓŻNICE KURSOWE W RENTOWNOŚCI

## 2.1 Gdzie powstaje różnica

Pieniądze poruszają się w czterech momentach, a kurs w każdym jest inny:

```
t0  wycena          kurs oferty          ← tu obiecujesz cenę
t1  koszt zaksięgowany   kurs księgowania
t2  zapłata dostawcy     kurs rozliczenia   → różnica na koszcie
t3  faktura klientowi    kurs fakturowania
t4  wpływ od klienta     kurs rozliczenia   → różnica na przychodzie
```

Wynik walutowy zlecenia:

```
różnica_na_przychodzie = kwota_walutowa × (kurs_t4 − kurs_t3)
różnica_na_koszcie     = kwota_walutowa × (kurs_t1 − kurs_t2)
wynik_fx = różnica_na_przychodzie + różnica_na_koszcie
```

Znak zależy od kierunku przepływu — należność zyskuje przy umocnieniu waluty obcej, zobowiązanie traci.

## 2.2 Wpięcie w architekturę — tak samo jak koszt pieniądza

Zgodnie z zasadą 3: **różnica kursowa to kolejna pozycja `shipment_charge`**, z kodem `FXDIFF`.

```
charge_code: FXDIFF
  name_pl:    Różnice kursowe
  side:       internal
  is_visible_to_customer: false
  computed:   true
```

Efekt: wszystkie raporty rentowności — per zlecenie, klient, relacja, handlowiec — uwzględniają wynik walutowy bez zmiany choćby jednego zapytania. Dokładnie tak samo, jak `FINCOST` z Aneksu 6.

## 2.3 Model danych

```sql
fx_rate                          -- notowania, pobierane cyklicznie
  id, source,                    -- nbp_a | nbp_b | ecb
  base_currency, quote_currency
  rate, quotation_date, table_no,
  fetched_at
  UNIQUE (source, base, quote, quotation_date)

-- rozszerzenie shipment_cash_event z Aneksu 6
shipment_cash_event
  ...
  amount_original, currency_original
  fx_rate_booked, fx_date_booked,      -- kurs przy księgowaniu
  amount_base_booked,                   -- kwota w walucie funkcjonalnej
  fx_rate_settled, fx_date_settled,     -- kurs przy rozliczeniu
  amount_base_settled,
  fx_difference                         -- wyliczana

shipment_fx_result
  shipment_id
  by_currency jsonb,             -- rozbicie per waluta
  realized_fx, unrealized_fx,
  net_exposure_by_currency jsonb,
  computed_at
```

## 2.4 Ekspozycja netto, nie brutto

To jest niuans, który zmienia obraz. Zlecenie, w którym kupujesz w dolarach i sprzedajesz w dolarach, ma **ekspozycję bliską zeru** — masz naturalne zabezpieczenie. Zlecenie, w którym kupujesz w dolarach, a sprzedajesz w złotych, ma ekspozycję pełną.

```
Zlecenie GD/2026/00412

  Przychód   3 528 USD          należność w USD
  Koszty     2 890 USD          zobowiązanie w USD
             1 240 PLN          zobowiązanie w PLN
  
  Ekspozycja netto USD:  +638 USD
  → ryzyko kursowe dotyczy tylko marży, nie całego obrotu  ✓
```

versus:

```
  Przychód  12 400 PLN          należność w PLN
  Koszty     2 890 USD          zobowiązanie w USD
  
  Ekspozycja netto USD:  −2 890 USD
  → osłabienie złotego o 3% kosztuje 350 zł, czyli ponad 1/4 marży  ⚠
```

**Ten wskaźnik pokazuj przy wycenie**, nie w raporcie miesięcznym. Handlowiec widzi wtedy, że oferta w złotych na koszty dolarowe jest ryzykowna, i może zaproponować klauzulę walutową zamiast obniżki ceny.

## 2.5 Ryzyko kursowe przy wycenie

Analogicznie do marży zagrożonej z Aneksu 4:

```
Oferta OF/2026/00913 · ważna 21 dni

  Marża brutto                     2 900 zł   11,7%
  Koszt finansowania (52 dni)       −310 zł
  Ekspozycja walutowa netto      −2 890 USD
  ─────────────────────────────────────────────
  Marża po koszcie kapitału        2 590 zł   10,4%
  
  ⚠ Ryzyko kursowe: przy zmienności USD/PLN z ostatnich 90 dni
     marża mieści się w przedziale 8,9% – 11,8% (ufność 80%)
     
  → Sugestia: klauzula walutowa przeniesie ryzyko na klienta
```

Zmienność liczysz z własnej historii notowań, nie z modelu — odchylenie standardowe zmian kursu w okresie odpowiadającym luce płatniczej. To jest statystyka, nie prognoza, i dlatego jest obronna.

## 2.6 Kurs podatkowy a kurs zarządczy

Istotne rozróżnienie, którego systemy zwykle nie robią.

**Do celów podatkowych i VAT** obowiązuje kurs średni NBP z ostatniego dnia roboczego poprzedzającego dzień powstania obowiązku podatkowego. To jest kurs narzucony, nie do wyboru.

**Do celów zarządczych** możesz chcieć innego — kursu z dnia wyceny, kursu budżetowego przyjętego na rok, kursu faktycznie uzyskanego przy wymianie w banku.

```sql
-- rozszerzenie shipment_charge
  fx_rate_tax,        -- NBP D-1, do faktury i księgowania
  fx_rate_mgmt,       -- do raportowania zarządczego
  fx_rate_actual      -- faktycznie uzyskany przy wymianie
```

Trzeci jest najciekawszy: różnica między kursem NBP a kursem, po którym faktycznie wymieniłeś walutę w banku, to realny wynik, który nigdzie się nie pojawia, a bywa znaczący.

## 2.7 Ekspozycja portfela i decyzja o zabezpieczeniu

Zestawienie z otwartych zleceń i ofert, w podziale na waluty i okna czasowe:

```
EKSPOZYCJA WALUTOWA — stan na 28.08

USD
  Oferty wysłane, nierozstrzygnięte     +184 000    (ryzyko warunkowe)
  Zlecenia w toku, niezafakturowane     −412 000
  Faktury niezapłacone                  +268 000
  ─────────────────────────────────────────────
  Ekspozycja netto                      −144 000 USD
  
  Wrażliwość: +3% na USD/PLN → −17 400 zł wyniku
  
  Okna:  do 30 dni  −62 000
         31–60 dni  −58 000
         61–90 dni  −24 000
```

Dla właściciela to jest podstawa decyzji, czy zabezpieczać. Dziś liczy się to w Excelu albo wcale.

## 2.8 Powiązanie z kosztem pieniądza

Warto to sobie uświadomić przy projektowaniu: **koszt kapitału i ryzyko kursowe to funkcje tej samej zmiennej** — luki czasowej między wypływem a wpływem.

Skrócenie terminu płatności klienta z 60 do 21 dni zmniejsza jednocześnie koszt finansowania i okno ekspozycji walutowej. Symulacja z Aneksu 6, sekcja 1.7, powinna pokazywać oba efekty razem:

```
Wariant A: 14 dni + rabat 1,5%
  marża po koszcie kapitału   10,9%
  ryzyko kursowe (przedział)   10,4% – 11,3%    ← wąski
  
Wariant C: 60 dni + rabat 1,5%
  marża po koszcie kapitału    8,9%
  ryzyko kursowe (przedział)    6,8% – 10,9%    ← szeroki
```

To jest argument, którego handlowiec dziś nie ma: długi termin płatności kosztuje nie tylko pieniądze, ale i przewidywalność.

---

# 3. KOLEJNOŚĆ BUDOWY

| Etap | Zakres | Dni |
|---|---|---|
| 1 | `fx_rate` + pobieranie NBP cyklicznie, historia | 2 |
| 2 | Tryby prezentacji na ofercie + reguły per klient | 3 |
| 3 | Kurs i data przy pozycji na PDF, klauzula walutowa | 2 |
| 4 | Spread walutowy jako pozycja marży | 2 |
| 5 | `FXDIFF` — różnice zrealizowane przy rozliczeniu | 3 |
| 6 | Ekspozycja netto per zlecenie, pokazywana przy wycenie | 3 |
| 7 | Ryzyko kursowe z własnej zmienności historycznej | 3 |
| 8 | Ekspozycja portfela z podziałem na okna czasowe | 3 |
| 9 | Trzy kursy: podatkowy, zarządczy, faktyczny | 2 |

Etapy 1–3 wchodzą razem z silnikiem wyceny, bo bez nich nie wystawisz poprawnej oferty wielowalutowej. Reszta po module rozliczeń, bo wymaga faktycznych dat i kwot płatności.
