# 231 repozytoriów pod budowę ERP spedycyjnego

**Jak czytać:** to katalog terenu, nie lista zakupów. Sekcja „Co faktycznie instalujesz" na końcu wskazuje ~25 pozycji na start. Reszta jest po to, żebyś wiedział, co istnieje, zanim zaczniesz coś pisać od zera.

**O dokładności:** część ścieżek zweryfikowałem wyszukiwaniem, reszta to projekty powszechnie znane. Repozytoria bywają przenoszone między organizacjami — sprawdź ścieżkę przed dodaniem do zależności.

---

## 1. Szkielet backendu (18)

| Repo | Po co |
|---|---|
| `fastapi/fastapi` | Rdzeń API |
| `fastapi/full-stack-fastapi-template` | Oficjalny szablon startowy — dzień zerowy |
| `fastapi/sqlmodel` | Model bazy i schemat API w jednym |
| `sqlalchemy/sqlalchemy` | ORM |
| `sqlalchemy/alembic` | Migracje |
| `pydantic/pydantic` | Walidacja, kontrakt z LLM |
| `encode/starlette` | ASGI pod FastAPI |
| `encode/uvicorn` | Serwer ASGI |
| `encode/httpx` | Klient HTTP async — integracje zewnętrzne |
| `celery/celery` | Kolejka zadań pipeline'u |
| `rq/rq` | Lżejsza kolejka |
| `hynek/structlog` | Logi strukturalne |
| `pytest-dev/pytest` | Testy |
| `HypothesisWorks/hypothesis` | Testy property-based — idealne na przeliczenia walutowe i chargeable weight |
| `fastapi/typer` | CLI do zadań administracyjnych |
| `astral-sh/ruff` | Linter + formatter, szybki |
| `astral-sh/uv` | Menedżer pakietów, zastępuje pip/poetry |
| `python/mypy` | Typowanie statyczne — przy 30 tabelach ratuje życie |

## 2. Postgres i okolice (14)

| Repo | Po co |
|---|---|
| `pgvector/pgvector` | Embeddingi opisów opłat |
| `supabase/supabase` | RLS + auth + storage z pudełka |
| `kvesteri/sqlalchemy-continuum` | Wersjonowanie rekordów |
| `sqlfluff/sqlfluff` | Linter SQL |
| `djrobstep/migra` | Diff schematów |
| `dimitri/pgloader` | Migracja danych z Excela/MySQL/CSV |
| `pgbouncer/pgbouncer` | Pooling połączeń |
| `wal-g/wal-g` | Backupy PITR |
| `prometheus-community/postgres_exporter` | Metryki bazy |
| `PostgREST/postgrest` | REST z schematu bazy — dobre na prototypy raportów |
| `hasura/graphql-engine` | GraphQL nad Postgresem |
| `citusdata/citus` | Skalowanie poziome, gdyby kiedyś było trzeba |
| `timescale/timescaledb` | Szeregi czasowe — historia stawek, trendy frachtu |
| `electric-sql/pglite` | Postgres w przeglądarce — do testów i demo offline |

## 3. Dane referencyjne (13)

| Repo | Po co |
|---|---|
| `datasets/un-locode` | Podstawa tabeli portów |
| `cristan/improved-un-locodes` | 670 tys. aliasów nazw + poprawione współrzędne |
| `geoapify/un-locode` | Klient Node |
| `marek5050/UN-LOCODE` | Prosty CSV do seeda |
| `SeaconLogistics/un_locode` | Model funkcji lokalizacji (port/rail/airport/ICD) |
| `tadziqusky/unlocode-ports` | Filtr: same porty morskie |
| `datasets/country-codes` | ISO 3166 + mapowania |
| `datasets/currency-codes` | ISO 4217 |
| `datasets/harmonized-system` | Kody HS — do klasyfikacji towaru na ofercie |
| `mledoze/countries` | Kraje z nazwami wielojęzycznymi |
| `dr5hn/countries-states-cities-database` | Pełna hierarchia adresowa do formularzy |
| `hexorx/countries` | Dane krajów z VAT i formatami adresów |
| `datasets/language-codes` | ISO 639 — dokumenty wielojęzyczne |

## 4. Referencje: ERP, TMS, WMS open source (18)

| Repo | Po co |
|---|---|
| `frappe/erpnext` | Najbliższy pełnemu ERP. Podpatrz model Party i Landed Cost |
| `frappe/frappe` | Framework pod ERPNext — metadane, uprawnienia, workflow |
| `odoo/odoo` | Moduł `account` i `stock` |
| `dolibarr/dolibarr` | Prostszy kod, czytelny model propozycji handlowej |
| `loadpartner/tms` | Jedyny żywy open-source TMS dla brokerów |
| `fleetbase/fleetbase` | Modułowa platforma logistyczna |
| `openwms/org.openwms` | Poważny WMS z warstwą sterowania magazynem automatycznym |
| `fjykTec/ModernWMS` | WMS wyjęty z komercyjnych wdrożeń ERP, otwarty |
| `myTinyWMS/myTinyWMS` | Lekki WMS dla MŚP |
| `openboxes/openboxes` | WMS z naciskiem na śledzenie ruchów towaru |
| `infiniteoo/wms` | WMS na Next.js + Postgres + Supabase — bliski twojemu stackowi |
| `hightower-systems/sentry-wms` | Świeży WMS w Pythonie, warstwa wykonawcza obok ERP |
| `bigcapitalhq/bigcapital` | Open-source księgowość z podwójnym zapisem |
| `invoiceninja/invoiceninja` | Fakturowanie multi-currency + szablony |
| `akaunting/akaunting` | Multi-company, izolacja danych |
| `frappe/books` | Lekka księgowość desktopowa |
| `medusajs/medusa` | Architektura modułowa w TS — wzorzec, jeśli robisz backend w Node |
| `ever-co/ever-gauzy` | ERP w NestJS — model uprawnień i multi-tenancy |

## 5. Parsowanie dokumentów (16)

| Repo | Po co |
|---|---|
| `docling-project/docling` | Główny parser cenników |
| `datalab-to/marker` | Szybsza alternatywa, pipeline małych modeli |
| `Unstructured-IO/unstructured` | Typowane elementy zamiast płaskiego tekstu |
| `microsoft/markitdown` | Szybka ścieżka dla prostych plików |
| `jsvine/pdfplumber` | Współrzędne znaków — podstawa `source_ref` |
| `pymupdf/PyMuPDF` | Najszybszy tekst + render stron do obrazów |
| `camelot-dev/camelot` | Tabele z liniami siatki |
| `opendataloader-project/opendataloader-pdf` | Wykrywa po cichu pominięte fragmenty stron |
| `genieincodebottle/parsemypdf` | Porównanie kilkunastu parserów na jednym zbiorze |
| `datalab-to/surya` | OCR + layout dla skanów |
| `tesseract-ocr/tesseract` | OCR offline jako fallback |
| `JaidedAI/EasyOCR` | OCR wielojęzyczny, prosty w użyciu |
| `PaddlePaddle/PaddleOCR` | Bardzo dobry na tabele i języki azjatyckie — cenniki od chińskich agentów |
| `mindee/doctr` | OCR zorientowany na dokumenty biznesowe |
| `tafia/calamine` | Najszybszy czytnik XLSX |
| `py-pdf/pypdf` | Cięcie, łączenie, metadane PDF |

## 6. LLM: ekstrakcja, kontrola, ewaluacja (16)

| Repo | Po co |
|---|---|
| `567-labs/instructor` | Wymuszanie schematu Pydantic na odpowiedzi modelu |
| `dottxt-ai/outlines` | Generowanie sterowane gramatyką |
| `BoundaryML/baml` | Prompty jako typowane funkcje |
| `anthropics/anthropic-sdk-python` | SDK + batch API |
| `anthropics/claude-cookbooks` | Wzorce ekstrakcji z dokumentów |
| `pydantic/pydantic-ai` | Agenty z typowanym wyjściem, spójne z resztą stacku |
| `BerriAI/litellm` | Jeden interfejs + tracking kosztów |
| `langfuse/langfuse` | Obserwowalność promptów — postaw od pierwszego dnia |
| `promptfoo/promptfoo` | Testy regresyjne promptów na twoich cennikach |
| `Arize-ai/phoenix` | Ewaluacja jakości ekstrakcji w czasie |
| `explodinggradients/ragas` | Metryki jakości — adaptowalne do ekstrakcji |
| `guardrails-ai/guardrails` | Walidatory wyjścia: zakresy kwot, formaty dat |
| `simonw/llm` | CLI do szybkich eksperymentów z promptem |
| `langchain-ai/langchain` | Znasz z tutoriali — używaj wybiórczo, nie jako fundamentu |
| `langchain-ai/langgraph` | Grafy stanów dla wieloetapowego pipeline'u |
| `run-llama/llama_index` | Indeksowanie archiwum cenników do wyszukiwania |

## 7. Poczta (7)

| Repo | Po co |
|---|---|
| `postalsys/emailengine` | IMAP → REST + webhooki. Największa oszczędność czasu w tej sekcji |
| `ikvk/imap_tools` | Klient IMAP w Pythonie, gdy chcesz sam |
| `SpamScope/mail-parser` | Parsowanie `.eml`/`.msg`, kodowania, załączniki |
| `microsoftgraph/msgraph-sdk-python` | Skrzynka na Microsoft 365 |
| `docker-mailserver/docker-mailserver` | Własna skrzynka `rates@` |
| `axllent/mailpit` | Przechwytywanie maili w developmencie — nie wyślesz oferty testowej klientowi |
| `foxcpp/maddy` | Lekki serwer pocztowy w Go |

## 8. EDI i komunikaty branżowe (10)

| Repo | Po co |
|---|---|
| `nerdocs/pydifact` | Parser i serializer UN/EDIFACT w Pythonie — jedyny sensowny |
| `parcelLab/edi-iftmin` | Parsowanie **IFTMIN i IFTSTA** — zlecenie transportowe i status przesyłki. Dokładnie twoje komunikaty |
| `xoscar/EDI-IFTMIN` | Druga implementacja tych samych komunikatów |
| `xlate/staedi` | Streaming reader/writer z walidacją schematów (Java) |
| `indice-co/EDI.Net` | Serializer EDIFACT/X12/TRADACOMS (.NET) |
| `smooks/smooks` | Framework transformacji EDI ↔ XML ↔ CSV |
| `walmartlabs/gozer` | Parser X12, gdyby doszły relacje amerykańskie |
| `michaelachrisco/Electronic-Interchange-Github-Resources` | Katalog wszystkich narzędzi EDI na GitHubie |
| `OpenAS2/OpenAs2App` | AS2 — protokół wymiany plików z liniami i dużymi klientami |
| `phax/as2-lib` | Biblioteka AS2 w Javie |

## 9. E-faktura: KSeF i UE (9)

| Repo | Po co |
|---|---|
| `CIRFMF/ksef-api` | Oficjalny przewodnik Ministerstwa Finansów po API KSeF 2.0 |
| `smekcio/ksef-client-python` | SDK Python, KSeF API v2, kryptografia, XAdES, QR |
| `ArturSkowronski/ksef-cli` | CLI: XML lub skan PDF na wejściu, wysyłka na wyjściu |
| `m32/ksef` | Skrypty Python — dobre do nauki flow autoryzacji |
| `m32/ksef-pdf` | Wizualizacja faktury: XML → PDF z numerem KSeF i QR |
| `Pafkaja/ksef_faktury_list` | Pobieranie faktur z KSeF |
| `fakturownia/API` | Integracja zamiast własnej księgowości |
| `akretion/factur-x` | Factur-X/ZUGFeRD — faktura hybrydowa PDF+XML dla klientów z DE/FR |
| `phax/ph-ubl` | UBL i Peppol — europejski standard e-faktury |

## 10. Polskie rejestry (5)

| Repo | Po co |
|---|---|
| `bigzbig/regonapi` | Klient REGON BIR1.1 w Pythonie, tryb sandbox bez klucza |
| `grzesieksw/GusApi` | Wariant .NET |
| `infirsoft/vat-whitelist-api` | Biała lista podatników VAT — weryfikacja rachunku |
| `m4rcelpl/WykazPodatnikow` | Biała lista, .NET, obsługa pliku płaskiego |
| `datasets/currency-codes` | Do walidacji walut na fakturze (patrz też sekcja 3) |

## 11. Księgowość i ledger (10)

| Repo | Po co |
|---|---|
| `beancount/beancount` | Podwójny zapis w plikach tekstowych. **Przeczytaj model, zanim zdecydujesz, że piszesz własny** |
| `beancount/fava` | Interfejs webowy nad Beancount |
| `beancount/beanquery` | Język zapytań nad księgą |
| `beancount/smart_importer` | Import wyciągów z uczeniem kategoryzacji |
| `ledger/ledger` | Klasyk plain-text accounting (C++) |
| `simonmichael/hledger` | Wariant w Haskellu, dobra dokumentacja modelu |
| `tigerbeetle/tigerbeetle` | Baza transakcyjna do podwójnego zapisu. Wymusza reguły na poziomie bazy — konto nie może zejść poniżej zera |
| `formancehq/ledger` | Ledger jako usługa, multi-currency, n:n |
| `hamsterbase/ledger-ts` | Księga jako kod TypeScript |
| `LedgerSMB/LedgerSMB` | Pełna księgowość ERP, dojrzały model planu kont |

## 12. Bank i płatności (4)

| Repo | Po co |
|---|---|
| `WoLpH/mt940` | **Parser wyciągów MT940** — format, w którym polskie banki oddają historię. Podstawa automatycznego rozliczania płatności |
| `nordigen/nordigen-python` | Dostęp do rachunków przez PSD2 (GoCardless Bank Account Data) |
| `csingley/ofxtools` | Format OFX, gdy bank tak eksportuje |
| `plaid/plaid-python` | Agregacja bankowa, głównie US — na przyszłość |

## 13. Pieniądze, waluty, daty (5)

| Repo | Po co |
|---|---|
| `python-babel/babel` | Formatowanie kwot i dat per locale |
| `limist/py-moneyed` | Typ Money — kwota nierozerwalnie z walutą. Zapobiega dodaniu EUR do USD |
| `dinerojs/dinero.js` | To samo po stronie frontendu |
| `sdispater/pendulum` | Daty i strefy czasowe bez bólu — ETD/ETA w różnych portach |
| `fawazahmed0/exchange-api` | Darmowe kursy jako backup dla NBP |

## 14. Frontend (18)

| Repo | Po co |
|---|---|
| `refinedev/refine` | Framework paneli CRUD — miesiące oszczędności przy ERP |
| `TanStack/table` | Tabela z sortowaniem, filtrowaniem, wirtualizacją |
| `TanStack/query` | Cache stanu serwera |
| `TanStack/router` | Routing typowany |
| `TanStack/form` | Formularze — alternatywa dla react-hook-form |
| `TanStack/virtual` | Wirtualizacja list przy dziesiątkach tysięcy stawek |
| `glideapps/glide-data-grid` | Siatka jak Excel — ekran review ekstrakcji |
| `ag-grid/ag-grid` | Najbogatsza siatka danych, wersja community MIT |
| `shadcn-ui/ui` | Komponenty do skopiowania, dobrze generowane przez Cursor |
| `tailwindlabs/tailwindcss` | Style |
| `ant-design/ant-design` | Gęste komponenty pod ERP |
| `mui/material-ui` | Alternatywa z dojrzałym DataGrid |
| `react-hook-form/react-hook-form` | Formularz oferty z 40+ polami |
| `colinhacks/zod` | Walidacja, wspólny schemat z backendem |
| `clauderic/dnd-kit` | Przeciąganie pozycji na ofercie, kolejność opłat |
| `recharts/recharts` | Wykresy: marża w czasie, trend frachtu |
| `date-fns/date-fns` | Operacje na datach |
| `vitejs/vite` | Build |

## 15. Mapy i trasowanie (7)

| Repo | Po co |
|---|---|
| `maplibre/maplibre-gl-js` | Mapa bez licencji Mapboxa — pozycje kontenerów |
| `Leaflet/Leaflet` | Prostsza mapa, gdy nie potrzeba WebGL |
| `openlayers/openlayers` | Zaawansowane warstwy geo |
| `visgl/deck.gl` | Wizualizacja tras i wolumenów |
| `Project-OSRM/osrm-backend` | Routing drogowy — dowóz i odwóz |
| `valhalla/valhalla` | Routing z profilami ciężarowymi |
| `graphhopper/graphhopper` | Routing + optymalizacja tras |

## 16. Generowanie dokumentów (8)

| Repo | Po co |
|---|---|
| `typst/typst` | Szablony oferty, B/L, CMR. Szybki, czytelna składnia |
| `Kozea/WeasyPrint` | HTML+CSS → PDF |
| `foliojs/pdfkit` | Generowanie programistyczne |
| `open-xml-templating/docxtemplater` | Szablony Word z podstawianiem danych |
| `python-openxml/python-docx` | Dokumenty Word z Pythona |
| `scanny/python-pptx` | Prezentacje — oferty handlowe, raporty dla klienta |
| `jgm/pandoc` | Konwersja między wszystkim |
| `carbone-io/carbone` | Szablony w LibreOffice → PDF/DOCX/XLSX |

## 17. Workflow i orkiestracja (9)

| Repo | Po co |
|---|---|
| `pytransitions/transitions` | Maszyna stanów dla statusu zlecenia |
| `temporalio/temporal` | Trwałe workflow z retry i historią |
| `temporalio/sdk-python` | SDK Python |
| `PrefectHQ/prefect` | Orkiestracja pipeline'ów danych |
| `dagster-io/dagster` | Pipeline'y z katalogiem zasobów danych |
| `apache/airflow` | Klasyk — cięższy, ale wszystko ma |
| `windmill-labs/windmill` | Skrypty + UI + cron |
| `n8n-io/n8n` | Integracje low-code, szybkie prototypy |
| `camunda/camunda-bpm-platform` | BPMN, gdyby workflow miał być konfigurowany przez użytkownika |

## 18. Wyszukiwanie i dopasowywanie (6)

| Repo | Po co |
|---|---|
| `rapidfuzz/RapidFuzz` | Fuzzy matching nazw opłat i portów |
| `seatgeek/thefuzz` | Prostsze API |
| `dedupeio/dedupe` | Deduplikacja kontrahentów — ten sam agent pod trzema nazwami |
| `meilisearch/meilisearch` | Wyszukiwarka odporna na literówki |
| `typesense/typesense` | Alternatywa, lżejsza |
| `opensearch-project/OpenSearch` | Gdy dojdą logi i analityka |

## 19. Uwierzytelnianie i uprawnienia (7)

| Repo | Po co |
|---|---|
| `keycloak/keycloak` | IdP, SSO, role — gotowe |
| `ory/kratos` | Zarządzanie tożsamością, lżejsze |
| `ory/keto` | Uprawnienia w modelu Zanzibar |
| `openfga/openfga` | To samo, prostsze wdrożenie. **Uprawnienia typu „handlowiec widzi tylko swoich klientów"** |
| `casbin/casbin` | RBAC/ABAC jako biblioteka |
| `authelia/authelia` | Brama uwierzytelniająca przed aplikacją |
| `logto-io/logto` | Nowocześniejsza alternatywa dla Keycloaka |

## 20. Infrastruktura i obserwowalność (12)

| Repo | Po co |
|---|---|
| `minio/minio` | Storage S3 na cenniki źródłowe i dokumenty |
| `getsentry/sentry` | Błędy produkcyjne |
| `redis/redis` | Cache, broker, sesje |
| `grafana/grafana` | Dashboardy operacyjne |
| `prometheus/prometheus` | Metryki |
| `open-telemetry/opentelemetry-python` | Tracing przez cały pipeline |
| `traefik/traefik` | Reverse proxy z auto-TLS |
| `caddyserver/caddy` | Prostsza alternatywa |
| `docker/compose` | Środowisko lokalne |
| `coollabsio/coolify` | Self-hosted PaaS — deploy bez DevOpsa |
| `netdata/netdata` | Monitoring serwera |
| `restic/restic` | Backupy plików i dokumentów |

## 21. Testy i jakość (7)

| Repo | Po co |
|---|---|
| `schemathesis/schemathesis` | Testuje API na podstawie OpenAPI — znajduje błędy, których nie napiszesz |
| `testcontainers/testcontainers-python` | Testy na prawdziwym Postgresie w kontenerze |
| `microsoft/playwright` | Testy E2E ścieżki oferta → zlecenie |
| `locustio/locust` | Testy obciążeniowe |
| `pre-commit/pre-commit` | Hooki — lint i format przed commitem |
| `tox-dev/tox` | Macierz środowisk |
| `nektos/act` | Uruchamianie GitHub Actions lokalnie |

## 22. Bezpieczeństwo i dane osobowe (5)

| Repo | Po co |
|---|---|
| `microsoft/presidio` | **Wykrywanie i anonimizacja danych osobowych.** Wysyłasz cenniki do LLM — warto wiedzieć, co w nich jest |
| `pyca/cryptography` | Szyfrowanie, podpisy, certyfikaty do KSeF |
| `trufflesecurity/trufflehog` | Wykrywanie sekretów w repo — Cursor lubi wkleić klucz API |
| `aquasecurity/trivy` | Skan podatności obrazów |
| `bitwarden/server` | Zarządzanie sekretami zespołu |

## 23. Praca z AI przy kodzie (7)

| Repo | Po co |
|---|---|
| `anthropics/claude-code` | Agent w terminalu — do zadań wieloplikowych, których Cursor nie ogarnia |
| `PatrickJS/awesome-cursorrules` | Gotowe `.cursorrules` per stack. Skopiuj i dostosuj — bardzo poprawia jakość generowania |
| `github/spec-kit` | Development sterowany specyfikacją. Twoje pliki spec'a jako źródło prawdy dla agenta |
| `cline/cline` | Agent w VS Code, alternatywa |
| `aider-AI/aider` | Agent CLI z dobrą obsługą gita |
| `continuedev/continue` | Autouzupełnianie i chat we własnym IDE |
| `Aider-AI/aider-composio`* | *(sprawdź aktualność — ekosystem agentów zmienia się co miesiąc)* |

---

## Co faktycznie instalujesz w pierwszym miesiącu

Reszta katalogu to mapa. To jest lista zakupów:

**Szkielet:** `full-stack-fastapi-template`, `sqlalchemy`, `alembic`, `pydantic`, `uv`, `ruff`, `mypy`, `pytest`, `hypothesis`

**Dane:** `improved-un-locodes`, `datasets/currency-codes`, `pgvector`

**Pieniądze:** `py-moneyed`, `babel`, `pendulum`

**Ekstrakcja:** `docling`, `marker`, `pdfplumber`, `calamine`, `instructor`, `langfuse`, `promptfoo`

**Poczta:** `emailengine`

**Frontend:** `refine`, `TanStack/table`, `glide-data-grid`, `shadcn-ui`, `zod`

**Dokumenty:** `typst`

**Infra:** `minio`, `redis`, `sentry`

To 30 pozycji. Wystarczy na fazy 1–3.

## Trzy rzeczy, które warto przeczytać, a nie instalować

1. **`beancount/beancount`** — model podwójnego zapisu. Godzina lektury oszczędzi ci decyzji o pisaniu własnej księgowości.
2. **`frappe/frappe`** — jak zrobić metadanowy system uprawnień i pól własnych, żeby każdy klient nie wymagał deploya.
3. **`tigerbeetle/tigerbeetle`** — dlaczego reguły finansowe powinny być wymuszane przez bazę, a nie przez kod aplikacji. To zmieni ci projekt tabeli `charge`.

## Czego wciąż nie ma

Silnika stawek morskich. Po przeszukaniu tagów `freight-forwarding`, `freight-management`, `logistics` i `edifact` — nie istnieje open-source'owy system obsługujący FCL/LCL z pełnym zestawem dopłat, terminami ważności i rozwiązywaniem kolizji cenników. Tabele `rate_sheet`, `rate_line` i `charge_code` piszesz sam. To jest jedyna część tego ERP, która jest naprawdę twoja.
