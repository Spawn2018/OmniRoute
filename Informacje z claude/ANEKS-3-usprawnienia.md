# Aneks 3 — Co poprawić i co dodać

Krytyczny przegląd wszystkiego, co dotąd zaprojektowaliśmy.

---

# CZĘŚĆ 1 — NAJWIĘKSZA LUKA: PĘTLA ZAPYTAŃ

## 1.1 Czego brakuje

Zaprojektowaliśmy parsowanie cenników od agentów i parsowanie zapytań od klientów. Ale nie zaprojektowaliśmy tego, co dzieje się **pomiędzy** — a to jest największy pożeracz czasu w spedycji.

Realny przebieg dnia spedytora:

```
09:12  mail od klienta: "proszę o stawkę Gdynia-Callao, 2×40HC, meble"
09:15  sprawdza bazę → nie ma stawki na Callao
09:20  pisze do pięciu agentów, każdemu osobno, każdemu to samo
       ...czeka...
11:40  odpowiada agent A — cena w treści maila
14:20  odpowiada agent C — Excel w załączniku
16:55  odpowiada agent B — "a jaki dokładnie towar? HS?"
       ...pisze do klienta z pytaniem...
[następny dzień]
10:30  komplet odpowiedzi, porównuje w Excelu
11:15  wysyła ofertę klientowi
```

**Dwadzieścia sześć godzin.** Z czego pracy merytorycznej jest może czterdzieści minut. Reszta to przepisywanie, czekanie i pilnowanie.

Czas do oferty jest w spedycji morskiej najważniejszym pojedynczym czynnikiem wygrywania zleceń. Skrócenie tego z doby do dwóch godzin to nie usprawnienie — to inny produkt.

## 1.2 Pętla, którą warto zbudować

```
[1] Mail od klienta
      ↓ ekstrakcja (ten sam pipeline co cenniki)
[2] Zapytanie strukturalne + wykryte braki
      ↓ jeśli braki krytyczne → mail zwrotny z KONKRETNYMI pytaniami
[3] Sprawdzenie bazy: mam stawkę? świeżą? na cały zakres opłat?
      ↓ NIE  →
[4] rate_request — jedno zapytanie, wysyłka do N agentów
      każdy dostaje mail w swoim języku i formacie
      z terminem odpowiedzi i unikalnym adresem zwrotnym
      ↓
[5] Odpowiedzi wpadają na adres zwrotny
      ↓ ta sama ekstrakcja co cenniki — Excel, PDF, treść maila
[6] Porównanie ofert agentów obok siebie, znormalizowane
      ↓
[7] Wybór + marża → oferta do klienta
      ↓
[8] Odpowiedzi agentów zapisane jako rate_line — baza rośnie sama
```

Punkt 8 jest niedoceniany. Każde zapytanie ofertowe **buduje ci bazę cen** na przyszłość, nawet jeśli tej konkretnej oferty nie wygrasz.

## 1.3 Model danych

```sql
rfq                              -- zapytanie od klienta
  id, organization_id
  source,                        -- email | portal | phone | manual
  source_message_id, received_at
  customer_party_id, contact_email
  raw_text, extracted jsonb
  pol, pod, mode, incoterm, commodity, hs_code
  cargo jsonb, ready_date
  completeness_score,            -- 0-100
  missing_fields text[],
  status,                        -- new | clarifying | sourcing
                                 -- quoted | won | lost | abandoned
  quotation_id NULL
  first_response_at, quoted_at   -- ← metryki czasu do oferty

rate_request                     -- zapytanie do agentów
  id, rfq_id NULL,               -- może być też proaktywne
  pol, pod, mode, container_spec jsonb
  commodity, ready_date, deadline_at
  reply_to_address,              -- unikalny adres: rr-{token}@...
  status, sent_at

rate_request_recipient
  id, rate_request_id, party_id, contact_email
  language,                      -- mail w języku agenta
  sent_at, opened_at, responded_at
  response_message_id, rate_sheet_id NULL,   -- ← wynik ekstrakcji
  status,                        -- sent | opened | responded
                                 -- declined | no_response
  reminder_sent_at

rfq_clarification                -- pytania zwrotne do klienta
  id, rfq_id, missing_fields text[]
  sent_at, answered_at
```

## 1.4 Szczegóły, które decydują o działaniu

**Unikalny adres zwrotny per zapytanie.** `rr-{token}@rates.twojadomena.pl`. Odpowiedź agenta trafia automatycznie do właściwego zapytania, bez zgadywania po treści. Rozwiązuje problem, który zabija większość prób automatyzacji poczty.

**Mail do agenta w jego języku i formacie.** Chiński agent dostaje po angielsku z tabelą, niemiecki po niemiecku. Szablon per `party`, uczy się z historii.

**Konkretne pytania zwrotne, nie ogólne.** Zamiast „proszę o uzupełnienie danych" — „aby przygotować ofertę, potrzebuję: waga brutto, kod HS, gotowość ładunku". Klient odpowiada raz zamiast trzy razy.

**Automatyczne przypomnienie.** Agent nie odpowiedział w połowie terminu — przypomnienie idzie samo.

**Widok porównawczy.** Odpowiedzi znormalizowane do wspólnych kodów opłat, obok siebie, z podświetleniem brakujących pozycji u każdego agenta. To jest ekran, na którym spedytor podejmuje decyzję.

## 1.5 Metryka, która sprzedaje produkt

`time_to_quote` — mediana od maila klienta do wysłanej oferty. Zmierz to u siebie przed wdrożeniem, zmierz po. Różnica jest twoim głównym argumentem handlowym, wyrażonym w liczbie, a nie w przymiotnikach.

---

# CZĘŚĆ 2 — POPRAWKI W ISTNIEJĄCYCH MODUŁACH

## 2.1 Kwotowanie

**Negocjacja jako model, nie jako wersja.**
Klient odpisuje „za drogo, dacie 1600?". Dziś to nowa wersja oferty. Powinno być: historia negocjacji, próg minimalnej marży (`margin_floor` per klient i relacja) i ostrzeżenie, gdy propozycja schodzi poniżej. Bez tego handlowiec schodzi z ceny w mailu i nikt się nie dowiaduje.

**„Dlaczego ta cena" jednym kliknięciem.**
Masz provenance w danych, ale nie masz go w interfejsie. Rozwijany panel przy każdej pozycji: z którego cennika, z którego wiersza, jaka reguła marży, jaki kurs, z którego dnia. Potrzebne wewnętrznie (zaufanie do systemu) i zewnętrznie (spór z klientem).

**Wycena wsadowa.**
Klient przysyła pięć relacji naraz. Dziś to pięć osobnych przejść. Powinno być jedno zapytanie i jedna oferta zbiorcza.

**Świeżość stawki jako sygnał wizualny.**
Stawka sprzed trzech dni i sprzed pięciu tygodni wyglądają dziś tak samo. Powinny mieć wyraźnie różny status i wpływać na sugerowaną ważność oferty.

**Mapa pokrycia.**
Ekran pokazujący, na których relacjach masz stawki, na których wygasły, a gdzie masz białą plamę. Dziś dowiadujesz się o luce dopiero przy zapytaniu klienta — czyli w najgorszym momencie.

## 2.2 Zbieranie cen zakupowych

**Wykrywanie anomalii przed zapisem.**
Nowa stawka 40% poniżej poprzedniej to zwykle nie okazja, tylko błąd jednostki — „per W/M" odczytane jako „per kontener". Reguła progowa i wymuszona weryfikacja, zanim taka pozycja trafi do wyceny. To jest tańsze niż jedna stracona oferta.

**Wielojęzyczny słownik aliasów od startu.**
Cenniki przychodzą po polsku, angielsku, niemiecku i chińsku. Zaseeduj `charge_code_alias` w czterech językach zamiast czekać, aż nauczy się z korekt.

**Portal agenta.**
Prosty formularz z linkiem wysyłanym mailem: agent wrzuca cennik przez przeglądarkę zamiast wysyłać załącznik. Dla współpracujących agentów eliminuje problem parsowania u źródła. Tydzień pracy, duża oszczędność.

**Buforowanie promptu i Batch API.**
Schemat ekstrakcji i instrukcje nie zmieniają się między cennikami — powinny iść z cache'u. Przetwarzanie archiwum przez Batch API. Oszczędność rzędu połowy rachunku, przy zerowej zmianie logiki.

## 2.3 Wyceny spot

**Kolejkowanie i limity per tenant.**
Limity zapytań u armatorów są per konto. Bez centralnej kolejki jeden użytkownik wyczerpie limit całej organizacji przed południem.

**Degradacja zamiast błędu.**
API armatora nie odpowiada → pokazujesz ostatnią znaną cenę z oznaczeniem czasu, nie pusty ekran. Spedytor woli starą cenę z etykietą niż brak odpowiedzi.

**Porównanie spot z kontraktem.**
Ta sama relacja, twoja stawka kontraktowa i live spot obok siebie, z różnicą. Bezpośrednio prowadzi do decyzji, którą dziś podejmuje się z pamięci.

## 2.4 Tracking

**Zarządzanie wyjątkami zamiast listy zdarzeń.**
Lista milestone'ów to funkcja, którą ma każdy. Wartość jest w tym, czego nikt nie ma: proaktywnym wykrywaniu problemów.

| Wyjątek | Wykrycie | Wartość |
|---|---|---|
| **Rollover** | kontener nie wypłynął zadeklarowanym statkiem | klient dowiaduje się od ciebie, nie od odbiorcy |
| **Poślizg ETA > 3 dni** | porównanie z ETA z bookingu | czas na reakcję u odbiorcy |
| **Zegar demurrage ruszył** | rozładunek + free time | **bezpośrednio pieniądze** |
| **Cut-off VGM za 24h bez zgłoszenia** | kalendarz vs status | uniknięcie rolloveru |
| **Kontener stoi > X dni** | brak zdarzenia | wykrycie zapomnianej przesyłki |
| **Zmiana portu przeładunku** | zdarzenie trasy | wpływ na tranzyt |

**Watchdog free time to najbardziej opłacalna funkcja w całym trackingu.** Demurrage i detention to koszty, które powstają z przeoczenia, a nie z decyzji.

**Powiadomienie do klienta, nie tylko do ciebie.**
Automatyczny mail lub SMS przy zdarzeniach istotnych dla klienta. Redukuje telefony „gdzie jest mój kontener" o rząd wielkości — a to jest czas twojego zespołu.

## 2.5 Dokumenty

**Walidacja krzyżowa przed wystawieniem.**
Dane na B/L kontra booking kontra VGM kontra faktura. Niezgodność numeru kontenera, wagi albo nazwy odbiorcy wykryta przed wysłaniem zamiast po. Korekta B/L kosztuje realne pieniądze i czas.

**Pętla zatwierdzenia draft B/L.**
Wysyłasz draft klientowi, on zatwierdza lub zgłasza poprawki w portalu, ty widzisz status. Dziś to wymiana pięciu maili z załącznikami o tej samej nazwie.

**Komplet dokumentów per typ zlecenia.**
Definiowana lista wymaganych dokumentów, widoczny postęp, blokada zamknięcia zlecenia przy brakach.

## 2.6 Moduł predykcyjny

**Dodaj to, co ważniejsze od indeksów: własną elastyczność cenową.**

Z danych win/loss można policzyć, przy jakiej marży wygrywasz u konkretnego klienta i na konkretnej relacji. To jest sygnał, którego nie ma żaden indeks rynkowy, bo dotyczy wyłącznie ciebie.

```sql
quotation_outcome
  quotation_id, outcome,         -- won | lost | expired | withdrawn
  lost_reason,                   -- price | transit | schedule | other
  competitor_price NULL,         -- jeśli klient powie
  our_price, our_margin_pct, decided_at
```

Po stu ofertach na relacji masz krzywą: przy marży 8% wygrywasz 70%, przy 14% wygrywasz 30%. To bezpośrednio ustawia `margin_rule` i jest wart więcej niż prognoza SCFI.

**Rozrzut cen jako alarm, nie jako raport.**
Odkryłeś CV 80,5% w danych drogowych. To powinno działać na bieżąco: gdy handlowiec wycenia relację znacząco poniżej lub powyżej mediany z ostatnich ofert, system to sygnalizuje **przed wysłaniem**.

---

# CZĘŚĆ 3 — CO WARTO DODAĆ

Uszeregowane wg stosunku wartości do nakładu.

| # | Funkcja | Nakład | Dlaczego |
|---|---|---|---|
| 1 | **Watchdog free time** | mały | Zapobiega kosztom powstającym z przeoczenia. Najszybszy zwrot w całym systemie |
| 2 | **`time_to_quote` jako metryka** | mały | Twój główny argument handlowy, wyrażony liczbą |
| 3 | **„Dlaczego ta cena"** | mały | Zaufanie do systemu i obrona przy sporze |
| 4 | **Wykrywanie anomalii w cennikach** | mały | Jedna złapana pomyłka jednostki zwraca koszt budowy |
| 5 | **Pętla RFQ → agenci** | duży | Największa zmiana jakościowa. Część 1 |
| 6 | **Zarządzanie wyjątkami w trackingu** | średni | Odróżnia od systemów pokazujących listę zdarzeń |
| 7 | **Portal agenta** | mały | Eliminuje parsowanie u współpracujących agentów |
| 8 | **Elastyczność cenowa z win/loss** | średni | Cenniejsza niż prognoza rynkowa |
| 9 | **Walidacja krzyżowa dokumentów** | średni | Korekta B/L kosztuje realnie |
| 10 | **Mapa pokrycia stawek** | mały | Widzisz luki przed klientem, nie po |
| 11 | **Widget wyceny na stronie klienta** | średni | Kanał pozyskiwania zapytań, działa nocą |
| 12 | **Porównanie spot vs kontrakt** | mały | Decyzja podejmowana dziś z pamięci |

**Zacznij od pozycji 1–4.** Cztery małe funkcje, każda zwraca się w pierwszym miesiącu, żadna nie wymaga nowej architektury.

---

# CZĘŚĆ 4 — CZEGO NIE DODAWAĆ

Równie ważne jak lista powyżej. Każda z tych rzeczy wygląda atrakcyjnie i każda zje miesiąc bez zwrotu.

**Własny tracking z AIS.** Pozycja statku to nie pozycja kontenera. Zdarzenia od armatorów wystarczą, AIS dokłada mapkę i nic więcej.

**Benchmark rynkowy z własnej bazy indeksów.** Ryzyko licencyjne opisane w Aneksie 2. Tylko w modelu subskrypcji klienta.

**Chatbot dla klientów końcowych.** Klient spedytora chce wiedzieć, gdzie jest kontener — do tego wystarczy status w portalu i powiadomienie. Chatbot dokłada powierzchnię błędu bez wartości.

**Aplikacja mobilna.** Responsywny interfejs wystarczy przez pierwsze dwa lata. Aplikacja to drugi produkt do utrzymania.

**EDI, zanim klient go zażąda.** Duża praca, wąskie zastosowanie. Poczekaj na konkretne żądanie z konkretną specyfikacją.

**Własna księgowość.** Ustalone i warte powtórzenia.

**Fracht lotniczy równolegle.** Inny model danych (chargeable weight, AWB, IATA), inny rynek, inni agenci. Dopiero gdy morze i droga stoją.

**Wielojęzyczny interfejs przed pierwszym klientem zagranicznym.** Przygotuj strukturę, ale nie tłumacz.

---

# CZĘŚĆ 5 — TRZY RZECZY, KTÓRE ZMIENIŁBYM W SPECYFIKACJI

**1. `rfq` powinno być encją pierwszej klasy, nie preludium do `quotation`.**
W obecnym modelu zapytanie klienta jest tylko wejściem. Powinno mieć własny cykl życia, własne metryki i własny widok listy — bo większość zapytań nigdy nie stanie się ofertą, a i tak niosą informację o rynku i o kliencie.

**2. `rate_line` powinno wiedzieć, skąd przyszło w sensie procesu, nie tylko pliku.**
Dodaj `origin_context`: cennik okresowy, odpowiedź na konkretne zapytanie, wynik przetargu, stawka spot. Stawka z odpowiedzi agenta na pilne zapytanie ma inną wiarygodność i inną trwałość niż pozycja z kwartalnego cennika.

**3. Metryki produktowe powinny być w schemacie od tygodnia pierwszego, nie w `usage_metric` jako dodatek.**
`time_to_quote`, wskaźnik wygranych, konwersja oferta–booking, świeżość stawek, skuteczność ekstrakcji. To nie jest telemetria — to jest funkcja produktu, którą klient pokaże swojemu szefowi, żeby uzasadnić zakup.
