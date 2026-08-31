# Aneks 14 — Cut-off, agregatorzy, kolej, mapa integracji

---

# 1. DATA ODNIESIENIA — POPRAWKA

Masz rację, moja poprzednia wersja była nieprecyzyjna. Wiążąca operacyjnie jest nie data wypłynięcia, tylko **cut-off pomniejszony o dowóz**.

## 1.1 Łańcuch dat

```
gotowość ładunku
    + czas dowozu do portu (1–2 dni, konfigurowalne per relacja)
    ≤ cut-off bramowy (CY/gate)
    
cut-off bramowy  ≈  ETD − 1…3 dni
cut-off dokumentacyjny ≈ gate − 1…2 dni
cut-off VGM      ≈ gate − 1 dzień
cut-off DG       ≈ gate − 5…10 dni   ← znacznie wcześniej
cut-off reefer   ≈ gate − 1…2 dni
```

Cut-off dla ładunków niebezpiecznych jest osobną sprawą i wypada o tydzień lub więcej wcześniej. Przy zapytaniu z klasą ADR system musi liczyć od niego, inaczej pokaże rejs, na który fizycznie nie da się zdążyć.

```sql
-- rozszerzenie rfq / quotation
  ready_date_from, ready_date_to
  drayage_days,              -- z historii relacji, edytowalne
  latest_gate_cutoff,        -- = ready_date_to + drayage_days
  applicable_cutoff_type     -- gate | doc | vgm | dg | reefer

-- rozszerzenie carrier_service / harmonogram
  sailing_id, etd, eta
  cutoff_gate, cutoff_doc, cutoff_vgm, cutoff_dg, cutoff_reefer
```

Silnik dobiera rejsy, których właściwy cut-off wypada **nie wcześniej** niż gotowość plus dowóz. Przy ładunku DG automatycznie przełącza się na cut-off DG.

## 1.2 Druga poprawka, ważniejsza

Różni armatorzy różnie definiują, **co decyduje o ważności stawki**. Jedni piszą „ważne dla rejsów wypływających między X a Y", inni „dla bookingów dokonanych w tym okresie", jeszcze inni odnoszą się do daty konosamentu.

To nie jest szczegół — przy stawce wygasającej za cztery dni różnica między datą bookingu a datą wypłynięcia decyduje o tym, czy zarabiasz.

```sql
-- rozszerzenie rate_line
  validity_basis      -- sailing | booking | bl_date | gate_in
```

Domyślnie `sailing`, ale pole musi istnieć i ekstraktor powinien je wychwytywać z treści cennika. Sformułowania typu „for bookings placed until…" albo „valid for sailings…" są w cennikach zapisane wprost.

## 1.3 Kierunek odwrotny

Ta sama logika działa w drugą stronę i jest przydatna handlowo:

```
Klient: „chcę, żeby towar był w Callao przed 20 października"

System liczy wstecz:
  ETA 20.10 → tranzyt 32 dni → ETD 18.09
  → cut-off bramowy 15.09
  → towar musi być gotowy do 13.09
  
  ⚠ To zostawia 16 dni. Kolejny rejs: ETD 25.09, ETA 27.10 — za późno.
```

Odpowiedź „musi pan mieć towar gotowy do 13 września" jest dla klienta cenniejsza niż sama cena.

---

# 2. AGREGATORZY — CZY BEZ NARZUTU

## 2.1 Trzy różne modele

Odpowiedź brzmi „zależy od dostawcy", a różnica jest zasadnicza.

**Model A — kanał dystrybucji, opłacany przez armatora.**
Po stronie bookingu przypomina fracht lotniczy: dla spedytora bezpłatnie, bo **armatorzy płacą stałe opłaty za booking** — tak działają WebCargo i cargo.one. Stawka jest stawką armatora, bez narzutu pośrednika.

**Model B — narzędzie SaaS, opłacane przez ciebie.**
Płacisz abonament, czasem dodatkowo za połączenia z armatorami albo za wykorzystanie API — tak jest przy Freightify Link i integracjach SeaRates. Stawka pochodzi od armatora albo z twojego kontraktu, dostawca nie jest stroną przewozu i nie dolicza marży do frachtu.

**Model C — pośrednik działający na własny rachunek.**
Marketplace albo NVOCC kupuje od armatora i sprzedaje tobie. **Tu narzut jest, tylko go nie widzisz** — i to on wystawia konosament.

## 2.2 Pięć pytań, które rozstrzygają

Zadaj je każdemu dostawcy przed podpisaniem:

1. **Kto jest stroną umowy przewozu — wy czy armator?**
2. **Kto wystawia konosament?**
3. **Widzę stawkę armatora czy waszą?** Jeśli waszą — jaka jest różnica?
4. **Model opłat:** abonament, per zapytanie, per booking, prowizja od wartości?
5. **Czy przez wasz kanał widzę moje własne stawki kontraktowe, czy tylko ich stawki publiczne?**

Piąte pytanie jest najważniejsze i najczęściej pomijane.

## 2.3 Czego agregator nie zastąpi

Stawki dostępne przez kanały publiczne to zwykle **oferta online armatora, nie twój kontrakt**. Jeśli masz wynegocjowaną umowę, twoja stawka będzie zwykle lepsza od tej, którą pokaże agregator.

Wniosek praktyczny: agregator jest uzupełnieniem zasięgu, nie zamiennikiem bezpośrednich relacji. Wartość ma tam, gdzie kontraktu nie masz — czyli na relacjach okazjonalnych i u armatorów, z którymi nie pracujesz regularnie. Dokładnie tam, gdzie dziś tracisz najwięcej czasu.

---

# 3. KOLEJ INTERMODALNA

## 3.1 Dlaczego to warto zbudować

Trzy powody, każdy niezależnie wystarczający:

- **Dowóz i odwóz kontenerów w Polsce i Europie** to część niemal każdego zlecenia morskiego. Dziś liczysz go z osobnych ofert
- **Ślad węglowy** — kolej ma wielokrotnie niższą emisję niż transport drogowy. To zasila moduł GLEC/ISO 14083 i staje się argumentem u klientów objętych raportowaniem
- **Nowy Jedwabny Szlak** — kolej Chiny–Europa przez Małaszewicze to realna alternatywa dla morza przy ładunkach czasowo wrażliwych. Możliwość porównania morze kontra kolej w jednej ofercie to funkcja, której nie ma prawie nikt

## 3.2 Stan integracji — ten sam problem, to samo rozwiązanie

Operatorzy intermodalni w Polsce i Europie w większości nie mają publicznych API. Mają portale klienta, adresy bookingowe i czasem EDI.

**Zastosuj tę samą abstrakcję kanałów co przy armatorach.** Operator kolejowy to kolejny wpis w `carrier_channel` z typem `email` albo `portal`. Mechanizm zapytań, personalizacji i ekstrakcji odpowiedzi już masz.

Kogo obejmuje: krajowi i regionalni operatorzy przewozów intermodalnych oraz operatorzy terminali. Zbuduj listę na podstawie własnej praktyki i uzupełniaj z każdego zapytania — ten sam mechanizm wzbogacania katalogu co przy agentach.

## 3.3 Model danych

Kolej wymaga rozszerzeń, bo nie jest przewozem port–port:

```sql
rail_operator                    -- rozszerzenie party
  party_id, operates_own_trains, terminals_served text[]

rail_service                     -- pociąg jako serwis
  id, operator_party_id
  origin_terminal_id, destination_terminal_id
  departure_days text[],         -- {MO,WE,FR}
  transit_hours
  capacity_teu
  accepts_reefer, accepts_dg, accepted_rid_classes text[]
  border_crossing,               -- np. przeładunek szerokotorowy
  is_active

rail_booking
  id, shipment_id, rail_service_id
  departure_date, container_ids uuid[]
  slot_reference, status
```

Uwagi domenowe, które trzeba przewidzieć:

- **terminal, nie port** — encja `terminal` z Aneksu 13 obsługuje jedno i drugie
- **rozkład stały** — pociąg jedzie trzy razy w tygodniu, nie codziennie. Wybór daty to wybór odjazdu, nie dowolny dzień
- **zmiana rozstawu szyn** na granicy wschodniej — przeładunek, dodatkowy czas i koszt, osobna pozycja
- **RID zamiast IMDG** — inne ograniczenia dla ładunków niebezpiecznych, część terminali ich nie przyjmuje
- **reefer na kolei** — nie wszędzie, wymaga agregatu i obsługi

## 3.4 Funkcja, która to spina: porównanie gałęzi

```
Dowóz Gdynia → Poznań, 1×40HC

  Droga    1 240 zł    18 h    ~340 kg CO₂
  Kolej      980 zł    36 h    ~ 95 kg CO₂   ✓ najtaniej i najniższa emisja
  
  ⚠ Kolej: odjazdy PN/ŚR/PT — najbliższy 4.09, cut-off 3.09 12:00
```

Ten widok w ofercie robi dwie rzeczy naraz: pokazuje klientowi wybór i uzasadnia twoją wartość dodaną. A dane emisyjne wpadają wprost do modułu śladu węglowego z Aneksu 5.

## 3.5 Nakład

| Element | Dni |
|---|---|
| `rail_operator`, `rail_service`, `rail_booking` | 3 |
| Kanał mailowy dla operatorów — istniejący mechanizm | 1 |
| Rozkłady i wybór odjazdu | 3 |
| Porównanie droga/kolej z emisją | 3 |
| Obsługa RID i ograniczeń terminali | 2 |

Dwanaście dni, bo większość mechanizmów już istnieje. Buduj po tym, jak działa fracht morski — kolej jest odcinkiem dowozowym, nie osobnym produktem.

---

# 4. MAPA INTEGRACJI ARMATORSKICH

## 4.1 Zasada: framework, nie integracje

Kluczem do „jak największej liczby" nie jest pisanie kolejnych integracji, tylko **sprowadzenie każdej nowej do mapowania, nie do kodu**.

```
CarrierAdapter (wspólny)
  ├── uwierzytelnianie: OAuth | klucz | certyfikat        [konfiguracja]
  ├── mapowanie endpointów                                 [konfiguracja]
  ├── mapowanie pól odpowiedzi → model wewnętrzny          [konfiguracja]
  ├── mapowanie kodów opłat → charge_code                  [konfiguracja]
  └── obsługa błędów i limitów                             [wspólna]
```

Pierwszy armator to dwa tygodnie. Piąty powinien być trzema dniami. Jeśli dziesiąty nadal zajmuje dwa tygodnie, framework jest źle zbudowany i to jest sygnał do refaktoryzacji, nie do zatrudniania.

## 4.2 Kolejność

**Fala 1 — armatorzy z dojrzałymi portalami deweloperskimi**

Hapag-Lloyd pierwszy: jako jedyny udostępnia specyfikację pokrycia, czyli obsługiwane relacje, typy kontenerów i rodzaje ładunku. To pozwala odsiać niemożliwe zapytania przed wysłaniem i eliminuje połowę obsługi błędów.

Maersk drugi: Offers API zwraca komplet — trasę, harmonogram, statek, deadline'y i ceny z dopłatami — a przewodnik onboardingowy jest publiczny.

CMA CGM trzeci, ze świadomością, że API cenowe zwraca sam fracht bez opłat lokalnych i inland, a SpotOn ma osobny interfejs.

**Fala 2 — armatorzy z API o mniejszej dojrzałości cenowej**
MSC, ONE, Evergreen, ZIM, HMM, OOCL. U większości tracking jest dojrzały wcześniej niż wyceny — integruj tracking od razu, ceny gdy będą dostępne.

**Fala 3 — konsolidatorzy LCL**
Przy drobnicy morskiej ważniejsi od armatorów są co-loaderzy. Kilku dużych ma portale i interfejsy programistyczne. Jeśli robisz LCL, ta fala może być ważniejsza od drugiej.

**Fala 4 — reszta świata przez kanał mailowy**
Armatorzy regionalni w Afryce, Ameryce Południowej, na Morzu Śródziemnym i w Azji Południowo-Wschodniej. Bez API, ale z adresem `pricing@`. Twój mechanizm z Aneksu 9 obsługuje ich bez jednej linijki nowego kodu.

## 4.3 DCSA jako dźwignia

Standard DCSA obejmuje już Track & Trace w wersjach wdrożonych przez większość dużych armatorów, a Booking jest wdrażany. Każdy kolejny obszar objęty standardem oznacza, że jedna implementacja obsługuje wielu armatorów.

Praktycznie: **implementuj według DCSA, nawet gdy armator ma własny format.** Mapuj jego odpowiedź na model DCSA zamiast na własny. Wtedy każdy armator, który wdroży standard, wchodzi niemal bez pracy.

## 4.4 Realistyczny cel na dwanaście miesięcy

| | Kanał | Liczba |
|---|---|---|
| API bezpośrednie, ceny i tracking | własne adaptery | 3–5 |
| API bezpośrednie, sam tracking | DCSA | 8–10 |
| Agregator | licencja | kilkadziesiąt |
| Mail automatyczny | twój mechanizm | bez ograniczeń |

To nie jest „wszyscy armatorzy przez API" — ale z punktu widzenia użytkownika **każdy armator jest osiągalny**, a różni się tylko czas odpowiedzi. I to jest obietnica, której dotrzymasz.
