# Analiza ByteByteGo 2024 pod kątem OmniRoute

**Materiał:** 368 stron, zbiór postów o projektowaniu systemów.
**Ocena użyteczności:** z około 140 tematów **osiem** ma bezpośrednie
zastosowanie w twoim projekcie. Reszta dotyczy skali, której nie masz,
technologii, które świadomie odrzuciłeś, albo przygotowania do rozmów
kwalifikacyjnych.

To nie jest zarzut wobec materiału — to konsekwencja tego, że jest pisany
dla inżynierów w firmach o skali Netflixa, a ty budujesz produkt dla
kilkudziesięciu spedytorów.

**Ale te osiem pozycji wykryło cztery realne luki w naszej architekturze.**

---

# CZĘŚĆ I — LUKI WYKRYTE

## L-01 · Awarie systemu cache — brak obsługi ⚠

**Co znalazłem.** Materiał opisuje cztery tryby awarii pamięci podręcznej,
z których dwa dotyczą nas wprost. **Problem stada:** duża liczba kluczy
wygasa jednocześnie, zapytania uderzają bezpośrednio w bazę i ją przeciążają.
Rozwiązanie: unikać jednakowego czasu wygaśnięcia, dodać losowy składnik.
**Przenikanie cache:** klucz nie istnieje ani w cache, ani w bazie, aplikacja
nie może go uzupełnić, obciążenie rośnie na obu warstwach. Rozwiązanie:
buforowanie wartości pustych albo filtr Blooma.

**Dlaczego to nas dotyczy.** Zaprojektowaliśmy cache stawek per relacja
z jednakowym czasem życia. Przy imporcie cennika obejmującego sto relacji
wszystkie klucze wygasną w tej samej sekundzie — i sto zapytań uderzy
w silnik wyceny naraz. To jest podręcznikowy problem stada, który sami
sobie stworzyliśmy.

**Zmiana do wprowadzenia:**

```python
def cache_ttl(base_seconds: int) -> int:
    """Losowy rozrzut ±20% zapobiega jednoczesnemu wygaśnięciu."""
    return int(base_seconds * random.uniform(0.8, 1.2))

# przenikanie: buforuj brak wyniku
if result is None:
    cache.set(key, NULL_MARKER, ttl=cache_ttl(60))
```

| Mocne strony | Słabe strony |
|---|---|
| Eliminuje szczyt obciążenia po imporcie cennika | Dane w cache żyją niejednakowo długo — trudniej przewidzieć zachowanie |
| Buforowanie wartości pustych chroni przed zapytaniami o nieistniejące relacje | Znacznik pustej wartości trzeba obsłużyć wszędzie, inaczej wygląda jak brak cache |
| Kilkanaście linii kodu | Wymaga testu odtwarzającego problem stada |

**Co osiągniesz:** przewidywalny czas odpowiedzi po każdym imporcie cennika,
zamiast kilkusekundowego zastoju, o którym dowiesz się od klienta.

**Nakład: pół dnia. Plaster 2.4.**

## L-02 · Stronicowanie w API — brak specyfikacji ⚠

**Co znalazłem.** Materiał wymienia stronicowanie jako pierwszy z pięciu
sposobów poprawy wydajności API i opisuje je jako optymalizację dużych
zbiorów wyników przez strumieniowanie ich do klienta.

**Dlaczego to nas dotyczy.** Mamy listę stawek z pięćdziesięcioma tysiącami
wierszy i budżet 500 ms — a **nigdzie nie ustaliliśmy, jak stronicujemy.**
To jest przeoczenie w specyfikacji API publicznego i we wszystkich listach.

**Rozstrzygnięcie, które proponuję:**

| Kontekst | Metoda | Uzasadnienie |
|---|---|---|
| Listy w interfejsie | kursor po `(created_at, id)` | stabilna przy wstawianiu, wydajna przy głębokim przewijaniu |
| API publiczne | kursor, nagłówek `Link` | standard, przewidywalny dla integratora |
| Eksport | strumień, bez stronicowania | jeden przebieg, bez limitu |
| Raporty | offset z limitem twardym | akceptowalny przy małych zbiorach |

Odrzucamy stronicowanie po przesunięciu w listach: przy pięćdziesięciu
tysiącach wierszy `OFFSET 40000` skanuje czterdzieści tysięcy wierszy,
żeby je odrzucić.

| Mocne strony | Słabe strony |
|---|---|
| Stały czas odpowiedzi niezależnie od głębokości | Kursor nie pozwala skoczyć na stronę numer sto |
| Brak duplikatów i pominięć przy wstawianiu w trakcie przeglądania | Trudniejsze do wytłumaczenia integratorowi niż numer strony |
| Wymagane przez API publiczne od pierwszej wersji | Zmiana później łamie kontrakt |

**Co osiągniesz:** lista stawek otwiera się tak samo szybko na pierwszej
i na pięćsetnej stronie, a integrator klienta nie napisze pętli, która
zabije bazę.

**Nakład: 2 dni. Plaster 0.7, bo dotyczy wszystkich list.**

## L-03 · Strategia ponowień — nieokreślona

**Co znalazłem.** Materiał opisuje cztery strategie i wskazuje wykładniczą
z rozrzutem jako łączącą zalety pozostałych: znacząco zmniejsza obciążenie
systemu i prawdopodobieństwo kolizji ponowień, a losowy składnik dodatkowo
je rozprasza. Wada: losowość bywa źródłem dłuższych niż konieczne opóźnień.

**Dlaczego to nas dotyczy.** W kilku miejscach napisaliśmy „ponowienie
z wycofaniem" bez określenia którym. Przy sześciu adapterach armatorskich
odpytywanych równolegle wycofanie liniowe doprowadzi do burzy ponowień —
wszystkie spróbują ponownie w tej samej sekundzie.

```python
RETRY_PROFILES = {
    "carrier_api":  ExponentialJitter(base=1, max=30, attempts=3),
    "ksef":         ExponentialJitter(base=2, max=120, attempts=5),
    "bank":         ExponentialJitter(base=5, max=300, attempts=3),
    "email":        ExponentialJitter(base=10, max=600, attempts=5),
    "sanctions":    Linear(interval=60, attempts=10),   # nie pilne
}
```

| Mocne strony | Słabe strony |
|---|---|
| Brak burzy ponowień przy równoległym odpytywaniu | Przy błędzie przejściowym rozwiązanie może przyjść później, niż mogło |
| Profil per integracja zamiast jednej reguły | Więcej parametrów do przemyślenia |
| Chroni przed zablokowaniem konta u armatora za nadmierną liczbę wywołań | — |

**Co osiągniesz:** awaria jednego armatora nie kaskaduje na pozostałych,
a limity zapytań nie wyczerpują się przez ponowienia.

**Nakład: 1 dzień. Plaster 3.1, razem z frameworkiem kanałów.**

## L-04 · Kompresja i logowanie nieblokujące

**Co znalazłem.** Wśród pięciu sposobów poprawy wydajności API materiał
wymienia kompresję ładunku oraz logowanie asynchroniczne — wysyłanie logów
do bufora bez blokad i natychmiastowy powrót, zamiast operacji dyskowej
przy każdym wywołaniu.

**Dlaczego to nas dotyczy.** Odpowiedź z listą stawek to kilkaset kilobajtów
JSON. Nie włączyliśmy kompresji. A `structlog` domyślnie zapisuje
synchronicznie — przy pipeline ekstrakcji generującym tysiące wpisów
to realny koszt.

| Mocne strony | Słabe strony |
|---|---|
| Kompresja: mniejszy transfer, szybsze ładowanie list | Koszt procesora przy kompresji — nieistotny przy tej skali |
| Logowanie do bufora: brak operacji dyskowej w ścieżce żądania | Przy nagłej awarii procesu można stracić ostatnie wpisy z bufora |
| Obie zmiany to konfiguracja, nie kod | — |

**Co osiągniesz:** kilkadziesiąt procent krótszy czas ładowania list
i brak wahań opóźnienia przy intensywnym logowaniu.

**Nakład: 2 godziny. Plaster 0.1.**

---

# CZĘŚĆ II — DECYZJE POTWIERDZONE

Trzy nasze rozstrzygnięcia mają w tym materiale niezależne potwierdzenie.

## P-01 · Idempotencja

Materiał wymienia sześć przypadków wymagających idempotencji.
Trzy z nich to dokładnie nasze moduły: przetwarzanie płatności (klient nie
może zostać obciążony wielokrotnie przez ponowienia), zarządzanie
zamówieniami (wielokrotne wysłanie skutkuje jednym zamówieniem)
oraz systemy rozproszone i kolejki (ponowne przetworzenie wiadomości
bez skutków ubocznych).

To potwierdza zasadę trzynastą i klucz idempotencji na ofercie
wcześniejszej zapłaty, gdzie duplikat oznaczałby podwójny przelew.

## P-02 · Siedem strategii skalowania bazy

Materiał wymienia: indeksy, widoki materializowane, denormalizację,
skalowanie pionowe, buforowanie, replikację i podział na fragmenty.

**Mamy sześć z siedmiu.** Brakuje jawnego rozważenia skalowania pionowego
— a to jest najtańsza opcja przy twojej skali. Zanim sięgniesz po Citus,
większy serwer w Hetznerze rozwiązuje problem za ułamek złożoności.

Do dopisania w dokumencie architektury jako pierwszy krok ścieżki skalowania.

## P-03 · Postgres jako jedyna baza

Materiał opisuje architekturę Reddita, który przy ponad miliardzie
użytkowników miesięcznie **nadal opiera rdzeń modelu danych na Postgresie**,
z memcached przed nim. To jest niezależne potwierdzenie, że twoja decyzja
nie jest kompromisem wynikającym ze skali, tylko właściwym wyborem.

---

# CZĘŚĆ III — JEDNA DECYZJA DO PONOWNEGO PRZEMYŚLENIA

## Przechwytywanie zmian danych zamiast odpytywania outboxa

**Co znalazłem.** Materiał opisuje przechwytywanie zmian danych jako
mechanizm monitorujący dziennik transakcji bazy, przetwarzający zmiany
i publikujący je do systemów docelowych. Wskazuje, że Reddit używa tego
mechanizmu do replikacji danych i utrzymania spójności cache.

**Dlaczego to warto rozważyć.** W analizie optymalizacyjnej zaproponowałem
zastąpienie odpytywania tabeli outbox mechanizmem powiadomień Postgresa.
Przechwytywanie zmian jest trzecią opcją i rozwiązuje dodatkowo problem,
którego tamte dwie nie ruszają: **odświeżanie widoków materializowanych
i unieważnianie cache przy zmianie danych źródłowych.**

| Podejście | Zalety | Wady |
|---|---|---|
| **Outbox + odpytywanie** *(dziś)* | proste, zero komponentów | opóźnienie sekundowe, obciążenie odpytywaniem |
| **Outbox + powiadomienia** *(propozycja)* | opóźnienie milisekundowe, nadal zero komponentów | powiadomienie ginie przy braku słuchacza — potrzebny mechanizm nadrabiania |
| **Przechwytywanie zmian** | wychwytuje każdą zmianę, także spoza aplikacji; rozwiązuje unieważnianie cache | dodatkowy komponent do utrzymania, zwykle z brokerem |

**Moja rekomendacja pozostaje bez zmian: outbox z powiadomieniami.**
Uzasadnienie: przechwytywanie zmian to komponent, który trzeba monitorować
i który przy jednej osobie dokłada powierzchnię awarii. Korzyść — wychwytywanie
zmian dokonanych poza aplikacją — jest u ciebie znikoma, bo wszystko przechodzi
przez repozytoria.

**Ale zapisz to jako ADR z jawnym uzasadnieniem odrzucenia**, żeby za rok
nie wracać do pytania.

---

# CZĘŚĆ IV — CZEGO NIE BRAĆ

Materiał zawiera dużo treści, która przy twoim projekcie zaszkodzi,
jeśli potraktujesz ją jako wskazówkę.

| Temat | Dlaczego nie |
|---|---|
| Architektury Netflixa i Reddita | mikrousługi, Kafka, GraphQL, Kubernetes — skala i zespoły, których nie masz |
| Dziewięć praktyk dla mikrousług | świadomie wybraliśmy monolit modularny |
| Federacja GraphQL | rozwiązuje problem wielu zespołów, nie wielu modułów |
| Cassandra, CockroachDB, ElasticSearch | Postgres wystarcza, każdy dodatkowy komponent to koszt utrzymania |
| Wzorce Kubernetes | Docker Compose na Hetznerze przez lata |
| Treści przygotowujące do rozmów | Linux, algorytmy, struktury danych — nie dotyczą budowy produktu |

**Największe ryzyko tego materiału:** pokazuje rozwiązania firm o skali
miliarda użytkowników jako wzorce godne naśladowania. Przy dwudziestu
klientach każde z nich jest przerostem formy, który zabierze czas
potrzebny na funkcje.

---

# CZĘŚĆ V — PODSUMOWANIE ZMIAN

| # | Zmiana | Nakład | Plaster | Priorytet |
|---|---|---|---|---|
| 1 | Rozrzut czasu życia cache i buforowanie wartości pustych | 0,5 dnia | 2.4 | **wysoki** |
| 2 | Stronicowanie kursorowe we wszystkich listach i API | 2 dni | 0.7 | **wysoki** |
| 3 | Profile ponowień z wycofaniem wykładniczym i rozrzutem | 1 dzień | 3.1 | średni |
| 4 | Kompresja odpowiedzi i logowanie nieblokujące | 2 h | 0.1 | średni |
| 5 | Skalowanie pionowe jako pierwszy krok ścieżki | 0 | dokumentacja | niski |
| 6 | ADR o odrzuceniu przechwytywania zmian | 1 h | 0.4 | niski |

**Razem 3,5 dnia.**

## Co realnie osiągniesz

**Zmiana druga jest najważniejsza** i najłatwiej ją przeoczyć. Stronicowanie
kursorowe wprowadzone teraz jest konfiguracją. Wprowadzone po pierwszej
integracji klienta z API publicznym jest zmianą łamiącą kontrakt, na którą
musisz dać dwanaście miesięcy uprzedzenia.

**Zmiana pierwsza chroni przed problemem, który sami sobie stworzyliśmy.**
Jednakowy czas życia cache stawek plus import stustronicowego cennika równa
się szczyt obciążenia bazy. Pół dnia pracy, żeby to się nigdy nie wydarzyło.

**Zmiany trzecia i czwarta to higiena.** Dają zauważalną poprawę odczuwalnej
szybkości przy nakładzie liczonym w godzinach.

## Ocena materiału jako źródła

Wartość: **cztery wykryte luki przy trzech i pół dnia pracy na ich usunięcie.**
To dobry stosunek, ale wynika z tego, że czytałeś go pod konkretny projekt,
z gotową architekturą do porównania.

Gdybyś czytał go przed zaprojektowaniem systemu, prawdopodobnie
skończyłbyś z mikrousługami, Kafką i Kubernetesem — bo tak wyglądają
przykłady, a nie rozwiązania proporcjonalne do skali.
