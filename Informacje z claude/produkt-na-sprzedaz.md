# Produkt na sprzedaż — co się zmienia

Decyzja podjęta przed fazą 1 kosztuje tygodnie. Ta sama decyzja podjęta przy trzecim kliencie kosztuje przepisanie systemu.

---

## 1. Najważniejsza rekomendacja: nie sprzedawaj ERP

To jest jedyna rzecz z tego dokumentu, którą warto przemyśleć zanim napiszesz cokolwiek dalej.

**Sprzedaż wymiany ERP:**
- cykl decyzyjny 6–12 miesięcy
- decyzja zarządu, nie kierownika
- migracja danych historycznych, przestój, opór zespołu
- konkurujesz z systemem, który u nich działa od lat i nikt go nie lubi, ale wszyscy umieją
- pierwszy klient zajmie ci rok

**Sprzedaż modułu stawek i ofertowania jako dodatku:**
- cykl decyzyjny 2–6 tygodni
- decyzja kierownika działu, budżet operacyjny
- zero migracji — działa obok tego, co mają
- rozwiązuje ból, który każdy spedytor morski odczuwa codziennie: cenniki w Excelu, zapomniane dopłaty, oferta liczona 40 minut
- eksport oferty do ich systemu, integracja przez API albo najzwyklejszy plik

Wchodzisz wąsko, budujesz bazę klientów i zaufanie, a dopiero potem dobudowujesz moduły i proponujesz ścieżkę wyjścia z ich starego systemu. Odwrotna kolejność — najpierw pełne ERP, potem sprzedaż — to najczęstszy sposób, w jaki takie projekty umierają: dwa lata budowy, zero klientów, brak informacji zwrotnej.

**Konsekwencja praktyczna:** fazy 1–3 z poprzedniego planu zostają bez zmian. Faza 4 i dalsze — dopiero po pierwszych płacących klientach, i w kolejności, którą oni wskażą.

---

## 2. Zmiany architektoniczne przed fazą 1

### 2.1 Multi-tenancy — obowiązkowo od pierwszej migracji
`organization_id` w każdej tabeli + RLS na poziomie bazy, nie w kodzie aplikacji. Doklejenie tego później oznacza przepisanie każdego zapytania i każdego testu.

### 2.2 Konfigurowalność bez deploya — to jest funkcja, która decyduje o skalowalności
Każdy spedytor ma inne kody opłat, inne szablony dokumentów, inną numerację, inny obieg zlecenia. Jeśli każdy nowy klient wymaga zmiany w kodzie, przy piątym kliencie utrzymanie zjada cały twój czas i firma przestaje rosnąć.

Co musi być danymi w bazie, a nie kodem:
- słownik `charge_code` z aliasami — per organizacja, z globalnym zestawem bazowym
- szablony dokumentów (oferta, B/L, CMR) — per organizacja
- schemat numeracji dokumentów — wzorzec konfigurowalny
- statusy zlecenia i przejścia między nimi
- pola własne na zleceniu, ofercie i kontrahencie
- reguły marży: per klient, per relacja, per typ opłaty
- role i uprawnienia

Wzorzec do podpatrzenia: `frappe/frappe`. Cały ERPNext stoi na modelu, w którym typy dokumentów i pola są rekordami w bazie. To dlatego jeden zespół obsługuje tysiące wdrożeń.

### 2.3 Izolacja danych jako argument sprzedażowy
Twoi klienci są dla siebie konkurentami. Spedytor, który wgra do twojego systemu swoje stawki zakupowe, oddaje ci najbardziej wrażliwą informację, jaką ma. Pierwsze pytanie na każdym spotkaniu handlowym będzie brzmiało: „a kto jeszcze to widzi".

Musisz mieć na to odpowiedź techniczną, nie deklaratywną:
- RLS wymuszany przez bazę, z testami dowodzącymi izolacji
- osobne klucze szyfrowania per tenant dla plików źródłowych
- audit log dostępu — klient widzi, kto i kiedy patrzył na jego dane
- opcja instancji dedykowanej dla największych klientów (droższy pakiet, ten sam kod)

### 2.4 Eksport i klauzula wyjścia
Możliwość pobrania wszystkich swoich danych w otwartym formacie, w każdej chwili, bez pytania ciebie o zgodę. Brzmi jak oddawanie broni — działa odwrotnie. Zdejmuje największą obawę przed kupnem od jednoosobowego dostawcy: „co jak on jutro zniknie".

### 2.5 Metering od pierwszego dnia
Nawet zanim wystawisz pierwszą fakturę, zbieraj: liczbę zleceń, ofert, sparsowanych cenników, aktywnych użytkowników, wywołań API — per organizacja. Model cenowy wymyślisz za pół roku, ale danych wstecz nie odtworzysz, a bez nich będziesz wyceniał na wyczucie.

### 2.6 Wersjonowanie API i migracje bez przestoju
Od momentu, gdy klient zintegruje się z twoim API, nie możesz go zepsuć. Migracje bazy muszą być wstecznie zgodne w obrębie jednego wdrożenia — najpierw dodaj kolumnę, potem przepnij kod, potem usuń starą.

---

## 3. Model cenowy

### Wybór metryki
| Metryka | Ocena |
|---|---|
| Per użytkownik | **Rekomendowana jako baza.** Przewidywalna, klient rozumie, rośnie z jego firmą |
| Per zlecenie | Kusząca, ale klient zacznie ukrywać wolumen albo omijać system |
| Per sparsowany cennik | Dobra jako dodatek ponad limit — bezpośrednio odzwierciedla twój koszt |
| Płaski abonament | Zostawia pieniądze na stole przy dużych klientach |

**Propozycja:** abonament bazowy za instancję + opłata za użytkownika + limit cenników miesięcznie, nadwyżka rozliczana osobno. `getlago/lago` obsługuje dokładnie taki model.

### Poziom cen
Punkt odniesienia dla klienta to nie konkurencyjny software, tylko **koszt etatu**. Osoba przepisująca cenniki i licząca oferty kosztuje 8–12 tys. zł miesięcznie z narzutami. Jeśli twój system oszczędza połowę jej czasu i eliminuje jedną zapomnianą dopłatę na kwartał, przedział 1 000–2 500 zł miesięcznie dla małego spedytora jest łatwy do obrony.

Nie zaczynaj od niskiej ceny „żeby pozyskać klientów". Podniesienie ceny istniejącym klientom jest wielokrotnie trudniejsze niż start od właściwej.

### Argument ROI, którym sprzedajesz
Nie „automatyzacja" i nie „AI". Dwie liczby:
1. Godziny miesięcznie na wprowadzanie cenników i liczenie ofert
2. Wartość jednej dopłaty pominiętej w wycenie — pomnożona przez to, jak często się to zdarza

Drugą liczbę każdy spedytor zna z bólu i nikt jej nie liczy.

---

## 4. Pierwsi klienci

**LOGMAR i HHL to klient zero, nie referencja.** Dogfooding jest niezbędny, ale rynek uzna to za dowód niczego — a konkurenci HHL zobaczą konflikt interesów.

**Potrzebujesz 2–3 partnerów wdrożeniowych** spoza własnego kręgu: firm, które dadzą ci prawdziwe cenniki, prawdziwe przypadki brzegowe i godzinę tygodniowo na rozmowę. W zamian: niższa cena na dwa lata, wpływ na kolejność funkcji.

Ale **niech płacą coś od początku.** Darmowe wdrożenie nie zobowiązuje, nie generuje informacji zwrotnej i nie dowodzi, że produkt ma wartość. Nawet symboliczna kwota zmienia charakter relacji.

---

## 5. Konflikt interesów — problem, który wybuchnie przy trzecim kliencie

Pracujesz w dziale sprzedaży H&H Logistics. Chcesz sprzedawać narzędzie firmom, które są dla HHL konkurencją. To nie jest teoretyczny problem prawny — to jest rozmowa, którą trzeba odbyć zanim podpiszesz pierwszą umowę, a nie po tym, jak ktoś się zorientuje.

Warianty do rozważenia:
- pełne rozdzielenie: produkt w osobnym podmiocie, jasne zasady, brak przepływu danych
- HHL jako partner albo udziałowiec w podmiocie produktowym — konflikt zamieniony we wspólny interes
- ograniczenie rynku docelowego tak, by nie nachodzić na segment HHL

To decyzja handlowa i relacyjna, nie techniczna. Ale wpływa na architekturę — jeśli produkt ma być w osobnym podmiocie, dane i infrastruktura muszą być rozdzielone od początku.

---

## 6. Warstwa prawna — trzy rzeczy, których nie da się dorobić później

### 6.1 Powierzenie przetwarzania i podpowierzenie
Przetwarzasz dane osobowe klientów swoich klientów (kontakty u kontrahentów, dane kierowców). Potrzebujesz umowy powierzenia (DPA) z każdym klientem.

**Punkt najczęściej pomijany:** wysyłasz cenniki i dokumenty do zewnętrznego API modelu językowego. To jest **podpowierzenie przetwarzania** i musi być ujawnione w umowie z klientem — z nazwą dostawcy, lokalizacją przetwarzania i informacją o retencji. Klient, który się o tym dowie po fakcie, ma podstawę do rozwiązania umowy i do zgłoszenia naruszenia.

Praktyczna konsekwencja architektoniczna: przewidź przełącznik „przetwarzanie wyłącznie lokalne" dla klientów, którzy tego zażądają. Modele lokalne z sekcji o inferencji istnieją właśnie po to.

### 6.2 Ograniczenie odpowiedzialności
Twój system liczy ceny. Błąd w stawce to realna szkoda majątkowa u klienta. Umowa musi ograniczać odpowiedzialność do wysokości opłat z ostatnich 12 miesięcy i wyłączać szkody pośrednie. Bez tego jeden błąd w rate engine kończy firmę.

Do tego ubezpieczenie OC działalności IT. Kilka tysięcy złotych rocznie, i jest to jedna z niewielu pozycji na całej liście kosztów, przy której nie ma sensu oszczędzać.

### 6.3 SLA, którego dotrzymasz
Nie obiecuj 99,9% dostępności, będąc jedną osobą. Obiecaj to, co utrzymasz przy grypie i w wakacje: okno serwisowe, czas reakcji w dni robocze, jasno zdefiniowana ścieżka awaryjna. Klienci wolą realny SLA od ambitnego i złamanego.

---

## 7. Wąskie gardło, o którym warto wiedzieć wcześniej

Przy 3–5 klientach jedna osoba nie utrzyma jednocześnie: sprzedaży, wdrożeń, wsparcia i rozwoju. To nie jest kwestia pracowitości — to arytmetyka. Wdrożenie jednego klienta to 20–40 godzin. Wsparcie jednego klienta to 3–5 godzin miesięcznie. Przy pięciu klientach masz 25 godzin miesięcznie samego wsparcia, zanim napiszesz linijkę kodu.

Trzy wyjścia, każde do wyboru świadomie:
1. **Wspólnik techniczny** — ty sprzedajesz i wdrażasz, on rozwija
2. **Partner wdrożeniowy** — firma, która wdraża i wspiera na twojej licencji
3. **Świadomy limit** — pięciu klientów, wysoka cena, brak ambicji wzrostu

Najgorszy wariant to nie wybrać i odkryć problem w praniu.

---

## 8. Wielkość rynku — policz to sam

Makrodane o branży TSL są bezużyteczne dla twojej decyzji. <cite index="120-1">W Polsce działa ponad 125 tysięcy firm transportowych, ale zdecydowana większość to małe przedsiębiorstwa z flotą do pięciu pojazdów</cite> — to przewoźnicy drogowi, nie twoi klienci.

Twój profil klienta to spedytor morski z własną bazą stawek zakupowych i co najmniej dwoma osobami w ofertowaniu. Znasz ten rynek lepiej niż jakikolwiek raport. Metoda:

1. Wypisz z pamięci firmy, które spełniają ten profil w Trójmieście i okolicy
2. Pomnóż przez współczynnik dla reszty kraju
3. Rozważ Czechy, Słowację, kraje bałtyckie — ten sam problem, ta sama skala firm, brak lokalnych rozwiązań
4. Pomnóż przez realną cenę roczną

Jeśli wynik to kilkadziesiąt milionów — budujesz produkt. Jeśli kilka — budujesz bardzo dobre narzędzie dla siebie i kilku znajomych, co też jest sensowną odpowiedzią, tylko prowadzi do innych decyzji.

**Zrób to ćwiczenie na kartce w tym tygodniu.** Zanim napiszesz pierwszą migrację.

---

## 9. Zmieniony plan najbliższych miesięcy

| Kiedy | Co |
|---|---|
| Ten tydzień | Oszacowanie rynku na kartce. Rozmowa o konflikcie interesów z HHL |
| Tydz. 1–2 | Schemat bazy **z multi-tenancy i RLS**. Słownik `charge_code` per organizacja. Metering |
| Tydz. 3–6 | Kontrahenci + ręczne wprowadzanie stawek. Konfigurowalność szablonów od razu, nie później |
| Tydz. 7–9 | Silnik wyceny + PDF + wysyłka. **Pierwszy pokaz dla partnera wdrożeniowego** |
| Tydz. 10–15 | Pipeline AI. Równolegle: DPA, umowa licencyjna, OC |
| Tydz. 16–20 | Zlecenie morskie. Pierwsza umowa płatna |
| Potem | Kolejność modułów wskazują klienci, nie plan |

Zwróć uwagę na tydzień 7–9: pokaz przed zbudowaniem AI. Jeśli sam silnik wyceny z ręcznie wprowadzonymi stawkami nie zrobi wrażenia na spedytorze, to znaczy, że rozwiązujesz problem, którego nie ma — a dowiesz się o tym trzy miesiące wcześniej i za jedną trzecią kosztu.
