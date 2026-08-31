# 72 repozytoria GitHub pod budowę systemu wycen morskich + AI rate ingestion

Podzielone wg roli w projekcie. Kolumna „po co" mówi konkretnie, do czego to wetkniesz — nie czym to jest.

---

## A. Szkielet backendu (10)

| Repo | Po co |
|---|---|
| `fastapi/fastapi` | Rdzeń API. Automatyczny OpenAPI = Cursor generuje frontend z kontraktu |
| `fastapi/full-stack-fastapi-template` | Oficjalny szablon: FastAPI + SQLModel + JWT + Docker. Twój dzień zerowy |
| `sqlalchemy/sqlalchemy` | ORM. Wymagany dla `numeric`, transakcji i partial unique indexes |
| `sqlalchemy/alembic` | Migracje. Przy 30+ tabelach nie ruszaj bazy inaczej |
| `pydantic/pydantic` | Walidacja schematu ekstrakcji z LLM. To jest twój kontrakt z modelem |
| `fastapi/sqlmodel` | SQLAlchemy + Pydantic w jednym modelu. Mniej duplikacji przy CRUD |
| `celery/celery` | Kolejka pipeline'u ingestion. Parsowanie cennika to zadanie na minuty, nie na request |
| `rq/rq` | Lżejsza alternatywa dla Celery, jeśli nie chcesz brokera z pełnym Rabbitem |
| `hynek/structlog` | Logi strukturalne. Przy debugowaniu ekstrakcji będziesz je grepował po `rate_sheet_id` |
| `pytest-dev/pytest` | Testy reguł biznesowych — sekcja 6 spec'a |

## B. Baza danych (5)

| Repo | Po co |
|---|---|
| `pgvector/pgvector` | Embeddingi opisów opłat → mapowanie nieznanych nazw na `charge_code` |
| `supabase/supabase` | Gotowe RLS + auth + storage. Skrót do multi-tenancy, jeśli nie chcesz pisać sam |
| `kvesteri/sqlalchemy-continuum` | Wersjonowanie rekordów. Historia zmian stawek za darmo |
| `sqlfluff/sqlfluff` | Linter SQL. Cursor produkuje niespójny SQL, to go pilnuje |
| `djrobstep/migra` | Diff schematów Postgresa. Ratuje, gdy migracje się rozjadą |

## C. Dane referencyjne — porty, kraje, waluty (7)

| Repo | Po co |
|---|---|
| `datasets/un-locode` | **Podstawa tabeli `port`.** Oficjalny UN/LOCODE w czystym CSV, aktualizowany przy każdym wydaniu UNECE |
| `cristan/improved-un-locodes` | Ten sam zbiór, ale z poprawionymi współrzędnymi (98,7% pokrycia) i **670 tys. aliasów** nazw miast. Aliasy to gotowe wejście do normalizacji „Gdynia"/„Gdingen"/„GDN" → `PLGDY` |
| `geoapify/un-locode` | Biblioteka Node do query po UN/LOCODE, jeśli robisz część w JS |
| `marek5050/UN-LOCODE` | Prosty ekstrakt CSV — dobry do szybkiego seeda bazy |
| `SeaconLogistics/un_locode` | Gem Ruby, ale ma sensowny podział na funkcje lokalizacji (port / rail / airport / ICD) — skopiuj model |
| `tadziqusky/unlocode-ports` | Notebook wyciągający *same porty morskie* z pełnego zbioru. Oszczędza filtrowanie |
| `datasets/country-codes` | ISO 3166 + mapowania na waluty, strefy, ITU. Do formularzy kontrahenta |

## D. Referencje branżowe — co budowali inni (9)

| Repo | Po co |
|---|---|
| `loadpartner/tms` | Jedyny żywy open-source TMS dla brokerów (Laravel). Zobacz ich model `load` i `carrier` |
| `fleetbase/fleetbase` | Modułowa platforma logistyczna. Wartość: architektura rozszerzeń, nie kod |
| `frappe/erpnext` | Pełne ERP. Podpatrz model `Item`, `Party`, `Landed Cost Voucher` — mają dobrą abstrakcję kontrahenta |
| `odoo/odoo` | Moduł `stock` i `account` — wzorce, których nie wymyślisz sam |
| `dolibarr/dolibarr` | Prostszy niż Odoo, czytelniejszy kod. Dobry na model faktury i propozycji handlowej |
| `bigcapitalhq/bigcapital` | Open-source księgowość. Zobacz, jak robią podwójny zapis, zanim zdecydujesz, że nie piszesz swojego |
| `invoiceninja/invoiceninja` | Fakturowanie + multi-currency + szablony PDF. Kopalnia rozwiązań na wycenę→fakturę |
| `akaunting/akaunting` | Multi-company, multi-currency. Wzorzec izolacji danych między firmami |
| `openlmis/openlmis-ref-distro` | Logistyka mikroserwisowa. Zobacz, jeśli rozważasz podział na serwisy (nie rozważaj na tym etapie) |

## E. Parsowanie dokumentów — serce modułu AI (12)

| Repo | Po co |
|---|---|
| `docling-project/docling` | **Pierwszy wybór.** IBM, konwertuje PDF/XLSX/DOCX/PPTX na strukturę z zachowaniem tabel. Model wizyjny czyta stronę jako obraz — radzi sobie z tabelami bez ramek |
| `datalab-to/marker` | Alternatywa dla Doclinga: pipeline pięciu małych modeli zamiast jednego VLM, wyraźnie szybszy. Porównaj oba na swoich cennikach i wybierz po wynikach, nie po opisie |
| `Unstructured-IO/unstructured` | Zwraca **typowane elementy** (Title, Table, ListItem) zamiast płaskiego markdown. Przydatne, gdy cennik ma sekcje z uwagami między tabelami |
| `microsoft/markitdown` | Najlżejszy — wszystko na markdown. Dobry jako szybka ścieżka dla prostych plików, zanim odpalisz ciężką artylerię |
| `jsvine/pdfplumber` | Dostęp do współrzędnych każdego znaku. **Niezbędny do `source_ref`** — bez tego nie zbudujesz provenance |
| `pymupdf/PyMuPDF` | Najszybsza ekstrakcja tekstu i renderowanie stron do obrazów dla ścieżki wizyjnej |
| `camelot-dev/camelot` | Tabele z PDF-ów z liniami siatki. Cenniki linii żeglugowych często takie są |
| `opendataloader-project/opendataloader-pdf` | Audytuje własny output i wykrywa **po cichu pominięte fragmenty strony**. Dokładnie ten problem opisałem jako `unparsed_regions` |
| `genieincodebottle/parsemypdf` | Porównanie kilkunastu parserów na jednym zestawie. Zaoszczędzi ci tygodnia testów |
| `datalab-to/surya` | OCR + detekcja layoutu dla skanów. Cenniki od mniejszych agentów bywają skanem faksu |
| `tesseract-ocr/tesseract` | Klasyczny OCR jako fallback, offline, bez kosztu |
| `tafia/calamine` | Najszybszy czytnik XLSX (Rust, binding `python-calamine`). Przy setkach arkuszy różnica jest odczuwalna |

## F. LLM — ekstrakcja, kontrola, ewaluacja (10)

| Repo | Po co |
|---|---|
| `567-labs/instructor` | Wymusza schemat Pydantic na odpowiedzi modelu + retry przy błędzie walidacji. **To jest twoja warstwa ekstrakcji** |
| `dottxt-ai/outlines` | Generowanie sterowane gramatyką — model *nie może* zwrócić niepoprawnego JSON-a |
| `BoundaryML/baml` | Osobny język do definiowania promptów jako typowanych funkcji. Warte rozważenia, gdy promptów przybędzie |
| `anthropics/anthropic-sdk-python` | SDK. Structured outputs, batch API (tańszy przy masowym przetwarzaniu archiwum cenników) |
| `anthropics/claude-cookbooks` | Gotowe wzorce ekstrakcji z dokumentów i pracy z PDF-ami |
| `BerriAI/litellm` | Jeden interfejs do wielu dostawców + tracking kosztów per request. Będziesz chciał wiedzieć, ile kosztuje sparsowanie jednego cennika |
| `langfuse/langfuse` | Obserwowalność: każdy prompt, odpowiedź, koszt, latencja. **Bez tego nie zdiagnozujesz, czemu ekstrakcja się psuje na cennikach jednego agenta** |
| `promptfoo/promptfoo` | Testy regresyjne promptów. Zbierz 30 realnych cenników jako zestaw testowy i mierz accuracy przy każdej zmianie |
| `Arize-ai/phoenix` | Ewaluacja i śledzenie jakości ekstrakcji w czasie |
| `guardrails-ai/guardrails` | Walidatory na wyjściu modelu — zakresy kwot, formaty dat, wymagane pola |

## G. Ingestion maili (5)

| Repo | Po co |
|---|---|
| `postalsys/emailengine` | **IMAP → REST + webhooki.** Stawiasz raz, dostajesz POST-a przy każdym mailu na `rates@`. Oszczędza tygodnia babrania się w IMAP-ie |
| `ikvk/imap_tools` | Jeśli wolisz sam: najprzyjemniejszy klient IMAP w Pythonie, sensowna obsługa załączników |
| `SpamScope/mail-parser` | Parsowanie `.eml` i `.msg` — nagłówki, treść, załączniki, kodowania |
| `microsoftgraph/msgraph-sdk-python` | Gdy skrzynka jest na Microsoft 365 (u ciebie prawdopodobnie tak) |
| `docker-mailserver/docker-mailserver` | Własna skrzynka `rates@` w kontenerze, jeśli nie chcesz mieszać z firmową pocztą |

## H. Dopasowywanie tekstu — normalizacja nazw opłat (4)

| Repo | Po co |
|---|---|
| `rapidfuzz/RapidFuzz` | Fuzzy matching w C++. Pierwsza warstwa mapowania „TERMINAL HANDLING POL" → `OTHC` |
| `seatgeek/thefuzz` | Prostsze API, gdy wydajność nie gra roli |
| `meilisearch/meilisearch` | Wyszukiwarka odporna na literówki — po bazie stawek, kontrahentów, ofert |
| `typesense/typesense` | Alternatywa, lżejsza w utrzymaniu |

## I. Frontend (9)

| Repo | Po co |
|---|---|
| `refinedev/refine` | **Framework do paneli CRUD.** Generuje listy, formularze, filtry z definicji zasobu. Dla ERP oszczędza miesiące |
| `TanStack/table` | Tabela z sortowaniem, filtrowaniem, wirtualizacją. Baza stawek to dziesiątki tysięcy wierszy |
| `TanStack/query` | Cache i synchronizacja stanu serwera. Nie pisz tego ręcznie |
| `glideapps/glide-data-grid` | Siatka w stylu Excela, płynna przy 100 tys. wierszy. Idealna na **ekran review kolejki ekstrakcji** |
| `shadcn-ui/ui` | Komponenty do skopiowania, nie zależność. Cursor generuje pod nie bardzo dobrze |
| `tailwindlabs/tailwindcss` | Styl |
| `react-hook-form/react-hook-form` | Formularz oferty ma 40+ pól. Bez tego przemontowuje się przy każdym znaku |
| `colinhacks/zod` | Walidacja po stronie klienta, ten sam schemat co w Pydantic |
| `ant-design/ant-design` | Alternatywa dla shadcn: gęste komponenty pod dane, bliżej estetyki ERP |

## J. Generowanie dokumentów (4)

| Repo | Po co |
|---|---|
| `typst/typst` | **Szablony oferty i B/L.** Składnia znośna, output profesjonalny, kompilacja w milisekundach. Lepszy wybór niż LaTeX i niż HTML→PDF |
| `Kozea/WeasyPrint` | HTML+CSS → PDF, jeśli wolisz szablony webowe |
| `foliojs/pdfkit` | Generowanie programistyczne, gdy układ zależy od danych |
| `python-openxml/python-docx` | Część dokumentów spedycyjnych klienci chcą w Wordzie, nie w PDF |

## K. Workflow i orkiestracja (5)

| Repo | Po co |
|---|---|
| `pytransitions/transitions` | Maszyna stanów dla `shipment.status`. Wymusza legalne przejścia zamiast `if`-ów |
| `temporalio/temporal` | Trwałe workflow z retry i historią. Rozważ, gdy pipeline ingestion urośnie |
| `PrefectHQ/prefect` | Lżejsza orkiestracja pipeline'ów danych |
| `windmill-labs/windmill` | Skrypty + UI + cron w jednym. Dobre na zadania operacyjne wokół systemu |
| `n8n-io/n8n` | Integracje bez kodu — szybkie prototypy połączeń z zewnętrznymi API |

## L. Polska specyfika (8)

| Repo | Po co |
|---|---|
| `CIRFMF/ksef-api` | **Oficjalny przewodnik integracyjny Ministerstwa Finansów** po API KSeF 2.0. Zacznij tutaj |
| `smekcio/ksef-client-python` | SDK Python pod KSeF API v2 — klienci sync/async, sesje online i wsadowe, kryptografia RSA/ECDH/AES, XAdES, QR. Najbliżej gotowca dla twojego stacku |
| `ArturSkowronski/ksef-cli` | CLI: podajesz XML albo skan PDF, narzędzie robi resztę. Ma flagę `--json` i skill dla Claude Code — nadaje się do wpięcia w pipeline agentowy |
| `m32/ksef` | Skrypty Python do konfiguracji, autoryzacji i komunikacji z KSeF 2.0. Czytelne, dobre do nauki flow |
| `m32/ksef-pdf` | Wizualizacja faktury ustrukturyzowanej: XML → PDF z numerem KSeF i kodem QR. Klienci tego oczekują |
| `fakturownia/API` | Jeśli integrujesz zamiast pisać księgowość — API z obsługą KSeF i schemą FA(3) |
| `bigzbig/regonapi` | Klient REGON BIR1.1 w Pythonie. Autouzupełnianie kontrahenta po NIP/REGON/KRS, ma tryb sandbox bez klucza |
| `infirsoft/vat-whitelist-api` | Wrapper API białej listy (PHP, ale kontrakt czytelny). Weryfikacja rachunku kontrahenta przed przelewem |

## M. Infrastruktura i operacje (4)

| Repo | Po co |
|---|---|
| `minio/minio` | Storage S3-kompatybilny na cenniki źródłowe i dokumenty. Provenance wymaga trzymania oryginałów |
| `getsentry/sentry` | Błędy produkcyjne. Self-hosted, jeśli dane nie mogą wyjść |
| `redis/redis` | Cache kursów NBP, sesje, broker kolejki |
| `python-babel/babel` | Formatowanie kwot i dat per język. Oferta dla klienta z Chin wygląda inaczej niż dla polskiego |

---

## Co pobrać w pierwszej kolejności

Jeśli masz zacząć jutro, to w tej kolejności:

1. `fastapi/full-stack-fastapi-template` — szkielet, dzień pierwszy
2. `cristan/improved-un-locodes` — seed portów z aliasami, dzień drugi
3. `docling-project/docling` + `datalab-to/marker` — odpal oba na pięciu swoich realnych cennikach **zanim** zdecydujesz o architekturze ekstrakcji
4. `567-labs/instructor` — warstwa ekstrakcji
5. `langfuse/langfuse` — postaw od razu, nie „później". Bez telemetrii pipeline AI jest czarną skrzynką i debugowanie go kosztuje wielokrotnie więcej niż wdrożenie
6. `refinedev/refine` + `glideapps/glide-data-grid` — ekran review, czyli miejsce, gdzie faktycznie spędzisz czas jako użytkownik własnego systemu

## Czego na tej liście nie ma i dlaczego

**Silnika stawek morskich.** Nie istnieje w otwartym kodzie. Ani jednego projektu obsługującego FCL/LCL z pełnym zestawem dopłat, walidacją terminów ważności i rozwiązywaniem kolizji cenników. Tabele z sekcji 1.3 i 2 spec'a piszesz od zera — i to jest dokładnie ta część, której nie da się skopiować, więc i konkurencji nie da się jej skopiować od ciebie.
