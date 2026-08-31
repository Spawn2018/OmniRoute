# Korekta modelu — odcinki transportowe

Rozstrzygnięcie przed pierwszą migracją. Dotyczy M-35, M-48, M-49, M-89.

---

# 1. PROBLEM

Zaprojektowaliśmy:

```sql
shipment
  transport_mode    -- SEA_FCL | SEA_LCL | ROAD_LTL | ROAD_FTL | ROAD_PART
shipment_sea        -- szczegóły morskie
shipment_road       -- szczegóły drogowe
```

To zakłada **jedno zlecenie = jedna gałąź**. Ale typowe zlecenie morskie
wygląda tak:

```
Poznań (drzwi klienta) ──[droga]──▶ Gdynia ──[morze]──▶ Callao ──[kolej]──▶ Lima
```

Jedno zlecenie, trzy odcinki, trzech różnych podwykonawców, trzy faktury
kosztowe, jedna oferta dla klienta i jedna marża.

W obecnym modelu nie da się tego zapisać poprawnie.

---

# 2. ROZSTRZYGNIĘCIE

**`shipment` jest jednostką handlową. `shipment_leg` jest jednostką operacyjną.**

| Byt | Znaczenie |
|---|---|
| `shipment` | to, co sprzedałeś klientowi — jedna oferta, jedna marża, jeden zestaw dokumentów |
| `shipment_leg` | odcinek z własną gałęzią, przewoźnikiem, datami i statusem |
| `carrier_order` | zlecenie wysłane do podwykonawcy na konkretny odcinek |
| `bill` | faktura kosztowa powiązana ze zleceniem do podwykonawcy |

Uzasadnienie: klient kupił jedną usługę drzwi-drzwi, marża liczy się na
całości, konosament obejmuje całość, a tracking musi pokazać jedną oś czasu.

**Zlecenie czysto drogowe to zlecenie z jednym odcinkiem drogowym.**
Ten sam model obsługuje oba przypadki bez wyjątków.

---

# 3. ZMIANY W SCHEMACIE

```sql
-- shipment traci dyskryminator gałęzi
ALTER TABLE shipment DROP COLUMN transport_mode;
ALTER TABLE shipment
    ADD COLUMN service_type text NOT NULL,   -- door_door | port_port
                                             -- door_port | port_door
    ADD COLUMN primary_mode text NOT NULL;   -- gałąź główna, do raportowania

-- nowa encja: odcinek
CREATE TABLE shipment_leg (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id     uuid NOT NULL REFERENCES organization(id),
    shipment_id         uuid NOT NULL REFERENCES shipment(id) ON DELETE CASCADE,
    sequence            smallint NOT NULL,
    leg_type            text NOT NULL,       -- pre_carriage | main_carriage
                                             -- on_carriage | transshipment
    mode                text NOT NULL,       -- SEA_FCL | SEA_LCL | ROAD_FTL
                                             -- ROAD_LTL | RAIL | AIR | BARGE
    origin_location_id      uuid NOT NULL REFERENCES location(id),
    destination_location_id uuid NOT NULL REFERENCES location(id),
    carrier_party_id    uuid REFERENCES party(id),
    planned_departure   timestamptz,
    planned_arrival     timestamptz,
    actual_departure    timestamptz,
    actual_arrival      timestamptz,
    status              text NOT NULL DEFAULT 'planned',
    -- planned | ordered | confirmed | in_progress | completed | cancelled
    created_source      text NOT NULL DEFAULT 'auto',
    is_manually_overridden boolean NOT NULL DEFAULT false,
    override_reason     text,
    version             integer NOT NULL DEFAULT 1,
    created_at          timestamptz NOT NULL DEFAULT now(),
    updated_at          timestamptz NOT NULL DEFAULT now(),
    created_by          uuid REFERENCES app_user(id),
    deleted_at          timestamptz,
    UNIQUE (shipment_id, sequence)
);

-- szczegóły per gałąź przypięte do ODCINKA, nie do zlecenia
ALTER TABLE shipment_sea  RENAME TO shipment_leg_sea;
ALTER TABLE shipment_leg_sea
    DROP COLUMN shipment_id,
    ADD COLUMN leg_id uuid NOT NULL REFERENCES shipment_leg(id) ON DELETE CASCADE;

ALTER TABLE shipment_road RENAME TO shipment_leg_road;
ALTER TABLE shipment_leg_road
    DROP COLUMN shipment_id,
    ADD COLUMN leg_id uuid NOT NULL REFERENCES shipment_leg(id) ON DELETE CASCADE;

CREATE TABLE shipment_leg_rail (
    leg_id              uuid PRIMARY KEY REFERENCES shipment_leg(id) ON DELETE CASCADE,
    rail_service_id     uuid REFERENCES rail_service(id),
    train_number        text,
    origin_terminal_id  uuid REFERENCES terminal(id),
    destination_terminal_id uuid REFERENCES terminal(id),
    wagon_number        text,
    cim_smgs_number     text,
    gauge_change_at     uuid REFERENCES location(id),
    cutoff_at           timestamptz
);

-- zlecenie do podwykonawcy wiąże się z ODCINKIEM
ALTER TABLE carrier_order
    ADD COLUMN leg_id uuid NOT NULL REFERENCES shipment_leg(id),
    ADD COLUMN mode text NOT NULL;           -- ROAD | RAIL | BARGE

-- opłata wie, którego odcinka dotyczy
ALTER TABLE shipment_charge
    ADD COLUMN leg_id uuid REFERENCES shipment_leg(id);
-- NULL = opłata dotyczy całego zlecenia (dokumentacja, agencja)

-- kontener przypisany do odcinków, na których jest przewożony
CREATE TABLE shipment_leg_container (
    leg_id          uuid NOT NULL REFERENCES shipment_leg(id) ON DELETE CASCADE,
    container_id    uuid NOT NULL REFERENCES shipment_container(id),
    PRIMARY KEY (leg_id, container_id)
);

-- alokacja kosztu przejazdu dotyczy odcinka drogowego
ALTER TABLE tour_assignment
    DROP COLUMN shipment_id,
    ADD COLUMN leg_id uuid NOT NULL REFERENCES shipment_leg(id);

-- potwierdzenie dostawy per odcinek
ALTER TABLE proof_of_delivery
    ADD COLUMN leg_id uuid REFERENCES shipment_leg(id);

CREATE INDEX ix_leg_shipment ON shipment_leg (shipment_id, sequence)
    WHERE deleted_at IS NULL;
CREATE INDEX ix_leg_carrier ON shipment_leg (organization_id, carrier_party_id, status)
    WHERE status IN ('ordered','confirmed','in_progress');
```

---

# 4. JAK TO DZIAŁA W PRAKTYCE

## 4.1 Zlecenie morskie drzwi-drzwi

```
shipment  GD/2026/00412 · service_type: door_door · primary_mode: SEA_FCL

  leg 1  pre_carriage   ROAD_FTL   Poznań → Gdynia
         przewoźnik: Trans-Pol         carrier_order → bill
  leg 2  main_carriage  SEA_FCL    Gdynia → Callao
         armator: Hapag-Lloyd          booking → bill
  leg 3  on_carriage    RAIL       Callao → Lima
         operator: Ferrovías Perú      carrier_order → bill

  charges:
    DRAY-EXP  leg 1   koszt Trans-Pol      sprzedaż klientowi
    OFR       leg 2   koszt Hapag          sprzedaż
    OTHC      leg 2   koszt agenta         sprzedaż
    DTHC      leg 2   koszt agenta         sprzedaż
    DRAY-IMP  leg 3   koszt Ferrovías      sprzedaż
    DOCFEE-O  NULL    koszt agenta         sprzedaż  ← dotyczy całości
```

**Marża liczy się na zleceniu**, bo to jest jednostka handlowa.
**Rentowność per odcinek jest dostępna**, bo każda opłata wie, gdzie należy.

## 4.2 Zlecenie do podwykonawcy

Ten sam mechanizm dla drogi i kolei — różni się kanał wysyłki:

| Gałąź | Kanał | Moduł |
|---|---|---|
| Droga | portal przewoźnika albo mail | M-199, M-89 |
| Kolej | mail albo portal operatora | M-49, kanał z M-19 |
| Morze | booking API albo mail | M-89, M-19 |

```
leg.status: planned → ordered → confirmed → in_progress → completed
```

Przejście na `ordered` wysyła zlecenie. Na `confirmed` — podwykonawca przyjął
w portalu albo mailem. Blokada: przypisanie przewoźnika bez ważnych dokumentów
zgodnościowych (M-200) nie przechodzi.

## 4.3 Faktura kosztowa

```
bill → carrier_order → shipment_leg → shipment
```

Dzięki temu łańcuchowi:
- **rozliczenie wyceny z fakturą** (M-41) działa per odcinek
- **rezerwy kosztowe** (M-90) tworzą się dla odcinków bez faktury
- **koszt kapitału** (M-43) liczy się od faktycznych terminów płatności
  każdego podwykonawcy osobno
- **karta wyników** (M-13) ocenia każdego podwykonawcę na jego odcinkach

## 4.4 Tracking

Jedna oś czasu dla klienta, składana z odcinków:

```
✓ 12.09  Załadunek u nadawcy            leg 1
✓ 13.09  Przyjęcie na terminalu Gdynia  leg 1 → leg 2
✓ 15.09  Gate-in                        leg 2
✓ 18.09  Wypłynięcie                    leg 2
  20.10  Przybycie Callao (prognoza)    leg 2
  22.10  Odjazd pociągu (prognoza)      leg 3
  23.10  Dostawa Lima (prognoza)        leg 3
```

Zdarzenia DCSA z armatora trafiają na odcinek morski. Statusy z portalu
przewoźnika na odcinki lądowe. Klient widzi jedno.

---

# 5. CO TO ZMIENIA W SILNIKU WYCENY

Wycena drzwi-drzwi składa się z odcinków, każdy ze swojego źródła stawek:

```
zapytanie: Poznań → Lima, 2×40HC, DAP

  leg 1  dowóz drogowy      → rate_line z cennika przewoźnika
                              albo zapytanie do przewoźnika
  leg 2  fracht morski      → cennik agenta / API armatora / zapytanie
  leg 3  odwóz kolejowy     → cennik operatora albo zapytanie mailem

  quotation_gap wykrywa brak na KAŻDYM odcinku osobno
```

**Porównanie wariantów odcinka** staje się naturalne: odwóz drogą kontra
koleją z kosztem, czasem i emisją — to jest funkcja z Aneksu 14, która
w tym modelu wynika sama.

---

# 6. WPŁYW NA PLAN

| Plaster | Zmiana |
|---|---|
| **2.4** silnik wyceny | dobór stawek per odcinek, nie per zlecenie |
| **2.5** `quotation_gap` | luki wykrywane per odcinek |
| **6.1** konwersja oferta → zlecenie | tworzy odcinki z wariantów oferty |
| **6.2** maszyna stanów | dwa poziomy: zlecenie i odcinek |
| **6.5** rozliczenie z fakturą | dopasowanie przez `carrier_order` do odcinka |
| **8.1** moduł drogowy | `tour_assignment` wiąże się z odcinkiem |
| **8.8** kolej | `shipment_leg_rail` zamiast osobnego bytu |
| **8.17** portal przewoźnika | przewoźnik widzi swoje odcinki, nie zlecenia |

**Nakład: 3 dni w tygodniach 1–2.** Wprowadzone teraz kosztuje trzy dni.
Wprowadzone po fazie 6 oznacza migrację zleceń, opłat, faktur i alokacji.

---

# 7. ODPOWIEDŹ WPROST

**Tak — zlecenia drogowe i kolejowe na dowozy i odwozy kontenerów są częścią
zlecenia morskiego.** Nie jako osobne zlecenia, tylko jako odcinki tego samego.

Wysyłka zleceń do podwykonawców: `carrier_order` per odcinek, kanałem
odpowiednim dla gałęzi — portal przewoźnika przy drodze, mail przy kolei,
booking API przy morzu.

Rejestracja faktur kosztowych: `bill` powiązany ze zleceniem do podwykonawcy,
a przez nie z odcinkiem i zleceniem. Cała analityka kosztowa — rozliczenie
z wyceną, rezerwy, koszt kapitału, ocena podwykonawcy — działa na tym łańcuchu
bez wyjątków.

**To była ostatnia luka strukturalna w modelu.** Dobrze, że wyszła przed
pierwszą migracją, a nie po sześciu miesiącach.
