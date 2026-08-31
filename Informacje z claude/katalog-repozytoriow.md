# Katalog repozytoriów — ERP spedycyjny

Wszystko, co znalazłem, w jednym miejscu, z rozszerzonymi opisami. Ułożone w kolejności, w jakiej będziesz tego potrzebował — nie alfabetycznie.

Przy każdej pozycji: **co to jest** i **kiedy po to sięgasz**. Repozytoria bywają przenoszone między organizacjami — sprawdź ścieżkę przed dodaniem do zależności.

---

# CZĘŚĆ I — FUNDAMENT

## 1. Szkielet backendu

**`fastapi/fastapi`**
Framework API oparty na typach Pythona. Generuje automatycznie specyfikację OpenAPI, z której wygenerujesz klienta frontendowego — to znaczy, że kontrakt między backendem a frontendem jest jeden i nie rozjeżdża się ręcznie. Rdzeń całego systemu.

**`fastapi/full-stack-fastapi-template`**
Oficjalny szablon: FastAPI, SQLModel, JWT, Docker Compose, migracje, testy. Zaczynasz od niego dzień pierwszy zamiast składać to samodzielnie przez tydzień.

**`fastapi/sqlmodel`**
Model bazy danych i schemat API zdefiniowane raz. Mniej duplikacji przy trzydziestu tabelach, ale przy skomplikowanych zapytaniach i tak zejdziesz do czystego SQLAlchemy.

**`sqlalchemy/sqlalchemy`**
ORM i warstwa zapytań. Potrzebny dla typu `numeric` (kwoty nigdy jako float), transakcji przy numeracji dokumentów i indeksów częściowych przy walidacji ważności stawek.

**`sqlalchemy/alembic`**
Migracje schematu. Przy trzydziestu tabelach i klientach na produkcji nie ma innej drogi — każda zmiana bazy przez migrację, wersjonowaną w gicie.

**`pydantic/pydantic`**
Walidacja danych oparta na typach. To jest twój kontrakt z modelem językowym: definiujesz schemat ekstrakcji cennika, model musi go spełnić albo dostajesz błąd zamiast cichej bzdury.

**`encode/starlette`** · **`encode/uvicorn`**
Warstwa ASGI pod FastAPI i serwer. Rzadko dotykasz bezpośrednio, ale przy konfiguracji timeoutów i workerów trzeba wiedzieć, że są.

**`encode/httpx`**
Klient HTTP z obsługą async. Wszystkie integracje zewnętrzne — KSeF, GUS, portale linii, API kursów — idą przez niego.

**`celery/celery`**
Kolejka zadań. Parsowanie cennika trwa minuty, nie może blokować żądania HTTP. Wymaga brokera (Redis albo RabbitMQ) jako dodatkowego komponentu.

**`rq/rq`**
Lżejsza kolejka na Redisie. Prostsza w utrzymaniu niż Celery, wystarczająca na twoją skalę.

**`procrastinate-org/procrastinate`**
Kolejka zadań działająca na samym Postgresie. Zero dodatkowych komponentów — przy jednoosobowym zespole to poważna zaleta, bo każdy komponent to coś, co może paść o trzeciej w nocy.

**`hynek/structlog`**
Logi strukturalne w JSON zamiast tekstu. Gdy będziesz szukał, czemu jeden cennik sparsował się źle, będziesz filtrował logi po `rate_sheet_id` — bez tego to grep po tysiącach linii.

**`pytest-dev/pytest`**
Testy. Reguły biznesowe z sekcji o walidacji piszesz tutaj, ręcznie, ze swojej wiedzy domenowej.

**`HypothesisWorks/hypothesis`**
Testy oparte na właściwościach — zamiast wymyślać przypadki, opisujesz regułę („suma pozycji zawsze równa się kwocie oferty") i biblioteka szuka kontrprzykładu. Idealne na przeliczenia walutowe i chargeable weight.

**`fastapi/typer`**
CLI z typów Pythona. Do zadań administracyjnych: seed słowników, reindeksacja, ręczne uruchomienie pipeline'u.

**`astral-sh/ruff`**
Linter i formatter napisany w Rust, kilkadziesiąt razy szybszy od poprzedników. Trzyma w ryzach kod generowany przez Cursora, który bywa niespójny stylistycznie.

**`astral-sh/uv`**
Menedżer pakietów i środowisk, zastępuje pip, venv i poetry. Instalacja zależności w sekundach zamiast minut.

**`python/mypy`**
Typowanie statyczne. Przy czterdziestu tabelach i setkach funkcji to jedyna rzecz, która wyłapie, że gdzieś przekazujesz kwotę tam, gdzie oczekiwana jest waluta.

## 2. Postgres i okolice

**`pgvector/pgvector`**
Wektory jako typ w Postgresie. Do mapowania nieznanych nazw opłat: „TERMINAL HANDLING CHG POL" nie pasuje tekstowo do żadnego aliasu, ale semantycznie jest blisko `OTHC`. Nie musisz stawiać osobnej bazy wektorowej.

**`supabase/supabase`**
Postgres z gotowym uwierzytelnianiem, storage i — kluczowe — dojrzałym Row Level Security. Rozważ jako skrót do multi-tenancy zamiast budowania izolacji tenantów samodzielnie.

**`kvesteri/sqlalchemy-continuum`**
Automatyczne wersjonowanie rekordów. Historia zmian stawek i ofert bez pisania własnego mechanizmu — a będziesz jej potrzebował przy pierwszej reklamacji klienta.

**`sqlfluff/sqlfluff`**
Linter SQL. Warto, bo kod generowany przez model bywa poprawny, ale nieczytelny za trzy miesiące.

**`djrobstep/migra`**
Porównuje dwa schematy Postgresa i generuje SQL wyrównujący różnicę. Ratunek, gdy migracje rozjadą się między środowiskami.

**`dimitri/pgloader`**
Migracja danych z MySQL, SQLite, CSV do Postgresa. Będzie potrzebna przy każdym wdrożeniu u klienta, który ma dane w czymkolwiek innym.

**`pgbouncer/pgbouncer`**
Pooling połączeń. Bez niego kilkudziesięciu workerów wyczerpie limit połączeń Postgresa.

**`wal-g/wal-g`** · **`pgbackrest/pgbackrest`**
Kopie zapasowe z odtwarzaniem do dowolnego punktu w czasie. Trzymasz cudze dane handlowe — utrata bazy kończy firmę, nie projekt. Wdrażasz przed pierwszym klientem, nie po.

**`prometheus-community/postgres_exporter`**
Metryki bazy do Prometheusa: wolne zapytania, blokady, rozmiar tabel.

**`ankane/pghero`**
Panel zdrowia Postgresa: brakujące indeksy, nieużywane indeksy, najwolniejsze zapytania. Jedno spojrzenie zamiast godziny w `pg_stat_statements`.

**`PostgREST/postgrest`**
Automatyczne REST API ze schematu bazy. Dobre na szybkie prototypy raportów, złe jako fundament produktu.

**`hasura/graphql-engine`**
GraphQL nad Postgresem z uprawnieniami na poziomie wiersza. Alternatywa, jeśli frontend miałby pytać elastycznie.

**`citusdata/citus`** · **`timescale/timescaledb`**
Skalowanie poziome i szeregi czasowe. Nie na teraz — ale timescale warto znać, jeśli będziesz analizował historię stawek w czasie.

**`electric-sql/pglite`**
Postgres skompilowany do przeglądarki. Do demonstracji offline i szybkich testów.

## 3. Dane referencyjne — porty, kraje, waluty

**`cristan/improved-un-locodes`** ← *najważniejsza pozycja w tej sekcji*
UN/LOCODE z poprawionymi współrzędnymi (98,7% pokrycia zamiast dziurawego oryginału) i **ponad 670 tysiącami aliasów nazw miast** — przy niecałych stu w zbiorze oficjalnym. To rozwiązuje twój realny problem: cennik mówi „Gdingen", drugi „GDN", trzeci „Gdynia Port", a wszystko to `PLGDY`. Bez tego pisałbyś normalizację portów tygodniami.

**`datasets/un-locode`**
Oficjalny zbiór UNECE w czystym CSV, z podziałem na osobne pliki tematyczne zamiast jednego worka. Podstawa tabeli `port`, aktualizowany przy każdym wydaniu.

**`geoapify/un-locode`**
Biblioteka Node do odpytywania zbioru, z uzupełnionymi współrzędnymi. Przydatna, jeśli część logiki trafi na frontend.

**`marek5050/UN-LOCODE`**
Prosty ekstrakt CSV. Najszybsza droga do zaseedowania bazy na etapie prototypu.

**`SeaconLogistics/un_locode`**
Gem w Ruby, ale ma dobrze przemyślany model funkcji lokalizacji: port, terminal kolejowy, terminal drogowy, lotnisko, ICD. Skopiuj sam model, nie kod.

**`tadziqusky/unlocode-ports`**
Notebook filtrujący sam podzbiór portów morskich z pełnego zbioru. Oszczędza pisanie filtra.

**`datasets/country-codes`**
ISO 3166 wraz z mapowaniami na waluty, strefy telefoniczne i kody ITU. Do formularzy kontrahenta i walidacji adresów.

**`datasets/currency-codes`**
ISO 4217 z liczbą miejsc po przecinku dla każdej waluty — istotne, bo nie wszystkie mają dwa (JPY ma zero).

**`datasets/harmonized-system`**
Kody HS do klasyfikacji towaru na ofercie i w dokumentach celnych.

**`mledoze/countries`**
Kraje z nazwami w wielu językach, granicami i przynależnością do organizacji.

**`dr5hn/countries-states-cities-database`**
Pełna hierarchia adresowa: kraj → region → miasto. Do formularzy adresowych kontrahentów.

**`hexorx/countries`**
Dane krajów z formatami adresów i informacjami o VAT.

**`datasets/language-codes`**
ISO 639. Potrzebne, gdy dokumenty będą wychodzić w kilku językach.

## 4. Referencje branżowe — co zbudowali inni

Żaden z tych projektów nie jest twoim rozwiązaniem. Wszystkie są kopalnią decyzji projektowych, których nie wymyślisz sam.

**`frappe/erpnext`**
Najbliższy pełnemu ERP w otwartym kodzie. Podpatrz model `Party` (jeden podmiot w wielu rolach) i `Landed Cost Voucher` (rozliczanie kosztów dodatkowych na przesyłce) — oba masz w swoim modelu.

**`frappe/frappe`** ← *warte przeczytania, nie użycia*
Framework, na którym stoi ERPNext. Kluczowa idea: typy dokumentów, pola i uprawnienia są **rekordami w bazie, nie kodem**. Dlatego jeden zespół obsługuje tysiące wdrożeń bez zmian w kodzie per klient. To jest dokładnie problem, który cię czeka przy piątym kliencie.

**`odoo/odoo`**
Moduły `account` i `stock`. Wzorce księgowe i magazynowe wypracowane przez lata — nie kopiuj kodu, ale zobacz, jakie przypadki brzegowe przewidzieli.

**`dolibarr/dolibarr`**
Prostszy i czytelniejszy niż Odoo. Dobry na model propozycji handlowej i konwersji oferta → zamówienie → faktura.

**`loadpartner/tms`**
Jedyny żywy open-source TMS dla brokerów frachtowych (Laravel). Zobacz model `load` i `carrier` oraz sposób obsługi statusów.

**`fleetbase/fleetbase`**
Modułowa platforma logistyczna. Wartość leży w architekturze rozszerzeń — jak dodać moduł bez ruszania rdzenia.

**`openwms/org.openwms`**
Poważny WMS z warstwą sterowania magazynem automatycznym. Sięgasz, jeśli dojdziesz do modułu magazynowego.

**`fjykTec/ModernWMS`**
WMS wyjęty z komercyjnych wdrożeń ERP i udostępniony. Kompletny i prosty.

**`myTinyWMS/myTinyWMS`** · **`openboxes/openboxes`** · **`infiniteoo/wms`** · **`hightower-systems/sentry-wms`**
Cztery lżejsze WMS-y. Ostatni w Pythonie i pomyślany jako warstwa wykonawcza obok ERP — najbliższy twojej filozofii.

**`bigcapitalhq/bigcapital`**
Open-source księgowość z podwójnym zapisem. Przeczytaj, zanim zdecydujesz, że piszesz własną.

**`invoiceninja/invoiceninja`**
Fakturowanie z obsługą wielu walut i szablonów. Kopalnia rozwiązań na ścieżkę oferta → faktura.

**`akaunting/akaunting`**
Multi-company. Wzorzec izolacji danych między firmami — bezpośrednio przydatny przy twoim multi-tenancy.

**`frappe/books`**
Lekka księgowość desktopowa. Czytelniejszy model niż pełny ERPNext.

**`medusajs/medusa`**
Architektura modułowa w TypeScript. Wzorzec, jeśli część backendu trafi do Node.

**`ever-co/ever-gauzy`**
ERP w NestJS. Zobacz model uprawnień i multi-tenancy — jeden z lepiej rozwiązanych w otwartym kodzie.

**`twentyhq/twenty`**
Nowoczesny CRM open source. Przeczytaj model danych, zanim zaprojektujesz swoją część CRM-ową — mają dobrze rozwiązane elastyczne pola i relacje.

**`openlmis/openlmis-ref-distro`**
Logistyka w architekturze mikroserwisowej. Ciekawe jako przestroga: pokazuje, ile złożoności kosztuje podział na serwisy. Nie rób tego na tym etapie.

## 5. Parsowanie dokumentów — serce modułu AI

**`docling-project/docling`** ← *pierwszy wybór*
Konwerter dokumentów od IBM. Czyta PDF, XLSX, DOCX i PPTX, zachowując strukturę tabel. Działa na modelu wizyjnym czytającym stronę jako obraz, więc radzi sobie z tabelami bez ramek i scalonymi komórkami — czyli z tym, co przysyłają agenci. Wolniejszy od alternatyw, bo generuje strukturę token po tokenie.

**`datalab-to/marker`**
Alternatywa: zamiast jednego dużego modelu wizyjnego używa pięciu mniejszych, wyspecjalizowanych, głównie klasyfikujących i wykrywających. Wyraźnie szybszy. **Odpal oba na pięciu swoich najbrzydszych cennikach i wybierz po wyniku, nie po opisie.**

**`Unstructured-IO/unstructured`**
Zwraca typowane elementy: nagłówek, tabela, akapit, lista. Przydatne, gdy cennik ma sekcje uwag pomiędzy tabelami i musisz wiedzieć, co jest czym.

**`microsoft/markitdown`**
Najlżejszy — wszystko na markdown. Szybka ścieżka dla plików prostych, zanim odpalisz cięższe narzędzia.

**`jsvine/pdfplumber`** ← *niezbędny*
Daje dostęp do współrzędnych każdego znaku i każdej komórki. **To jest podstawa `source_ref`** — bez współrzędnych nie zbudujesz provenance, a bez provenance nie odpowiesz klientowi, skąd wzięła się cena na jego fakturze.

**`pymupdf/PyMuPDF`**
Najszybsza ekstrakcja tekstu i renderowanie stron do obrazów pod ścieżkę wizyjną.

**`camelot-dev/camelot`**
Wyciąganie tabel z PDF-ów mających linie siatki. Cenniki linii żeglugowych często takie właśnie są.

**`opendataloader-project/opendataloader-pdf`** ← *rozwiązuje realne ryzyko*
Parser, który audytuje własny wynik i wykrywa strony po cichu pominięte przez inne narzędzia. To dokładnie zagrożenie `unparsed_regions` z twojej specyfikacji: najgorszy błąd to nie zła stawka, tylko cicho zignorowana tabela z dopłatami.

**`genieincodebottle/parsemypdf`**
Porównanie kilkunastu parserów na jednym zbiorze testowym. Zaoszczędzi ci tygodnia własnych testów.

**`datalab-to/surya`**
OCR z detekcją układu strony. Do skanów od mniejszych agentów.

**`tesseract-ocr/tesseract`**
Klasyczny OCR, offline, bez kosztu. Fallback, gdy nowsze narzędzia zawiodą.

**`JaidedAI/EasyOCR`**
OCR wielojęzyczny, bardzo prosty w użyciu.

**`PaddlePaddle/PaddleOCR`**
Najlepszy z tej grupy na tabele i języki azjatyckie. Cenniki od chińskich agentów to realny przypadek.

**`mindee/doctr`**
OCR pomyślany pod dokumenty biznesowe: faktury, formularze.

**`tafia/calamine`**
Najszybszy czytnik plików XLSX (Rust, z bindingiem `python-calamine`). Przy cennikach z dwudziestoma arkuszami różnica jest odczuwalna.

**`py-pdf/pypdf`**
Cięcie, łączenie, obracanie, metadane PDF. Podstawowa obróbka przed parsowaniem.

## 6. Document AI nowej generacji

**`opendatalab/MinerU`**
Bardzo dobry na PDF-y z gęstymi, zagnieżdżonymi tabelami.

**`allenai/olmocr`**
OCR na modelu wizyjnym z otwartymi wagami — możesz uruchomić lokalnie, bez wysyłania cudzych cenników na zewnątrz. Istotne przy klientach wrażliwych na dane.

**`getomni-ai/zerox`**
Prosta idea: strona → obraz → model wizyjny → markdown. Zaskakująco skuteczny na brzydkich skanach.

**`microsoft/table-transformer`**
Model wykrywający strukturę tabeli: gdzie są wiersze, kolumny, komórki scalone. Warstwa pomocnicza przed właściwą ekstrakcją.

**`huridocs/pdf-document-layout-analysis`**
Analiza układu strony przed ekstrakcją — co jest nagłówkiem, co tabelą, co stopką.

**`Filimoa/open-parse`**
Podział dokumentu na fragmenty z zachowaniem układu wizualnego, nie tylko kolejności tekstu.

**`docling-project/docling-serve`**
Docling jako usługa HTTP. Wpinasz w pipeline zamiast importować jako bibliotekę — łatwiej skalować i wersjonować.

## 7. Zbiór testowy i anotacja

Bez tej sekcji „95% skuteczności ekstrakcji" jest liczbą wymyśloną.

**`HumanSignal/label-studio`** ← *wdrożyć razem z pipeline'em*
Narzędzie do anotacji. Bierzesz trzydzieści swoich realnych cenników, ręcznie oznaczasz poprawne wyniki i masz zbiór referencyjny. Od tego momentu każda zmiana promptu albo modelu jest mierzalna, a nie odczuwalna.

**`doccano/doccano`**
Lżejsza alternatywa do etykietowania tekstu.

**`iterative/dvc`**
Wersjonowanie zbiorów danych razem z kodem. Zbiór testowy zmienia się w czasie — musisz wiedzieć, na której wersji mierzyłeś.

**`mlflow/mlflow`**
Śledzenie eksperymentów: który prompt, który model, jakie parametry, jaki wynik. Po trzech miesiącach iteracji nie będziesz tego pamiętał.
---

# CZĘŚĆ II — WARSTWA AI

## 8. Ekstrakcja strukturalna z modeli językowych

**`567-labs/instructor`** ← *twoja warstwa ekstrakcji*
Wymusza schemat Pydantic na odpowiedzi modelu i automatycznie ponawia, gdy walidacja nie przejdzie. To jest miejsce, w którym definiujesz, że stawka musi mieć kwotę, walutę i podstawę naliczenia — a model nie ma jak zwrócić czegoś innego.

**`dottxt-ai/outlines`**
Generowanie sterowane gramatyką: model fizycznie nie może wyprodukować niepoprawnego JSON-a, bo niedozwolone tokeny są odcinane na poziomie próbkowania. Mocniejsza gwarancja niż walidacja po fakcie.

**`BoundaryML/baml`**
Osobny język do definiowania promptów jako typowanych funkcji, z testami i wersjonowaniem. Warte rozważenia, gdy promptów zrobi się kilkanaście i zaczną się rozjeżdżać.

**`pydantic/pydantic-ai`**
Agenci z typowanym wyjściem, od twórców Pydantic. Spójny z resztą twojego stacku, bez narzutu dużych frameworków.

**`anthropics/anthropic-sdk-python`**
SDK. Istotne przy twoim zastosowaniu: buforowanie promptu (schemat i instrukcje nie zmieniają się między cennikami) i Batch API do masowego przetwarzania archiwum.

**`anthropics/claude-cookbooks`**
Gotowe wzorce pracy z dokumentami i ekstrakcji strukturalnej. Zacznij tutaj, zanim wymyślisz własne podejście.

**`anthropics/anthropic-quickstarts`**
Działające szkielety aplikacji — dobre jako punkt odniesienia dla architektury wywołań.

**`BerriAI/litellm`**
Jeden interfejs do wielu dostawców plus śledzenie kosztów per żądanie. Będziesz chciał wiedzieć, ile kosztuje sparsowanie konkretnego cennika, żeby wycenić usługę.

**`simonw/llm`**
CLI do szybkich eksperymentów z promptem, bez pisania kodu.

**`guardrails-ai/guardrails`**
Walidatory na wyjściu: zakresy kwot, formaty dat, wymagane pola. Warstwa poza schematem — schemat mówi, że kwota jest liczbą, guardrails mówi, że fracht za 40HC nie może wynosić 3 dolarów.

**`langchain-ai/langchain`**
Znany z tutoriali. Używaj wybiórczo do pojedynczych elementów, nie jako fundamentu — abstrakcje zmieniają się szybciej, niż zdążysz je opanować.

**`langchain-ai/langgraph`**
Grafy stanów dla wieloetapowych procesów. Sensowne, jeśli pipeline ekstrakcji rozrośnie się w rozgałęzioną maszynę stanów.

**`run-llama/llama_index`**
Indeksowanie archiwum cenników pod wyszukiwanie semantyczne: „pokaż wszystkie stawki na Szanghaj z zeszłego kwartału".

## 9. MCP — twój system jako narzędzie agenta

Najważniejsza sekcja tego katalogu z punktu widzenia różnicowania produktu. Nikt na polskim rynku spedycyjnym tego nie ma.

**`modelcontextprotocol/python-sdk`** ← *wdrożyć po fazie 1*
Opakowuje twoje API w serwer MCP. Kilkadziesiąt linii kodu, a Claude potrafi wystawić ofertę, sprawdzić stawkę i zamknąć zlecenie. To nie jest chatbot doklejony obok aplikacji — to aplikacja jako narzędzie agenta.

**`modelcontextprotocol/typescript-sdk`**
To samo po stronie Node.

**`modelcontextprotocol/servers`**
Oficjalne implementacje referencyjne. Zanim zaprojektujesz własne narzędzia, zobacz, jak wyglądają dobrze zaprojektowane — granulacja i opisy narzędzi decydują o tym, czy agent ich użyje poprawnie.

**`modelcontextprotocol/inspector`**
Debugger narzędzi MCP. Bez niego pisanie serwera to zgadywanie, dlaczego agent wywołał złą funkcję.

**`modelcontextprotocol/registry`**
Rejestr serwerów, coś w rodzaju katalogu aplikacji dla MCP. Miejsce, gdzie kiedyś opublikujesz swój.

**`wong2/awesome-mcp-servers`**
Katalog społecznościowy. Zawiera m.in. serwer do polskiego KRS — gotowa weryfikacja kontrahenta bez pisania integracji.

**`appcypher/awesome-mcp-servers`** · **`korchasa/awesome-mcp`** · **`TensorBlock/awesome-mcp-servers`**
Trzy kolejne katalogi, częściowo rozłączne. Ostatni generuje gotowe wpisy konfiguracyjne dla Cursora i Claude Desktop.

**`mcp-finder/best-mcp-servers-2026`**
Ranking według niezawodności i aktywności utrzymania zamiast liczby gwiazdek. Wiele serwerów zdobyło gwiazdki przy premierze protokołu i od tego czasu nie było aktualizowanych — ten ranking to pokazuje.

**`metorial/mcp-containers`**
Setki serwerów MCP w kontenerach. Bezpieczne uruchamianie cudzego kodu, który ma dostęp do twoich danych.

**`microsoft/playwright-mcp`**
Sterowanie przeglądarką przez MCP.

**`QuantGeekDev/docker-mcp`**
Zarządzanie kontenerami przez agenta — do zadań operacyjnych.

## 10. Text-to-SQL i warstwa semantyczna

Problem: użytkownik chce raportu, którego nie przewidziałeś. Rozwiązanie: przestań przewidywać raporty.

**`Canner/WrenAI`** ← *po fazie 3*
Text-to-SQL planowany przeciwko warstwie semantycznej i sprawdzany dry-planem przed wykonaniem. Kluczowa różnica wobec naiwnego podejścia: agent nie zgaduje schematu, tylko korzysta z modeli i metryk, które sam zdefiniowałeś. Wynik jest sprawdzalny, nie prawdopodobny.

**`cube-js/cube`**
Warstwa semantyczna. Definiujesz raz, czym jest „marża" i „rentowność relacji" — wszystkie narzędzia i wszyscy klienci liczą to tak samo. Bez tego dwa raporty pokażą dwie różne liczby i stracisz zaufanie.

**`tobymao/sqlglot`** ← *obowiązkowo razem z powyższym*
Parser i transpiler SQL. Waliduje zapytanie wygenerowane przez model, zanim dotknie bazy. Bez tego wpuszczasz do produkcyjnej bazy zapytanie, którego nikt nie sprawdził — a użytkownik pyta o dane kilku firm naraz.

**`vanna-ai/vanna`**
RAG nad schematem bazy, uczy się na zapytaniach, które zaakceptowałeś.

**`eosphoros-ai/DB-GPT`**
Pełna platforma agentów nad bazą danych, z interfejsem.

**`FalkorDB/QueryWeaver`**
Text2SQL rozumiejący schemat jako graf. Lepszy przy zapytaniach wymagających wielu złączeń — a twój model danych ich wymaga.

**`defog-ai/sqlcoder`**
Model wyspecjalizowany w generowaniu SQL, uruchamialny lokalnie.

**`duckdb/duckdb`**
Silnik analityczny działający w procesie. Raporty nad milionami wierszy bez stawiania hurtowni. Świetnie współpracuje z Parquet i pandas.

**`dbt-labs/dbt-core`**
Transformacje danych jako kod. Oddziela warstwę raportową od operacyjnej — ważne, gdy raporty zaczną obciążać bazę produkcyjną.

**`apache/superset`** · **`metabase/metabase`**
Dashboardy dla użytkowników, którzy wolą klikać niż pytać. Metabase jest szybszy we wdrożeniu, Superset bogatszy.

## 11. Agenci i automatyzacja procesów

**`browser-use/browser-use`** ← *rozwiązuje realną barierę biznesową*
Agent sterujący przeglądarką na podstawie opisu celu. Linie żeglugowe nie dają API małym spedytorom — ale mają portale. To jest droga do stawek spot bez czekania na integrację, której nikt ci nie da.

**`Skyvern-AI/skyvern`**
To samo, z naciskiem na powtarzalne wypełnianie formularzy.

**`steel-dev/steel-browser`**
Przeglądarka jako usługa dla agentów: sesje, proxy, zarządzanie stanem logowania.

**`openai/openai-agents-python`**
Lekki framework agentowy, minimum abstrakcji.

**`microsoft/autogen`**
Wieloagentowe konwersacje. Wzorzec przydatny w pipeline: agent ekstrahujący, agent weryfikujący, agent normalizujący.

**`crewAIInc/crewAI`**
Agenci z przypisanymi rolami. Prostszy model mentalny niż AutoGen.

**`All-Hands-AI/OpenHands`** · **`SWE-agent/SWE-agent`**
Agenci piszący i naprawiający kod w repozytorium. Uzupełnienie Cursora przy zadaniach obejmujących wiele plików.

**`geekan/MetaGPT`**
Symulacja zespołu programistów. Ciekawe koncepcyjnie, mało praktyczne w produkcji.

**`e2b-dev/E2B`**
Sandbox do bezpiecznego wykonywania kodu generowanego przez agenta. Potrzebny, jeśli pozwolisz użytkownikowi na analizy ad hoc.

## 12. Głos i telefonia

Spedycja to branża telefoniczna. Kierowca nie wypełni formularza, ale zadzwoni.

**`livekit/agents`**
Agent głosowy działający w czasie rzeczywistym. Kierowca dzwoni, podaje numer kontenera i status, system aktualizuje zlecenie. Funkcja, która na demonstracji robi większe wrażenie niż cała reszta.

**`pipecat-ai/pipecat`**
Framework pipeline'ów głosowych, prostszy próg wejścia.

**`openai/whisper`**
Transkrypcja mowy. Nagrania rozmów z klientami i agentami jako źródło danych o ustaleniach.

**`SYSTRAN/faster-whisper`**
Czterokrotnie szybszy przy tej samej jakości, dobra polszczyzna.

**`ggml-org/whisper.cpp`**
Transkrypcja lokalnie, na CPU, bez wysyłania nagrań na zewnątrz.

**`rhasspy/piper`**
Synteza mowy offline z obsługą polskiego.

## 13. Modele lokalne i kontrola kosztu

**`ollama/ollama`**
Uruchomienie modelu lokalnie jednym poleceniem. Do zadań, których nie chcesz wysyłać na zewnątrz — i jako odpowiedź dla klientów żądających przetwarzania wyłącznie lokalnego.

**`ggml-org/llama.cpp`**
Inferencja na CPU. Klasyfikacja maili („czy to cennik?") nie potrzebuje GPU ani zewnętrznego API.

**`vllm-project/vllm`**
Serwowanie z wysoką przepustowością. Sensowne przy jednorazowym przetwarzaniu archiwum tysięcy cenników.

**`huggingface/text-generation-inference`**
Alternatywa produkcyjna, dojrzała.

**`huggingface/transformers`**
Podstawa całego ekosystemu.

**`unslothai/unsloth`** ← *po roku zbierania danych*
Efektywny fine-tuning. Po roku masz zbiór cenników, którego nie ma nikt inny. Mały model dotrenowany na nim będzie tańszy i celniejszy od ogólnego — i jest to przewaga, której konkurencja nie skopiuje.

**`axolotl-ai-cloud/axolotl`**
Fine-tuning konfigurowany w YAML, bez pisania kodu treningowego.

## 14. RAG, pamięć i wiedza firmowa

**`FlagOpen/FlagEmbedding`**
Embeddingi wielojęzyczne z dobrą obsługą polskiego. Kluczowe przy mapowaniu nazw opłat, które przychodzą po polsku, angielsku i w mieszance obu.

**`qdrant/qdrant`**
Baza wektorowa. Sięgasz, gdy wyrośniesz z pgvectora — czyli prawdopodobnie nigdy na twojej skali.

**`chroma-core/chroma`**
Najprostsza do prototypu, działa lokalnie.

**`weaviate/weaviate`**
Wyszukiwanie hybrydowe: wektory plus filtry strukturalne. Przydatne, gdy szukasz semantycznie, ale w obrębie jednego tenanta i zakresu dat.

**`infiniflow/ragflow`**
RAG z naciskiem na dokumenty o złożonym układzie — bliski twojemu przypadkowi.

**`deepset-ai/haystack`**
Dojrzały framework RAG, dobrze udokumentowany.

**`microsoft/graphrag`**
RAG po grafie powiązań. Odpowiada na pytania typu „którzy agenci obsługują tę relację i po jakich stawkach" lepiej niż wyszukiwanie wektorowe.

**`mem0ai/mem0`**
Pamięć długoterminowa agenta: preferencje klientów, historia negocjacji, ustalenia z rozmów.

**`getzep/zep`**
Alternatywa z modelem pamięci czasowej.

**`Mintplex-Labs/anything-llm`**
Gotowy interfejs do firmowej bazy wiedzy. Do wewnętrznego użytku, nie jako część produktu.

## 15. Ewaluacja i niezawodność

**`promptfoo/promptfoo`** ← *wdrożyć z pierwszym promptem*
Testy regresyjne promptów. Trzydzieści realnych cenników jako zestaw testowy, mierzysz skuteczność przy każdej zmianie. Bez tego „poprawiłem prompt" znaczy tyle co nic.

**`langfuse/langfuse`** ← *wdrożyć od pierwszego dnia*
Obserwowalność: każdy prompt, odpowiedź, koszt i opóźnienie. Gdy za trzy miesiące cenniki jednego agenta zaczną się psuć, bez historii nie ustalisz dlaczego. Godzina wdrożenia teraz, tydzień śledztwa później.

**`confident-ai/deepeval`**
Testy jednostkowe dla modeli, wpinane w CI. Regresja skuteczności nie przechodzi do produkcji.

**`Arize-ai/phoenix`**
Ewaluacja i śledzenie jakości w czasie, z wizualizacją.

**`comet-ml/opik`**
Śledzenie i ocena wywołań, open source, prosty w uruchomieniu.

**`traceloop/openllmetry`**
OpenTelemetry dla LLM. Spójny z resztą twojej obserwowalności — jeden system śladów zamiast dwóch.

**`helicone/helicone`**
Proxy z logowaniem, cache i limitami kosztów. Zabezpieczenie przed rachunkiem, którego się nie spodziewasz.

**`truera/trulens`** · **`openai/evals`** · **`explodinggradients/ragas`**
Trzy kolejne frameworki ewaluacji. Ragas ma metryki adaptowalne do oceny ekstrakcji.

**`Giskard-AI/giskard`**
Automatyczne wyszukiwanie słabych punktów modelu — testuje przypadki, których nie wymyśliłeś.

## 16. Bezpieczeństwo warstwy AI

**`protectai/llm-guard`** ← *od pierwszego dnia pipeline'u*
Filtrowanie wejścia i wyjścia modelu. Cennik od nieznanego agenta to **niezaufane wejście**: wystarczy, że ktoś wpisze w kolumnie „uwagi" instrukcję dla modelu, a twój ekstraktor zacznie zwracać stawki, których w cenniku nie ma. Najtańszy sposób oszukania systemu takiego jak twój.

**`protectai/rebuff`**
Wykrywanie prób wstrzyknięcia promptu, wielowarstwowe.

**`NVIDIA/NeMo-Guardrails`**
Reguły określające, czego agent nie może zrobić — na przykład zatwierdzić stawki bez akceptacji człowieka.

**`leondz/garak`**
Skaner podatności modelu. Testuje twój system tak, jak zrobiłby to atakujący.

**`microsoft/presidio`**
Wykrywanie i anonimizacja danych osobowych. Wysyłasz cudze cenniki i maile do zewnętrznego API — warto wiedzieć, co w nich jedzie, i móc to udokumentować w umowie powierzenia.

## 17. Interfejs z AI w środku

**`CopilotKit/CopilotKit`** ← *funkcja demonstracyjna*
Copilot wbudowany w aplikację React. Użytkownik pisze „oferta dla Jurgi, Gdynia–Szanghaj, dwa czterdziestki wysokie", formularz się wypełnia. To jest różnica, którą klient zobaczy w pierwszej minucie pokazu i o której opowie kolegom z branży.

**`vercel/ai`**
Streaming odpowiedzi i generatywne UI — komponenty budowane przez model w locie.

**`assistant-ui/assistant-ui`**
Gotowe komponenty czatu z obsługą narzędzi i strumieniowania.

**`vercel/next.js`**
Framework frontendowy, jeśli oddzielisz warstwę prezentacji.
---

# CZĘŚĆ III — INTEGRACJE I INTERFEJS

## 18. Poczta jako wejście do systemu

**`postalsys/emailengine`** ← *największa oszczędność czasu w tej sekcji*
Zamienia skrzynkę IMAP w REST API z webhookami. Stawiasz raz, dostajesz żądanie HTTP przy każdym mailu na `rates@`. Oszczędza tygodnia walki z IMAP-em, kodowaniami i wykrywaniem duplikatów.

**`ikvk/imap_tools`**
Najprzyjemniejszy klient IMAP w Pythonie, jeśli wolisz zrobić to sam. Sensowna obsługa załączników i flag.

**`SpamScope/mail-parser`**
Parsowanie plików `.eml` i `.msg`: nagłówki, treść, załączniki, kodowania. Potrzebne przy przetwarzaniu archiwum starych maili.

**`microsoftgraph/msgraph-sdk-python`**
Dostęp do skrzynki na Microsoft 365 przez Graph API. Prawdopodobnie twój przypadek i przypadek większości klientów.

**`docker-mailserver/docker-mailserver`**
Własna skrzynka `rates@` w kontenerze, oddzielona od firmowej poczty.

**`axllent/mailpit`**
Przechwytuje maile w środowisku deweloperskim. Zabezpieczenie przed wysłaniem oferty testowej prawdziwemu klientowi — a to się zdarza każdemu.

**`foxcpp/maddy`**
Lekki serwer pocztowy w Go, prosty w konfiguracji.

**`postalserver/postal`**
Własny serwer wysyłkowy, gdy wolumen powiadomień przekroczy limity zewnętrznych dostawców.

**`nodemailer/nodemailer`**
Podstawa wysyłki po stronie Node.

## 19. EDI i komunikaty branżowe

**`parcelLab/edi-iftmin`** ← *twoje komunikaty*
Parser **IFTMIN** (zlecenie transportowe) i **IFTSTA** (status przesyłki) — dokładnie tych, którymi wymieniasz dane z liniami i większymi klientami. Zwraca czytelny JSON zamiast surowego EDIFACT-u.

**`xoscar/EDI-IFTMIN`**
Druga implementacja tych samych komunikatów. Warto mieć obie do porównania przy trudnych plikach.

**`nerdocs/pydifact`**
Parser i serializer UN/EDIFACT w Pythonie — port dobrej biblioteki PHP. Jedyna sensowna opcja w tym języku.

**`xlate/staedi`**
Strumieniowy reader i writer z walidacją względem schematów (Java). Najbardziej dojrzały w tym zestawieniu.

**`indice-co/EDI.Net`**
Serializer EDIFACT, X12 i TRADACOMS w .NET.

**`smooks/smooks`**
Framework transformacji między EDI, XML, CSV i obiektami. Przydatny, gdy każdy partner chce innego formatu.

**`walmartlabs/gozer`**
Parser X12, gdyby doszły relacje amerykańskie.

**`michaelachrisco/Electronic-Interchange-Github-Resources`**
Katalog wszystkiego, co w temacie EDI istnieje na GitHubie. Zacznij tutaj, zanim zaczniesz szukać.

**`OpenAS2/OpenAs2App`** · **`phax/as2-lib`**
Protokół AS2 — standard wymiany plików z liniami i dużymi klientami korporacyjnymi. Wcześniej czy później ktoś tego zażąda.

## 20. E-faktura: KSeF i standardy europejskie

**`CIRFMF/ksef-api`** ← *zacznij tutaj*
Oficjalny przewodnik integracyjny Ministerstwa Finansów po API KSeF 2.0, podzielony na sekcje odpowiadające funkcjom systemu. Przykłady kodu oparte o biblioteki utrzymywane przez zespoły MF.

**`smekcio/ksef-client-python`** ← *najbliżej gotowca dla twojego stacku*
SDK Python zgodne z aktualnym kontraktem API: klienci synchroniczni i asynchroniczni, sesje online i wsadowe, kryptografia RSA/ECDH/AES, opcjonalny podpis XAdES, generowanie kodów QR i linków weryfikacyjnych. Dostępne na PyPI jako `ksef-client`.

**`ArturSkowronski/ksef-cli`**
Narzędzie wiersza poleceń: podajesz XML albo nawet skan PDF, ono obsługuje uwierzytelnianie, szyfrowanie sesji, budowę XML w schemie FA(3), wysyłkę i odpytywanie o status. Ma tryb `--json` i dołączony skill dla Claude Code — nadaje się do wpięcia w pipeline agentowy.

**`m32/ksef`**
Zestaw skryptów Python do konfiguracji, autoryzacji i komunikacji z KSeF 2.0. Czytelne — dobre do zrozumienia przepływu, zanim sięgniesz po gotowe SDK.

**`m32/ksef-pdf`**
Wizualizacja faktury ustrukturyzowanej: XML na PDF z numerem KSeF i kodem QR. Użytkownicy oczekują PDF-u, nie XML-a — bez tego integracja jest niepełna.

**`Pafkaja/ksef_faktury_list`**
Pobieranie faktur zakupowych z KSeF, z opcją zapisu XML i PDF oraz wysyłką mailem.

**`fakturownia/API`**
API systemu księgowego z obsługą KSeF i schemy FA(3). Ścieżka „integruj, zamiast pisać własną księgowość" — najrozsądniejsza decyzja na twoim etapie.

**`akretion/factur-x`**
Factur-X i ZUGFeRD: faktura hybrydowa, PDF z osadzonym XML-em. Standard oczekiwany przez klientów niemieckich i francuskich.

**`phax/ph-ubl`**
UBL i Peppol — europejski standard e-faktury. Potrzebny przy ekspansji poza Polskę.

## 21. Polskie rejestry i weryfikacja kontrahenta

**`bigzbig/regonapi`**
Klient REGON BIR 1.1 w Pythonie. Wyszukiwanie po NIP, REGON albo KRS, zwraca pełne dane adresowe i kody PKD. **Ma tryb sandbox działający bez klucza API** — możesz zacząć od razu, wniosek o klucz złożyć równolegle.

**`grzesieksw/GusApi`**
Ten sam rejestr w wersji .NET.

**`infirsoft/vat-whitelist-api`**
Wrapper API białej listy podatników VAT: sprawdzenie po NIP, po REGON, po numerze rachunku i weryfikacja pary NIP–rachunek na wskazany dzień. Napisany w PHP, ale kontrakt API czytelny i łatwy do odtworzenia.

**`m4rcelpl/WykazPodatnikow`**
Biblioteka .NET do białej listy, z obsługą pliku płaskiego — ważne, bo API ministerstwa bywa niedostępne, a plik płaski działa offline.

## 22. Księgowość i księga główna

Przeczytaj tę sekcję, zanim zdecydujesz, że piszesz własną księgowość. Rekomendacja pozostaje: integruj, nie pisz.

**`beancount/beancount`** ← *do przeczytania, nie wdrożenia*
Podwójny zapis w plikach tekstowych. Najczystszy model księgi, jaki znajdziesz — godzina lektury dokumentacji da ci więcej niż tydzień czytania kodu ERP-ów.

**`beancount/fava`**
Interfejs webowy nad Beancount. Pokazuje, jak zaprezentować bilans i rachunek wyników.

**`beancount/beanquery`**
Język zapytań nad księgą — wzorzec dla twoich raportów finansowych.

**`beancount/smart_importer`**
Import wyciągów z uczeniem kategoryzacji. Wzorzec dopasowywania płatności do faktur.

**`ledger/ledger`** · **`simonmichael/hledger`**
Klasyki plain-text accounting. hledger ma najlepszą dokumentację modelu pojęciowego.

**`tigerbeetle/tigerbeetle`** ← *zmieni ci projekt tabeli `charge`*
Baza danych zaprojektowana wyłącznie pod transakcje finansowe. Kluczowa idea: reguły księgowe są wymuszane **przez bazę, nie przez kod aplikacji**. Flaga typu „obciążenia nie mogą przekroczyć uznań" eliminuje całą klasę błędów — konto nie zejdzie poniżej zera niezależnie od tego, co zrobi aplikacja, bez wyścigów i podwójnych zapisów.

**`formancehq/ledger`**
Księga jako usługa: wiele walut, wiele aktywów, transakcje wiele-do-wielu.

**`hamsterbase/ledger-ts`**
Księga zapisywana jako kod TypeScript, kompilowany do formatu Beancount.

**`LedgerSMB/LedgerSMB`**
Pełna księgowość ERP. Dojrzały model planu kont i zamknięć okresów.

## 23. Bank i płatności

**`WoLpH/mt940`** ← *tania funkcja o dużej widoczności*
Parser wyciągów bankowych w formacie MT940 — tym, w którym polskie banki oddają historię rachunku. Fundament automatycznego dopasowywania wpłat do faktur. Kilka dni pracy, a użytkownik widzi różnicę codziennie.

**`nordigen/nordigen-python`**
Dostęp do rachunków przez PSD2. Alternatywa dla ręcznego wgrywania wyciągów.

**`csingley/ofxtools`**
Format OFX, gdy bank eksportuje w nim zamiast MT940.

**`plaid/plaid-python`**
Agregacja bankowa, głównie rynek amerykański. Na później.

**`getlago/lago`**
Rozliczanie subskrypcji według zużycia. Gdy zaczniesz sprzedawać: opłata per użytkownik plus limit sparsowanych cenników, nadwyżka osobno.

**`killbill/killbill`**
Dojrzały silnik subskrypcji i fakturowania cyklicznego.

**`stripe/stripe-python`**
Płatności kartą. Pamiętaj, że przy sprzedaży do UE VAT rozliczasz sam — inaczej niż u pośredników typu Merchant of Record.

## 24. Pieniądze, waluty, daty

**`limist/py-moneyed`** ← *wdrożyć od pierwszej tabeli*
Typ `Money` łączący kwotę z walutą nierozerwalnie. Uniemożliwia dodanie euro do dolarów — błąd, który w systemie z siedmioma walutami na jednej ofercie zdarzy się na pewno, jeśli używasz gołych liczb.

**`python-babel/babel`**
Formatowanie kwot, dat i liczby mnogiej zależnie od języka. Oferta dla klienta z Chin wygląda inaczej niż dla polskiego.

**`dinerojs/dinero.js`**
To samo po stronie frontendu, z bezpieczną arytmetyką na liczbach całkowitych.

**`sdispater/pendulum`**
Daty i strefy czasowe bez bólu. ETD w Gdyni i ETA w Szanghaju to dwie różne strefy, a cut-off dokumentacyjny to trzecia.

**`fawazahmed0/exchange-api`**
Darmowe kursy walut jako zapasowe źródło, gdy API NBP nie odpowiada.

## 25. Frontend

**`refinedev/refine`** ← *miesiące oszczędności*
Framework do paneli administracyjnych. Generuje listy, formularze, filtry i uprawnienia z definicji zasobu. Przy ERP z czterdziestoma ekranami CRUD to różnica między pół rokiem a dwoma miesiącami.

**`TanStack/table`**
Tabela bez własnego renderowania: sortowanie, filtrowanie, grupowanie, wirtualizacja. Baza stawek to dziesiątki tysięcy wierszy.

**`TanStack/query`**
Cache i synchronizacja stanu serwera. Nie pisz tego ręcznie — to jedno z tych miejsc, gdzie własna implementacja zawsze wychodzi gorzej.

**`TanStack/virtual`**
Wirtualizacja list. Bez niej przeglądarka umiera przy pięciu tysiącach pozycji cennika.

**`TanStack/router`** · **`TanStack/form`**
Routing i formularze z pełnym typowaniem, spójne z resztą rodziny.

**`glideapps/glide-data-grid`** ← *ekran kolejki review*
Siatka w stylu Excela, płynna przy stu tysiącach wierszy. To jest komponent, na którym spędzisz najwięcej czasu jako użytkownik własnego systemu — przeglądając i poprawiając wyniki ekstrakcji.

**`ag-grid/ag-grid`**
Najbogatsza funkcjonalnie siatka danych, wersja community na licencji MIT. Alternatywa, gdy potrzebujesz grupowania i osi przestawnych.

**`shadcn-ui/ui`**
Komponenty kopiowane do projektu, nie instalowane jako zależność. Cursor generuje pod nie bardzo dobrze — to realna zaleta przy twoim trybie pracy.

**`ant-design/ant-design`**
Gęste komponenty pomyślane pod systemy biznesowe. Estetyka bliższa ERP niż shadcn.

**`mui/material-ui`**
Alternatywa z dojrzałym komponentem DataGrid.

**`tailwindlabs/tailwindcss`**
Style.

**`react-hook-form/react-hook-form`**
Formularze bez przemontowywania przy każdym znaku. Formularz oferty ma czterdzieści pól — bez tego jest nieużywalny.

**`colinhacks/zod`**
Walidacja po stronie klienta. Ten sam schemat co w Pydantic, jedno źródło prawdy.

**`clauderic/dnd-kit`**
Przeciąganie i upuszczanie: kolejność pozycji na ofercie, przenoszenie opłat między sekcjami.

**`recharts/recharts`**
Wykresy: marża w czasie, trend frachtu, udział relacji w przychodzie.

**`date-fns/date-fns`**
Operacje na datach, modułowe, bez ciągnięcia całej biblioteki.

**`vitejs/vite`**
Build i serwer deweloperski.

## 26. Mapy i trasowanie

**`maplibre/maplibre-gl-js`**
Mapa wektorowa bez licencji komercyjnej. Pozycje kontenerów, trasy, mapa relacji.

**`Leaflet/Leaflet`**
Prostsza, gdy nie potrzebujesz WebGL.

**`openlayers/openlayers`**
Zaawansowane warstwy geograficzne i projekcje.

**`visgl/deck.gl`**
Wizualizacja dużych zbiorów: wolumeny na relacjach, gęstość ruchu.

**`Project-OSRM/osrm-backend`**
Trasowanie drogowe — dowozy i odwozy, szacowanie czasu.

**`valhalla/valhalla`**
Trasowanie z profilami pojazdów ciężarowych: ograniczenia wysokości, masy, ADR.

**`graphhopper/graphhopper`**
Trasowanie z optymalizacją tras wielopunktowych.

## 27. Generowanie dokumentów

**`typst/typst`** ← *rekomendowany*
Nowoczesny system składu. Szablony oferty, B/L i CMR — czytelna składnia, kompilacja w milisekundach, output jakości drukarskiej. Lepszy wybór niż LaTeX (mniej bólu) i niż HTML na PDF (precyzja).

**`Kozea/WeasyPrint`**
HTML i CSS na PDF. Wybierz, jeśli wolisz projektować szablony w technologiach webowych.

**`foliojs/pdfkit`**
Generowanie programistyczne, gdy układ zależy od danych.

**`open-xml-templating/docxtemplater`**
Szablony Word z podstawianiem danych. Część dokumentów spedycyjnych klienci chcą w formacie edytowalnym.

**`python-openxml/python-docx`**
Tworzenie dokumentów Word z Pythona.

**`scanny/python-pptx`**
Prezentacje: oferty handlowe, raporty kwartalne dla klienta.

**`jgm/pandoc`**
Konwersja między wszystkimi formatami tekstowymi.

**`carbone-io/carbone`**
Szablony projektowane w LibreOffice, generowanie do PDF, DOCX i XLSX.

**`MatthiasValvekens/pyHanko`**
Podpis PDF w standardzie PAdES. Dokumenty spedycyjne z podpisem elektronicznym — funkcja, o którą klienci pytają, a mało kto ma.

**`documenso/documenso`** · **`docuseal/docuseal`**
Obieg podpisów: umowy z agentami, zlecenia stałe, potwierdzenia.

**`Stirling-Tools/Stirling-PDF`**
Operacje na PDF: łączenie, dzielenie, stemplowanie, znak wodny, kompresja.
---

# CZĘŚĆ IV — PROCESY, INFRASTRUKTURA, NARZĘDZIA

## 28. Workflow i orkiestracja

**`pytransitions/transitions`**
Maszyna stanów dla statusu zlecenia. Wymusza legalne przejścia zamiast rozsypanych po kodzie instrukcji warunkowych — zlecenie nie przeskoczy z „zabookowane" na „dostarczone" z pominięciem wypłynięcia.

**`temporalio/temporal`** · **`temporalio/sdk-python`**
Trwałe workflow z automatycznym ponawianiem i pełną historią wykonania. Rozważ, gdy pipeline ekstrakcji rozrośnie się i zaczniesz tracić zadania przy restartach.

**`PrefectHQ/prefect`**
Orkiestracja pipeline'ów danych, lżejsza niż Airflow, przyjazna w Pythonie.

**`dagster-io/dagster`**
Pipeline'y z katalogiem zasobów danych — wiesz, który cennik zasilił którą stawkę i którą ofertę.

**`apache/airflow`**
Klasyk. Cięższy, ale ma wszystko i każdy go zna.

**`windmill-labs/windmill`**
Skrypty, interfejs i harmonogram w jednym. Dobre na zadania operacyjne wokół systemu, bez budowania osobnych ekranów.

**`n8n-io/n8n`**
Integracje low-code. Szybkie prototypy połączeń, zanim napiszesz je porządnie.

**`camunda/camunda-bpm-platform`**
BPMN. Sensowne tylko wtedy, gdy obieg zlecenia ma być konfigurowany przez klienta bez twojego udziału — a przy sprzedaży produktu to realna potrzeba.

**`hatchet-dev/hatchet`** · **`riverqueue/river`**
Kolejki z ponawianiem, priorytetami i panelem. River działa na Postgresie, bez dodatkowego brokera.

**`agronholm/apscheduler`**
Zadania cykliczne: pobranie kursów NBP o 12:15, poranne sprawdzenie wygasających stawek, nocna synchronizacja.

**`mcuadros/ofelia`**
Cron dla kontenerów, bez wchodzenia do środka.

## 29. Wyszukiwanie i dopasowywanie

**`rapidfuzz/RapidFuzz`** ← *pierwsza warstwa normalizacji*
Dopasowanie rozmyte napisane w C++. Pierwszy krok mapowania „TERMINAL HANDLING POL" na kod `OTHC`, zanim sięgniesz po embeddingi.

**`seatgeek/thefuzz`**
Prostsze API, wolniejsze. Wystarczy przy małych słownikach.

**`dedupeio/dedupe`**
Deduplikacja rekordów z uczeniem. Ten sam agent występuje w bazie pod trzema nazwami — to jest narzędzie, które to znajdzie.

**`meilisearch/meilisearch`**
Wyszukiwarka odporna na literówki, błyskawiczna, prosta w utrzymaniu. Po bazie stawek, kontrahentów i ofert.

**`typesense/typesense`**
Alternatywa, jeszcze lżejsza we wdrożeniu.

**`opensearch-project/OpenSearch`**
Cięższe działo. Sięgasz, gdy dojdą logi i analityka na dużą skalę.

## 30. Uwierzytelnianie i uprawnienia

**`openfga/openfga`** ← *pasuje do twojego przypadku*
Uprawnienia w modelu Zanzibar. Odpowiada na pytania typu „handlowiec widzi tylko swoich klientów, kierownik cały oddział, a klient tylko swoje zlecenia" bez zaszywania tego w kodzie każdego zapytania.

**`ory/keto`**
Ten sam model, inna implementacja.

**`casbin/casbin`**
RBAC i ABAC jako biblioteka wbudowana w aplikację. Prostsze wdrożenie, mniej możliwości.

**`keycloak/keycloak`**
Pełny dostawca tożsamości: SSO, federacja, role. Klienci korporacyjni będą pytać o logowanie przez ich Active Directory — tu jest odpowiedź.

**`ory/kratos`**
Zarządzanie tożsamością, lżejsze niż Keycloak.

**`logto-io/logto`**
Nowocześniejsza alternatywa, przyjemniejsza w konfiguracji.

**`authelia/authelia`**
Brama uwierzytelniająca przed aplikacją, dobra na panele wewnętrzne.

## 31. Infrastruktura i wdrożenie

**`docker/compose`**
Środowisko lokalne i proste wdrożenia produkcyjne.

**`coollabsio/coolify`**
Własne PaaS na twoim serwerze. Deploy przez `git push`, bez płacenia za zewnętrzne platformy.

**`dokku/dokku`** · **`caprover/caprover`**
Lżejsze alternatywy tego samego pomysłu.

**`portainer/portainer`**
Zarządzanie kontenerami przez przeglądarkę. Przydatne, gdy trzeba coś zrestartować z telefonu.

**`k3s-io/k3s`**
Lekki Kubernetes. Sensowny dopiero, gdy będziesz uruchamiał oddzielne instancje dla dużych klientów.

**`ansible/ansible`**
Powtarzalna konfiguracja serwerów. Drugi serwer stawiasz w dziesięć minut, nie w pół dnia.

**`hashicorp/terraform`**
Infrastruktura jako kod.

**`traefik/traefik`** · **`caddyserver/caddy`**
Reverse proxy z automatycznym HTTPS. Caddy prostszy, Traefik lepszy przy wielu usługach.

**`minio/minio`**
Storage zgodny z S3 na własnym serwerze. Cenniki źródłowe i dokumenty — provenance wymaga trzymania oryginałów w nienaruszonej postaci.

**`redis/redis`**
Cache kursów, sesje, broker kolejki.

**`restic/restic`** · **`borgbackup/borg`** · **`duplicati/duplicati`**
Kopie zapasowe plików: deduplikowane, szyfrowane, przyrostowe.

## 32. Obserwowalność i analityka

**`getsentry/sentry`**
Błędy produkcyjne ze śladem stosu i kontekstem żądania. Pierwsza rzecz po pierwszym wdrożeniu.

**`grafana/grafana`** · **`prometheus/prometheus`**
Dashboardy i metryki. Podstawa monitoringu technicznego.

**`grafana/loki`** · **`grafana/tempo`**
Agregacja logów i śledzenie rozproszone, spójne z Grafaną.

**`SigNoz/signoz`**
APM open source: ślady, metryki i logi w jednym narzędziu. Alternatywa dla składania trzech osobnych.

**`open-telemetry/opentelemetry-python`**
Standard instrumentacji. Jeden ślad przechodzący przez cały pipeline: mail, ekstrakcja, normalizacja, zapis.

**`louislam/uptime-kuma`**
Monitoring dostępności z powiadomieniem na telefon. Dowiadujesz się o awarii przed klientem.

**`netdata/netdata`**
Monitoring serwera w czasie rzeczywistym, bez konfiguracji.

**`PostHog/posthog`** ← *dane zbierają się tylko do przodu*
Analityka produktowa: kto czego faktycznie używa. Zbudujesz dwadzieścia funkcji, klienci będą używać pięciu — bez tego nie wiesz których, a to decyduje o kolejności rozwoju.

## 33. Testy i jakość

**`schemathesis/schemathesis`**
Generuje testy z twojej specyfikacji OpenAPI i szuka przypadków, których nie przewidziałeś. Znajduje błędy, których sam byś nie napisał.

**`testcontainers/testcontainers-python`**
Testy na prawdziwym Postgresie uruchamianym w kontenerze. Migracje i zapytania testowane naprawdę, nie na SQLite udającym Postgresa.

**`microsoft/playwright`** · **`vitest-dev/vitest`**
Testy end-to-end i jednostkowe frontendu. Ścieżka oferta → zlecenie → dokument musi mieć test, bo to serce produktu.

**`mswjs/msw`** · **`mockoon/mockoon`** · **`wiremock/wiremock`**
Mockowanie API w testach. WireMock szczególnie przy integracjach zewnętrznych: KSeF, GUS, portale linii — nie testujesz na produkcyjnym KSeF.

**`joke2k/faker`** · **`fakerjs/faker`**
Generowanie danych testowych. Nie testuj silnika wyceny na trzech ręcznie wpisanych stawkach.

**`locustio/locust`** · **`grafana/k6`** · **`tsenart/vegeta`**
Testy obciążeniowe, od najbardziej rozbudowanego do najprostszego.

**`pre-commit/pre-commit`**
Lint, format i podstawowe kontrole przed commitem.

**`tox-dev/tox`**
Macierz środowisk testowych.

**`nektos/act`**
Uruchamianie GitHub Actions lokalnie. Nie czekasz pięciu minut na pipeline, żeby zobaczyć literówkę.

## 34. Jakość danych

**`great-expectations/great_expectations`** ← *niedoceniane, a kluczowe*
Testy na danych, nie na kodzie. „Żadna stawka frachtu nie jest ujemna", „każda pozycja ma walutę", „suma dopłat nie przekracza pięciokrotności frachtu bazowego" — sprawdzane ciągle, przy każdym imporcie. Błędne dane w bazie stawek są niewidoczne aż do reklamacji klienta.

**`unionai-oss/pandera`**
Walidacja struktur danych schematem, wprost w pipeline ekstrakcji.

**`sodadata/soda-core`**
Monitoring jakości danych z regułami zapisanymi w YAML.

**`ydataai/ydata-profiling`**
Raport o zbiorze jednym poleceniem. Szybka ocena nowego cennika przed wpuszczeniem do bazy.

**`pola-rs/polars`**
Przetwarzanie danych szybsze od pandas, z lepszym systemem typów i leniwą ewaluacją.

**`apache/arrow`**
Format kolumnowy do wymiany danych między komponentami bez kopiowania.

**`awslabs/deequ`**
Metryki jakości na dużych zbiorach.

## 35. ETL i integracje danych

**`dlt-hub/dlt`**
Ładowanie danych w kilkunastu linijkach Pythona, z automatyczną obsługą schematu. Do importu danych klienta przy wdrożeniu — a każde wdrożenie się od tego zaczyna.

**`airbytehq/airbyte`**
Setki gotowych konektorów. Gdy klient trzyma dane w SAP-ie, Comarchu albo Google Sheets.

**`meltano/meltano`**
ETL jako kod, wersjonowany w gicie.

**`redpanda-data/connect`**
Strumieniowe przetwarzanie z prostą konfiguracją deklaratywną.

**`apache/nifi`**
Przepływy danych z interfejsem graficznym. Ciężkie, ale czasem szybsze do pokazania klientowi.

**`singer-io/getting-started`**
Standard konektorów, na którym stoi znaczna część powyższych.

## 36. Powiadomienia

**`novuhq/novu`**
Warstwa powiadomień: mail, SMS, push i in-app z jednego API, z szablonami i preferencjami użytkownika. Alerty o wygasających stawkach, zmianie ETA, przekroczonym limicie kredytowym.

**`caronc/apprise`**
Jedno API do ponad stu kanałów. Najprostsze wejście, gdy chcesz tylko wysyłać.

**`knadh/listmonk`**
Mailing do klientów: nowe stawki na relacji, biuletyn rynkowy. Element utrzymania relacji handlowej.

## 37. Konfiguracja, sekrety, flagi

**`flipt-io/flipt`**
Feature flags. Włączasz nową wersję silnika wyceny dla jednego klienta, obserwujesz, dopiero potem dla reszty. Przy produkcie wielodostępnym to nie luksus, tylko warunek bezpiecznego wdrażania zmian.

**`Unleash/unleash`**
Alternatywa, bogatsza w strategie udostępniania.

**`open-feature/spec`**
Standard, żeby nie przywiązywać się do jednego dostawcy.

**`infisical/infisical`** · **`getsops/sops`**
Zarządzanie sekretami: pierwszy jako usługa, drugi jako szyfrowane pliki w repozytorium.

**`bitwarden/server`**
Menedżer haseł dla ciebie i przyszłego zespołu.

## 38. Bezpieczeństwo

**`trufflesecurity/trufflehog`**
Wykrywanie sekretów w repozytorium i historii commitów. Cursor potrafi wkleić klucz API w kod — to go złapie.

**`aquasecurity/trivy`**
Skan podatności obrazów kontenerów i zależności.

**`pyupio/safety`**
Podatności w pakietach Pythona.

**`zaproxy/zaproxy`**
Skan aplikacji webowej. Zrób przed pierwszym klientem, nie po audycie, którego zażąda.

**`crowdsecurity/crowdsec`**
Ochrona serwera przed automatycznymi atakami, z reputacją współdzieloną między instalacjami.

**`pyca/cryptography`**
Szyfrowanie, podpisy i obsługa certyfikatów. Podstawa integracji z KSeF.

## 39. Wydajność

**`benfred/py-spy`**
Profiler działający na uruchomionym procesie, bez modyfikacji kodu. Gdy wycena liczy się osiem sekund, tu zobaczysz, na czym.

**`bloomberg/memray`**
Profiler pamięci. Parsowanie dużych arkuszy potrafi zjeść wszystko dostępne.

**`powa-team/pg_stat_kcache`**
Diagnostyka zapytań na poziomie zużycia zasobów systemowych.

## 40. Optymalizacja — algorytmy, nie modele językowe

Ta sekcja daje pieniądze najszybciej ze wszystkich w tym katalogu.

**`google/or-tools`**
Solver od Google: programowanie całkowitoliczbowe, przepływy, przydziały. Odpowiada na pytanie „czy opłaca się doładować ten kontener i o ile podnieść cenę" — decyzja podejmowana dziś na wyczucie.

**`skjolber/3d-bin-container-packing`**
Upakowanie kontenera w trzech wymiarach. Ile palet wejdzie do 40HC i w jakim układzie — z wynikiem, który można pokazać klientowi.

**`jerry800416/3D-bin-packing`**
To samo w Pythonie, prostsze w integracji.

**`PyVRP/PyVRP`**
Trasowanie z ograniczeniami: okna czasowe, ładowność, wiele pojazdów. Do dowozów i odwozów.

**`TimefoldAI/timefold-solver`**
Solver ograniczeń ogólnego przeznaczenia: harmonogramy, przydziały, plany załadunków.

**`coin-or/pulp`**
Programowanie liniowe w Pythonie. Wybór optymalnego dostawcy przy wielu ograniczeniach jednocześnie.

## 41. Prognozowanie

**`Nixtla/statsforecast`**
Metody statystyczne, bardzo szybkie. Prognoza stawek i wolumenów na twoich danych historycznych.

**`Nixtla/neuralforecast`**
Modele głębokie, gdy zgromadzisz wystarczająco długą historię.

**`unit8co/darts`**
Jednolite API do kilkudziesięciu modeli — dobre do porównania, który działa na twoich danych.

**`facebook/prophet`**
Sezonowość i trend, użyteczny bez głębokiej wiedzy statystycznej. Fracht morski ma wyraźną sezonowość.

## 42. Generowanie kodu ze schematu

Każda linijka, której nie napiszesz, to linijka, której nie utrzymujesz.

**`hey-api/openapi-ts`** ← *wdrożyć od razu*
Generuje klienta TypeScript z twojej specyfikacji OpenAPI. Zmieniasz endpoint w FastAPI — frontend dostaje nowe typy automatycznie. Zero ręcznej synchronizacji, zero rozjazdów.

**`OpenAPITools/openapi-generator`**
Klienty w kilkudziesięciu językach. Przyda się, gdy klient poprosi o SDK do integracji.

**`fern-api/fern`**
SDK i dokumentacja z jednej definicji.

**`stoplightio/prism`**
Mock server generowany z OpenAPI. Frontend nie czeka na gotowy backend.

**`scalar/scalar`** · **`Redocly/redoc`**
Dokumentacja API. Scalar ładniejszy, Redoc lepszy do dokumentacji publicznej dla integratorów.

**`sqlc-dev/sqlc`**
Typowany kod generowany z zapytań SQL.

**`prisma/prisma`** · **`drizzle-team/drizzle-orm`** · **`kysely-org/kysely`**
ORM-y i query buildery dla części w Node, uszeregowane od najbogatszego do najbliższego czystemu SQL.

## 43. Automatyzacja repozytorium

**`renovatebot/renovate`** ← *wdrożyć w pierwszym tygodniu*
Automatyczne pull requesty z aktualizacjami zależności, z changelogiem i wynikiem testów. Przy trzydziestu bibliotekach ręczne pilnowanie jest niewykonalne, a zaległości kumulują się wykładniczo — po roku bez aktualizacji migracja to osobny projekt.

**`dependabot/dependabot-core`**
Alternatywa wbudowana w GitHuba, prostsza w konfiguracji.

**`semantic-release/semantic-release`** · **`googleapis/release-please`**
Wersjonowanie i changelog generowane z commitów. Klient pyta „co się zmieniło w tej wersji" — masz odpowiedź bez pisania jej ręcznie.

**`commitizen-tools/commitizen`** · **`conventional-changelog/commitlint`**
Wymuszenie i walidacja formatu commitów, wymagane przez powyższe.

**`casey/just`**
Task runner. `just dev`, `just migrate`, `just seed` zamiast pamiętania trzech linijek każdego polecenia.

**`earthly/earthly`**
Powtarzalne buildy: to samo lokalnie i w CI.

**`qodo-ai/pr-agent`** ← *twój recenzent*
Automatyczny przegląd pull requestów. Piszesz ten system sam — nie masz kto cię sprawdzić. To jedyna warstwa kontroli między Cursorem a produkcją.

## 44. Panele wewnętrzne i szybkie narzędzia

**`directus/directus`**
Panel administracyjny nad istniejącą bazą, postawiony w godzinę. Masz CRUD do słowników, zanim napiszesz własne ekrany.

**`nocodb/nocodb`** · **`teableio/teable`**
Arkusz kalkulacyjny nad Postgresem. Do ręcznych korekt stawek, zanim zbudujesz porządny interfejs.

**`appsmithorg/appsmith`** · **`ToolJet/ToolJet`** · **`Budibase/budibase`**
Narzędzia wewnętrzne składane z komponentów. Do zadań operacyjnych, na które szkoda pisać ekrany.

## 45. Dokumentacja i wiedza

**`squidfunk/mkdocs-material`**
Dokumentacja techniczna z plików markdown. Twoje pliki specyfikacji jako żywa dokumentacja, przeszukiwalna i wersjonowana razem z kodem.

**`facebook/docusaurus`**
Dokumentacja dla klientów i integratorów, z wersjonowaniem.

**`slatedocs/slate`**
Jednostronicowa dokumentacja API.

**`outline/outline`** · **`AppFlowy-IO/AppFlowy`**
Baza wiedzy i notatki, self-hosted.

**`mermaid-js/mermaid`**
Diagramy jako tekst. Działają w dokumentacji, w opisach pull requestów i w kontekście podawanym modelowi.

## 46. Modelowanie i diagramy

**`azimuttapp/azimutt`**
Wizualna eksploracja schematu bazy. Przy czterdziestu tabelach z relacjami to jedyny sposób, żeby zobaczyć całość naraz.

**`holistics/dbml`**
Schemat bazy jako czytelny tekst. Świetne wejście dla Cursora — opisujesz model, dostajesz migracje.

**`structurizr/dsl`**
Architektura w modelu C4 zapisana jako kod.

**`excalidraw/excalidraw`**
Szkice, które nie udają dokumentacji.

**`jgraph/drawio`**
Diagramy formalne dla klientów i audytorów.

## 47. Wielojęzyczność

**`i18next/i18next`**
Interfejs w wielu językach. Twoi agenci zagraniczni nie mówią po polsku, a to oni będą wprowadzać stawki — bez tego odcinasz sobie połowę użytkowników.

**`lingui/js-lingui`**
Alternatywa z automatyczną ekstrakcją tekstów z kodu.

**`formatjs/formatjs`**
Formatowanie liczb, dat i liczby mnogiej zgodnie z regułami języka.

**`WeblateOrg/weblate`**
Zarządzanie tłumaczeniami, gdy będzie ich więcej niż dwa.

## 48. CRM i obsługa klienta

**`chatwoot/chatwoot`**
Kanał wsparcia w aplikacji: czat, mail, historia rozmów.

**`zammad/zammad`**
Ticketing, gdy klientów będzie więcej niż kilku.

## 49. Praca z agentami kodującymi

**`github/spec-kit`** ← *przy projekcie tej wielkości robi różnicę*
Development sterowany specyfikacją. Twoje pliki spec'a stają się źródłem prawdy dla agenta zamiast promptowania z pamięci. Przy systemie o czterdziestu tabelach to różnica między porządkiem a chaosem po trzecim miesiącu.

**`PatrickJS/awesome-cursorrules`**
Gotowe pliki `.cursorrules` dla różnych stacków. Wyraźnie poprawia jakość generowanego kodu — skopiuj i dostosuj do swoich konwencji.

**`x1xhlol/system-prompts-and-models-of-ai-tools`**
Zebrane prompty systemowe narzędzi AI. Nauka inżynierii promptu na działających przykładach, nie na tutorialach.

**`anthropics/claude-code`**
Agent terminalowy. Do zadań obejmujących wiele plików naraz, gdzie Cursor gubi kontekst.

**`cline/cline`** · **`continuedev/continue`** · **`aider-AI/aider`**
Trzy alternatywne agenty: w VS Code, jako rozszerzenie i w terminalu. Warto znać, bo każdy ma inne mocne strony.

**`BuilderIO/micro-agent`**
Agent piszący kod pod testy: najpierw test, potem implementacja aż do przejścia. Dobre przy regułach biznesowych, gdzie poprawność jest weryfikowalna.

**`danielmiessler/fabric`**
Biblioteka wzorców promptów do zadań powtarzalnych.

## 50. Drobne, które oszczędzają godziny

**`charmbracelet/gum`**
Ładne skrypty powłoki. Narzędzia operacyjne, których nie chce ci się pisać w Pythonie.

**`sharkdp/fd`** · **`BurntSushi/ripgrep`**
Szukanie plików i treści szybsze niż w IDE.

**`jqlang/jq`**
Obróbka JSON-a z odpowiedzi API prosto w terminalu.

**`httpie/cli`**
Wywołania API bez pamiętania składni curla.

**`direnv/direnv`**
Automatyczne wczytywanie zmiennych środowiskowych per katalog.

---

# JAK Z TEGO KORZYSTAĆ

## Instalujesz w pierwszym miesiącu

`full-stack-fastapi-template` · `sqlalchemy` · `alembic` · `pydantic` · `uv` · `ruff` · `mypy` · `pytest` · `hypothesis` · `py-moneyed` · `babel` · `pendulum` · `improved-un-locodes` · `pgvector` · `docling` · `marker` · `pdfplumber` · `calamine` · `instructor` · `langfuse` · `promptfoo` · `llm-guard` · `emailengine` · `refine` · `TanStack/table` · `glide-data-grid` · `shadcn-ui` · `zod` · `typst` · `minio` · `redis` · `sentry` · `renovate` · `pgbackrest` · `posthog`

Trzydzieści pięć pozycji. Reszta katalogu to mapa, do której wracasz przy konkretnym module.

## Czytasz, zamiast instalować

**`frappe/frappe`** — jak zbudować system, w którym typy dokumentów i pola są danymi, nie kodem. To rozwiązuje problem, który cię zabije przy piątym kliencie.

**`beancount/beancount`** — najczystszy model podwójnego zapisu. Godzina lektury oszczędza decyzji o pisaniu własnej księgowości.

**`tigerbeetle/tigerbeetle`** — dlaczego reguły finansowe powinny być wymuszane przez bazę, a nie przez kod. Zmieni ci projekt tabeli `charge`.

**`twentyhq/twenty`** — dobrze rozwiązane elastyczne pola i relacje w nowoczesnym CRM.

## Wdrażasz wcześniej, niż podpowiada intuicja

**`langfuse`** — telemetria zbiera się tylko do przodu. Godzina teraz, tydzień śledztwa później.

**`label-studio`** — bez zbioru referencyjnego nie zmierzysz skuteczności ekstrakcji, a bez pomiaru nie poprawisz.

**`pgbackrest`** — pierwszy backup robi się przed pierwszym klientem. Trzymasz cudze dane handlowe.

**`renovate`** — zaległości w zależnościach rosną wykładniczo.

**`posthog`** — dane o użyciu zbierają się tylko do przodu, wstecz ich nie odzyskasz.

**`llm-guard`** — przetwarzasz pliki od nieznanych nadawców i wysyłasz je do modelu.

## Czego w tym katalogu nie ma

**Silnika stawek morskich.** Po przeszukaniu tagów `freight-forwarding`, `freight-management`, `logistics`, `edifact` i `text2sql` — nie istnieje open-source'owy system obsługujący FCL i LCL z pełnym zestawem dopłat, terminami ważności i rozwiązywaniem kolizji cenników.

Tabele `rate_sheet`, `rate_line` i `charge_code` piszesz sam. To jest jedyna część tego systemu, która jest naprawdę twoja — i jedyna, której konkurencja nie skopiuje z GitHuba.
