# Aneks 13 — Daty, zasięg armatorów, sankcje, porty, towary niebezpieczne

---

# 1. DATA GOTOWOŚCI I WAŻNOŚĆ STAWEK NA TĘ DATĘ

## 1.1 Problem, który dobrze wychwyciłeś

Stawka ważna dziś nie musi być ważna w dniu wypłynięcia. Silnik wyceny z głównej specyfikacji sprawdza ważność względem **dzisiaj** — to jest błąd, który trzeba poprawić.

Właściwa data odniesienia to nie gotowość ładunku, tylko **przewidywane wypłynięcie**:

```
data_wypłynięcia ≈ gotowość + dowóz do portu + bufor na cut-off
```

Dla Gdyni z załadunkiem u klienta pod Poznaniem to zwykle kilka dni. Dla dowozu z zagranicy — więcej. Bufor konfigurowalny per relacja, domyślny z historii własnych zleceń.

## 1.2 Rozpoznawanie daty

```sql
-- rozszerzenie rfq
  ready_date_from date,
  ready_date_to date,
  ready_date_precision,   -- exact | week | half_month | month | asap | unknown
  ready_date_raw text,    -- co napisał klient
  expected_sailing_date,  -- wyliczone
  sailing_buffer_days
```

**Zawsze zakres, nigdy jedna data.** „Połowa września" to 10–20 września, nie 15 września. Precyzja jest częścią informacji i wpływa na to, jak agresywnie system reaguje.

Formy, które muszą działać:

| Zapis klienta | Wynik |
|---|---|
| „15.09" / „15 września" | dokładna |
| „połowa września" | 10–20.09, precyzja `half_month` |
| „wrzesień" | 01–30.09, precyzja `month` |
| „za dwa tygodnie" | względem daty maila |
| „week 38" / „tydzień 38" | 15–21.09 |
| „ASAP" / „pilne" | od dziś, precyzja `asap` |
| „po chińskim Nowym Roku" | z kalendarza wydarzeń z Aneksu 2 |
| „gdy dostaniemy towar, ok. 3 tygodnie" | +21 dni, precyzja `month` |
| brak | `unknown` → pytanie do klienta |

Parsowanie dwuetapowo: kod obsługuje formaty jednoznaczne i względne, model językowy wyrażenia opisowe. Model zwraca zakres i precyzję, nigdy jedną datę.

## 1.3 Sprawdzenie pokrycia na datę wypłynięcia

```
Dla każdej wymaganej pozycji kosztowej:

  stawka pokrywa expected_sailing_date?
    ├─ TAK, cały zakres          → OK
    ├─ TAK, ale wygasa w trakcie → ⚠ częściowe pokrycie
    ├─ NIE, wygasła              → ✗ luka
    └─ brak stawki w ogóle       → ✗ luka
    
  Dodatkowo:
    ├─ GRI/PSS ogłoszony przed datą wypłynięcia?  → ⚠ (Aneks 2)
    └─ stawka starsza niż próg świeżości?          → ⚠
```

Ekran zapytania pokazuje to wprost:

```
Gotowość: połowa września (10–20.09)
Przewidywane wypłynięcie: 18–24.09

  Ocean freight   Andes Cargo    ważna do 30.09   ✓
  DTHC Callao     Andes Cargo    ważna do 15.09   ✗ wygasa przed wypłynięciem
  Odwóz Lima      brak stawki                     ✗ luka
  
  ⚠ GRI Hapag ogłoszony na 01.10 — dotyczy późniejszej części zakresu

  → 2 luki. [ Wyślij zapytanie do agentów (3 sugerowanych) ]
```

## 1.4 Automatyczne wyzwolenie zapytania

```sql
rate_gap_policy
  id, organization_id
  trigger,                  -- on_rfq_created | on_quote_open | scheduled
  action,                   -- auto_send | propose | notify_only
  min_gap_severity,         -- missing | expiring | stale
  max_recipients,
  agent_selection,          -- suggested | all_in_country | manual
  require_confirmation      -- czy wymaga kliknięcia
```

Domyślnie `propose` — system przygotowuje zapytanie z zaznaczonymi agentami, człowiek klika. Tryb `auto_send` włączany świadomie dla relacji, gdzie luki zdarzają się często i czas ma znaczenie.

**Wariant, który warto dodać: uprzedzanie.** Zadanie cykliczne przegląda historię zapytań i wykrywa relacje, na których stawki wygasną w ciągu dwóch tygodni, a klient pytał o nie ostatnio. Wysyła zapytania do agentów **zanim** przyjdzie kolejne zapytanie. Wtedy oferta wychodzi z bazy, a nie po dobie czekania.

---

# 2. „WSZYSCY ARMATORZY ŚWIATA"

## 2.1 Uczciwe postawienie sprawy

Armatorów kontenerowych na świecie jest kilkaset. API cenowe ma kilkunastu. Bezpośrednia integracja ze wszystkimi jest fizycznie niewykonalna i nikt jej nie ma — również Freightify, Cargofive czy WebCargo.

**Ale cel jest osiągalny, jeśli przedefiniujesz „integrację" jako kanał, a nie jako API.**

## 2.2 Cztery kanały, jeden interfejs

Interfejs adaptera z Aneksu 12 nie musi wiedzieć, co jest pod spodem:

```python
class CarrierChannel(Protocol):
    channel_type: Literal["api", "aggregator", "email", "portal"]
    expected_latency: timedelta
    def request_spot(self, req) -> ChannelResult: ...
```

| Kanał | Zasięg | Czas odpowiedzi | Kto |
|---|---|---|---|
| **API bezpośrednie** | ~15 armatorów | sekundy | Hapag, Maersk, CMA, MSC, ONE, Evergreen, ZIM, HMM… |
| **Agregator** | ~50–100 | sekundy | Freightify Link, SeaRates, Okargo, WebCargo |
| **Mail automatyczny** | **wszyscy pozostali** | godziny | twój własny mechanizm z Aneksu 9 |
| **Portal** | ostateczność | minuty | `browser-use`, na poświadczeniach klienta |

## 2.3 Trzeci kanał to twoja przewaga

Niszowy armator obsługujący Afrykę Zachodnią albo kabotaż w Ameryce Południowej nie ma API. Ma skrzynkę `pricing@`.

**Twój mechanizm zapytań do agentów działa dla niego identycznie.** Zbudowałeś go już — spersonalizowany mail, token w odpowiedzi, ekstrakcja cennika, porównanie. Armator bez API to po prostu kolejny odbiorca.

To jest rzecz, której konkurenci nie robią, bo myślą kategoriami integracji, nie kanałów. Efekt: **twój zasięg jest nieograniczony, tylko czas odpowiedzi się różni.** Sekundy dla piętnastu największych, godziny dla reszty świata — a dziś dla reszty świata jest doba i telefon.

```sql
carrier_channel
  id, carrier_party_id, organization_id
  channel_type,             -- api | aggregator | email | portal
  priority,                 -- kolejność prób
  credential_id NULL,
  pricing_email NULL,
  aggregator_ref NULL,
  avg_response_time, success_rate, last_success_at
  is_active
```

System sam wybiera najlepszy dostępny kanał i pokazuje użytkownikowi spodziewany czas odpowiedzi przy każdym armatorze.

## 2.4 Uwaga strategiczna, którą muszę dodać

Freightify obsługuje ponad dwustu spedytorów w czterdziestu pięciu krajach, przetwarza cenniki z Excela, PDF, maila i zrzutów ekranu, oferuje portal klienta, track & trace i API. Cargofive, Okargo i WebCargo robią podobne rzeczy.

**Samo zarządzanie stawkami i ofertowanie nie jest białą plamą.** To jest rynek z kilkoma dojrzałymi graczami.

Twoja przewaga leży gdzie indziej i warto to sobie powiedzieć wprost:

- pętla od maila klienta przez zapytanie do agentów po rozliczenie faktury — **żaden z nich tego nie zamyka**
- koszt pieniądza i wirtualny CFO — nie ma tego nikt
- polska specyfika: KSeF, biała lista, GUS, KRS, RDF
- integracja z twoim silnikiem rentowności drogowej

Rozważ też ścieżkę pragmatyczną: **licencjonuj warstwę agregacji zamiast budować dwieście integracji.** Freightify Link albo SeaRates jako kanał drugi kosztuje pieniądze, ale oszczędza rok pracy — który wydasz na to, czego oni nie mają.

---

# 3. LISTY SANKCYJNE — AUTOMAT

## 3.1 Źródła, wszystkie darmowe

| Lista | Wydawca | Format |
|---|---|---|
| Skonsolidowana lista UE | Komisja Europejska | XML/CSV |
| Consolidated List | Rada Bezpieczeństwa ONZ | XML |
| SDN + Consolidated | OFAC (USA) | XML/CSV, aktualizacja codzienna |
| UK Sanctions List | OFSI | XML/CSV |
| Lista krajowa | MSWiA | publikowana |

Do tego listy podmiotów objętych kontrolą eksportu i wykazy statków.

## 3.2 Architektura

```
CODZIENNIE, harmonogram:
  pobierz każdą listę → hash → zmiana?
      ↓ TAK
  zapisz nową wersję, policz różnicę
      ↓
  ⚠ PRZESKANUJ PONOWNIE WSZYSTKICH KONTRAHENTÓW
      ↓
  nowe trafienia → alert o wysokim priorytecie
```

**Punkt oznaczony gwiazdką jest najważniejszy w całej sekcji.** Kontrahent czysty wczoraj może być na liście dziś. Jednorazowe sprawdzenie przy zakładaniu jest bezwartościowe — a dokładnie tak robi większość systemów.

```sql
sanctions_list
  id, code, source_url, format
  current_version, last_fetched_at, last_changed_at

sanctions_entry
  id, list_id, list_version
  entity_type,              -- person | entity | vessel | aircraft
  primary_name, aliases text[]
  name_normalized, name_transliterated
  identifiers jsonb,        -- IMO, NIP, paszport, data urodzenia
  program, listed_at, delisted_at

screening_run
  id, organization_id, subject_type, subject_id
  list_versions jsonb,      -- ← wersje list użyte przy tym skanie
  screened_at, trigger,     -- create | booking | list_update | scheduled
  result, hit_count

screening_hit
  id, screening_run_id, sanctions_entry_id
  match_score, matched_on,  -- name | alias | identifier
  status,                   -- pending | true_positive | false_positive
  reviewed_by, reviewed_at, justification

screening_whitelist         -- zarządzanie fałszywymi trafieniami
  id, organization_id, subject_id, sanctions_entry_id
  approved_by, approved_at, expires_at, justification
```

`list_versions` w `screening_run` jest wymogiem audytowym. Pytanie kontrolera brzmi „na jakiej wersji listy sprawdzaliście to zlecenie" — i musisz umieć odpowiedzieć.

## 3.3 Dopasowywanie nazw

Największe źródło problemów. Konieczne:

- normalizacja: wielkość liter, znaki diakrytyczne, formy prawne (Ltd, GmbH, Sp. z o.o.), interpunkcja
- transliteracja: arabskie, cyrylica, chińskie — jedna osoba ma pięć zapisów łacińskich
- dopasowanie rozmyte z progiem konfigurowalnym, `RapidFuzz`
- dopasowanie po identyfikatorach — NIP, numer IMO — jest pewne i ma pierwszeństwo przed nazwą
- obsługa aliasów z list

Próg ustaw ostrożnie i pogódź się z fałszywymi trafieniami. Przeoczone trafienie prawdziwe to problem karny, fałszywe to minuta pracy.

## 3.4 Zakres skanowania — nie tylko kontrahenci

- **strony zlecenia**: klient, shipper, consignee, notify, agent, przewoźnik
- **statek** — po nazwie i numerze IMO. Statki bywają objęte sankcjami, a w żegludze morskiej to realne ryzyko; sprawdzaj przed bookingiem
- **kraje** — relacja przez port w kraju objętym restrykcjami
- **towar** — kod HS wobec wykazu towarów podwójnego zastosowania. Tu tylko sygnalizuj, nie rozstrzygaj: klasyfikacja podwójnego zastosowania wymaga wiedzy eksperckiej

## 3.5 Momenty skanowania

| Kiedy | Co |
|---|---|
| Zakładanie kontrahenta | wszystkie strony |
| Utworzenie zlecenia | wszystkie strony + kraje |
| Przed bookingiem | wszystkie strony + statek |
| **Aktualizacja listy** | **wszyscy aktywni kontrahenci** |
| Cyklicznie, co miesiąc | pełny przegląd |

---

# 4. PORTY ŚWIATA

## 4.1 Warstwy danych

**UN/LOCODE** jako podstawa — kilkadziesiąt tysięcy lokalizacji, w tym kilka tysięcy portów morskich. Wariant `cristan/improved-un-locodes` z poprawionymi współrzędnymi i aliasami, opisany w katalogu.

**World Port Index** (NGA, darmowy) uzupełnia o charakterystykę: głębokość, typ kotwicowiska, dostępne usługi, rodzaje obsługiwanych ładunków. Kilka tysięcy portów z parametrami, których UN/LOCODE nie ma.

**OpenStreetMap** — geometria portu, nabrzeża, terminale.

**Kody obiektów portowych ISPS** — do zgłoszeń bezpieczeństwa.

## 4.2 Czego UN/LOCODE nie da

**Poziomu terminalu.** Kod `PLGDY` to Gdynia, ale kontener idzie na BCT albo GCT, i to jest różnica operacyjna. Terminale buduj z trzech źródeł: rozkłady armatorów, własna historia bookingów, ręczne uzupełnianie.

```sql
port                         -- UN/LOCODE + World Port Index
terminal
  id, port_unlocode, code, name, operator_party_id
  facility_isps_code, lat, lng
  services text[], max_draft_m
  source, is_active
```

**Aktualności.** Część wpisów UN/LOCODE jest przestarzała, część lokalizacji nie ma kodu. Przewidź ręczne dodawanie lokalizacji własnych per organizacja — z oznaczeniem, że nie jest to kod oficjalny.

**Relacji obsługiwanych.** Który armator pływa skąd dokąd — to `carrier_service` z Aneksu 12, nie dane portowe.

---

# 5. TOWARY NIEBEZPIECZNE

## 5.1 Cztery regulacje, jedna baza

| Gałąź | Regulacja |
|---|---|
| Morze | Kodeks IMDG |
| Droga | ADR |
| Lotnictwo | IATA DGR |
| Kolej | RID |

Rdzeń jest wspólny — numery UN, klasy i grupy pakowania pochodzą z Przepisów Modelowych ONZ. Różnice dotyczą wymagań szczegółowych.

## 5.2 Model danych

```sql
dg_substance
  un_number,                    -- UN1203
  proper_shipping_name_en, proper_shipping_name_pl
  class, division,              -- 3 | 2.1 | 5.1 | 8 ...
  subsidiary_risks text[]
  packing_group,                -- I | II | III
  labels text[]
  is_marine_pollutant, is_environmentally_hazardous
  special_provisions text[]
  limited_quantity, excepted_quantity
  tunnel_code,                  -- ADR
  ems_code,                     -- IMDG: schemat awaryjny
  segregation_group,            -- IMDG: grupa segregacyjna
  source, source_version        -- ← która edycja przepisów

dg_segregation_rule
  class_a, class_b, requirement  -- away | separated | separated_by | prohibited

shipment_dg_item
  id, shipment_id, container_id
  un_number, packing_group, net_quantity, packaging_type
  flashpoint, technical_name
  declaration_path              -- DGD
```

## 5.3 Kwestia praw autorskich — ważna

**Tekst Kodeksu IMDG jest publikacją IMO objętą prawem autorskim.** To samo dotyczy IATA DGR. Nie możesz ich reprodukować w produkcie.

Natomiast **tekst umowy ADR wraz z załącznikami jest publikowany bezpłatnie przez EKG ONZ**, a same fakty — numer UN, prawidłowa nazwa przewozowa, klasa, grupa pakowania — nie są chronione jako takie.

Praktycznie:
- zbuduj tabelę numerów UN z publicznie dostępnych załączników ADR
- dla pól specyficznych dla IMDG (EmS, segregacja) potrzebujesz licencjonowanego źródła albo ręcznego uzupełnienia
- nie kopiuj tekstu przepisów do systemu
- zapisuj `source_version` — przepisy zmieniają się co dwa lata i zlecenie sprzed roku podlegało innej edycji

## 5.4 Funkcje, które faktycznie pomagają

**Walidacja zgłoszenia.** Klient podaje UN1263, klasa 3, grupa II. System sprawdza, czy kombinacja istnieje, czy temperatura zapłonu jest wymagana, czy nazwa techniczna jest potrzebna.

**Segregacja w kontenerze i na statku.** Dwa numery UN w jednej przesyłce — sprawdzenie tabeli segregacji. To jest wyliczenie, nie porada.

**Akceptacja przez armatora.** Nie każdy armator przyjmuje każdą klasę na każdej relacji. To rozszerzenie `carrier_service`:

```sql
carrier_dg_acceptance
  carrier_party_id, pol, pod
  accepted_classes text[], excluded_un_numbers text[]
  requires_pre_approval, lead_time_days
```

Przy wycenie ładunku klasy 5.1 na Amerykę Południową system od razu odsiewa armatorów, którzy go nie wezmą — zamiast dowiadywać się o tym przy bookingu.

**Ilości ograniczone.** Poniżej progu limited quantity część wymagań odpada. Sprawdzenie automatyczne oszczędza kosztów i opóźnień.

**Komplet dokumentów.** DGD, karta charakterystyki, certyfikat pakowania — lista wymagana per klasa, z blokadą zamknięcia zlecenia przy brakach.

## 5.5 Granica odpowiedzialności

**System waliduje i ostrzega. Nie klasyfikuje i nie doradza.**

Klasyfikacja towaru niebezpiecznego to odpowiedzialność nadawcy i doradcy do spraw bezpieczeństwa. Jeśli twoje oprogramowanie zasugeruje numer UN, a klasyfikacja okaże się błędna, wchodzisz w odpowiedzialność, której nie chcesz i której nie pokryje żadne ubezpieczenie.

Formułuj komunikaty jako sprawdzenia, nie jako porady: „podana kombinacja UN i grupy pakowania nie występuje w wykazie" zamiast „powinieneś użyć UN1203". Różnica jest zasadnicza i wynika wprost z zasady 4 głównej specyfikacji.
