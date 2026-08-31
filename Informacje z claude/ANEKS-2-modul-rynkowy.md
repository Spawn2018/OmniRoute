# Aneks 2 — Moduł rynkowy: dane zewnętrzne i prognozowanie stawek

Uzupełnienie SPEC-master o warstwę, której brakowało: zbieranie danych politycznych, makroekonomicznych i rynkowych oraz przewidywanie kierunku cen.

---

## 1. Zacznijmy od tego, czego ten moduł nie może obiecywać

Stawki spot w kontenerach są jedną z trudniejszych do prognozowania serii w całej logistyce. Napędzają je decyzje o dyscyplinie podażowej podejmowane przez kilkunastu armatorów, nagłe zdarzenia geopolityczne i sezonowość, która co roku wygląda inaczej. Rozkład ma grube ogony — pojedyncze zdarzenie potrafi podwoić stawkę w trzy tygodnie.

Jeśli sprzedasz klientowi funkcję „AI przewiduje ceny frachtu", pierwsza rozjechana prognoza zniszczy zaufanie do całego systemu, łącznie z tymi modułami, które działają bezbłędnie.

**Sprzedawaj co innego: „wiesz wcześniej i wiesz dlaczego".** To jest obietnica, której dotrzymasz, i która ma większą wartość operacyjną niż liczba z modelu.

## 2. Trzy warstwy uporządkowane wg pewności

To jest główna decyzja projektowa tego modułu. Każda warstwa ma inny status epistemiczny i inne prawo wstępu do wyceny.

| Warstwa | Charakter | Wchodzi do oferty? |
|---|---|---|
| **1. Deterministyczna** | fakty ogłoszone albo wyliczalne ze wzoru | **Tak**, jako konkretna kwota |
| **2. Statystyczna** | prognoza z przedziałem ufności i zmierzoną skutecznością | **Tak, ale tylko jako ryzyko**, nigdy jako cena |
| **3. Kontekstowa** | narracja, zdarzenia, doniesienia | **Nigdy.** Wyłącznie alert dla człowieka |

**Około 80% wartości biznesowej leży w warstwie 1, która nie wymaga uczenia maszynowego w ogóle.** To jest najważniejsze zdanie w tym aneksie.

## 3. Warstwa 1 — deterministyczna

Rzeczy, które są ogłaszane z wyprzedzeniem albo wynikają ze wzoru. Zbieranie danych, nie prognozowanie.

### 3.1 Ogłoszenia armatorów

| Sygnał | Źródło | Wyprzedzenie |
|---|---|---|
| **GRI** (General Rate Increase) | strony armatorów, taryfy publiczne, powiadomienia FMC dla relacji USA | zwykle 15–30 dni |
| **PSS** (Peak Season Surcharge) | jw. | 2–4 tygodnie |
| **Blank sailings** | ogłoszenia aliansów i armatorów, rozkłady | 2–6 tygodni |
| Zmiany serwisów, nowe pętle | jw. | 4–12 tygodni |
| Zmiany opłat lokalnych i THC | taryfy terminali i armatorów | 30 dni |

GRI nie jest prognozą. GRI jest ogłoszeniem. Zbieranie tych ogłoszeń i wiązanie ich z relacjami w twojej bazie stawek daje ci alert: „stawka zakupowa na Gdynia–Szanghaj wzrośnie 1 października o 800 USD/FEU, a masz trzy oferty ważne po tej dacie".

To jest funkcja, która zwraca się w pierwszym miesiącu i nie ma w sobie ani grama uczenia maszynowego.

### 3.2 Dopłaty wyliczalne ze wzoru

Część dopłat to funkcje, nie zagadki:

- **BAF/FAF** — formuła od ceny paliwa (VLSFO w Rotterdamie i Singapurze), zużycia na relacji i współczynnika armatora. Formuły są publikowane. Znając trend cen bunkra, znasz BAF na następny kwartał z dużą dokładnością
- **ETS** — procent fazy wdrożenia × emisja na relacji × cena uprawnień EUA. Wszystkie trzy składniki są publiczne
- **Dopłaty kanałowe** — ogłaszane, powiązane z ograniczeniami zanurzenia
- **CAF** — funkcja kursu walutowego

### 3.3 Kalendarz

Chiński Nowy Rok, Golden Week, sezon przedświąteczny. Chińskie fabryki wysyłają agresywnie w okresie czterech do sześciu tygodni przed Księżycowym Nowym Rokiem. To jest powtarzalne co roku, znane z wyprzedzeniem i mierzalne w twoich własnych danych.

## 4. Warstwa 2 — statystyczna

### 4.1 Co prognozować

Nie „cenę frachtu". Trzy konkretne rzeczy:

1. **Kierunek indeksu na 2–6 tygodni** z przedziałem ufności
2. **Twoją własną stawkę zakupową na twoich relacjach** — tu masz dane, których nie ma nikt inny, i to jest zdecydowanie najbardziej predykcyjny zbiór, jakim dysponujesz
3. **Ryzyko wygaśnięcia marży** — prawdopodobieństwo, że koszt wzrośnie w okresie ważności wystawionej oferty

Trzeci punkt to jedyny, który naprawdę potrzebny jest przy wycenie.

### 4.2 Reguła sygnału, którą warto zaszyć

Ruchy tygodniowe poniżej 5% to zwykle szum; utrzymujące się przez kilka tygodni ruchy rzędu 10% lub więcej, zwłaszcza na wielu relacjach jednocześnie, to sygnał wart reakcji.

Zaimplementuj to jako regułę progową, zanim sięgniesz po jakikolwiek model. Odfiltruje większość fałszywych alarmów.

### 4.3 Backtesting jest obowiązkowy

```
baseline = "jutro będzie tak jak dziś" (random walk)

jeśli model nie bije baseline na danych historycznych 
   → nie wdrażasz modelu
   → wdrażasz uczciwe zdanie: "brak wiarygodnego sygnału"
```

Zapisuj każdą prognozę razem z późniejszą realizacją w `forecast_evaluation`. Po roku będziesz miał zmierzoną skuteczność i będziesz mógł uczciwie powiedzieć klientowi: „nasze prognozy dwutygodniowe mylą się średnio o X%". To jest sprzedawalne. „AI przewiduje ceny" nie jest.

### 4.4 Wskaźniki wyprzedzające, które warto testować

Nie zakładaj z góry, że działają — sprawdź korelację na swoich danych:

- ceny bunkra VLSFO (Rotterdam, Singapur)
- wykorzystanie zdolności przewozowych, blank sailings, księga zamówień statków
- czas oczekiwania na redzie z danych AIS — kongestia portowa
- PMI przemysłowe Chin, strefy euro, USA
- przeładunki w portach (Gdańsk i Gdynia publikują statystyki)
- stosunek zapasów do sprzedaży w handlu detalicznym USA i UE
- kurs USD/PLN — wpływa na koszt w złotówkach niezależnie od stawki w dolarach

## 5. Warstwa 3 — kontekstowa

Zdarzenia geopolityczne, strajki, ograniczenia żeglugowe, cła, sankcje. Zbierane z serwisów informacyjnych i baz zdarzeń, streszczane przez model językowy.

**Twarda zasada: ta warstwa nigdy nie produkuje liczby.** Produkuje alert z odnośnikiem do źródła i pytaniem do człowieka. Model streszcza i klasyfikuje, nie wnioskuje o cenach.

```
Alert: Ograniczenia przepustowości na kanale
Wpływ: relacje Azja–Wschodnie Wybrzeże USA
Twoja ekspozycja: 3 aktywne oferty, 2 otwarte zlecenia
Źródła: [link] [link]
→ Rozważ skrócenie ważności ofert na tych relacjach
```

Bez oceny „ceny wzrosną o 12%". Z listą twoich ofert, których to dotyczy.

## 6. Źródła danych i status prawny

Tu jest pułapka, o której trzeba wiedzieć przed napisaniem pierwszego scrapera.

| Źródło | Dostępność | Uwaga |
|---|---|---|
| **SCFI** | publikowany w piątki przez Shanghai Shipping Exchange, poziom zbiorczy publiczny | tylko eksport z Szanghaju do 15 regionów, **bez powrotów** |
| **WCI (Drewry)** | tygodniowo, w poniedziałek za poprzedni tydzień; poziom zbiorczy publiczny | 8 relacji, tylko FEU, miesza spot z kontraktami krótkoterminowymi. Metodologia opublikowana, ale mechanika wyliczeń nie |
| **CCFI** | poziom zbiorczy publiczny | dane historyczne i szczegółowe wymagają subskrypcji |
| **FBX (Freightos)** | 12 relacji | dane wyłącznie z platformy Freightos — obciążenie źródła |
| **XSI (Xeneta)** | miesięcznie | kontrakty krótko- i długoterminowe |
| Ceny bunkra | częściowo publiczne | |
| Przeładunki portowe | publiczne | Gdańsk, Gdynia, Rotterdam publikują |
| PMI, kursy, makro | publiczne API | FRED, Eurostat, NBP |
| Bazy zdarzeń informacyjnych | publiczne | GDELT i podobne |
| Ogłoszenia GRI/PSS | publiczne | strony armatorów |

### Ryzyko licencyjne — czytaj uważnie

Dane indeksowe są dostępne publicznie na poziomie zbiorczym, ale dane historyczne i szczegółowe wymagają subskrypcji. Konsekwencja dla ciebie:

**Możesz** pokazywać klientowi publiczny poziom zbiorczy z podaniem źródła. **Nie możesz** budować z niego własnej bazy historycznej i redystrybuować jej klientom SaaS jako funkcji produktu. To jest to samo ryzyko co przy redystrybucji stawek kontraktowych armatorów (zasada 9 w SPEC).

Bezpieczna architektura: klient wnosi własną subskrypcję Drewry albo Xenety, ty ją tylko konsumujesz w jego imieniu. Model „przynieś własne poświadczenia" działa tu identycznie jak przy armatorach — i masz go już w tabeli `carrier_credential`, wystarczy uogólnić na `external_data_credential`.

## 7. Model danych

```sql
market_indicator                 -- definicja wskaźnika
  id, code,                      -- SCFI_COMPOSITE, WCI_SHA_RTM, VLSFO_RTM
  name, unit, source, frequency,
  license_type,                  -- public | subscription | own_data
  is_redistributable bool        -- ← kontrola przed pokazaniem klientowi

market_observation
  id, indicator_id, observed_at, value, revision_of NULL
  source_url, fetched_at

market_event                     -- warstwa 3
  id, event_type,                -- gri | pss | blank_sailing | geopolitical
                                 -- regulatory | strike | canal | tariff
  title, summary,                -- streszczenie modelu
  effective_from, effective_to
  affected_lanes jsonb,          -- relacje, których dotyczy
  affected_carriers uuid[]
  amount NULL, currency NULL,    -- wypełnione TYLKO dla warstwy 1
  confidence, sources jsonb,     -- zawsze odnośniki
  layer smallint                 -- 1 | 2 | 3 ← determinuje prawa

lane_risk_score                  -- wynik dla wyceny
  id, organization_id, pol, pod, mode
  computed_at, valid_days
  risk_score,                    -- 0–100
  direction,                     -- up | flat | down | unknown
  drivers jsonb,                 -- co składa się na wynik
  confidence_interval jsonb

rate_forecast
  id, indicator_id NULL, lane_key NULL
  horizon_days, forecast_value, ci_low, ci_high
  model_name, model_version, generated_at

forecast_evaluation              -- ← uczciwość mierzalna
  id, forecast_id, actual_value, error_abs, error_pct
  baseline_error_pct,            -- błąd random walk
  beat_baseline bool, evaluated_at

external_data_credential         -- uogólnienie carrier_credential
  id, organization_id, provider, credentials_encrypted, scopes
```

## 8. Zastosowania produktowe — po co to komu

Cztery funkcje, w kolejności wartości:

### 8.1 Ryzyko ważności oferty — najważniejsza

Wystawiasz ofertę ważną 30 dni. Jeśli stawka zakupowa wzrośnie w tym czasie, marża znika, a zobowiązanie zostaje.

```
Oferta OF/2026/00847 — Gdynia → Szanghaj, ważna do 25.09
⚠ Ryzyko podwyższone (72/100)
   • GRI ogłoszony na 01.10: +800 USD/FEU  [warstwa 1]
   • Indeks na tej relacji +11% w trzy tygodnie  [warstwa 2]
→ Sugestia: skróć ważność do 20.09 albo dodaj klauzulę GRI
```

To jest funkcja, która wprost chroni pieniądze i którą łatwo wytłumaczyć spedytorowi w trzydzieści sekund.

### 8.2 Benchmark stawki zakupowej

Czy twoja stawka jest dobra na tle rynku. Wymaga danych licencjonowanych — działa w modelu „klient wnosi własną subskrypcję".

### 8.3 Timing: kontrakt czy spot

Kiedy zakontraktować, kiedy zostać na spocie. Decyzja podejmowana dziś na wyczucie, a warta dużych pieniędzy.

### 8.4 Alert ekspozycji

Zdarzenie rynkowe wiązane automatycznie z twoimi otwartymi ofertami i zleceniami. Nie „coś się dzieje w rejonie kanału", tylko „to dotyczy tych pięciu twoich zleceń".

## 9. Odpowiednik dla transportu drogowego

Ta sama architektura, inne wskaźniki:

| Warstwa | Sygnały drogowe |
|---|---|
| **1. Deterministyczna** | ceny ON (publikowane), stawki myta i ich zmiany, płace minimalne kierowców w krajach tranzytu wg pakietu mobilności, zmiany akcyzy, terminy zakazów ruchu, kalendarz świąt w krajach docelowych |
| **2. Statystyczna** | sezonowość na twoich kierunkach z własnych danych, relacja podaż/popyt z giełd transportowych, wskaźnik pustych powrotów per kierunek |
| **3. Kontekstowa** | blokady graniczne, protesty przewoźników, zmiany regulacyjne, warunki drogowe |

Dla drogi warstwa 1 jest jeszcze mocniejsza niż w morzu: **cena paliwa to zwykle 25–35% kosztu przejazdu i jest publikowana codziennie**. Model kosztu przejazdu z automatyczną aktualizacją dopłaty paliwowej to funkcja deterministyczna o natychmiastowym zwrocie — i wpina się wprost w twój silnik alokacji z Aneksu 1.

## 10. Stack

| Element | Wybór |
|---|---|
| Prognozowanie | `Nixtla/statsforecast` (start), `unit8co/darts` (porównanie modeli), `Nixtla/neuralforecast` (dopiero przy długiej historii) |
| Ewaluacja i dryf | `mlflow` (rejestr modeli), `evidently` (dryf danych) |
| Pozyskiwanie treści | `trafilatura` (ekstrakcja artykułów), `scrapy`, RSS |
| Zdarzenia globalne | GDELT jako darmowa baza zdarzeń informacyjnych |
| Makro | FRED API, Eurostat, NBP |
| Jakość danych | `great-expectations` — obserwacja poza zakresem sanity nie wchodzi do bazy |
| Klasyfikacja zdarzeń | model językowy z ustrukturyzowanym wyjściem, warstwa 3 |
| Harmonogram | `apscheduler` — pobrania cykliczne |

## 11. Kiedy to budować

**Nie teraz.** Ten moduł ma sens dopiero, gdy masz historię własnych stawek — bo twoje dane są cenniejsze predykcyjnie niż jakikolwiek indeks globalny.

| Kiedy | Co |
|---|---|
| Tydzień ~30, po pierwszym płacącym kliencie | Warstwa 1: zbieranie ogłoszeń GRI/PSS i blank sailings, wiązanie z relacjami. Zero ML |
| Tydzień ~34 | Wzory dopłat: BAF od bunkra, ETS, CAF. Automatyczna aktualizacja |
| Tydzień ~38 | Alert ekspozycji (8.4) — łączy warstwę 1 z twoimi ofertami |
| Po 12 miesiącach danych | Warstwa 2 z obowiązkowym backtestingiem |
| Nigdy bez subskrypcji klienta | Benchmark rynkowy |

**Kolejność ma znaczenie.** Warstwa 1 wdrożona pierwsza daje realną wartość i zbiera dane, na których warstwa 2 będzie mogła się kiedyś oprzeć. Warstwa 2 wdrożona pierwsza da model wytrenowany na cudzych danych, którego skuteczności nie zmierzysz.

Dopisz do decyzji otwartych w D8 jako punkt 7: **czy benchmark rynkowy w ogóle wchodzi w zakres**, biorąc pod uwagę, że wymaga, by klient miał własną subskrypcję Drewry lub Xenety.
