# Aneks 18 — Rozszerzalność

Uczciwa odpowiedź na pytanie: czy dobudowywanie funkcji będzie łatwe.

---

# 1. GDZIE BĘDZIE ŁATWO

Te wzorce są w projekcie celowo i działają na twoją korzyść.

## 1.1 `charge` jako jedyne miejsce prawdy — najmocniejszy wzorzec

Dowód, że działa: dodaliśmy `FINCOST` (koszt kapitału) i `FXDIFF` (różnice
kursowe) jako zwykłe pozycje `shipment_charge`. **Wszystkie raporty
rentowności — per zlecenie, klient, relacja, handlowiec — zaczęły je
uwzględniać bez zmiany ani jednego zapytania.**

Każdy przyszły składnik wyniku wchodzi tą samą drogą: nowy `charge_code`
z flagą `computed`, funkcja licząca, koniec. Emisje CO₂, koszt ubezpieczenia,
rezerwa na reklamacje — wszystko tak samo.

## 1.2 Konfiguracja jako dane

Nowy typ opłaty, reguła marży, szablon dokumentu, schemat numeracji, pole
własne, workflow — to wiersz w bazie, nie wdrożenie. Klient, który potrzebuje
własnego kodu opłaty, dostaje go bez twojego udziału.

## 1.3 Framework kanałów

Nowy armator albo agregator to plik konfiguracyjny z mapowaniem. Jeśli
kiedykolwiek zacznie wymagać kodu, to sygnał do refaktoryzacji frameworku,
nie do pisania wyjątku.

## 1.4 Granice modułów

`import-linter` gwarantuje, że zmiana wnętrza modułu nie przecieka na zewnątrz.
Możesz przepisać silnik wyceny, nie dotykając zleceń.

## 1.5 Outbox

Nowy odbiorca zdarzenia nie wymaga zmiany nadawcy. Moduł emisji CO₂ podpina
się pod zdarzenia zlecenia bez ingerencji w moduł zleceń.

---

# 2. GDZIE ZABOLI

Tu jestem szczery, bo to są konsekwencje decyzji, które podjęliśmy świadomie.

## 2.1 Nowy wymiar doboru stawek

Silnik jest SQL-owy dla wydajności. Cena tej decyzji: dodanie nowego wymiaru
dopasowania — na przykład stawek zależnych od grupy towarowej albo od klasy
ADR — oznacza:

```
nowa kolumna → nowy indeks pokrywający → przepisanie zapytania doboru
→ ponowny test wydajności → sprawdzenie planu wykonania
```

To nie jest godzina, to jest dzień. W kodzie aplikacyjnym byłoby to szybsze,
ale wtedy nie zmieściłbyś się w budżecie 300 ms.

**Świadomy kompromis:** szybki system, droższy w rozszerzaniu w tym jednym
miejscu. Zaprojektuj `rate_line` z zapasem — dołóż `conditions jsonb` już teraz
na wymiary rzadkie, a kolumny indeksowane rezerwuj dla często używanych.

## 2.2 Funkcje ponadtenantowe są zamknięte

Zasada 12 blokuje zapytania sięgające po dane więcej niż jednego tenanta.
To jest właściwe — chroni przed ryzykiem antymonopolowym i umożliwia
przeniesienie klienta do osobnej bazy.

**Ale to znaczy, że nigdy nie zbudujesz benchmarku z danych klientów.**
Jeśli kiedyś tego zechcesz, jedyna droga to osobny produkt z jawną zgodą
i anonimizacją — czyli nowy projekt, nie rozszerzenie.

## 2.3 Retroaktywne przeliczenia

ADR-001 rezygnuje z pełnego event sourcingu. Konsekwencja: **nie przeliczysz
historycznych ofert nową regułą marży.** Masz historię zmian encji, nie
strumień zdarzeń do odtworzenia.

Jeśli za dwa lata zechcesz odpowiedzieć na pytanie „jak wyglądałaby nasza
marża w zeszłym roku przy obecnych regułach", odpowiedź brzmi: nie da się
bez przebudowy.

## 2.4 Funkcje przecinające wszystkie moduły

To jest realny problem i dotyczy każdego systemu tej wielkości. Przykłady:

| Funkcja | Ile modułów dotyka |
|---|---|
| Wielojęzyczność dokumentów | wszystkie generujące dokumenty |
| Wersjonowanie dowolnej encji | wszystkie |
| Globalne wyszukiwanie | wszystkie |
| Załączniki przy dowolnym obiekcie | większość |
| Komentarze i notatki | większość |
| Znaczniki i kategorie własne | większość |
| Eksport i import danych | wszystkie |

**Dodane później kosztują tyle, ile modułów już istnieje.** Przy module
czterdziestym to jest przepisywanie czterdziestu miejsc.

---

# 3. ROZWIĄZANIE: PRYMITYWY PLATFORMY

To jest odpowiedź na punkt 2.4 i najlepsza inwestycja w rozszerzalność.

## M-79 · Prymitywy platformy
**Domena:** N · **Spec:** `primitives.md` · **Kiedy:** faza 0, plaster 0.12

Sześć mechanizmów generycznych, dowiązywalnych do dowolnej encji przez parę
`(entity_type, entity_id)`. Zbudowane raz, dostępne dla każdego przyszłego modułu.

```sql
attachment                  -- załącznik przy czymkolwiek
  id, organization_id, entity_type, entity_id
  file_path, filename, mime_type, size_bytes
  visibility,               -- internal | customer
  uploaded_by, uploaded_at

note                        -- komentarz przy czymkolwiek
  id, organization_id, entity_type, entity_id
  body, is_internal, author_id, created_at
  mentions uuid[]           -- powiadomienia

tag                         -- znacznik przy czymkolwiek
  id, organization_id, name, color, scope_entity_type
entity_tag
  tag_id, entity_type, entity_id

subscription                -- kto ma być powiadamiany o czym
  id, organization_id, user_id
  entity_type, entity_id NULL,   -- NULL = wszystkie danego typu
  event_types text[], channels text[]

data_import                 -- import z CSV/Excel do dowolnej encji
  id, organization_id, entity_type
  file_path, mapping jsonb, status
  rows_total, rows_ok, rows_failed, errors jsonb

data_export                 -- eksport dowolnej encji
  id, organization_id, entity_type
  filter jsonb, format, file_path, status
```

**Koszt: około tygodnia w fazie 0. Oszczędność: tydzień na każdym module,
który by je potrzebował.** Przy trzydziestu modułach różnica jest oczywista.

### Wielojęzyczność jako prymityw

```sql
translation
  id, organization_id NULL,   -- NULL = systemowa
  entity_type, entity_id, field_name, language, value
```

Nawet jeśli uruchamiasz się po polsku, **struktura musi istnieć od początku**.
Dokładanie tłumaczeń do dwudziestu modułów później to praca, której nie
chcesz wykonywać.

### Wersjonowanie jako prymityw

`sqlalchemy-continuum` włączony globalnie w fazie 0 daje historię zmian
każdej encji bez pisania mechanizmu per moduł.

---

# 4. TEST ROZSZERZALNOŚCI

Nie zgaduj, czy architektura jest rozszerzalna. Zmierz.

Wykonaj te scenariusze po fazie 2 i zapisz czasy. Jeśli któryś przekracza
limit, architektura ma problem w tym miejscu.

| Scenariusz | Limit | Co sprawdza |
|---|---|---|
| Dodaj nowy kod opłaty z aliasami | 10 min | konfiguracja jako dane |
| Dodaj regułę marży dla nowego klienta | 5 min | kaskada narzutów |
| Dodaj nowy typ dokumentu z szablonem | 1 h | szablony per tenant |
| Dodaj nowego armatora przez API | 3 h | framework kanałów |
| Dodaj nowego armatora przez mail | 30 min | kanał mailowy |
| Dodaj pole własne na ofercie | 15 min | `custom_field` |
| Dodaj nowy status zlecenia z przejściem | 30 min | workflow konfigurowalny |
| Dodaj załącznik do nowej encji | 15 min | prymityw `attachment` |
| Dodaj nowy język interfejsu | 4 h | i18n od początku |
| Dodaj nowy wymiar doboru stawek | 1 dzień | tu wiadomo, że zaboli |
| Dodaj nowy moduł domenowy | 3 dni | granice i wzorzec plastra |

**Zapisz wyniki w `docs/EXTENSIBILITY.md` i powtórz test po fazie 5.**
Jeśli czasy urosły, architektura degraduje — i dowiesz się o tym z pomiaru,
zanim stanie się nieodwracalne.

---

# 5. CZTERY DECYZJE DO PODJĘCIA TERAZ

Tanie teraz, drogie później. Wszystkie w fazie 0.

**① Usuwanie: miękkie czy twarde.**
Rekomendacja: miękkie (`deleted_at`) dla encji biznesowych, twarde dla
technicznych. Zmiana później to migracja wszystkich tabel i wszystkich zapytań.

**② Identyfikatory: UUID czy sekwencje.**
Rekomendacja: UUID v7 — sortowalne czasowo, bezpieczne przy scalaniu baz,
gotowe na Citus. Sekwencje uniemożliwią późniejszy sharding.

**③ Strefy czasowe: wszystko w UTC czy lokalnie.**
Rekomendacja: UTC w bazie, konwersja w warstwie prezentacji, strefa na
`organization` i na `party`. Przy ETD w Gdyni i ETA w Szanghaju pomyłka
tutaj to godziny debugowania później.

**④ Nazewnictwo kluczy obcych i tabel łączących.**
Konwencja spisana w `GLOSSARY.md` w dniu czwartym. Brzmi błaho — przy stu
trzydziestu tabelach niespójność kosztuje realny czas agenta i twój.

---

# 6. ODPOWIEDŹ WPROST

**Tak, będziesz mógł dobudowywać funkcje** — pod trzema warunkami:

1. **Prymitywy platformy w fazie 0.** Tydzień pracy, który zwraca się
   przy piątym module.
2. **Cztery decyzje z sekcji 5 podjęte teraz**, nie odkładane.
3. **Test rozszerzalności powtarzany co kilka faz.** Degradacja architektury
   jest procesem, nie zdarzeniem — zauważysz ją tylko przez pomiar.

**Trzy rzeczy pozostaną trudne niezależnie od tego, co zrobisz:** nowy wymiar
doboru stawek, funkcje ponadtenantowe i retroaktywne przeliczenia historii.
To są świadome kompromisy za wydajność, izolację danych i prostotę — i warto
wiedzieć, że je zapłaciłeś.

Do rejestru dochodzi M-79. Do harmonogramu plaster `0.12` w fazie zerowej.
