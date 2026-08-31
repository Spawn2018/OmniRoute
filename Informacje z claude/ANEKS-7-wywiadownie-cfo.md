# Aneks 7 — Wywiadownie gospodarcze i Wirtualny Dyrektor Finansowy

Naturalne przedłużenie Aneksu 6. Skoro liczysz koszt kredytowania klienta, następne pytanie brzmi: czy w ogóle powinieneś go kredytować i na ile.

---

# CZĘŚĆ 1 — INTEGRACJA Z WYWIADOWNIAMI

## 1.1 Poprawka do założenia

Napisałeś „podanie loginu i hasła w ustawieniach konta". Kierunek jest właściwy — to ten sam wzorzec „przynieś własną subskrypcję", który stosujemy przy armatorach — ale mechanizm musi być inny.

**Dlaczego nie login i hasło:**

- KRD, BIG InfoMonitor, ERIF, Coface, Creditreform i Dun & Bradstreet udostępniają dostęp programistyczny przez **klucze API albo certyfikaty**, wydawane na podstawie umowy z abonentem. Nie przez formularz logowania
- Automatyzacja logowania cudzym hasłem jest zwykle naruszeniem regulaminu i naraża twojego klienta na utratę dostępu
- Przechowywanie haseł do systemów finansowych osób trzecich to odpowiedzialność, której nie chcesz brać na siebie jako jednoosobowy dostawca

**Właściwy wzorzec** — identyczny jak `carrier_credential` z głównej specyfikacji:

```sql
external_data_credential
  id, organization_id
  provider,                     -- krd | big_infomonitor | erif | coface
                                -- creditreform | dnb | krz | krs_api
  auth_method,                  -- api_key | oauth | certificate
  credentials_encrypted bytea,  -- klucz szyfrujący per tenant
  account_ref, scopes text[]
  quota_monthly, quota_used
  is_active, last_ok_at, last_error
```

Klient wprowadza swój klucz API raz w ustawieniach, ty odpytujesz w jego imieniu, raporty należą do niego. Ty nie jesteś abonentem i nie redystrybuujesz cudzych danych.

## 1.2 Zacznij od źródeł darmowych — pokrywają większość potrzeby

To jest najważniejszy praktyczny wniosek tej sekcji. Zanim klient wykupi jakąkolwiek subskrypcję, możesz mu dać znaczną część wartości za zero złotych.

| Źródło | Co daje | Koszt |
|---|---|---|
| **API KRS** | Odpis aktualny lub pełny w formie danych, także wpisy wykreślone, oraz lista podmiotów ze zmianami w danym dniu — czyli **gotowy mechanizm monitoringu zmian** | darmowe |
| **RDF (Repozytorium Dokumentów Finansowych)** | Sprawozdania finansowe spółek KRS: bilans, RZiS, przepływy — **w XML, czyli gotowe do parsowania**, plus PDF. Od lutego 2026 także raporty ESG | darmowe |
| **Krajowy Rejestr Zadłużonych** | Postępowania upadłościowe i restrukturyzacyjne | darmowe |
| **Monitor Sądowy i Gospodarczy** | Ogłoszenia o upadłości, restrukturyzacji, przekształceniach | darmowe |
| **CEIDG API** | Dane jednoosobowych działalności, status zawieszenia | darmowe |
| **Biała lista VAT** | Status VAT, rachunki bankowe | darmowe |
| **VIES** | Weryfikacja VAT UE | darmowe |
| **GUS BIR** | REGON, PKD, forma prawna | darmowe |

Sprawozdanie w XML jest kluczowe: dostajesz pozycje bilansu i rachunku wyników jako **strukturę, nie obrazek**. Wskaźniki finansowe liczysz deterministycznie, bez OCR i bez modelu językowego.

**Ograniczenie do obejścia uczciwie:** wyszukiwarka RDF jest zabezpieczona przed automatycznym pobieraniem, a oficjalne API ma limity zapytań. Przy małym wolumenie działa; przy dużym trzeba albo respektować limity i kolejkować, albo skorzystać z komercyjnego pośrednika udostępniającego te same dane w JSON bez limitów. Nie omijaj zabezpieczeń.

**Czego darmowe źródła nie dają:** jednoosobowe działalności nie składają sprawozdań, więc dla JDG zostaje wyłącznie wywiadownia i twoja własna historia płatnicza. Brak też danych o zaległościach bieżących — to jest domena BIG-ów.

## 1.3 Wymogi prawne — nie do pominięcia

**Zapytanie do BIG o osobę fizyczną prowadzącą działalność wymaga upoważnienia.** To wynika z ustawy o udostępnianiu informacji gospodarczych, nie z regulaminu. Spółka kapitałowa — bez upoważnienia. Twój system musi to rozróżniać i wymuszać zebranie upoważnienia, zanim pozwoli na zapytanie o JDG.

```sql
credit_check_authorization
  id, party_id, authorized_by_name
  scope, granted_at, expires_at
  document_path,                -- skan albo podpis elektroniczny
  is_valid
```

**Raporty są treścią licencjonowaną.** Użytek własny abonenta, bez redystrybucji. Twój system je przechowuje dla klienta, który je zamówił — i dla nikogo więcej. Ustal retencję i usuwaj po terminie.

**Dane osobowe.** Raport o JDG zawiera dane osobowe. Cel przetwarzania, podstawa prawna, retencja, rejestr czynności. To wpada do dokumentacji RODO, o której była mowa w głównej specyfikacji.

## 1.4 Model danych raportu

```sql
credit_report
  id, organization_id, party_id
  provider, report_type
  requested_by, requested_at
  authorization_id NULL,        -- wymagane dla JDG
  raw_document_path,            -- oryginał w MinIO
  raw_payload jsonb,            -- odpowiedź API
  extracted jsonb,              -- znormalizowana struktura
  provider_score NULL, provider_grade NULL
  cost_amount,                  -- ile kosztowało zapytanie
  expires_at,                   -- retencja
  supersedes_id NULL

financial_statement             -- z RDF, darmowe
  id, party_id, fiscal_year
  source,                       -- rdf | uploaded | provider
  document_path, xml_parsed jsonb
  revenue, ebit, net_profit
  total_assets, equity, current_assets, current_liabilities
  cash, receivables, inventory, debt_total
  is_audited, filed_at

financial_ratio                 -- wyliczane, nie wprowadzane
  id, party_id, fiscal_year
  current_ratio, quick_ratio
  debt_to_equity, debt_to_assets
  ros, roe, roa
  receivables_days, payables_days, inventory_days
  cash_conversion_cycle
  revenue_growth, profit_growth
```

---

# CZĘŚĆ 2 — WIRTUALNY DYREKTOR FINANSOWY

## 2.1 Zasada nadrzędna

Ten moduł wydaje rekomendacje o skutkach finansowych i prawnych. Dlatego obowiązuje tu zasada 4 z głównej specyfikacji, w zaostrzonej formie:

> **Liczby liczy deterministyczny kod. Model językowy pisze uzasadnienie i wychwytuje ryzyka jakościowe. Nigdy odwrotnie.**

Limit kredytowy wyliczony przez model językowy jest nie do obrony — ani przed klientem, ani przed audytorem, ani przed samym sobą za pół roku. Limit wyliczony formułą, z uzasadnieniem napisanym przez model, jest jednym i drugim.

## 2.2 Architektura

```
WEJŚCIA
├─ sprawozdania finansowe (RDF, XML)      → wskaźniki, deterministycznie
├─ raport wywiadowni (jeśli klient ma)    → scoring dostawcy, wpisy, zaległości
├─ KRS: zarząd, kapitał, zmiany, wzmianki → sygnały strukturalne
├─ KRZ i MSiG                             → upadłość, restrukturyzacja
├─ biała lista, VIES                      → status podatkowy
└─ TWOJA historia płatnicza               → najsilniejszy predyktor ze wszystkich
        │
        ▼
[1] SILNIK PUNKTOWY — kod, formuły, wagi konfigurowalne
        │
        ▼
[2] FORMUŁA LIMITU I TERMINU — kod, powiązana z Aneksem 6
        │
        ▼
[3] MODEL JĘZYKOWY — uzasadnienie, ryzyka jakościowe z części opisowej
        │                raportu, projekt notatki
        ▼
[4] CZŁOWIEK — zatwierdza, modyfikuje lub odrzuca. Zapisane kto i kiedy
```

## 2.3 Silnik punktowy

Wymiary i wagi jako punkt wyjścia do kalibracji na własnych danych:

| Wymiar | Waga | Źródło |
|---|---|---|
| **Zachowanie płatnicze wobec ciebie** | 30% | własna historia — najmocniejszy predyktor, jaki masz |
| Płynność (bieżąca, szybka) | 15% | sprawozdanie |
| Zadłużenie (D/E, D/A) | 15% | sprawozdanie |
| Rentowność i jej trend | 10% | sprawozdanie, 3 lata |
| Skala i kapitał własny | 10% | sprawozdanie |
| Wpisy w BIG i KRZ | 10% | wywiadownia, KRZ |
| Sygnały strukturalne | 10% | KRS |

**Sygnały strukturalne warte osobnej uwagi** — to są rzeczy, które widać w KRS, a które rzadko kto sprawdza:

- częste zmiany w zarządzie w krótkim okresie
- zmiana siedziby na adres wirtualny
- zmiana nazwy
- brak złożenia sprawozdania za ostatni rok mimo obowiązku
- kapitał zakładowy nieproporcjonalnie niski do skali
- wiek spółki poniżej roku przy dużym zamówieniu

Każdy z osobna nic nie znaczy. Trzy naraz to sygnał.

**Krytyczne dla wiarygodności:** brak danych to nie jest neutralna informacja. Spółka, która nie złożyła sprawozdania, dostaje wynik gorszy, nie średni. Model musi to rozróżniać.

## 2.4 Formuła limitu

```
limit_bazowy = min(
    α × kapitał_własny,              -- typowo kilka do kilkunastu procent
    β × oczekiwany_obrót_miesięczny, -- wielokrotność miesięcznego obrotu
    cap_dla_klasy_ryzyka             -- twardy sufit
) × mnożnik_ryzyka

gdzie mnożnik_ryzyka wynika z wyniku punktowego,
a α, β i sufity są konfigurowalne per organizacja
```

Formuła jest prosta celowo. Ma być zrozumiała dla właściciela spedycji, obronna w rozmowie z klientem i kalibrowalna na własnej historii strat. Wyrafinowany model, którego nikt nie rozumie, nie zostanie użyty.

## 2.5 Sugerowany termin płatności — tu wpina się Aneks 6

To jest miejsce, w którym oba moduły dają razem więcej niż osobno. Termin płatności ma **policzalny koszt**, więc rekomendacja może być ekonomiczna, a nie tylko ostrożnościowa:

```
Sugerowany termin: 21 dni

  Ryzyko kredytowe pozwala na 30 dni
  Ale przy waszym koszcie kapitału 30 dni kosztuje 1,9% marży
  na typowym zleceniu tego klienta

  Rekomendacja: 21 dni standardowo
                30 dni przy podwyżce ceny o 0,9%
                14 dni z rabatem 0,6% — najlepszy wynik dla obu stron
```

Żaden system spedycyjny ani żadna wywiadownia tego nie robi, bo wywiadownia nie zna twojego kosztu kapitału, a system spedycyjny nie zna ryzyka klienta. Ty będziesz miał oba.

## 2.6 Format wyniku

```
OPINIA KREDYTOWA — [nazwa klienta]
Sporządzono: 2026-08-28 · Klasa ryzyka: B (62/100)

OCENA
Spółka działa 11 lat, rentowna w trzech ostatnich latach, choć marża
spadła z 4,1% do 2,3%. Płynność bieżąca 1,34 — poniżej średniej
w branży, ale stabilna. Brak wpisów w rejestrach zadłużenia.

MOCNE STRONY
• Historia współpracy: 34 faktury, średnie opóźnienie 4 dni
• Kapitał własny 2,1 mln zł, rosnący
• Sprawozdania składane terminowo

RYZYKA
• Spadek rentowności trzeci rok z rzędu
• Zadłużenie do kapitału wzrosło z 0,9 do 1,6
• Zmiana w zarządzie w maju 2026 — do zweryfikowania
• Sektor pod presją kosztową

REKOMENDACJA
  Limit kredytowy:        180 000 zł   (obecny: 250 000 zł ▼)
  Termin płatności:       21 dni       (obecny: 30 dni ▼)
  Zabezpieczenie:         niewymagane przy tym limicie
  Przegląd:               za 6 miesięcy lub przy nowym sprawozdaniu

PODSTAWA WYLICZENIA
  8% kapitału własnego = 168 000 zł  ← wiążące ograniczenie
  2,5 × obrót miesięczny = 210 000 zł
  mnożnik klasy B = 1,05
  → 176 400 zł, zaokrąglone do 180 000 zł

⚠ Rekomendacja wymaga zatwierdzenia przez uprawnionego użytkownika.
```

Sekcja „podstawa wyliczenia" jest obowiązkowa. Bez niej to jest wyrocznia, a nie narzędzie.

## 2.7 Monitoring ciągły zamiast jednorazowej oceny

Ocena kredytowa robiona raz przy zakładaniu klienta jest bezwartościowa po roku. API KRS pozwala pobrać listę podmiotów, w których dokonano wpisów w danym dniu — masz gotowy mechanizm wykrywania zmian bez odpytywania każdego klienta osobno.

```sql
credit_watch
  party_id, is_active
  triggers jsonb,               -- co obserwujemy
  last_checked_at

credit_alert
  id, party_id, alert_type,     -- new_statement | krs_change | krz_entry
                                -- payment_deterioration | limit_exceeded
                                -- vat_status_change
  severity, detected_at, details jsonb
  acknowledged_by, action_taken
```

Alerty warte wdrożenia od początku: nowe sprawozdanie w RDF, wpis w KRZ lub MSiG, zmiana w zarządzie lub siedzibie, wykreślenie z białej listy VAT, pogorszenie własnej dyscypliny płatniczej, przekroczenie limitu.

**Ostatni jest najważniejszy i całkowicie darmowy** — twoje własne dane wykrywają problem wcześniej niż jakakolwiek wywiadownia, bo klient przestaje płacić tobie, zanim trafi do rejestru.

## 2.8 Odpowiedzialność i wymóg prawny

**Decyzja kredytowa nie może być w pełni zautomatyzowana wobec osoby fizycznej.** RODO daje prawo do interwencji człowieka przy zautomatyzowanych decyzjach wywołujących skutki prawne lub istotnie wpływających na osobę. Odmowa kredytu kupieckiego wobec jednoosobowej działalności mieści się w tej kategorii.

Konsekwencje projektowe:

- system **rekomenduje**, człowiek **decyduje** — zawsze, bez wyjątku
- decyzja zapisana z osobą, czasem i uzasadnieniem odstępstwa
- klient końcowy ma prawo poznać powody — więc „podstawa wyliczenia" musi być zachowana razem z decyzją
- w umowie z twoim klientem: ograniczenie odpowiedzialności za rekomendacje. **Nie jesteś doradcą finansowym i nie możesz nim być** — narzędzie dostarcza analizę, odpowiedzialność za decyzję zostaje po stronie użytkownika

To nie jest formalność do dopisania na koniec. To jest wymóg, który kształtuje interfejs.

---

# CZĘŚĆ 3 — DLACZEGO TO DZIAŁA RAZEM

Trzy moduły, które osobno są zwykłe, a razem tworzą coś, czego nie ma:

```
Aneks 6: koszt pieniądza     → wiesz, ile kosztuje termin płatności
Aneks 7: ocena kredytowa     → wiesz, na ile klienta stać i czy jest wiarygodny
Aneks 5: koszt obsługi       → wiesz, ile kosztuje jego obsłużenie
        ↓
Pełny obraz rentowności klienta, jakiego nie ma żaden system spedycyjny
ani żadna wywiadownia — bo każde z nich widzi tylko jeden wymiar
```

Wywiadownia powie ci, czy klient zapłaci. Nie powie, czy warto go mieć. System spedycyjny pokaże marżę brutto. Nie pokaże, ile ta marża kosztowała w kapitale i w godzinach.

**Ty będziesz jedynym miejscem, gdzie te trzy liczby spotykają się na jednym ekranie.** To jest odpowiedź na pytanie o oprogramowanie, którego nie ma.

## Co zrobić w tygodniach 1–2

Sam moduł zbudujesz później, ale trzy rzeczy muszą wejść od razu:

1. `external_data_credential` — uogólnienie `carrier_credential`, ten sam wzorzec
2. `credit_check_authorization` — bez tego nie odpytasz o JDG zgodnie z prawem
3. Rejestrowanie faktycznych dat płatności (już w Aneksie 6) — bo to jest 30% wagi w scoringu i jedyne źródło, którego nie kupisz

Integrację z KRS i RDF możesz zrobić wcześnie — jest darmowa, publiczna i daje natychmiastową wartość przy zakładaniu kontrahenta: nazwa, zarząd, kapitał i trzy ostatnie sprawozdania podciągnięte automatycznie po numerze KRS.
