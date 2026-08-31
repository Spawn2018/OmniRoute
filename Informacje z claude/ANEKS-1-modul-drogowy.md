# Aneks 1 — Moduł drogowy i silnik rentowności

Rozszerzenie SPEC-master o transport drogowy: drobnica własnym systemem, całopojazdowy, doładunki. Oraz o wpięcie istniejącego silnika rentowności.

---

## 1. Co już masz i co to zmienia

Silnik rentowności drobnicy drogowej ma elementy, których nowy system nie ma i których nie warto pisać drugi raz:

| Element | Wartość w połączonym systemie |
|---|---|
| Silnik alokacji, tryby shared i capacity | **Rdzeń modułu drogowego.** Alokacja kosztu pojazdu na przesyłki to problem, którego frachtu morskiego w ogóle nie dotyczy |
| Model zysku kierunkowego | Podstawa reguł marży per relacja — dziś liczysz to po fakcie, po integracji będzie działać przy wycenie |
| Widoczność kosztu pustych powrotów | Wejście do decyzji o doładunku: czy przyjąć ładunek, który sam w sobie ledwo się spina, ale wypełnia powrót |
| Normalizacja kluczy tras z trzech źródeł | Gotowa warstwa, którą w morzu robisz przez UN/LOCODE — tu masz odpowiednik dla dróg |
| ~70 KPI | Warstwa raportowa modułu drogowego, nie do napisania od nowa |
| Importer wsadowy PDF | Zbieżny z pipeline'em ingestion z części C — patrz sekcja 5 |

**Najważniejsze ustalenie:** rozrzut cen CV 80,5% to nie jest ciekawostka analityczna. To jest teza produktowa. Twoje dane dowodzą, że ta sama usługa sprzedawana jest w bardzo szerokim przedziale cenowym — a silnik stawek z regułami marży zwęża ten przedział przy każdej wycenie, nie po kwartale.

## 2. Co w modelu danych generalizuje się bez zmian

Te tabele z części B działają dla drogi bez modyfikacji:

`organization` · `app_user` · `role` · `audit_log` · `usage_metric` · `party` · `party_contact` · `party_bank_account` · `party_charge_override` · `charge_code` · `charge_code_alias` · `quotation` · `quotation_variant` · `quotation_line` · `quotation_gap` · `margin_rule` · `invoice` · `bill` · `payment` · `document_template` · `numbering_scheme` · `custom_field` · `rate_sheet` · `extraction_template`

To potwierdza zasadę 3: `charge` z kupnem i sprzedażą na jednym rekordzie jest niezależne od gałęzi transportu. Cała rentowność liczy się tak samo dla kontenera i dla palety.

## 3. Co wymaga uogólnienia — zrób to w tygodniach 1–2

Trzy zmiany. Wprowadzone teraz kosztują kilka dni, wprowadzone po fazie 3 oznaczają przepisanie.

### 3.1 Lokalizacja zamiast portu

Morze operuje na UN/LOCODE. Droga na kodach pocztowych i strefach. Potrzebna abstrakcja:

```sql
location
  id, organization_id NULL       -- NULL = globalna
  kind,                          -- unlocode | postal_zone | address | terminal
  unlocode NULL,                 -- PLGDY
  country_code, postal_prefix,   -- "PL-80", "DE-2"
  zone_code NULL,                -- własna strefa taryfowa klienta
  lat, lng, name, aliases text[]

location_zone_member             -- strefa → zakresy kodów
  zone_id, country_code, postal_from, postal_to
```

Strefy taryfowe są konfigurowalne per organizacja (zasada 2) — każdy spedytor drogowy ma własny podział Polski i Europy i żaden nie zgodzi się na twój.

### 3.2 Przedziały w stawkach

`rate_line` z części B zakłada stawkę per typ kontenera. Drobnica drogowa to macierz przedziałów wagowych i metrów ładunkowych:

```sql
-- rozszerzenie rate_line:
  bracket_unit,        -- KG | LDM | PALLET | CBM | NONE
  bracket_from numeric,
  bracket_to numeric,
  min_charge,
  -- container_type staje się nullable (tylko morze)
```

Przykład: Gdańsk → Berlin, 100–200 kg, 0,45 zł/kg, minimum 180 zł. To ta sama tabela co stawka za 40HC, tylko z wypełnionymi innymi kolumnami.

### 3.3 Zlecenie z dyskryminatorem gałęzi

```sql
shipment
  -- wspólne: id, job_number, strony, incoterm, status, operator
  transport_mode,      -- SEA_FCL | SEA_LCL | ROAD_LTL | ROAD_FTL | ROAD_PART
  origin_location_id, destination_location_id

shipment_sea            -- to, co dziś jest w shipment
  shipment_id, pol, pod, vessel_name, voyage, mbl, hbl,
  cutoff_doc, cutoff_vgm, cutoff_gate

shipment_road
  shipment_id, vehicle_type, plate, trailer_plate, driver_name
  loading_meters, pallets, gross_weight_kg, volume_cbm
  is_adr, adr_class, requires_tail_lift, requires_timeslot
  loading_window_from, loading_window_to
  unloading_window_from, unloading_window_to
  cmr_number, tour_id NULL       -- ← przypisanie do przejazdu
```

## 4. Co jest nowe i specyficznie drogowe

### 4.1 Przejazd jako jednostka kosztowa

To pojęcie nie istnieje w morzu i jest sercem twojego silnika alokacji.

```sql
tour                             -- przejazd / kurs pojazdu
  id, organization_id
  tour_number, vehicle_type, carrier_party_id
  departure_location_id, arrival_location_id
  departure_at, arrival_at
  capacity_ldm, capacity_kg, capacity_pallets
  cost_total, cost_currency,     -- koszt pojazdu, kupno
  cost_basis,                    -- fixed | per_km | negotiated
  distance_km, is_return_leg, paired_tour_id NULL
  status

tour_assignment                  -- przesyłka na przejeździe
  id, tour_id, shipment_id
  used_ldm, used_kg, used_pallets
  sequence,                      -- kolejność załadunku/rozładunku
  allocated_cost,                -- ← wynik silnika alokacji
  allocation_mode,               -- shared | capacity | marginal
  allocation_run_id
```

### 4.2 Silnik alokacji — trzy tryby

Twoje dwa istniejące plus jeden, który wynika z doładunków:

| Tryb | Zasada | Kiedy |
|---|---|---|
| **shared** | koszt przejazdu dzielony proporcjonalnie do zajętości (LDM, kg, palety) | domyślny dla drobnicy, gdy wszystkie przesyłki są równorzędne |
| **capacity** | koszt dzielony wg zadeklarowanej pojemności, nie faktycznego wykorzystania | gdy chcesz obciążyć niewykorzystaną przestrzeń kierunkiem, a nie przesyłkami |
| **marginal** | doładunek obciążony wyłącznie kosztem krańcowym; koszt bazowy pozostaje na ładunku pierwotnym | **decyzja o doładunku** — patrz 4.3 |

Wynik alokacji zapisuje się na `tour_assignment.allocated_cost` i **stamtąd trafia do `shipment_charge` jako pozycja kupna**. Dzięki temu drogowa rentowność liczy się tą samą tabelą co morska (zasada 3).

### 4.3 Doładunek to inna matematyka

W morzu pytanie brzmi „ile kosztuje kontener". W doładunku brzmi „ile kosztuje **dodatkowa** paleta na pojeździe, który i tak jedzie".

```
decyzja o przyjęciu doładunku:
  koszt krańcowy = objazd_km × stawka_km
                 + czas_postoju × koszt_godziny
                 + ryzyko_opóźnienia_ładunku_bazowego
                 
  przyjmij, jeśli: przychód > koszt krańcowy × (1 + minimalna_marża)
  
  szczególny przypadek — powrót:
     jeśli tour.is_return_leg i brak innego ładunku,
     koszt bazowy jest już poniesiony → próg jest bardzo niski
     to jest miejsce, gdzie twoja widoczność kosztu pustych powrotów
     zamienia się w konkretną decyzję sprzedażową
```

Ta reguła musi być dostępna **w momencie wyceny**, nie w raporcie miesiąc później. To jest największa pojedyncza zmiana, jaką daje połączenie obu systemów.

### 4.4 Planowanie załadunku

Tu narzędzia z katalogu przestają być teoretyczne:

- `google/or-tools` — czy opłaca się przyjąć doładunek, jak zestawić przesyłki na przejazdach
- `skjolber/3d-bin-container-packing` — czy fizycznie wejdzie, z układem do pokazania kierowcy
- `PyVRP/PyVRP` — kolejność załadunku i rozładunku przy wielu punktach

## 5. Ingestion cenników drogowych

Pipeline z części C działa bez zmian koncepcyjnych, ale wejście wygląda inaczej:

| | Morze | Droga |
|---|---|---|
| Format | arkusz relacji port–port | **macierz stref × przedziałów wagowych** |
| Osie | POL, POD, typ kontenera | strefa nadania, strefa dostawy, przedział kg/LDM |
| Typowy rozmiar | dziesiątki wierszy | setki do tysięcy komórek |
| Dopłaty | osobne wiersze | zwykle osobna zakładka: paliwowa, ADR, winda, awizacja, przestój |

Macierz stref to dla modelu językowego **łatwiejszy** przypadek niż cennik morski — jest regularna. Ale wymaga innego schematu ekstrakcji: zamiast listy `lanes` z `charges`, dostajesz siatkę, którą rozwijasz do wierszy `rate_line` w kodzie.

Twój importer wsadowy PDF prawdopodobnie już to robi dla części dostawców. Warto go potraktować jako gotowy adapter dla znanych formatów — czyli dokładnie to, czym jest `extraction_template` z sekcji C2.5.

## 6. Pętla zwrotna — to jest właściwy produkt

```
   ┌──────────────────────────────────────────────────────┐
   │                                                       │
   ▼                                                       │
quotation ──► shipment ──► tour_assignment ──► alokacja    │
(marża                     (koszt              (twój       │
 planowana)                 rzeczywisty)        silnik)    │
   ▲                                               │       │
   │                                               ▼       │
   │                                        shipment_charge│
   │                                               │       │
   │                                               ▼       │
   └──────────── margin_rule ◄────────────── KPI, CV cen ──┘
                (korekta cennika)
```

Dziś masz prawą połowę tej pętli — mierzysz, co się wydarzyło. Lewej nie masz, więc pomiar nie wraca do decyzji cenowej. Po połączeniu:

1. System wycenia z planowaną marżą
2. Zlecenie się realizuje, koszty spływają
3. Silnik alokacji liczy rzeczywistą marżę per przesyłka, kierunek, klient
4. Odchylenie planowana–rzeczywista aktualizuje `margin_rule`
5. Następna wycena jest lepsza

Rozrzut CV 80,5% jest miarą tego, jak bardzo tej pętli dziś brakuje.

## 7. Jak to wpiąć praktycznie — trzy etapy

**Etap 1: wspólny model danych (tygodnie 1–2, razem z resztą)**
Uogólnij `location`, `rate_line` o przedziały i `shipment` o dyskryminator. Dodaj `tour` i `tour_assignment` do schematu, nawet jeśli nic ich jeszcze nie wypełnia. Koszt: kilka dni. Bez tego wracasz do migracji za pół roku.

**Etap 2: silnik rentowności jako konsument (po fazie 3)**
Streamlit czyta z tej samej bazy zamiast z importowanych plików. Nie przepisujesz logiki — podmieniasz źródło danych. Normalizacja kluczy tras, którą masz zrobioną, staje się mapowaniem na `location`.

**Etap 3: alokacja jako moduł backendu (po pierwszym płacącym kliencie)**
Port logiki alokacji z Pythona analitycznego do warstwy domenowej, uruchamiany przy zamknięciu przejazdu. Wynik zapisywany na `tour_assignment` i propagowany do `shipment_charge`. Dopiero wtedy pętla z sekcji 6 się domyka.

## 8. Pytanie strategiczne, na które muszę zwrócić uwagę

Może masz to odwrotnie, niż zakładaliśmy.

Rynek drogowy w Polsce jest wielokrotnie większy niż spedycja morska. Twoim profilem klienta w morzu jest spedytor z własną bazą stawek i co najmniej dwiema osobami w ofertowaniu — takich firm są setki. Spedytorów drogowych i operatorów drobnicowych są tysiące.

Do tego w module drogowym masz przewagę, której w morskim nie masz: **działający, zwalidowany na realnych danych silnik**, który już pokazał konkretną liczbę (CV 80,5%) będącą gotowym argumentem sprzedażowym. W morzu zaczynasz od zera.

Argument za morzem pozostaje mocny: ból z parsowaniem cenników od agentów jest tam znacznie ostrzejszy, a automatyczna baza cen zakupowych to funkcja, której nikt nie ma. W drodze cenniki są bardziej regularne, więc ta przewaga jest mniejsza.

**Nie rozstrzygam tego za ciebie — znasz oba rynki.** Ale zauważ, że pytanie dotyczy kolejności faz, nie architektury. Wspólny model danych z sekcji 3 jest właściwą decyzją niezależnie od odpowiedzi, i dlatego warto go wprowadzić teraz, zanim odpowiedź będzie znana.

Dodaj to do decyzji otwartych w D8 jako punkt 6, z terminem: przed tygodniem 7.
