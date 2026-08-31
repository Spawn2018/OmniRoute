# Audyt kompletności planu głównego

Metoda: przegląd 39 dokumentów wobec `PLAN-GLOWNY.md`. Weryfikacja, czy każde
ustalenie, moduł i rozstrzygnięcie znalazło odzwierciedlenie w planie.

**Wynik: 10 luk.** Jedna to sprzeczność wewnętrzna po mojej stronie.

---

# CZĘŚĆ 1 — LUKI

## L-01 · Moduł sprzedażowy (pipeline handlowy) — POMINIĘTY CAŁKOWICIE

**Źródło:** `shipthis-inwentarz-modulow.md` §1.6

Inwentarz ShipThis zawierał pełny moduł Sales: dashboard sprzedaży, pipeline
z etapami i szansami, prognoza, follow-upy, aktywność handlowców w terenie.
Do rejestru 71 modułów **nigdy nie trafił**.

To nie jest drobiazg. Twój produkt zbiera `rfq`, `quotation`, `quotation_outcome`
i `lead` — czyli wszystkie dane potrzebne do pipeline'u — a nie ma warstwy,
która by je pokazała handlowcowi jako lejek.

## L-02 · Portal agenta — POMINIĘTY

**Źródło:** `ANEKS-3` §2.2

Prosty formularz z linkiem wysyłanym mailem: agent wrzuca cennik przez
przeglądarkę zamiast wysyłać załącznik. Dla współpracujących agentów eliminuje
problem parsowania u źródła. Oceniłem to na tydzień pracy przy dużej oszczędności
— i wypadło z rejestru.

## L-03 · Cyfrowy bliźniak kosztu zlecenia — POMINIĘTY

**Źródło:** `ANEKS-4` §2.5

Ciągłe przeliczanie prognozy wyniku zlecenia przy każdym zdarzeniu: rollover
odejmuje detention, poślizg ETA dokłada składowanie, faktura agenta koryguje
o rozbieżność. Alert przy przekroczeniu progu.

W rejestrze mam `FINCOST` i `FXDIFF` jako pozycje wyliczane, ale **nie ma
mechanizmu przeliczania na zdarzeniach**. To osobna funkcja i realnie użyteczna:
dziś spedytor dowiaduje się o utraconej marży przy zamknięciu miesiąca.

## L-04 · Wdrożenie w jeden dzień jako funkcja produktu — POMINIĘTE

**Źródło:** `ANEKS-4` §3.3

Ścieżka: rejestracja → dane z GUS po NIP → przeciągnięcie plików Excel z
cennikami → parsowanie i akceptacja → pierwsza wycena na własnych stawkach.
Cztery godziny.

Opisałem to jako jedną z czterech funkcji łańcucha różnicującego, po czym
w planie zostało tylko jako uwaga o onboardingu. **Moduł ekstrakcji jest
jednocześnie procesem wdrożenia** — to wymaga osobnego ekranu i przepływu,
nie dzieje się samo.

## L-05 · Architektura zdarzeniowa — REKOMENDOWANA I PO CICHU PORZUCONA ⚠

**Źródło:** `ANEKS-4` §3.4

Rekomendowałem rdzeń oparty na zdarzeniach: odtworzenie stanu na dowolny moment
w przeszłości, retroaktywne przeliczenie ofert nową regułą marży, naprawa przez
powtórzenie strumienia. Napisałem, że „dorobione później nie da się dorobić wcale".

Potem, w rewizji stosu, wprowadziłem `outbox` i `audit_log` — i **nie powiedziałem,
że rezygnuję z pełnego event sourcingu**. To jest sprzeczność, którą powinienem
był zgłosić.

**Rozstrzygnięcie, które proponuję:** pełny event sourcing to znaczna złożoność
dla jednej osoby. `outbox` plus `audit_log` na triggerze plus niemutowalne
`rate_line` dają 80% korzyści przy ułamku kosztu. Ale to musi być **świadoma
decyzja zapisana jako ADR**, a nie milczące pominięcie. Cena: nie odtworzysz
dowolnego stanu z przeszłości, tylko historię zmian encji.

## L-06 · Porównanie spot kontra kontrakt — POMINIĘTE

**Źródło:** `ANEKS-3` §2.3

Ta sama relacja, twoja stawka kontraktowa i live spot obok siebie z różnicą.
Decyzja podejmowana dziś z pamięci. Tanie w budowie, bo oba źródła już masz.

## L-07 · Profesjonalizm biznesowy — POMINIĘTY

**Źródło:** `ANEKS-4` §4

Osiem pozycji, które nie są funkcjami, a decydują, czy spedytor powierzy ci
dane handlowe: publiczna strona statusu, publiczny changelog, deklarowana
lokalizacja danych w UE, gotowość audytowa (rejestr czynności, DPA, retencja,
lista podprzetwarzających), eksport wszystkich danych na żądanie, środowisko
testowe dla klienta przed zakupem, publiczne API z dokumentacją, realny SLA.

W planie zostało tylko RODO w M-56. Reszta wypadła.

## L-08 · Warstwa rynkowa dla transportu drogowego — POMINIĘTA

**Źródło:** `ANEKS-2` §9

Ceny ON to 25–35% kosztu przejazdu i są publikowane codziennie. Model kosztu
przejazdu z automatyczną aktualizacją dopłaty paliwowej to funkcja
deterministyczna o natychmiastowym zwrocie, wpinająca się wprost w silnik
alokacji. Do tego stawki myta, płace minimalne kierowców w krajach tranzytu,
zakazy ruchu.

M-61 opisuje wyłącznie rynek morski.

## L-09 · Partnerzy wdrożeniowi — POMINIĘCI

**Źródło:** `produkt-na-sprzedaz.md` §4

LOGMAR i HHL to klient zero, nie referencja rynkowa. Potrzebujesz 2–3 firm
spoza własnego kręgu, dających realne cenniki i godzinę tygodniowo, w zamian
za niższą cenę na dwa lata. **I muszą płacić coś od początku** — darmowe
wdrożenie nie zobowiązuje i nie generuje informacji zwrotnej.

W planie jest tylko punkt kontrolny „demo dla trzech spedytorów", bez modelu
relacji.

## L-10 · Brak odnośników do katalogów — DROBNE

Plan nie odsyła do `katalog-repozytoriow.md` (407 pozycji) ani do
`50-narzedzi.md`. W praktyce oznacza to, że przy każdym module trzeba szukać
w rejestrze zamiast w planie.

---

# CZĘŚĆ 2 — UZUPEŁNIENIE REJESTRU

Sześć nowych modułów. Rejestr rośnie z 71 do 77.

## M-72 · Pipeline handlowy
**Domena:** M (sprzedaż) · **Spec:** `sales.md` · **Źródło:** ShipThis §1.6

| Obiekty | Funkcje |
|---|---|
| `opportunity` · `sales_stage` · `sales_activity` · `sales_forecast` | lejek z etapami · konwersja `lead` → `opportunity` → `quotation` · prognoza z krzywej elastyczności (M-25) · follow-upy · aktywność handlowca · dashboard sprzedaży |

Zasilany bez dodatkowej pracy przez `rfq`, `quotation_outcome` i `lead`.

## M-73 · Portal agenta
**Domena:** F · **Spec:** `rfq.md` · **Źródło:** Aneks 3 §2.2

| Obiekty | Funkcje |
|---|---|
| `agent_portal_token` · `agent_upload` | link jednorazowy wysyłany mailem · wgranie cennika przez przeglądarkę · walidacja przed przyjęciem · trafia do tej samej kolejki review co ekstrakcja |

Nakład: około tygodnia. Eliminuje parsowanie dla agentów współpracujących.

## M-74 · Cyfrowy bliźniak kosztu zlecenia
**Domena:** I (finanse) · **Spec:** `finance.md` · **Źródło:** Aneks 4 §2.5

| Obiekty | Funkcje |
|---|---|
| `shipment_margin_forecast` · `margin_event` | przeliczenie prognozy wyniku przy każdym zdarzeniu · powiązanie zdarzeń trackingu z kosztem (rollover → detention, poślizg → składowanie) · alert przy przekroczeniu progu · ścieżka od marży planowanej do zrealizowanej |

Wpina się w M-37 (wyjątki) i M-43/M-44 (koszt kapitału, FX).

## M-75 · Wdrożenie klienta
**Domena:** M · **Spec:** `onboarding.md` · **Źródło:** Aneks 4 §3.3

| Obiekty | Funkcje |
|---|---|
| `onboarding_session` · `onboarding_step` | kreator: dane z GUS po NIP → wgranie cenników → parsowanie → akceptacja → pierwsza wycena · postęp widoczny · miara: czas do pierwszej wyceny |

**To jest funkcja sprzedażowa, nie techniczna.** Konkurencja wdraża się
miesiącami, bo migracja cenników jest ręczna.

## M-76 · Zaufanie i przejrzystość
**Domena:** N (platforma) · **Spec:** `trust.md` · **Źródło:** Aneks 4 §4

| Obiekty | Funkcje |
|---|---|
| `status_incident` · `changelog_entry` · `data_export_job` · `trial_tenant` | publiczna strona statusu · changelog · eksport wszystkich danych tenanta na żądanie · środowisko próbne z danymi klienta · pakiet audytowy: rejestr czynności, DPA, retencja, lista podprzetwarzających |

Nakład: około dwóch tygodni łącznie. Każda pozycja z osobna jest tania,
a razem decydują, czy jednoosobowy dostawca wygląda wiarygodnie.

## M-77 · Dane rynkowe transportu drogowego
**Domena:** L · **Spec:** `market.md` · **Źródło:** Aneks 2 §9

| Obiekty | Funkcje |
|---|---|
| rozszerzenie `market_indicator` o wskaźniki drogowe | **ceny ON publikowane codziennie → automatyczna aktualizacja dopłaty paliwowej** · stawki myta · płace minimalne w krajach tranzytu · zakazy ruchu · sezonowość kierunkowa z własnych danych |

Warstwa deterministyczna jest tu mocniejsza niż w morzu, bo paliwo to
25–35% kosztu przejazdu i jest znane codziennie.

---

# CZĘŚĆ 3 — POPRAWKI DO PLANU GŁÓWNEGO

## Do części I (Produkt) — dopisz

**I.6 Partnerzy wdrożeniowi**

LOGMAR i HHL to klient zero, nie referencja. Potrzebujesz 2–3 firm spoza
własnego kręgu: dają realne cenniki, prawdziwe przypadki brzegowe i godzinę
tygodniowo, w zamian za niższą cenę na dwa lata i wpływ na kolejność funkcji.
**Płacą od początku, choćby symbolicznie** — darmowe wdrożenie nie zobowiązuje.

**I.7 Sygnały wiarygodności** → M-76.

## Do części II (Architektura) — dopisz ADR

**ADR-001: Rezygnacja z pełnego event sourcingu**

Rozważane: rdzeń zdarzeniowy z możliwością odtworzenia stanu na dowolny moment.
Wybrane: `outbox` + `audit_log` na triggerze + niemutowalne `rate_line`.
Uzasadnienie: 80% korzyści przy ułamku złożoności, wykonalne przez jedną osobę.
Konsekwencja: nie odtworzysz dowolnego stanu z przeszłości, tylko historię
zmian encji i pochodzenie stawek.

To ma być pierwszy ADR w repozytorium, napisany w dniu czwartym.

## Do części VII (Harmonogram) — wstaw

| Plaster | Moduł | Faza | Uzasadnienie umiejscowienia |
|---|---|---|---|
| `2.12` | M-75 | 2 | wdrożenie w jeden dzień jest częścią demo |
| `2.13` | M-76 | 2 | strona statusu i changelog przed pierwszym pokazem |
| `4.12` | M-73 | 4 | portal agenta po pipeline ekstrakcji |
| `5.16` | M-72 | 5 | pipeline handlowy, gdy są już `rfq` i `outcome` |
| `6.14` | M-74 | 6 | cyfrowy bliźniak po `FINCOST` i `FXDIFF` |
| `7.14` | — | 7 | porównanie spot vs kontrakt (L-06) |
| `8.15` | M-77 | 8 | rynek drogowy po module drogowym |

Razem 103 plastry zamiast 96.

## Do części X (Pierwsze dni) — zmień dzień 4

> **Dzień 4:** `ARCHITECTURE.md` i `GLOSSARY.md` piszesz sam.
> **Plus ADR-001** o rezygnacji z event sourcingu.

---

# CZĘŚĆ 4 — CO ZWERYFIKOWAŁEM I JEST W PORZĄDKU

Żeby audyt był rzetelny w obie strony — te elementy sprawdziłem i **są
poprawnie odzwierciedlone**:

| Obszar | Status |
|---|---|
| 14 zasad architektonicznych | wszystkie obecne, w tym trzy z rewizji stosu i jedna z badawczej |
| Trzy źródła stawek z różną semantyką ważności | obecne |
| `validity_basis` i cut-off DG | obecne |
| `is_applicable=false` jako wiedza negatywna | obecne |
| `FINCOST` i `FXDIFF` jako pozycje `shipment_charge` | obecne |
| `buy_source: customer_contract` | obecne |
| Token per odbiorca, kaskada 4 poziomów | obecne |
| Domena podobna = ostrzeżenie, nie sugestia | obecne |
| Pamięci wyłączone przy ekstrakcji | obecne |
| `network_member` per tenant | obecne |
| Przeskanowanie przy zmianie listy sankcyjnej | obecne |
| Statki po IMO, trasa dla kolei chińskiej | obecne |
| W/M liczone kodem, próg LCL vs FCL | obecne |
| Uczenie opłat portowych z faktur | obecne |
| RODO art. 22 przy decyzji kredytowej | obecne |
| Trzy kursy walutowe | obecne |
| Ekspozycja netto przy wycenie | obecne |
| Orkiestrator + subagenty, odrzucenie person | obecne |
| Hooks, Skills, Custom Modes, `/goal`, Automations | obecne |
| Metryka stosunku refaktoryzacji | obecne |
| Budżety wydajności | obecne |
| Oracle Frankfurt, moment przejścia na płatne | obecne |
| Punkt kontrolny po fazie 2 | obecne |
| Decyzja otwarta: morze czy droga | obecne |

**Wskaźnik pokrycia: 24 z 34 obszarów bez zastrzeżeń, 10 luk uzupełnionych
powyżej.** Po wprowadzeniu poprawek plan jest kompletny wobec ustaleń
tej rozmowy.
