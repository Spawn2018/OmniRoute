# Aneks 12 — Automatyczne pozyskiwanie stawek i silnik narzutów

---

# CZĘŚĆ 1 — AKCEPTACJA CZŁOWIEKA JAKO ZASADA

## 1.1 Stanowisko

Domyślnie: **oferta wymaga zatwierdzenia człowieka. Pozyskiwanie stawek jest w pełni automatyczne.**

Uzasadnienie:

- opóźnienie bierze się z szukania stawek, nie z wysyłki. Automatyzując pierwsze, zyskujesz 95% korzyści
- ryzyko jest asymetryczne — błędna oferta wysłana automatycznie kosztuje pieniądze i wiarygodność, a zatwierdzenie kosztuje sekundy
- odpowiedzialność handlowa zostaje po stronie człowieka, co ma znaczenie także prawne
- klient kupujący system łatwiej mu zaufa, wiedząc, że nic nie wychodzi bez zatwierdzenia

Ale to działa tylko przy jednym warunku:

## 1.2 Zatwierdzenie musi być jednym dotknięciem

Jeśli akceptacja wymaga zalogowania się do systemu, funkcja traci sens. Projektuj tak:

```
📱 Powiadomienie push, 22:15

   Oferta gotowa — Meblexport Sp. z o.o.
   Gdynia → Callao · 2×40HC
   3 095 USD · marża 11,2%
   
   Stawka: Andes Cargo, 4 dni temu, zweryfikowana
   ⚠ Brak kodu HS w zapytaniu
   
   [ Wyślij ]      [ Otwórz ]      [ Odrzuć ]
```

Handlowiec przy telefonie wysyła ofertę o 22:16. Konkurencja odpowiada nazajutrz po południu. **Przewaga jest praktycznie taka sama jak przy pełnym automacie, a ryzyka nie ma.**

## 1.3 Wybór użytkownika — trzy tryby per klient i relacja

```sql
quote_automation_policy
  id, organization_id
  customer_party_id NULL,        -- NULL = domyślna
  lane_pattern NULL
  mode,                          -- manual | assisted | auto
  -- manual:   system nic nie robi, handlowiec wycenia od zera
  -- assisted: system przygotowuje projekt, człowiek zatwierdza  ← DOMYŚLNE
  -- auto:     wysyłka bez zatwierdzenia, w granicach reguł
  auto_conditions jsonb,         -- warunki z Aneksu 11, sekcja 8
  notify_channels text[]         -- push | email | slack
```

Tryb `auto` zostaje dostępny, ale jako świadomy wybór, włączany per klient i relacja — dla ruchu powtarzalnego, gdzie wszystko jest znane. Nie jako domyślny.

---

# CZĘŚĆ 2 — AUTOMATYCZNE ODPYTYWANIE ARMATORÓW

Twoja propozycja: przy każdym zapytaniu system sam pyta wszystkich armatorów mających serwis na tej relacji.

## 2.1 Skąd wiadomo, kto ma serwis

```sql
carrier_service                  -- pokrycie relacji przez armatora
  id, carrier_party_id
  service_name,                  -- nazwa pętli, np. AE7
  pol, pod, via
  transit_days, frequency,       -- tygodniowo, co dwa tygodnie
  equipment_types text[]
  source,                        -- api_coverage | schedules | booking_history
  last_verified_at, is_active
```

Trzy źródła, w kolejności wiarygodności:

**API pokrycia.** Hapag-Lloyd udostępnia specyfikację obsługiwanych relacji, typów kontenerów i rodzajów ładunku — pobierasz to raz i odświeżasz cyklicznie. To najlepsze źródło i kolejny powód, żeby zacząć integracje właśnie od nich.

**API rozkładów.** Maersk i CMA CGM zwracają rozkłady rejsów — z nich wynika, kto pływa skąd dokąd.

**Własna historia bookingów.** Jeśli zabookowałeś tę relację u danego armatora, to znaczy, że ma serwis. Buduje się samo.

## 2.2 Przepływ

```
Zapytanie: Gdynia → Callao
        ↓
Kto ma serwis? → 4 armatorów
        ↓
Kto ma poświadczenia tego tenanta? → 2 z 4
        ↓
RÓWNOLEGLE, z limitem czasu 5 s:
  ├─ Hapag Quick Quotes Spot   → 2 890 USD  ✓  1,8 s
  ├─ Maersk Offers             → 2 750 USD  ✓  3,1 s
  ├─ CMA CGM                   → brak poświadczeń  ⚙ skonfiguruj
  └─ MSC                       → brak poświadczeń  ⚙ skonfiguruj
        ↓
RÓWNOLEGLE, natychmiast:
  └─ Baza stawek z cenników    → Andes Cargo 2 340 USD (4 dni)
                                 Hapag cennik 2 510 USD (34 dni) ⚠
```

Brak poświadczeń pokazuj jako możliwość konfiguracji, nie jako błąd — to jest naturalny moment, w którym klient sam chce dodać kolejnego armatora.

## 2.3 Ograniczenia, które trzeba obsłużyć

**Limity zapytań.** Sześciu armatorów × pięćdziesiąt zapytań dziennie to trzysta wywołań. Limity są per konto abonenta, więc wyczerpanie ich blokuje całą organizację. Konieczne: kolejka z priorytetami, licznik zużycia widoczny dla użytkownika, degradacja do cennika przy wyczerpaniu.

**Cache relacji.** Ta sama relacja i typ kontenera odpytane w ciągu godziny — użyj poprzedniej odpowiedzi z widoczną etykietą czasu. Ceny spot nie zmieniają się co dziesięć minut.

**Limit czasu.** Adapter nie odpowie w pięć sekund — pokazujesz resztę. Odpowiedź, która przyjdzie później, dopina się do zapytania i generuje powiadomienie, jeśli jest tańsza od wybranej.

**Kompletność.** CMA CGM w API cenowym zwraca wyłącznie fracht, bez opłat lokalnych, inland i DDSM. Oferta z tego źródła musi być oznaczona jako niepełna i uzupełniona z twojej bazy opłat lokalnych — inaczej wygląda najtaniej i jest najdroższa.

## 2.4 Kiedy odpytywać

| Moment | Zachowanie |
|---|---|
| Wpłynięcie zapytania | automatycznie, jeśli relacja ma skonfigurowanych armatorów |
| Otwarcie zapytania przez handlowca | odśwież, jeśli cache starszy niż 60 min |
| Kliknięcie „odśwież stawki" | zawsze, ręcznie |
| Przed wysłaniem oferty | sprawdź, czy stawka nie wygasła |

---

# CZĘŚĆ 3 — SILNIK NARZUTÓW

Twój punkt drugi jest strategicznie najciekawszy w całym aneksie. To nie jest kalkulator — to narzędzie pozycjonowania cenowego.

## 3.1 Po co to naprawdę służy

Klient korporacyjny zna cenę frachtu morskiego. Ma benchmark, pyta trzech spedytorów, porównuje jedną liczbę. **Nie zna natomiast ceny odwozu z Callao do Limy, odprawy celnej ani opłaty dokumentacyjnej.**

Możliwość ustawienia zerowego narzutu na fracht i zarobku na usługach otwiera dokładnie te drzwi, o których piszesz: klientów obsługiwanych dotąd bezpośrednio przez armatorów, którzy mają własny kontrakt frachtowy i potrzebują wyłącznie obsługi lokalnej.

## 3.2 Model danych

```sql
markup_rule
  id, organization_id
  name, priority                 -- kolejność stosowania
  
  -- ZAKRES
  scope_type,                    -- all_in | charge_code | charge_category
                                 -- charge_side | mode
  scope_ref,                     -- kod, kategoria albo origin/freight/destination
  customer_party_id NULL,
  lane_pattern NULL,             -- "PL*→PE*"
  mode NULL,
  
  -- METODA
  method,                        -- percent | fixed_amount | fixed_per_unit
                                 -- target_margin | fixed_sell_price
  value numeric,
  per_unit,                      -- container | bl | shipment | wm | kg
  
  -- OGRANICZENIA
  min_amount, max_amount,        -- widełki narzutu
  min_margin_pct,                -- próg, poniżej którego nie schodzi
  rounding,                      -- do 5 / 10 / 50 jednostek
  
  -- PREZENTACJA
  display_mode,                  -- visible | folded_into_all_in | hidden
  
  valid_from, valid_to, is_active
```

## 3.3 Metody — i różnica, którą wszyscy mylą

**Narzut a marża to nie to samo.** Narzut 20% na koszcie 100 daje cenę 120 i marżę 16,7%. Marża 20% na cenie daje cenę 125 i narzut 25%.

System musi pozwalać wpisać jedno i pokazywać oba, na żywo:

```
Ocean freight    koszt 2 340    narzut  0%  →  2 340    marża  0,0%
DTHC Callao      koszt   310    narzut 25%  →    388    marża 20,0%
Odwóz Lima       koszt   240    narzut 40%  →    336    marża 28,6%
Odprawa celna    koszt   180    narzut 30%  →    234    marża 23,1%
D/O fee          koszt    85    narzut 20%  →    102    marża 16,7%
──────────────────────────────────────────────────────────────────
RAZEM            koszt 3 155                    3 400    marża  7,2%
                                          narzut łączny  7,8%
```

Ta tabela jest ekranem, na którym handlowiec spędzi najwięcej czasu. Zaprojektuj ją porządnie: edycja w miejscu, przeliczanie na żywo, obsługa klawiatury, wklejanie z Excela.

## 3.4 Poziomy i ich kolejność

Reguły stosują się kaskadowo, od najbardziej szczegółowej:

```
1. Narzut na konkretnej pozycji, ustawiony ręcznie w tej ofercie
2. Reguła dla klienta + relacji + kodu opłaty
3. Reguła dla klienta + kodu opłaty
4. Reguła dla kodu opłaty
5. Reguła dla kategorii (origin / freight / destination)
6. Reguła all-in dla klienta
7. Reguła domyślna organizacji
```

Handlowiec musi widzieć, **która reguła zadziałała** — najeżdżasz na pozycję, widzisz „reguła: Meblexport / opłaty destination / 25%". Bez tego nikt nie zaufa automatycznemu cennikowi.

## 3.5 Kontrakt frachtowy klienta — otwarcie na korporacje

To jest funkcja, która wynika wprost z twojego pomysłu i której nie ma nikt w tym segmencie.

Duży klient ma własny kontrakt z armatorem. Nie potrzebuje twojego frachtu — potrzebuje obsługi. Model musi to unieść:

```sql
-- rozszerzenie rate_line
  buy_source,                    -- own_contract | agent | carrier_api
                                 -- customer_contract  ← nowe
  customer_contract_id NULL      -- kontrakt należący do klienta
```

Wtedy:

```
Ocean freight    kontrakt klienta MSC    2 100 USD   narzut  0%   → 2 100
                 (przenoszone bez marży, do informacji)
DTHC             twój koszt                310 USD   narzut 25%   →   388
Odprawa                                    180 USD   narzut 30%   →   234
Odwóz                                      240 USD   narzut 40%   →   336
──────────────────────────────────────────────────────────────────────
                                                                    3 058
Twoja marża: 288 USD na usługach, 0 na frachcie
```

Klient widzi, że nie dokładasz do jego frachtu — co buduje zaufanie — a ty zarabiasz na tym, czego nie robi za niego armator. To jest dokładnie model, którym duzi spedytorzy zdobywają konta obsługiwane dotąd bezpośrednio.

## 3.6 Analiza: gdzie naprawdę zarabiamy

Skoro marża jest rozbita na pozycje, powstaje raport, którego nikt nie ma:

```
STRUKTURA MARŻY — ostatnie 12 miesięcy

Kategoria              Obrót      Marża     Udział w marży
──────────────────────────────────────────────────────────
Fracht morski      4 820 000 zł   118 000 zł      9%
Opłaty origin        890 000 zł   214 000 zł     17%
Opłaty destination   740 000 zł   468 000 zł     37%
Transport lądowy   1 210 000 zł   396 000 zł     31%
Odprawy celne        320 000 zł    78 000 zł      6%
──────────────────────────────────────────────────────────
                                1 274 000 zł
```

Wniosek strategiczny: 68% marży pochodzi z opłat destination i transportu lądowego, przy 24% udziału w obrocie. Fracht generuje trzy czwarte obrotu i 9% zysku.

To zmienia sposób prowadzenia firmy — i jest dokładnie tym, co miałeś na myśli pisząc o kontroli, gdzie jesteśmy mocni. Ten raport uzasadnia decyzję o zerowym narzucie na fracht liczbami, a nie przeczuciem.

## 3.7 Prezentacja klientowi

Trzy tryby per pozycja, ustawiane regułą i nadpisywalne ręcznie:

- **widoczna** — klient widzi pozycję i kwotę
- **zwinięta w all-in** — wliczona w jedną kwotę zbiorczą
- **ukryta** — pozycja wewnętrzna, np. koszt finansowania z Aneksu 6

Ten sam wariant oferty da się wysłać w dwóch układach: rozbitym dla klienta chcącego szczegółów i all-in dla klienta chcącego jednej liczby. Bez przeliczania czegokolwiek.

## 3.8 Bezpieczniki

- **próg minimalnej marży** per klient i relacja, z ostrzeżeniem przed wysłaniem
- **zerowy narzut wymaga świadomego działania** — pole ustawione na zero pokazuje adnotację, żeby nie było skutkiem pomyłki
- **ostrzeżenie o odchyleniu** — pozycja wyceniona znacząco poniżej mediany z ostatnich ofert na tej relacji (to jest ten sam mechanizm co przy CV 80,5% z twoich danych drogowych)
- **historia zmian narzutu** w audycie — kto obniżył marżę i kiedy

## 3.9 Nakład

| Element | Dni |
|---|---|
| `markup_rule` + kaskada + rozstrzyganie priorytetów | 4 |
| Ekran pozycji z edycją w miejscu i przeliczaniem | 4 |
| Tryby prezentacji i generowanie PDF w dwóch układach | 2 |
| `buy_source: customer_contract` | 2 |
| Raport struktury marży | 2 |
| Bezpieczniki i ostrzeżenia | 2 |

Szesnaście dni. Z tego kontrakt frachtowy klienta i raport struktury marży to dwie funkcje, które mają największy potencjał sprzedażowy w całym systemie — pierwsza otwiera segment korporacyjny, druga zmienia sposób, w jaki właściciel patrzy na własną firmę.
