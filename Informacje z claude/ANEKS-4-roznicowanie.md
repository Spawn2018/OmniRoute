# Aneks 4 — Jak zbudować produkt, którego nie ma

---

# CZĘŚĆ 1 — CZTERY ZAŁOŻENIA, KTÓRYCH KONKURENCJA NIE MOŻE ZMIENIĆ

Istniejące systemy spedycyjne mają w fundamentach cztery założenia. Każde z nich jest przestarzałe, a żadnego nie da się wymienić bez przepisania systemu. To są twoje cztery wektory różnicowania — i jedyne, które są obronne.

| Założenie zastane | Twoje założenie | Dlaczego nie do skopiowania |
|---|---|---|
| **Dane wprowadza człowiek.** Wszystko jest formularzem | Dane przychodzą jako nieustrukturyzowana poczta, strukturyzuje je maszyna, człowiek zatwierdza | Odwrócenie kierunku przepływu. Nie da się dokleić do systemu, w którym formularz jest jedynym wejściem |
| **Stawka to liczba.** Rekord w tabeli | Stawka to obiekt z pochodzeniem, wiarygodnością, świeżością i zmiennością | Zmienia typ danych w rdzeniu. Retrofit oznacza migrację każdej stawki i każdej wyceny |
| **System obsługuje człowiek przez ekran** | System jest narzędziem, którym operuje też agent programowy | Wymaga API-first od pierwszego dnia. Systemy z 20-letnim UI mają logikę w warstwie prezentacji |
| **Sprzedaż przez wdrożenie.** 9 miesięcy, dział IT | Samoobsługowe uruchomienie w jeden dzień | To jest inny model biznesowy, nie inna funkcja |

Wszystko poniżej wynika z tych czterech.

---

# CZĘŚĆ 2 — MODUŁY, KTÓRYCH NIKT NIE MA

## 2.1 Rozliczenie wyceny z fakturą — największy wyciek pieniędzy w spedycji

**To jest pojedyncza najmocniejsza funkcja z całego dokumentu.**

Wyceniłeś zlecenie z ośmioma pozycjami kosztowymi. Agent przysłał fakturę z jedenastoma. Trzy dodatkowe: dopłata, o której nie wspomniał w ofercie, korekta wagi, opłata za przestój. Nikt tego nie porównuje pozycja po pozycji, bo nie ma czasu — więc marża wyparowuje po cichu, zlecenie po zleceniu.

Ty masz obie strony w jednej bazie: ofertę agenta jako `rate_line` i jego fakturę jako `bill`. Porównanie jest trywialne technicznie i nie robi go nikt, bo nikt nie ma obu.

```sql
cost_variance
  id, shipment_id, bill_id
  charge_code
  quoted_amount, invoiced_amount, variance_amount, variance_pct
  variance_type,      -- new_charge | rate_diff | qty_diff | fx_diff
  source_rate_line_id,
  status,             -- detected | disputed | accepted | credited
  disputed_at, resolved_at, recovered_amount
```

**Efekt:** raz w miesiącu spedytor dostaje listę „agenci doliczyli w tym miesiącu 14 200 zł ponad ofertę, w tym 6 800 zł bez podstawy". Część odzyska, resztę uwzględni w przyszłych wycenach.

To jest funkcja, która **sama się finansuje w pierwszym miesiącu** i której argumentacja sprzedażowa jest jednozdaniowa.

## 2.2 Karta wyników agenta

Z tej samej pętli wynika drugi zbiór danych, którego nikt nie ma, bo nikt nie zamyka obiegu:

```sql
party_scorecard              -- przeliczane cyklicznie
  party_id, period
  inquiries_sent, response_rate, median_response_hours
  competitiveness_rank,      -- pozycja cenowa vs inni na tych samych relacjach
  quote_accuracy,            -- % pozycji zgodnych z późniejszą fakturą
  cost_variance_avg,         -- średnie przekroczenie
  rollover_rate, claim_rate, on_time_rate
  lanes_strong text[],       -- gdzie realnie wygrywa ceną
  overall_score
```

**Zastosowanie natychmiastowe:** zapytanie o stawkę na nową relację idzie najpierw do trzech agentów o najwyższym wyniku na tej relacji, nie do wszystkich piętnastu. Skrócenie czasu do oferty i mniej szumu u agentów.

**Zastosowanie długoterminowe:** to jest zbiór danych, który rośnie z każdym zleceniem i którego konkurent nie odtworzy, bo nie ma historii. To jest właściwa fosa — nie algorytm, tylko nagromadzone dane operacyjne.

## 2.3 Stawka jako obiekt probabilistyczny

Wszystkie systemy traktują stawkę jak pewnik. Nie jest.

```
Dziś:    fracht = 1850 USD
Powinno: fracht = 1850 USD
                  ├─ pochodzenie: cennik agenta X, arkusz FCL, wiersz 47
                  ├─ świeżość: 19 dni
                  ├─ wiarygodność: 0,94 (ekstrakcja + weryfikacja człowieka)
                  ├─ zmienność relacji: σ = 11% / 30 dni
                  └─ ryzyko zdarzeniowe: GRI ogłoszony na 01.10
```

Silnik wyceny propaguje niepewność do marży:

```
Marża: 12,4%  (przedział 8,1–15,2 przy ufności 80%)
Prawdopodobieństwo zejścia poniżej progu 8%:  22%
Główny czynnik: GRI 01.10, oferta ważna do 15.10
```

To nie jest ozdobnik statystyczny. To jest **inna decyzja handlowa** — spedytor widzi, że ta konkretna oferta jest ryzykowna, zanim ją wyśle.

## 2.4 Marża zagrożona i optymalna ważność oferty

Pojęcie zapożyczone z finansów, w spedycji nieobecne.

```
Ważność 30 dni → prawdopodobieństwo wygranej 34%, ryzyko marży 22%
Ważność 14 dni → prawdopodobieństwo wygranej 29%, ryzyko marży  6%
Ważność  7 dni → prawdopodobieństwo wygranej 21%, ryzyko marży  2%

Optimum wartości oczekiwanej: 14 dni
```

System sam proponuje okres ważności zamiast domyślnych trzydziestu dni. Wymaga danych win/loss z Aneksu 3 i zmienności z modułu rynkowego z Aneksu 2 — czyli **wynika z rzeczy, które i tak budujesz**, i dlatego jest wykonalne, a dla konkurencji nie.

## 2.5 Cyfrowy bliźniak kosztu zlecenia

Marża nie jest liczbą ustaloną przy wycenie. Zmienia się przy każdym zdarzeniu.

```
Zlecenie GD/2026/00412
  przy wycenie:        marża 1 840 zł  (12,1%)
  po bookingu:         marża 1 840 zł
  ⚠ rollover:          marża 1 340 zł  (–500 zł: detention 3 dni)
  ⚠ ETA +4 dni:        marża   940 zł  (–400 zł: prognoza składowania)
  po fakturze agenta:  marża   760 zł  (–180 zł: dopłata bez podstawy → spór)
```

Prognoza wyniku aktualizowana zdarzeniami, z alertem przy przekroczeniu progu. Dziś spedytor dowiaduje się o utraconej marży przy zamknięciu miesiąca — czyli wtedy, gdy nie może już nic zrobić.

## 2.6 Graf wiedzy o sieci

Z danych operacyjnych, których nikt inny nie ma:

- który agent jest realnie mocny na której relacji (nie deklaratywnie)
- który armator rolluje kontenery na którym serwisie i w jakim okresie
- które porty przeładunkowe generują opóźnienia w których miesiącach
- które kombinacje towar–relacja generują roszczenia
- gdzie twoja sieć ma dziury, których jeszcze nie zauważyłeś

Zasila `graphrag`, zasila rekomendacje przy wycenie, zasila kartę wyników. Wartość rośnie kwadratowo z wolumenem — i to jest jedyny mechanizm w całym produkcie, który działa na twoją korzyść z upływem czasu.

## 2.7 Cyfrowi współpracownicy

Nie chatbot. Zestaw autonomicznych agentów o wąskim zakresie, uruchamianych cyklicznie, każdy z bramką akceptacji i mierzalnym wynikiem.

| Agent | Zadanie | Bramka |
|---|---|---|
| **Ponaglacz** | agenci, którzy nie odpowiedzieli w połowie terminu | wysyłka automatyczna |
| **Strażnik świeżości** | wykrywa relacje z wygasającymi stawkami, generuje zapytania | akceptacja listy |
| **Rozjemca** | znajduje rozbieżności faktura–wycena, przygotowuje treść sporu | akceptacja treści |
| **Dyspozytor wyjątków** | rollover, poślizg ETA — projekt maila do klienta | akceptacja treści |
| **Uzupełniacz** | niekompletne zapytanie klienta → konkretne pytania zwrotne | wysyłka automatyczna |
| **Audytor cenników** | wykrywa anomalie i pomyłki jednostek w nowych stawkach | zawsze człowiek |

Każdy raportuje: ile zadań wykonał, ile zaakceptowano, ile pieniędzy odzyskał. To jest mierzalne i to się sprzedaje — inaczej niż „asystent AI".

## 2.8 Symulacja portfela

```
Pytanie: co jeśli stracę kontrakt z armatorem X?
Odpowiedź: 34% wolumenu azjatyckiego, marża spada o 3,1 pkt proc.
           przy przeniesieniu na drugiego najtańszego dostawcę.
           Relacje krytyczne: Gdynia–Ningbo, Gdynia–Ho Chi Minh
           
Pytanie: co jeśli paliwo +20%?
Odpowiedź: BAF +180 USD/FEU, marża –1,4 pkt proc. na kontraktach stałych,
           bez wpływu na spot.
```

Analiza scenariuszowa na poziomie portfela zleceń. Narzędzie dla właściciela, nie dla operatora — i argument przy sprzedaży, bo rozmawiasz wtedy z osobą decyzyjną.

---

# CZĘŚĆ 3 — SZYBKOŚĆ

## 3.1 Wycena poniżej sekundy

Spedytor wycenia kilkanaście razy dziennie. Trzy sekundy różnicy to nie wygoda, to odczucie klasy produktu.

- **Materializowany widok stawek** per relacja, przeliczany przy zmianie cennika, nie przy zapytaniu
- **Wstępnie policzone warianty** dla najczęstszych relacji klienta — gotowe, zanim zapyta
- **Live spot równolegle i przyrostowo**: stawki z bazy natychmiast, oferty z API doklejają się w miarę spływania
- **Twarde limity czasu**: adapter armatora nie odpowiada w 4 s → pokazujesz resztę z adnotacją

## 3.2 Interfejs pod klawiaturę

Niedoceniana rzecz. Spedytorzy to użytkownicy zaawansowani, pracujący w jednym narzędziu osiem godzin dziennie. Systemy, z których przychodzą, obsługuje się skrótami. Interfejs wymagający myszy przy każdej czynności odbierają jako wolny, niezależnie od czasu odpowiedzi serwera.

- paleta poleceń pod jednym skrótem
- pełna ścieżka zapytanie → wycena → wysyłka bez dotykania myszy
- wklejenie z Excela wprost do siatki pozycji
- skróty do najczęstszych operacji, konfigurowalne

To jest tydzień pracy i najsilniejszy sygnał „ten produkt zrobił ktoś z branży".

## 3.3 Wdrożenie w jeden dzień

Pierwsze zetknięcie klienta z produktem powinno być jego najlepszą funkcją:

```
Dzień 1, godzina 1:  rejestracja, dane firmy z GUS po NIP
         godzina 2:  przeciągasz swoje pliki Excel z cennikami
         godzina 3:  system je sparsował, przeglądasz i akceptujesz
         godzina 4:  pierwsza wycena na własnych stawkach
```

Moduł ekstrakcji, który zbudowałeś jako funkcję operacyjną, jest jednocześnie **twoim procesem onboardingu**. Konkurencja wdraża się miesiącami, bo migracja cenników jest ręczna. U ciebie jest produktem.

## 3.4 Architektura zdarzeniowa w rdzeniu

Decyzja niewidoczna dla użytkownika, otwierająca funkcje niemożliwe do dorobienia później:

- odtworzenie stanu na dowolny moment w przeszłości — „co wiedzieliśmy 14 sierpnia, gdy wysyłaliśmy tę ofertę"
- pełny audyt bez osobnego mechanizmu
- retroaktywna analiza: przeliczenie wszystkich ofert nową regułą marży
- naprawa błędu przez powtórzenie strumienia, nie przez ręczne korekty

Wprowadzone teraz kosztuje kilka dni projektowania. Dorobione później nie da się dorobić wcale.

---

# CZĘŚĆ 4 — PROFESJONALIZM BIZNESOWY

Rzeczy, które nie są funkcjami, a decydują, czy spedytor powierzy ci dane handlowe.

| Element | Dlaczego | Nakład |
|---|---|---|
| **Publiczna strona statusu** | Sygnał dojrzałości. Firma jednoosobowa bez niej wygląda jak projekt hobbystyczny | 1 dzień |
| **Publiczny changelog** | Klient widzi, że produkt żyje i że jego zgłoszenia trafiają do wydań | 1 dzień |
| **Dane w UE, jasno zadeklarowane** | Realna przewaga nad amerykańskimi SaaS w rozmowie o RODO | konfiguracja |
| **Gotowość na audyt** | Rejestr czynności, DPA, polityka retencji, lista podprzetwarzających. Pierwszy większy klient o to zapyta | 1 tydzień |
| **Eksport wszystkich danych na żądanie** | Zdejmuje obawę „a jak on jutro zniknie" | 3 dni |
| **Środowisko testowe dla klienta** | Sprawdza system na swoich danych przed zakupem. Skraca cykl sprzedaży | konfiguracja |
| **Publiczne API i dokumentacja** | Sygnał otwartości, umożliwia integracje partnerskie | wynika z OpenAPI |
| **Umowa SLA, której dotrzymasz** | Realny bije ambitny i złamany | 1 dzień |

---

# CZĘŚĆ 5 — CO ZROBIĆ Z TĄ LISTĄ

Muszę powiedzieć rzecz, która przeczy duchowi pytania.

**Wszystkiego naraz nie zbudujesz, a próba oznacza, że nie powstanie nic.** Powyżej jest osiem lat pracy dla zespołu. Dla jednej osoby z agentem kodującym to jest mapa na trzy do pięciu lat, nie plan na rok.

Wybór, który proponuję, gdyby trzeba było wskazać jeden łańcuch:

```
1. Pętla RFQ → agenci                    (Aneks 3, część 1)
2. Rozliczenie wyceny z fakturą          (2.1)
3. Karta wyników agenta                  (2.2)
4. Wdrożenie w jeden dzień               (3.3)
```

Te cztery są ze sobą powiązane i wzajemnie się wzmacniają. Pętla RFQ generuje dane o agentach. Rozliczenie faktur weryfikuje ich rzetelność. Karta wyników zamyka obieg i kieruje kolejne zapytania. Wdrożenie w jeden dzień sprawia, że klient dociera do tego wszystkiego w cztery godziny zamiast w trzy miesiące.

**Razem tworzą coś, czego nie ma, i czego nie da się skopiować przez dodanie funkcji** — bo wymagają posiadania całej pętli od zapytania po fakturę. Konkurent mający tylko ofertowanie albo tylko operacje nie zbuduje tego, choćby chciał.

Reszta z tego dokumentu to kierunki na lata drugi i trzeci. Zapisz je, wracaj do nich, ale nie zaczynaj.

Jedno zdanie na koniec, ważniejsze od całej listy: **oprogramowanie, którego nie ma, powstaje z jednej rzeczy zrobionej naprawdę dobrze, a nie z dwudziestu zrobionych poprawnie.** Wszystko powyżej jest tylko materiałem do wyboru tej jednej.
