# 99 repozytoriów — narzędzia i automatyzacja

Uzupełnienie o warstwę, która nie jest funkcją produktu, tylko sprawia, że jedna osoba jest w stanie utrzymać system tej wielkości. Razem ze wszystkim wcześniej: **433 pozycje**.

---

## A. Generowanie kodu ze schematu (10)

Piszesz sam. Każda linijka, której nie napiszesz, to linijka, której nie utrzymujesz.

| Repo | Po co |
|---|---|
| `hey-api/openapi-ts` | **Klient TypeScript generowany z OpenAPI FastAPI.** Zmieniasz endpoint — frontend dostaje typy automatycznie. Zero ręcznej synchronizacji |
| `OpenAPITools/openapi-generator` | Klienty w kilkudziesięciu językach — gdy klient poprosi o integrację |
| `fern-api/fern` | SDK + dokumentacja z jednej definicji API |
| `stoplightio/prism` | Mock server z OpenAPI — frontend nie czeka na backend |
| `scalar/scalar` | Dokumentacja API, ładniejsza niż domyślna |
| `Redocly/redoc` | Alternatywa, dobra do dokumentacji dla klientów |
| `sqlc-dev/sqlc` | Typowany kod z zapytań SQL |
| `prisma/prisma` | ORM z generowaniem typów, gdyby część była w Node |
| `drizzle-team/drizzle-orm` | Lżejszy, bliżej SQL |
| `kysely-org/kysely` | Query builder z pełnym typowaniem |

## B. Automatyzacja repozytorium (10)

| Repo | Po co |
|---|---|
| `renovatebot/renovate` | **Automatyczne PR-y z aktualizacjami zależności.** Przy 30 bibliotekach ręczne pilnowanie jest niewykonalne |
| `dependabot/dependabot-core` | Alternatywa wbudowana w GitHuba |
| `semantic-release/semantic-release` | Wersjonowanie i changelog z commitów |
| `googleapis/release-please` | To samo, bardziej przewidywalne |
| `commitizen-tools/commitizen` | Wymusza format commitów — potrzebny dla powyższych |
| `conventional-changelog/commitlint` | Walidacja commitów w CI |
| `casey/just` | Task runner. `just dev`, `just migrate`, `just seed` zamiast pamiętania poleceń |
| `earthly/earthly` | Powtarzalne buildy — to samo lokalnie i w CI |
| `nektos/act` | GitHub Actions lokalnie, bez czekania na pipeline |
| `pre-commit/pre-commit` | Lint i format przed commitem |

## C. Jakość danych (7)

| Repo | Po co |
|---|---|
| `great-expectations/great_expectations` | **Testy na danych, nie na kodzie.** „Żadna stawka frachtu nie może być ujemna", „każda pozycja ma walutę" — sprawdzane ciągle, nie raz |
| `unionai-oss/pandera` | Walidacja DataFrame'ów schematem — w pipeline ekstrakcji |
| `sodadata/soda-core` | Monitoring jakości danych z regułami w YAML |
| `ydataai/ydata-profiling` | Raport o zbiorze jednym poleceniem — do oceny nowego cennika |
| `pola-rs/polars` | Przetwarzanie danych szybsze od pandas, lepsze typy |
| `apache/arrow` | Format kolumnowy pod wymianę danych |
| `awslabs/deequ` | Metryki jakości na dużych zbiorach |

## D. ETL i integracje (6)

| Repo | Po co |
|---|---|
| `dlt-hub/dlt` | **Ładowanie danych w kilkunastu linijkach Pythona.** Import z systemów klientów przy wdrożeniach |
| `airbytehq/airbyte` | Setki konektorów gotowych — gdy klient ma dane w SAP-ie albo Comarchu |
| `meltano/meltano` | ETL jako kod, wersjonowany |
| `redpanda-data/connect` | Strumieniowe przetwarzanie z prostą konfiguracją |
| `apache/nifi` | Przepływy danych z interfejsem graficznym |
| `singer-io/getting-started` | Standard konektorów, na którym stoi reszta |

## E. Powiadomienia (5)

| Repo | Po co |
|---|---|
| `novuhq/novu` | **Warstwa powiadomień: mail, SMS, push, in-app z jednego API.** Alerty o wygasających stawkach, zmianie ETA, przekroczonym limicie kredytowym |
| `caronc/apprise` | Jedno API do stu kanałów — najprostsze wejście |
| `knadh/listmonk` | Mailing do klientów: nowe stawki na relacji, biuletyn rynkowy |
| `postalserver/postal` | Własny serwer wysyłkowy, gdy wolumen rośnie |
| `nodemailer/nodemailer` | Podstawa wysyłki po stronie Node |

## F. Harmonogramowanie i kolejki (5)

| Repo | Po co |
|---|---|
| `procrastinate-org/procrastinate` | **Kolejka zadań na samym Postgresie.** Bez Redisa, bez Celery, bez dodatkowego komponentu do utrzymania. Przy jednoosobowym zespole to poważna zaleta |
| `hatchet-dev/hatchet` | Kolejka z retry, priorytetami i dashboardem |
| `agronholm/apscheduler` | Zadania cykliczne: kursy NBP o 12:15, sprawdzanie wygasających stawek co rano |
| `riverqueue/river` | Kolejka na Postgresie w Go |
| `mcuadros/ofelia` | Cron dla kontenerów |

## G. Konfiguracja i sekrety (5)

| Repo | Po co |
|---|---|
| `flipt-io/flipt` | **Feature flags.** Włączasz nową wersję rate engine dla jednego klienta, nie dla wszystkich |
| `Unleash/unleash` | Alternatywa, bogatsza |
| `open-feature/spec` | Standard, żeby nie przywiązywać się do dostawcy |
| `infisical/infisical` | Zarządzanie sekretami zespołu |
| `getsops/sops` | Szyfrowane sekrety w repozytorium |

## H. Panele wewnętrzne i szybkie narzędzia (6)

| Repo | Po co |
|---|---|
| `directus/directus` | **Panel administracyjny nad istniejącą bazą.** Postawiasz w godzinę i masz CRUD do słowników, zanim napiszesz własny |
| `nocodb/nocodb` | Arkusz nad Postgresem — dla ciebie do ręcznych poprawek stawek |
| `teableio/teable` | Alternatywa, bliżej Airtable |
| `appsmithorg/appsmith` | Narzędzia wewnętrzne z komponentów |
| `ToolJet/ToolJet` | To samo, inny model licencji |
| `Budibase/budibase` | Aplikacje wewnętrzne bez pisania frontendu |

## I. Dokumentacja (6)

| Repo | Po co |
|---|---|
| `squidfunk/mkdocs-material` | **Dokumentacja techniczna z markdownu.** Twoje pliki spec'a jako żywa dokumentacja, nie pliki w folderze |
| `facebook/docusaurus` | Dokumentacja dla klientów i integratorów |
| `outline/outline` | Baza wiedzy zespołu, gdy będzie zespół |
| `mermaid-js/mermaid` | Diagramy jako tekst — w dokumentacji, w PR-ach, w Cursorze |
| `slatedocs/slate` | Jednostronicowa dokumentacja API |
| `AppFlowy-IO/AppFlowy` | Notatki i zadania self-hosted |

## J. Modelowanie i diagramy (5)

| Repo | Po co |
|---|---|
| `azimuttapp/azimutt` | **Eksploracja schematu bazy.** Przy 40 tabelach z relacjami to jedyny sposób, żeby zobaczyć całość |
| `holistics/dbml` | Schemat bazy jako czytelny tekst — dobre wejście dla Cursora |
| `structurizr/dsl` | Architektura w modelu C4 jako kod |
| `excalidraw/excalidraw` | Szkice, które nie udają dokumentacji |
| `jgraph/drawio` | Diagramy formalne dla klientów |

## K. Testy i dane testowe (6)

| Repo | Po co |
|---|---|
| `joke2k/faker` | **Generowanie danych testowych.** Nie testuj rate engine na trzech ręcznie wpisanych stawkach |
| `fakerjs/faker` | To samo w JS |
| `mswjs/msw` | Mockowanie API w testach frontendu |
| `mockoon/mockoon` | Mock server z interfejsem |
| `wiremock/wiremock` | Mockowanie integracji zewnętrznych — KSeF, GUS, portale linii |
| `vitest-dev/vitest` | Testy frontendu, szybkie |

## L. Wielojęzyczność (4)

| Repo | Po co |
|---|---|
| `i18next/i18next` | **Interfejs po polsku i angielsku.** Twoi agenci zagraniczni nie mówią po polsku — a to oni będą wprowadzać stawki |
| `lingui/js-lingui` | Alternatywa z ekstrakcją tłumaczeń z kodu |
| `formatjs/formatjs` | Formatowanie liczb, dat, liczby mnogiej |
| `WeblateOrg/weblate` | Zarządzanie tłumaczeniami, gdy będzie ich więcej niż dwa |

## M. Wdrożenie i infrastruktura (6)

| Repo | Po co |
|---|---|
| `dokku/dokku` | **Deploy jednym `git push`.** Najprostsze PaaS na własnym serwerze |
| `caprover/caprover` | To samo z interfejsem graficznym |
| `portainer/portainer` | Zarządzanie kontenerami przez przeglądarkę |
| `k3s-io/k3s` | Lekki Kubernetes, gdy dojdą klienci na oddzielnych instancjach |
| `ansible/ansible` | Powtarzalna konfiguracja serwerów |
| `hashicorp/terraform` | Infrastruktura jako kod |

## N. Kopie zapasowe (3)

| Repo | Po co |
|---|---|
| `pgbackrest/pgbackrest` | **Backup Postgresa z odtwarzaniem do punktu w czasie.** Trzymasz cudze dane handlowe. Utrata bazy kończy firmę |
| `borgbackup/borg` | Deduplikowane kopie plików i dokumentów |
| `duplicati/duplicati` | Kopie do chmury z interfejsem |

## O. Monitoring i analityka produktu (5)

| Repo | Po co |
|---|---|
| `PostHog/posthog` | **Kto czego faktycznie używa.** Zbudujesz dwadzieścia funkcji, klienci będą używać pięciu. Bez tego nie wiesz których |
| `louislam/uptime-kuma` | Monitoring dostępności — SMS, gdy padnie |
| `SigNoz/signoz` | APM open source: ślady, metryki, logi w jednym |
| `grafana/loki` | Agregacja logów |
| `grafana/tempo` | Rozproszone śledzenie żądań |

## P. Podpisy i obieg dokumentów (4)

| Repo | Po co |
|---|---|
| `MatthiasValvekens/pyHanko` | **Podpis PDF w standardzie PAdES.** Dokumenty spedycyjne z podpisem elektronicznym — funkcja, o którą klienci pytają |
| `documenso/documenso` | Obieg podpisów — umowy z agentami, zlecenia stałe |
| `docuseal/docuseal` | Alternatywa, prostsza |
| `Stirling-Tools/Stirling-PDF` | Operacje na PDF: łączenie, dzielenie, stemplowanie, znak wodny |

## Q. Rozliczanie subskrypcji (3)

Potrzebne dopiero, gdy zaczniesz sprzedawać. Ale projektuj tak, żeby dało się doszyć.

| Repo | Po co |
|---|---|
| `getlago/lago` | **Rozliczanie według zużycia.** Cennik per liczba zleceń albo per sparsowany cennik — a nie płaska opłata |
| `killbill/killbill` | Dojrzały silnik subskrypcji |
| `stripe/stripe-python` | Płatności kartą dla klientów zagranicznych |

## R. CRM i obsługa klienta (3)

| Repo | Po co |
|---|---|
| `twentyhq/twenty` | **Nowoczesny CRM open source.** Przeczytaj model danych, zanim zaprojektujesz swoją część CRM-ową |
| `chatwoot/chatwoot` | Kanał wsparcia dla użytkowników systemu |
| `zammad/zammad` | Ticketing, gdy klientów będzie więcej |

## S. Bezpieczeństwo (5)

| Repo | Po co |
|---|---|
| `trufflesecurity/trufflehog` | Wykrywanie sekretów w repo |
| `aquasecurity/trivy` | Skan podatności obrazów i zależności |
| `zaproxy/zaproxy` | Skan aplikacji webowej |
| `pyupio/safety` | Podatności w zależnościach Pythona |
| `crowdsecurity/crowdsec` | Ochrona serwera przed automatycznymi atakami |

## T. Wydajność i skalowanie (5)

| Repo | Po co |
|---|---|
| `benfred/py-spy` | **Profiler bez modyfikacji kodu.** Gdy wycena liczy się osiem sekund, tu zobaczysz dlaczego |
| `bloomberg/memray` | Profiler pamięci — parsowanie dużych Exceli potrafi zjeść wszystko |
| `grafana/k6` | Testy obciążeniowe |
| `powa-team/pg_stat_kcache` | Diagnostyka wolnych zapytań |
| `ankane/pghero` | Panel zdrowia Postgresa: brakujące indeksy, wolne zapytania |

## U. Drobne, a oszczędzają godziny (6)

| Repo | Po co |
|---|---|
| `charmbracelet/gum` | Ładne skrypty powłoki — narzędzia operacyjne, których nie chce ci się pisać w Pythonie |
| `sharkdp/fd` · `BurntSushi/ripgrep` | Szukanie w kodzie szybsze niż w IDE |
| `jqlang/jq` | Obróbka JSON-a z odpowiedzi API w terminalu |
| `tsenart/vegeta` | Szybki test obciążeniowy pojedynczego endpointu |
| `httpie/cli` | Ręczne wywołania API bez składni curla |
| `direnv/direnv` | Automatyczne wczytywanie zmiennych środowiskowych per katalog |

---

## Zasada doboru

Instalujesz narzędzie, gdy ból jest już realny, nie zapobiegawczo. Wyjątki, które wdraża się od razu, bo później kosztują wielokrotnie więcej:

- `renovatebot/renovate` — bo zaległości w zależnościach kumulują się wykładniczo
- `pgbackrest/pgbackrest` — bo pierwszy backup robi się przed pierwszym klientem
- `great-expectations` — bo błędne dane w bazie stawek są niewidoczne aż do reklamacji
- `PostHog` — bo dane o użyciu zbierają się tylko do przodu
