# Aneks 15 — Opłaty portowe, agregatorzy, kolej, LCL

---

# 1. BAZA OPŁAT PORTOWYCH

## 1.1 Dlaczego to trudniejsze niż stawka frachtowa

Masz rację co do warunkowości. Opłata w porcie docelowym potrafi zależeć od:

- **portu i kraju nadania** — najczęstszy przypadek, który wskazałeś
- armatora i jego kontraktu serwisowego
- typu kontenera (reefer, ponadgabaryt, DG)
- tego, czy fracht jest opłacony z góry, czy przez odbiorcę
- tego, czy przesyłka jest bezpośrednia, czy z przeładunkiem
- grupy towarowej

I najważniejsze: reguła może opłatę **znosić**, a nie tylko zmieniać jej wysokość. „CIC nie jest naliczany dla kontenerów z Europy" to nie jest brak stawki — to jest reguła o wartości zerowej i trzeba ją zapisać jawnie, inaczej system będzie ciągle pytał agenta o coś, czego nie ma.

## 1.2 Model warunkowy

```sql
port_charge_rule
  id, organization_id
  
  -- GDZIE I CO
  port_unlocode, side,          -- origin | destination
  charge_code
  carrier_party_id NULL,        -- NULL = dowolny armator
  
  -- WARUNKI (NULL = dowolne)
  origin_port NULL,
  origin_country NULL,
  origin_region NULL,           -- EUR | ASIA | NAM | SAM | AFR | OCE
  dest_country NULL,
  container_type NULL,
  commodity_group NULL,
  is_transshipment NULL,
  freight_payment NULL,         -- prepaid | collect
  service_contract NULL,
  
  -- WARTOŚĆ
  is_applicable bool,           -- ← FALSE oznacza: nie nalicza się
  amount, currency, basis,
  min_amount, max_amount,
  
  -- ROZSTRZYGANIE
  specificity_score int,        -- wyliczany z liczby wypełnionych warunków
  valid_from, valid_to,
  
  -- POCHODZENIE
  source,                       -- tariff | invoice | agent_quote
                                -- carrier_api | manual
  source_ref jsonb, confidence, verified_by
```

**Rozstrzyganie konfliktów przez specyficzność.** Wygrywa reguła z największą liczbą dopasowanych warunków — jak w kaskadzie stylów. Reguła „DTHC w Callao dla kontenerów z Europy, armator Hapag, 40HC" bije regułę „DTHC w Callao".

Przy remisie specyficzności decyduje świeższe `valid_from`, a przy dalszym remisie system pyta człowieka i zapisuje decyzję jako nową regułę.

## 1.3 Automatyzacja budowy bazy — pięć źródeł

Tu jest odpowiedź na „zautomatyzować najmocniej jak to możliwe".

**Źródło 1 — taryfy publikowane przez armatorów.** Duzi armatorzy publikują wykazy opłat lokalnych per port, zwykle jako PDF albo strony z tabelami. To jest materiał dla twojego istniejącego pipeline'u ekstrakcji. Pobieranie cykliczne, wykrywanie zmian przez hash, przetwarzanie tylko przy zmianie.

**Źródło 2 — odpowiedzi API armatorów.** Maersk zwraca ceny wraz z dopłatami. Każde zapytanie spot to darmowa próbka struktury opłat w danym porcie dla danej relacji. Zapisuj rozbicie, nie tylko sumę.

**Źródło 3 — oferty agentów.** Każda odpowiedź na twoje zapytanie zawiera opłaty lokalne w porcie docelowym, z kontekstem relacji. To jest już w twoim systemie.

**Źródło 4 — faktury. I to jest najmocniejsze.**

Faktura od agenta albo armatora zawiera opłaty, które **faktycznie zostały naliczone**, dla konkretnego portu, konkretnego armatora i konkretnej relacji nadania. To nie jest deklaracja z taryfy — to jest fakt.

```
Faktura agenta za zlecenie GD/2026/00412
  Gdynia → Callao, Hapag, 40HC
  
  DTHC              310 USD  → reguła: Callao/DTHC/HAPAG/origin_region=EUR/40HC
  D/O fee            85 USD  → reguła: Callao/DO-FEE/HAPAG
  CIC                 0 USD  → reguła: Callao/CIC/origin_region=EUR
                               is_applicable = FALSE  ← wiedza negatywna
```

Mechanizm rozliczania faktury z wyceną z Aneksu 4 **już porównuje te dane pozycja po pozycji**. Wystarczy, żeby przy okazji zapisywał regułę. Zero dodatkowej pracy operatora, a baza rośnie z każdym zamkniętym zleceniem.

Po roku masz bazę opłat portowych opartą na tym, co realnie zapłaciłeś — czyli dokładniejszą od jakiejkolwiek taryfy.

**Źródło 5 — uczenie negatywne z zapytań.** Agent odpisuje „CIC nie dotyczy przesyłek z Europy" — ekstraktor zapisuje regułę zerową. To jest ta sama wiedza, którą dziś ma w głowie doświadczony spedytor i która znika, gdy odchodzi z firmy.

## 1.4 Priorytet zaufania

```
faktura (potwierdzona)  >  API armatora  >  taryfa publikowana
                        >  oferta agenta  >  wpis ręczny
```

Reguła z faktury nadpisuje regułę z taryfy, bo taryfa mówi, co powinno być, a faktura co było.

## 1.5 Wykorzystanie przy wycenie

Silnik wyceny, znając POL, POD, armatora i typ kontenera, dobiera zestaw opłat automatycznie — łącznie z tymi, które się nie naliczają. Do `quotation_gap` trafiają wyłącznie opłaty, o których **nic nie wiadomo**, a nie te, o których wiadomo, że ich nie ma.

To znacząco zmniejsza liczbę zapytań do agentów, bo dziś pytasz o wszystko za każdym razem.

---

# 2. AGREGATORZY — DANE

## 2.1 Zebrane informacje

| | Zasięg | Model opłat | Uwagi |
|---|---|---|---|
| **cargo.one** | ponad 40 linii lotniczych, stawki agentów z ponad 30 krajów | **Bezpłatny dla spedytora** — model oparty wyłącznie na prowizji linii lotniczej, ceny pokazywane all-in, rozliczenie przez CASS. Plan Basic darmowy, Pro płatny (zaawansowane zarządzanie stawkami, oferty PDF z szablonami, dostęp do stawek agentów), Enterprise negocjowany | **Wyłącznie fracht lotniczy.** Do morza nieprzydatny. Ponad 1 900 biur spedycyjnych korzysta |
| **WebCargo / Freightos for Forwarders** | Platforma Freightos łączy **77 przewoźników lotniczych i morskich**, ponad 1,4 mln transakcji rocznie, ponad 4 000 spedytorów w ponad 10 000 biur. Po stronie morskiej: bezpośrednia integracja bookingowa z **kluczowymi armatorami**, nie wszystkimi | Cennik niepubliczny | Nazwa WebCargo przeszła w „Freightos for Forwarders". Zarządzanie stawkami, ofertowanie, booking, portal klienta, jednolity widok lotnictwo–morze |
| **Freightify** | Własne API: **ponad 10 armatorów**. Usługa Freightify Link rozszerza pokrycie danych | Cennik niepubliczny; przy Freightify Link opłaty za połączenia z armatorami i wykorzystanie API | Certyfikat ISO 27001. Deklaruje skrócenie czasu pozyskiwania stawek nawet o 92%. Profil klienta: spedytor 50–300 osób. Użytkownicy zgłaszają okresowe spowolnienia i błędy platformy |
| **SeaRates** (grupa DP World) | Stawki morskie, lotnicze i lądowe; API Logistics Explorer, API zarządzania stawkami, API indeksu frachtowego | Cennik niepubliczny — token API wydaje opiekun handlowy, więc sprzedaż prowadzona indywidualnie | Kalkulator w białej etykiecie do osadzenia na stronie; możliwość udostępniania stawek sieci partnerów |

## 2.2 Wnioski

**Żaden nie publikuje cen.** Wszyscy sprzedają przez handlowca, z ceną zależną od liczby użytkowników, wolumenu i modułów. Nie podam ci kwot, bo każda byłaby zmyślona — ale mogę powiedzieć, jak je wydobyć.

**Zasięg jest mniejszy, niż sugeruje marketing.** Freightify deklaruje w API ponad dziesięciu armatorów. Freightos łączy 77 przewoźników, ale **łącznie lotniczych i morskich**. To nie jest „wszyscy armatorzy świata" — to kilkunastu do dwudziestu kilku po stronie morskiej.

**To potwierdza strategię kanałową z Aneksu 14.** Agregator daje ci kilkunastu armatorów bez pisania integracji. Reszty świata i tak nie dostaniesz inaczej niż mailem — a mechanizm mailowy budujesz sam i jest darmowy.

## 2.3 Jak negocjować

Pytania, na które musisz mieć odpowiedź na piśmie przed podpisaniem:

1. **Lista armatorów po stronie morskiej — imiennie.** Nie „kluczowi armatorzy", tylko nazwy. I osobno: u ilu z nich dostępny jest booking, a u ilu tylko stawki
2. **Czy widzę swoje stawki kontraktowe, czy tylko ich publiczne**
3. **Model opłat:** abonament, per użytkownik, per zapytanie, per booking, prowizja
4. **Czy koszt rośnie z wolumenem** — przy automatycznym odpytywaniu przy każdym zapytaniu klienta liczba wywołań będzie duża
5. **Limity zapytań** i co się dzieje po przekroczeniu
6. **Czy dostęp API jest w cenie, czy jako dodatek** — to jest najczęstsza pułapka
7. **Okres wypowiedzenia i eksport danych** przy zakończeniu współpracy

Punkt czwarty jest kluczowy przy twoim modelu. Automat odpytujący sześciu armatorów przy każdym zapytaniu generuje wolumen, który przy rozliczeniu za wywołanie robi się kosztem znaczącym.

## 2.4 Rekomendacja

Rób jedno i drugie, ale w tej kolejności:

1. **Bezpośrednio: Hapag, Maersk, CMA CGM** — masz kontrolę, brak pośrednika, brak opłat za wywołanie
2. **Kanał mailowy dla całej reszty świata** — darmowy, nieograniczony zasięg
3. **Agregator dopiero wtedy**, gdy klienci zaczną płacić i będziesz wiedział, których armatorów faktycznie brakuje

Odwrotna kolejność oznacza płacenie abonamentu za coś, czego jeszcze nie umiesz wykorzystać.

---

# 3. KOLEJ DOWOZOWA I ODWOZOWA

## 3.1 Struktura stawki

Odcinek kolejowy to nie jedna liczba, tylko cztery:

```
Terminal morski → terminal lądowy → drzwi klienta

  1. THC w terminalu morskim        per kontener
  2. Przewóz kolejowy               per kontener, terminal → terminal
  3. Obsługa w terminalu lądowym    per kontener
  4. Dowóz drogowy z terminalu      per kontener + km
  + ewentualnie: postojowe, przechowanie, prąd do reefera
```

Klient chce jednej liczby. System musi umieć złożyć ją z czterech i pokazać rozbicie na żądanie — a to jest dokładnie mechanizm `charge_code` z narzutami per pozycja z Aneksu 12.

```sql
rail_rate
  id, organization_id, operator_party_id
  origin_terminal_id, destination_terminal_id
  container_type, direction,     -- import | export
  amount, currency, basis
  includes_terminal_handling bool,
  min_volume_teu,                -- stawka może zależeć od wolumenu
  valid_from, valid_to, validity_basis
  source_ref
```

## 3.2 Automatyzacja

Operatorzy intermodalni w Polsce i Europie w większości nie mają publicznych API. Mają portale i skrzynki bookingowe.

**Kanał mailowy z Aneksu 9 obsługuje ich bez jednej nowej linijki kodu.** Operator kolejowy to kolejny wpis w `carrier_channel` z typem `email`. Cenniki intermodalne są przy tym łatwiejsze do sparsowania niż morskie — to zwykle regularna macierz terminal × typ kontenera.

Gdzie operator ma portal z rozkładem i wolnymi miejscami, dołóż `browser-use` na poświadczeniach klienta. Gdzie ma API — adapter jak przy armatorze.

## 3.3 Porównanie gałęzi w ofercie

Funkcja, która to spina i której prawie nikt nie ma:

```
Odwóz Gdynia → Poznań, 1×40HC

  Droga         1 240 zł   18 h   ~340 kg CO₂
  Kolej + dowóz   980 zł   36 h   ~ 95 kg CO₂  ✓
  
  Kolej: odjazdy PN/ŚR/PT, najbliższy 4.09, cut-off 3.09 12:00
```

Dane emisyjne idą wprost do modułu śladu węglowego. Dla klienta objętego raportowaniem to bywa argument silniejszy od ceny.

---

# 4. KOLEJ Z CHIN

## 4.1 Dlaczego warto

Tranzyt istotnie krótszy od morza przy koszcie istotnie niższym od lotu. Dla ładunków czasowo wrażliwych to realna trzecia opcja, a Polska leży na głównym wejściu do UE — Małaszewicze są dla twoich klientów naturalnym punktem.

Możliwość pokazania w jednej ofercie **morza, kolei i lotu obok siebie** to funkcja, której nie ma prawie żaden system w tym segmencie.

## 4.2 Specyfika, którą trzeba zamodelować

```sql
rail_service                     -- rozszerzenie z Aneksu 14
  ...
  corridor,                      -- northern | middle | southern
  gauge_change_point,            -- punkt przeładunku na inny rozstaw
  gauge_change_hours,
  transit_countries text[],      -- ← istotne dla sankcji
  is_lcl_available,
  cfs_origin_id, cfs_destination_id
```

**Rozstaw szyn.** Na granicy wschodniej UE następuje przeładunek na inny rozstaw. To dodatkowy czas i koszt, i musi być osobną pozycją, nie ukryte w stawce.

**Kraje tranzytu a sankcje.** To jest punkt, którego nie wolno pominąć. Korytarz północny prowadzi przez kraje objęte różnymi reżimami sankcyjnymi, korytarz środkowy przez Morze Kaspijskie je omija — kosztem czasu i ceny.

**System musi sprawdzać trasę wobec list sankcyjnych z Aneksu 13, nie tylko strony transakcji.** Ładunek dopuszczalny, kontrahent czysty, a trasa prowadząca przez terytorium objęte restrykcjami — to jest realne ryzyko prawne dla twojego klienta i funkcja, która sama uzasadnia zakup systemu.

```sql
route_sanctions_check
  id, quotation_id, rail_service_id
  transit_countries text[]
  restricted_countries text[]
  risk_level, checked_at, list_versions jsonb
```

**Sezonowość i zatory.** Przepustowość przejść granicznych bywa ograniczona, terminy się wydłużają. To dane do modułu rynkowego z Aneksu 2.

## 4.3 Drobnica kolejowa z Chin

Konsolidacja w terminalu chińskim, dekonsolidacja w Polsce. Struktura stawki jak przy LCL morskim — podstawa W/M — ale z terminalami zamiast portów.

Ci sami operatorzy zwykle oferują i FCL, i LCL, więc to jedno zapytanie z dwoma wariantami, nie dwa procesy.

## 4.4 Integracja

Operatorzy korytarza Chiny–Europa nie mają API. Kanał mailowy, portale u nielicznych. Rozkłady odjazdów bywają publikowane — warto je pobierać cyklicznie, bo pozwalają pokazać klientowi konkretną datę zamiast „około trzech tygodni".

---

# 5. DROBNICA MORSKA

## 5.1 Kto jest dostawcą

Przy LCL kluczowi nie są armatorzy, tylko **konsolidatorzy** — NVOCC prowadzące własne serwisy drobnicowe między terminalami CFS. Kilku dużych działa globalnie, wielu regionalnie. Część większych ma portale ze stawkami online.

To zmienia kolejność integracji: jeśli robisz dużo drobnicy, konsolidatorzy są ważniejsi od armatorów numer cztery i pięć.

## 5.2 Specyfika stawki

```sql
lcl_rate
  id, organization_id, consolidator_party_id
  cfs_origin_id, cfs_destination_id
  service_name, frequency,       -- np. tygodniowo, wtorek
  transit_days
  
  rate_per_wm, currency,
  min_charge,                    -- minimum, zwykle 1–2 W/M
  wm_ratio,                      -- domyślnie 1 t = 1 CBM
  
  max_single_piece_kg,
  max_dimensions jsonb,
  accepts_dg, accepted_classes text[]
  
  valid_from, valid_to
```

**Wagę obliczeniową liczy kod, nie model językowy:**

```
chargeable_wm = max(waga_w_tonach, objętość_w_cbm)
jeżeli chargeable_wm < min_charge → min_charge
```

Wygląda trywialnie, a jest jednym z częstszych źródeł błędów w ofertach — bo stosunek W/M bywa inny niż 1:1 u niektórych konsolidatorów i na niektórych relacjach.

**Cut-off CFS** jest wcześniejszy niż bramowy dla FCL, bo towar musi trafić do magazynu konsolidacyjnego przed załadunkiem kontenera. Do łańcucha dat z Aneksu 14 dochodzi kolejne ogniwo.

**Dopłaty specyficzne dla LCL:** obsługa CFS w obu portach, opłata konsolidacyjna, dekonsolidacja, składowanie po darmowym okresie, dopłaty za ponadgabaryt i nadwagę pojedynczej sztuki.

## 5.3 Automatyzacja

Tak samo jak wszędzie: portal albo API u dużych, kanał mailowy u reszty. Cenniki drobnicowe są regularne — macierz relacji CFS × stawka W/M plus zakładka z dopłatami — więc dla ekstraktora są łatwiejsze niż cenniki FCL.

## 5.4 Funkcja, której nikt nie ma: LCL kontra FCL

```
Ładunek: 18 CBM, 4 200 kg, Gdynia → Callao

  LCL   18 W/M × 68 USD  =  1 224 USD  + lokalne 340 = 1 564 USD   38 dni
  FCL   20DV                              all-in     = 1 890 USD   32 dni
  
  → Różnica 326 USD. Przy 22 CBM FCL byłby tańszy.
  → Próg opłacalności na tej relacji: 20,4 CBM
```

Spedytor liczy to w głowie albo wcale. Automatyczne pokazanie progu opłacalności przy każdym zapytaniu drobnicowym to funkcja tania w budowie i bardzo widoczna dla klienta — a przy okazji często zwiększa twoją marżę, bo FCL jest zwykle prostszy operacyjnie.

---

# 6. KOLEJNOŚĆ

| Priorytet | Zakres | Uzasadnienie |
|---|---|---|
| 1 | **Opłaty portowe uczące się z faktur** | Zero dodatkowej pracy, mechanizm rozliczania faktur już istnieje |
| 2 | **LCL: struktura stawki i próg FCL** | Prosta matematyka, duża widoczność dla klienta |
| 3 | **Kolej dowozowa kanałem mailowym** | Mechanizm istnieje, dotyczy większości zleceń |
| 4 | Porównanie droga/kolej z emisją | Wynika z punktu 3 |
| 5 | Konsolidatorzy LCL — portale i API | Po ustaleniu, ilu obsługujesz |
| 6 | Kolej z Chin | Wymaga sprawdzania sankcji trasy — buduj po module sankcyjnym |
| 7 | Agregator | Dopiero gdy wiesz, których armatorów brakuje |
