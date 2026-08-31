# Audyt kompletności modułów

---

# CZĘŚĆ I — STAN FAKTYCZNY

## 1.1 Klasyfikacja

| Poziom | Definicja | Liczba |
|---|---|---|
| **A — kompletny** | wszystkie 12 sekcji standardu, gotowy do implementacji bez pytań | **1** |
| **B — rozwinięty** | model danych, reguły, przepływ; brak przypadków brzegowych i błędów | **11** |
| **C — zarys** | tabela obiektów, lista funkcji, rozstrzygnięcia | **~140** |
| **D — pozycja katalogowa** | nazwa i jedno zdanie | **~60** |

## 1.2 Które są na jakim poziomie

**Poziom A:** M-50 kolej Chiny–Europa.

**Poziom B:** M-17 stawki · M-18 opłaty portowe · M-19 kanały armatorskie ·
M-20 ekstrakcja · M-21 silnik wyceny · M-22 narzuty · M-30 zapytania do agentów ·
M-43 koszt kapitału · M-44 różnice kursowe · M-207 finansowanie ·
M-208 dyskonto.

**Poziom C:** większość modułów z rejestru — mają obiekty i funkcje, brakuje
przepływów, przypadków brzegowych, obsługi błędów i kryteriów akceptacji.

**Poziom D:** M-137 do M-178 z katalogu warstw B i C.

## 1.3 Co to oznacza w praktyce

Agent dostający specyfikację poziomu C zada od pięciu do piętnastu pytań
przy pierwszym plastrze albo — gorzej — nie zada i zgadnie.

**Poziom C wystarcza do zaplanowania. Nie wystarcza do zbudowania.**

---

# CZĘŚĆ II — STANDARD KOMPLETNEGO MODUŁU

Dwanaście sekcji. Plik `docs/spec/<moduł>.md`, do 400 linii.
Powyżej — podział na `<moduł>-<część>.md`.

```markdown
# M-xx · Nazwa

## 1. Cel i zakres
Dwa zdania: po co istnieje. Trzy punkty: co robi.
Trzy punkty: czego świadomie nie robi.

## 2. Pojęcia
Terminy specyficzne dla modułu, których nie ma w GLOSSARY.

## 3. Model danych
Tabele z pełnym DDL: kolumny, typy, ograniczenia, indeksy, RLS.
Diagram powiązań. Uzasadnienie każdego indeksu.

## 4. Reguły biznesowe
Ponumerowane, sprawdzalne. Każda z podaniem, gdzie jest egzekwowana:
baza, serwis, interfejs.

## 5. Przepływy
Maszyna stanów albo diagram sekwencji. Wszystkie przejścia z warunkami.
Ścieżki powrotu i anulowania.

## 6. Obliczenia
Wzory z przykładami liczbowymi. Odwołania do domain/calc.
Reguły zaokrągleń. Przypadki zerowe i graniczne.

## 7. Przypadki brzegowe
Lista z oczekiwanym zachowaniem. To jest sekcja, która najczęściej
decyduje o jakości implementacji.

## 8. Błędy i wyjątki
Katalog wyjątków domenowych, komunikaty dla użytkownika,
kody dla API, sposób obsługi.

## 9. Droga ręczna
Co użytkownik może utworzyć, zmienić, usunąć i nadpisać.
Jak działa przycisk „przelicz automatycznie".

## 10. Powiązania
Zdarzenia wysyłane i odbierane. Moduły zależne i zależące.
Kontrakty między modułami.

## 11. Interfejs
Ekrany, kluczowe interakcje, skróty klawiszowe, stany
loading/empty/error/partial.

## 12. Kryteria akceptacji
Sprawdzalne maszynowo. Podstawa testów i weryfikatora.
```

## 2.1 Sekcje, których brakuje najczęściej

Analiza modułów poziomu B pokazuje, że brakuje przede wszystkim:

| Sekcja | Brak w |
|---|---|
| **7. Przypadki brzegowe** | wszystkich |
| **8. Błędy i wyjątki** | wszystkich |
| **9. Droga ręczna** | wszystkich poza tymi z Aneksu 24 |
| **6. Obliczenia z przykładami** | większości |
| **11. Interfejs** | większości |
| **12. Kryteria akceptacji** | wszystkich poza planem |

**To są sekcje, których agent nie wymyśli poprawnie.** Model danych zgadnie
z nazw, reguły biznesowe częściowo — ale przypadku „klient przysłał zapytanie
o relację, na której mamy stawkę wygasającą dzień po planowanym wypłynięciu"
nie wymyśli.

---

# CZĘŚĆ III — WZORZEC REFERENCYJNY: M-06

Pełna specyfikacja modułu o średniej złożoności. Wzorzec dla pozostałych.

```markdown
# M-06 · Słownik opłat

## 1. Cel i zakres

Słownik kodów opłat jest fundamentem całego systemu rozliczeniowego.
Każda kwota — zakupowa i sprzedażowa — ma przypisany kod, który określa
jej charakter, podstawę naliczenia i miejsce w strukturze kosztu.

**Robi:** utrzymuje słownik kodów per organizacja z zestawem globalnym ·
mapuje nazwy z cenników i faktur na kody · uczy się aliasów z korekt ·
określa wymagalność opłat wg incoterm i gałęzi.

**Nie robi:** nie ustala wysokości opłat (M-17, M-18) · nie decyduje
o zastosowaniu (M-21) · nie nalicza (domain/calc).

## 2. Pojęcia

**Kod opłaty** — identyfikator rodzaju kosztu, np. OTHC.
**Alias** — wariant nazwy używany przez konkretnego dostawcę.
**Strona** — origin, freight, filing, destination, internal.
**Podstawa naliczenia** — jednostka, wg której liczy się kwota.
**Wymagalność** — czy opłata musi wystąpić przy danym incoterm.

## 3. Model danych

    CREATE TABLE charge_code (
        id              uuid PRIMARY KEY DEFAULT uuid_generate_v7(),
        organization_id uuid REFERENCES organization(id),  -- NULL = globalny
        code            text NOT NULL,
        category        text NOT NULL,
        side            text NOT NULL,
        default_basis   text NOT NULL,
        default_currency currency_code,
        applies_to      text[] NOT NULL DEFAULT '{}',   -- FCL|LCL|ROAD|RAIL|AIR
        is_percentage   boolean NOT NULL DEFAULT false,
        percent_of      text,
        has_free_time   boolean NOT NULL DEFAULT false,
        is_formula      boolean NOT NULL DEFAULT false,
        formula_note    text,
        required_for_incoterms text[] NOT NULL DEFAULT '{}',
        usual_on_lanes  jsonb,          -- statystyka do wykrywania luk
        account_code    text,           -- konto przychodowe
        account_code_cost text,         -- konto kosztowe
        vat_rate_code   text REFERENCES vat_rate(code),
        is_visible_to_customer_default boolean NOT NULL DEFAULT true,
        is_active       boolean NOT NULL DEFAULT true,
        effective_from  date NOT NULL DEFAULT CURRENT_DATE,
        effective_to    date,
        sort_order      integer,
        created_source  text NOT NULL DEFAULT 'seed',
        is_manually_overridden boolean NOT NULL DEFAULT false,
        override_reason text,
        version         integer NOT NULL DEFAULT 1,
        created_at      timestamptz NOT NULL DEFAULT now(),
        updated_at      timestamptz NOT NULL DEFAULT now(),
        created_by      uuid REFERENCES app_user(id),
        deleted_at      timestamptz,
        CONSTRAINT chk_side CHECK (side IN
            ('origin','freight','filing','destination','internal')),
        CONSTRAINT chk_basis CHECK (default_basis IN
            ('PER_CONTAINER','PER_BL','PER_SHIPMENT','PER_WM','PER_TON',
             'PER_CBM','PER_TEU','PER_KG','PER_LDM','PER_PALLET',
             'PER_CONTAINER_DAY','PER_HOUR','PERCENT','FLAT')),
        CONSTRAINT chk_percent CHECK (
            (is_percentage AND percent_of IS NOT NULL) OR NOT is_percentage),
        CONSTRAINT chk_validity CHECK (
            effective_to IS NULL OR effective_from <= effective_to)
    );

    CREATE UNIQUE INDEX ux_charge_code
        ON charge_code (COALESCE(organization_id,
            '00000000-0000-0000-0000-000000000000'), code)
        WHERE deleted_at IS NULL;

    CREATE INDEX ix_charge_code_lookup
        ON charge_code (organization_id, side, is_active)
        WHERE deleted_at IS NULL;
    -- uzasadnienie: silnik wyceny filtruje po stronie przy doborze
    -- opłat wymaganych dla incoterm

    CREATE TABLE charge_code_alias (
        id              uuid PRIMARY KEY DEFAULT uuid_generate_v7(),
        organization_id uuid REFERENCES organization(id),
        charge_code_id  uuid NOT NULL REFERENCES charge_code(id),
        alias           text NOT NULL,
        alias_normalized text NOT NULL,   -- wielkie litery, bez znaków
        language        char(2),
        party_id        uuid REFERENCES party(id),  -- alias tego dostawcy
        source,                            -- seed | learned | manual
        confidence      numeric(4,3) NOT NULL DEFAULT 1.0,
        confirmed_by    uuid REFERENCES app_user(id),
        confirmed_at    timestamptz,
        usage_count     integer NOT NULL DEFAULT 0,
        last_used_at    timestamptz,
        created_at      timestamptz NOT NULL DEFAULT now(),
        deleted_at      timestamptz
    );

    CREATE UNIQUE INDEX ux_alias
        ON charge_code_alias (
            COALESCE(organization_id, '00000000-0000-0000-0000-000000000000'),
            COALESCE(party_id, '00000000-0000-0000-0000-000000000000'),
            alias_normalized)
        WHERE deleted_at IS NULL;

    CREATE INDEX ix_alias_trgm
        ON charge_code_alias USING gin (alias_normalized gin_trgm_ops);
    -- uzasadnienie: dopasowanie rozmyte przy nieznanym aliasie

    CREATE TABLE charge_code_embedding (
        charge_code_id  uuid PRIMARY KEY REFERENCES charge_code(id),
        embedding       vector(1024),
        model_version   text NOT NULL,
        computed_at     timestamptz NOT NULL DEFAULT now()
    );

    CREATE INDEX ix_charge_embedding
        ON charge_code_embedding USING hnsw (embedding vector_cosine_ops);

## 4. Reguły biznesowe

R1. Kod globalny (organization_id NULL) jest widoczny dla wszystkich
    organizacji. Egzekwowane w zapytaniu, nie w RLS.
R2. Organizacja może utworzyć kod o tym samym symbolu co globalny —
    wtedy jej wersja ma pierwszeństwo. Egzekwowane w serwisie.
R3. Kod użyty w co najmniej jednej ofercie nie może być usunięty,
    wyłącznie dezaktywowany. Egzekwowane wyzwalaczem.
R4. Alias jest unikalny w obrębie pary organizacja–dostawca.
    Egzekwowane indeksem.
R5. Kod procentowy musi wskazywać podstawę naliczenia.
    Egzekwowane ograniczeniem.
R6. Zmiana podstawy naliczenia kodu używanego w aktywnych cennikach
    wymaga zatwierdzenia. Egzekwowane w serwisie przez M-179.
R7. Alias potwierdzony przez człowieka ma pewność 1.0 i pierwszeństwo
    przed dopasowaniem rozmytym.
R8. Kod z wymagalnością dla incoterm musi wystąpić w ofercie albo
    zostać jawnie wykluczony. Egzekwowane w M-21.

## 5. Przepływy

### 5.1 Mapowanie nazwy na kod

    tekst z cennika
        │
        ▼
    normalizacja: wielkie litery, bez znaków diakrytycznych,
    bez interpunkcji, skrócenie wielokrotnych spacji
        │
        ▼
    ① dopasowanie dokładne aliasu dla tego dostawcy    → pewność 1.00
        │ brak
        ▼
    ② dopasowanie dokładne aliasu organizacji          → pewność 0.95
        │ brak
        ▼
    ③ dopasowanie dokładne aliasu globalnego           → pewność 0.90
        │ brak
        ▼
    ④ dopasowanie rozmyte (pg_trgm, próg 0.75)         → pewność 0.60–0.85
        │ brak
        ▼
    ⑤ podobieństwo wektorowe (próg 0.80)               → pewność 0.50–0.75
        │ brak
        ▼
    ⑥ nierozpoznany → kolejka review, is_mapped = false

### 5.2 Uczenie aliasu

    korekta w kolejce review
        │
        ▼
    zapis aliasu z party_id, source='learned', confidence=1.0
        │
        ▼
    przeliczenie usage_count i last_used_at
        │
        ▼
    następne wystąpienie → dopasowanie na poziomie ①

## 6. Obliczenia

Moduł nie nalicza kwot. Dostarcza podstawę naliczenia, którą stosuje
domain/calc.

Przykład rozstrzygania podstawy przy konflikcie:

    cennik podaje:  "THC 310 USD per container"
    charge_code:    OTHC, default_basis = PER_CONTAINER
    wynik:          zgodność, basis = PER_CONTAINER

    cennik podaje:  "Documentation fee 85 USD per shipment"
    charge_code:    DOCFEE-O, default_basis = PER_BL
    wynik:          ⚠ rozbieżność → basis z cennika ma pierwszeństwo,
                    ostrzeżenie w kolejce review

## 7. Przypadki brzegowe

| Przypadek | Zachowanie |
|---|---|
| Alias pasuje do dwóch kodów z równą pewnością | kolejka review, nie zgadujemy |
| Cennik zawiera kod, którego nie ma nigdzie | tworzy się jako propozycja, nie kod aktywny |
| Dostawca używa tego samego skrótu na dwie różne opłaty | alias z party_id rozstrzyga; bez party_id → review |
| Kod ma podstawę procentową, a podstawa nie występuje w ofercie | pozycja pomijana z ostrzeżeniem |
| Organizacja dezaktywuje kod globalny | dezaktywacja lokalna, kod globalny nietknięty |
| Nazwa po chińsku, brak aliasu | próba wektorowa, potem review |
| Alias zawiera tylko cyfry albo jeden znak | odrzucany przy zapisie |
| Zmiana kodu w cenniku po jego zatwierdzeniu | nowy rekord rate_line, stary superseded |

## 8. Błędy i wyjątki

| Wyjątek | Kiedy | Komunikat | Kod API |
|---|---|---|---|
| `ChargeCodeNotFound` | odwołanie do nieistniejącego | „Nie znaleziono kodu opłaty: {code}" | 404 |
| `DuplicateChargeCode` | kod istnieje w organizacji | „Kod {code} już istnieje" | 409 |
| `ChargeCodeInUse` | próba usunięcia używanego | „Kod użyty w {n} ofertach. Możesz go dezaktywować." | 409 |
| `AmbiguousAlias` | alias pasuje do wielu | „Nazwa {alias} pasuje do kilku kodów" | 422 |
| `InvalidPercentBase` | procent bez podstawy | „Kod procentowy wymaga wskazania podstawy" | 422 |
| `BasisChangeRequiresApproval` | zmiana podstawy używanego kodu | „Zmiana wymaga zatwierdzenia" | 403 |

## 9. Droga ręczna

**Tworzenie:** formularz pełny oraz szybkie dodanie z poziomu wyceny
(nazwa, podstawa, strona — reszta później).
**Edycja:** wszystkie pola; zmiana podstawy wymaga zatwierdzenia.
**Usuwanie:** miękkie; przy użyciu w ofertach wyłącznie dezaktywacja.
**Aliasy:** dodawanie, usuwanie, przypisanie do dostawcy, zmiana kodu docelowego.
**Nadpisanie mapowania:** w kolejce review użytkownik wskazuje inny kod;
zapis jako alias potwierdzony.
**Przelicz automatycznie:** ponowne mapowanie pozycji po zmianie słownika,
z podglądem, co się zmieni.
**Import i eksport:** CSV z kodami i aliasami, z mapowaniem kolumn.

## 10. Powiązania

**Wysyła zdarzenia:**
- `charge_code.created` → M-18 (możliwa nowa reguła opłaty portowej)
- `charge_code.deactivated` → M-21 (ostrzeżenie w aktywnych ofertach)
- `charge_code_alias.learned` → M-20 (aktualizacja słownika ekstrakcji)

**Odbiera zdarzenia:**
- `extraction.unmapped_charge` → utworzenie propozycji kodu
- `bill.charge_unrecognized` → jw.

**Zależy od:** M-01, M-03, M-07 (waluty), M-82 (stawki VAT)
**Zależą od niego:** M-17, M-18, M-20, M-21, M-22, M-40, M-41, M-90

## 11. Interfejs

**Lista kodów:** tabela z filtrem po stronie, kategorii i statusie;
kolumna liczby użyć; oznaczenie kodów globalnych i własnych.
**Karta kodu:** dane podstawowe, aliasy z liczbą użyć, historia zmian,
lista cenników używających.
**Kolejka nierozpoznanych:** nazwa źródłowa, kontekst, propozycje z pewnością,
przyciski akceptacji i wskazania innego kodu.
**Szybkie dodanie:** modal z trzema polami, wywoływany z wyceny.
**Skróty:** `n` nowy kod, `a` nowy alias, `/` szukaj.

## 12. Kryteria akceptacji

- [ ] Zestaw 60 kodów globalnych zaseedowany z aliasami w 4 językach
- [ ] Mapowanie „TERMINAL HANDLING POL" → OTHC działa na poziomie ③
- [ ] Alias potwierdzony ręcznie działa na poziomie ① przy następnym wystąpieniu
- [ ] Alias tego samego skrótu dla dwóch dostawców rozstrzyga się poprawnie
- [ ] Próba usunięcia kodu użytego w ofercie zwraca 409
- [ ] Zmiana podstawy naliczenia tworzy wniosek o zatwierdzenie
- [ ] Test izolacji tenantów dla charge_code i charge_code_alias
- [ ] Mapowanie 1000 nazw poniżej 2 sekund (p95)
```

---

# CZĘŚĆ IV — PROCEDURA ROZWIJANIA POZOSTAŁYCH

## 4.1 Zasada

**Nie rozwijaj wszystkich.** Rozwijaj ten, który za chwilę budujesz.
Specyfikacja napisana pół roku przed implementacją zdezaktualizuje się,
zanim ją wykorzystasz.

**Reguła: moduł osiąga poziom A najpóźniej w dniu rozpoczęcia plastra.**
Rozwinięcie to pierwsza czynność plastra, przed planem.

## 4.2 Polecenie dla Claude Code

```
Rozwiń docs/spec/<moduł>.md z poziomu C do poziomu A.

Wzorzec: docs/spec/charge-codes.md — zachowaj dokładnie tę strukturę
dwunastu sekcji.

Materiał źródłowy:
- obecna treść docs/spec/<moduł>.md
- rejestr: docs/MODULES.md, wpis <M-xx>
- powiązane aneksy: <lista plików>
- schemat bazy: przez MCP Postgres

Wymagania:
- sekcja 3: pełny DDL z ograniczeniami, indeksami i uzasadnieniem
  każdego indeksu; typy domenowe z ANALIZA-KOMPLETNOSCI §1.1
- sekcja 4: reguły ponumerowane, każda z miejscem egzekwowania
- sekcja 7: minimum osiem przypadków brzegowych
- sekcja 8: katalog wyjątków z komunikatami po polsku i kodami HTTP
- sekcja 9: droga ręczna wg wzorca W-01 z Aneksu 24
- sekcja 12: kryteria sprawdzalne maszynowo

Zasady:
- zero wymyślania: brak informacji oznacz jako DO USTALENIA
- obliczenia wyłącznie przez domain/calc, nie własne implementacje
- maksimum 400 linii; powyżej podziel na części
- zachowaj wszystkie rozstrzygnięcia z rejestru bez zmian

Na końcu wypisz listę pozycji DO USTALENIA jako pytania do mnie.
```

## 4.3 Weryfikacja po rozwinięciu

```bash
# długość
wc -l docs/spec/<moduł>.md          # < 400

# kompletność sekcji
grep -c "^## " docs/spec/<moduł>.md  # = 12

# braki do rozstrzygnięcia
grep -n "DO USTALENIA" docs/spec/<moduł>.md

# przypadki brzegowe
sed -n '/## 7/,/## 8/p' docs/spec/<moduł>.md | grep -c '^|'  # >= 8
```

Trzy losowe reguły biznesowe sprawdź wobec aneksów źródłowych.
Jeśli któraś nie ma pokrycia — powtórz.

## 4.4 Nakład

| Poziom wyjściowy | Czas rozwinięcia | Twój udział |
|---|---|---|
| C → A, moduł prosty | 30 min | 15 min weryfikacji |
| C → A, moduł złożony | 90 min | 40 min weryfikacji |
| D → A | nie rób — najpierw do C przy planowaniu | — |

**Dla 35 modułów faz 0–3: około 40 godzin łącznie**, rozłożone po
jednym module przed każdym plastrem.

---

# CZĘŚĆ V — KOLEJNOŚĆ

Rozwijaj w kolejności budowy, nie numeracji.

| Kiedy | Moduły do rozwinięcia |
|---|---|
| **Przed fazą 0** | M-01, M-02, M-03, M-04 |
| Przed fazą 1 | M-05, M-06 ✓, M-07, M-08, M-10, M-80, M-82, M-86 |
| Przed fazą 2 | M-17, M-18, M-21, M-22, M-23, M-24, M-26, M-27, M-83, M-84, M-85, M-205 |
| Przed fazą 3 | M-19, M-36, M-37, M-34 |
| Przed fazą 4 | M-20, M-11, M-32 |

Reszta — przed odpowiednią fazą.

## Trzy moduły, które rozwiń najpierw

**M-01 wielodostępność.** Buduje się w plastrze 0.3, czyli za kilka dni,
a jego przypadki brzegowe decydują o bezpieczeństwie całego produktu.

**M-21 silnik wyceny.** Najbardziej złożony w systemie i najbardziej
zależny od przypadków brzegowych: stawka wygasająca między gotowością
a wypłynięciem, brak jednej opłaty przy kompletnym zestawie, konflikt
podstaw naliczenia, oferta na relację bez pokrycia.

**M-03 konfiguracja.** Wszystkie moduły z niego korzystają, a jest
zarysem — dziesięć tabel wymienionych bez reguł i przepływów.
