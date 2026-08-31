# Aneks 8 — Sieci spedycyjne i katalog agentów

Cel: pracownik działu pricingu wybiera agenta w kraju docelowym i wysyła zapytanie ofertowe dwoma kliknięciami, zamiast szukać w katalogu sieci, przepisywać adres i pisać maila od zera.

---

## 1. Stan faktyczny — czego nie ma

Zanim projektowanie: **żadna z dużych sieci spedycyjnych nie udostępnia publicznego API do katalogu członków.** Ani WCA, ani Globalia, ani JCtrans, ani Conqueror, ani Cargo Connections. Katalog jest korzyścią członkowską dostępną po zalogowaniu.

Dodatkowo katalogi członków są w Unii chronione **prawem sui generis do baz danych**. Oznacza to, że masowe pobranie zawartości jest naruszeniem nawet wtedy, gdy pojedyncze dane — nazwa firmy, adres, telefon — same w sobie nie podlegają ochronie. Scraping katalogu i wbudowanie go w produkt SaaS to ryzyko, którego nie chcesz brać jako jednoosobowy dostawca.

**Ale to nie jest przeszkoda.** Twój klient jest członkiem sieci i ma legalny dostęp do katalogu. Wzorzec jest dokładnie ten sam, który stosujemy przy armatorach i wywiadowniach.

## 2. Architektura — katalog per tenant, nigdy wspólny

```sql
network
  id, code,                     -- wca | globalia | jctrans | conqueror
                                -- fiata | pisil | cargo_connections | ...
  name, website, region_scope
  is_global                     -- katalog globalny czy krajowy

network_membership              -- członkostwo TWOJEGO klienta
  id, organization_id, network_id
  member_id_in_network, member_since, valid_until
  tier,                         -- poziom członkostwa, jeśli sieć je ma
  is_active

network_member                  -- rekord katalogowy
  id, network_id
  organization_id,              -- ← KRYTYCZNE: kopia per tenant
  company_name, legal_name
  country_code, city, address
  ports_covered text[],         -- UN/LOCODE
  services text[],              -- FCL | LCL | AIR | PROJECT | CUSTOMS | WAREHOUSE
  specializations text[],       -- reefer | DG | oversize | pharma
  languages text[]
  member_id_in_network, member_since
  website, general_email, phone
  source,                       -- import | manual | enriched | public
  imported_at, last_verified_at
  linked_party_id NULL          -- powiązanie z twoim kontrahentem

network_member_contact
  id, network_member_id
  name, position, email, phone, languages text[]
  is_primary, prefers_channel
  last_contacted_at, response_count
```

**Pole `organization_id` na `network_member` jest fundamentem legalności tego modułu.** Każdy tenant ma własną kopię katalogu, zaimportowaną na podstawie własnego członkostwa. Nic się nie zlewa, nic się nie współdzieli, nic nie jest redystrybuowane.

To rozwiązuje jednocześnie drugi problem, o którym była mowa wcześniej: zestawianie danych między konkurującymi spedytorami byłoby ryzykiem antymonopolowym. Ta architektura czyni je strukturalnie niemożliwym — i możesz to powiedzieć wprost w rozmowie handlowej.

## 3. Skąd biorą się dane

Cztery ścieżki, uszeregowane od najlepszej:

**Import własnego eksportu.** Klient pobiera z portalu sieci to, do czego ma prawo jako członek, i wrzuca do systemu. Ten sam pipeline ekstrakcji, który parsuje cenniki, obsłuży Excel albo PDF katalogu. Zero nowego kodu.

**Wzbogacanie z własnej historii.** Każdy agent, do którego kiedykolwiek wysłałeś zapytanie albo od którego dostałeś cennik, staje się rekordem automatycznie. Po roku ta baza jest lepsza od oficjalnego katalogu, bo zawiera to, czego katalog nie ma: kto realnie odpowiada, jak szybko i po jakiej cenie.

**Źródła publiczne.** Listy członków izb — PISiL, FIATA i krajowych stowarzyszeń — bywają jawne. Te można pobierać normalnie.

**Wprowadzanie wspomagane.** Wklejasz stronę katalogu, model wyciąga strukturę. Legalne w zakresie twojego własnego dostępu członkowskiego, do użytku wewnętrznego.

## 4. Deduplikacja — problem, który wypłynie od razu

Ta sama firma jest w WCA, Globalii i JCtrans, pod trzema wariantami nazwy i z dwoma adresami mailowymi. Bez deduplikacji katalog liczący trzy tysiące rekordów opisuje tysiąc dwustu agentów, a karta wyników z Aneksu 4 rozjeżdża się na trzy niepowiązane rekordy.

Rozwiązanie: `dedupe` plus `RapidFuzz` na nazwie, domenie mailowej i adresie, z ręcznym potwierdzeniem przy niskiej pewności. Jeden `party` może mieć wiele członkostw:

```sql
network_member_link
  party_id, network_member_id, confidence, confirmed_by
```

## 5. Wybór agenta — tu jest właściwa wartość

Katalog sam w sobie jest niczym. Sieć ma dwanaście tysięcy członków i lista dwunastu tysięcy nazwisk nie pomaga nikomu.

Wartość leży w **kolejności**, w jakiej system je pokazuje:

```
Zapytanie: Gdynia → Callao, 2×40HC, meble

SUGEROWANI (5)
① Andes Cargo SAC              WCA  Lima
   ✓ 8 zapytań, odpowiada średnio w 3,2 h
   ✓ najtańszy w 5 z 8 przypadków
   ✓ zgodność oferty z fakturą 100%
   
② Pacific Forwarding Peru      WCA, Globalia  Callao
   ✓ 4 zapytania, odpowiada w 6,8 h
   ⚠ raz doliczył dopłatę spoza oferty
   
③ TransAndina Logistics        JCtrans  Lima
   ○ brak historii — nowy kontakt
   
[pokaż wszystkich 34 w Peru]
```

Ranking buduje się z `party_scorecard` z Aneksu 4: wskaźnik odpowiedzi, mediana czasu odpowiedzi, konkurencyjność cenowa na tej relacji, zgodność oferty z późniejszą fakturą. Sieć i kraj to tylko filtr — sortowanie robi twoja historia.

## 6. Dwa kliknięcia do zapytania

Wybór agentów zasila `rate_request` z Aneksu 3. Cały mechanizm już jest zaprojektowany:

```
[1] Zaznaczasz trzech agentów z listy
[2] Klikasz „Wyślij zapytanie"
    ↓
    szablon w języku agenta, dane zlecenia wypełnione automatycznie
    unikalny adres zwrotny rr-{token}@rates.twojadomena.pl
    termin odpowiedzi, automatyczne przypomnienie w połowie terminu
    ↓
    odpowiedzi wpadają, ekstrakcja parsuje je jak cenniki
    porównanie obok siebie, znormalizowane do wspólnych kodów opłat
    ↓
    wybór → oferta dla klienta
    a wszystkie odpowiedzi zapisują się jako rate_line
```

## 7. Ograniczenie liczby odbiorców — funkcja, nie brak

Kuszące będzie umożliwienie wysyłki do wszystkich trzydziestu czterech agentów w Peru jednym kliknięciem. **Nie rób tego, i to nie tylko z powodów prawnych.**

Powód praktyczny: agenci rozpoznają masową wysyłkę i traktują ją niżej niż zapytanie kierowane. Zapytanie do czterech dobrze wybranych agentów daje lepsze i szybsze odpowiedzi niż do trzydziestu. Sieci również nie patrzą przychylnie na członków zasypujących katalog.

Powód prawny: masowa wysyłka handlowa podlega przepisom o komunikacji elektronicznej. Zapytanie ofertowe kierowane do konkretnego partnera w ramach wspólnej sieci to co innego niż mailing do listy.

Ustaw domyślny limit odbiorców na zapytanie — pięciu, może ośmiu — z możliwością podniesienia i ostrzeżeniem. Ograniczenie sprzedasz jako funkcję jakościową, bo nią jest.

## 8. Mapa pokrycia siecią

Ekran, który powie właścicielowi coś, czego nie wie:

```
POKRYCIE AGENCYJNE

Ameryka Południowa
  Peru        3 agentów   ✓ sprawdzeni (8 zapytań, 6 odpowiedzi)
  Chile       1 agent     ⚠ jeden kontakt, brak historii
  Kolumbia    0           ✗ biała plama — 4 zapytania klientów w tym roku
  
Azja Południowo-Wschodnia
  Wietnam     5 agentów   ✓
  Kambodża    0           ✗ biała plama
```

Białe plamy zestawione z liczbą zapytań klientów, których nie obsłużyłeś. To jest lista rzeczy do zrobienia przed następnym zjazdem sieci — konkretna, nie intuicyjna.

## 9. Wzbogacanie zwrotne

Każda odpowiedź agenta aktualizuje rekord: faktyczna osoba kontaktowa, rzeczywisty czas odpowiedzi, obsługiwane porty (wynikają z tego, na co odpowiada), języki, konkurencyjność.

Po roku katalog w systemie jest dokładniejszy niż katalog sieci, bo katalog sieci opisuje deklaracje, a twój opisuje zachowanie.

To jest ten sam mechanizm, co przy karcie wyników agenta — dane operacyjne, których konkurent nie odtworzy, bo nie ma historii. **Każda funkcja w tym systemie powinna działać w ten sposób: wykonywać zadanie dziś i zostawiać po sobie dane, które jutro czynią ją lepszą.**

## 10. Nakład i kolejność

| Element | Nakład | Kiedy |
|---|---|---|
| Model danych `network`, `network_member`, kontakty | 2 dni | tygodnie 1–2, razem z resztą |
| Import katalogu przez pipeline ekstrakcji | 2 dni | wykorzystuje istniejący kod |
| Wzbogacanie z historii korespondencji | 3 dni | automatyczne, w tle |
| Deduplikacja | 3 dni | konieczna od razu, inaczej dane się psują |
| Ekran wyboru z rankingiem | 4 dni | po `party_scorecard` |
| Wpięcie w `rate_request` | 1 dzień | mechanizm już istnieje |
| Mapa pokrycia | 2 dni | dowolnie później |

Razem około siedemnastu dni roboczych, z czego większość to kod, który już masz w innych modułach. To jest jeden z lepszych stosunków wartości do nakładu w całym projekcie — bo nie buduje nowego mechanizmu, tylko daje wejście mechanizmowi już zaprojektowanemu.
