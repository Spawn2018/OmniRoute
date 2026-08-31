# 103 repozytoria AI — warstwa, która robi z ERP system XXI wieku

Uzupełnienie poprzedniego katalogu. Razem: **334 pozycje**.

---

## Najpierw: co faktycznie czyni ten system nowoczesnym

Nie liczba bibliotek AI. Osiem zdolności, których nie ma żaden komercyjny system spedycyjny na polskim rynku:

1. **Automatyczna baza cen zakupowych** — cennik wpada mailem, po minucie jest w systemie *(opisane w poprzednim spec'u)*
2. **ERP jako serwer MCP** — Claude operuje twoim systemem: „wystaw ofertę dla Jurgi na Gdynia–Szanghaj, 2×40HC". Nie chatbot obok aplikacji, tylko aplikacja jako narzędzie agenta
3. **Copilot w interfejsie** — użytkownik pyta w oknie, dostaje wypełniony formularz
4. **Raporty bez pisania raportów** — text-to-SQL nad warstwą semantyczną: „marża na relacjach azjatyckich w Q2 vs Q1"
5. **Agent przeglądarkowy** — sam loguje się do portali linii i ściąga stawki spot
6. **Głos** — kierowca dzwoni, agent przyjmuje status i aktualizuje zlecenie
7. **Load planning** — algorytmiczna konsolidacja drobnicy, upakowanie kontenera
8. **Prognoza stawek** — sezonowość i trend na twoich własnych danych historycznych

Poniższe repozytoria mapują dokładnie te osiem.

---

## 1. MCP — twój ERP jako narzędzie agenta (13)

To jest najważniejsza sekcja w tym dokumencie. Jeśli wystawisz swoje API jako serwer MCP, dostajesz asystenta operacyjnego bez pisania asystenta.

| Repo | Po co |
|---|---|
| `modelcontextprotocol/python-sdk` | **Opakuj FastAPI w serwer MCP.** Kilkadziesiąt linii, a Claude umie wystawić ofertę i sprawdzić stawkę |
| `modelcontextprotocol/typescript-sdk` | To samo po stronie Node |
| `modelcontextprotocol/servers` | Oficjalne implementacje referencyjne — wzorce, jak projektować narzędzia |
| `modelcontextprotocol/registry` | Rejestr serwerów, coś w rodzaju sklepu z aplikacjami dla MCP |
| `modelcontextprotocol/inspector` | Debugger narzędzi MCP. Bez niego pisanie serwera to zgadywanie |
| `wong2/awesome-mcp-servers` | Katalog. **Ma m.in. serwer do polskiego KRS** — gotowa weryfikacja kontrahenta |
| `appcypher/awesome-mcp-servers` | Drugi katalog, inne pozycje |
| `korchasa/awesome-mcp` | Trzeci, z licznikami gwiazdek i językiem |
| `TensorBlock/awesome-mcp-servers` | Rejestr z podglądem konfiguracji instalacji dla Cursora i Claude Desktop |
| `mcp-finder/best-mcp-servers-2026` | Ranking wg niezawodności i aktywności utrzymania, nie wg gwiazdek |
| `metorial/mcp-containers` | Setki serwerów MCP w kontenerach — bezpieczne uruchamianie |
| `microsoft/playwright-mcp` | Agent steruje przeglądarką przez MCP |
| `QuantGeekDev/docker-mcp` | Zarządzanie kontenerami przez agenta |

## 2. Text-to-SQL i warstwa semantyczna (11)

Problem: użytkownik chce raportu, którego nie przewidziałeś. Rozwiązanie: nie przewidujesz raportów.

| Repo | Po co |
|---|---|
| `Canner/WrenAI` | **Text-to-SQL z warstwą semantyczną (MDL) i walidacją planu zapytania.** Agent nie zgaduje schematu — pyta o modele i metryki, które sam zdefiniowałeś. Kluczowe: wynik jest sprawdzalny, nie „prawdopodobny" |
| `cube-js/cube` | Warstwa semantyczna: definiujesz „marża", „rentowność relacji" raz, wszystkie narzędzia liczą tak samo |
| `tobymao/sqlglot` | **Parsowanie i walidacja SQL wygenerowanego przez model.** Bez tego wpuszczasz do bazy zapytanie, którego nikt nie sprawdził |
| `vanna-ai/vanna` | RAG nad schematem bazy — uczy się na twoich zapytaniach |
| `eosphoros-ai/DB-GPT` | Pełna platforma agentów nad bazą danych |
| `FalkorDB/QueryWeaver` | Text2SQL rozumiejący schemat jako graf — dobre przy wielu joinach |
| `defog-ai/sqlcoder` | Model wyspecjalizowany w SQL, uruchamialny lokalnie |
| `duckdb/duckdb` | Silnik analityczny w procesie. Raporty nad milionami wierszy bez hurtowni |
| `dbt-labs/dbt-core` | Transformacje jako kod — warstwa raportowa oddzielona od operacyjnej |
| `apache/superset` | Dashboardy dla użytkowników, którzy wolą klikać niż pytać |
| `metabase/metabase` | Prostsze BI, szybsze wdrożenie |

## 3. Agenci i automatyzacja (11)

| Repo | Po co |
|---|---|
| `browser-use/browser-use` | **Agent logujący się do portali linii żeglugowych i ściągający stawki spot.** Linie nie dają API małym spedytorom — to jest obejście |
| `Skyvern-AI/skyvern` | To samo, z naciskiem na formularze i powtarzalne procesy |
| `steel-dev/steel-browser` | Przeglądarka jako usługa dla agentów, z sesjami i proxy |
| `openai/openai-agents-python` | Lekki framework agentowy |
| `pydantic/pydantic-ai` | Agenci z typowanym wyjściem — spójny z twoim stackiem |
| `microsoft/autogen` | Wieloagentowe konwersacje |
| `crewAIInc/crewAI` | Agenci z rolami — np. „ekstraktor" + „weryfikator" + „normalizator" |
| `All-Hands-AI/OpenHands` | Agent piszący i uruchamiający kod |
| `SWE-agent/SWE-agent` | Agent naprawiający błędy w repozytorium |
| `geekan/MetaGPT` | Symulacja zespołu — ciekawe, mało praktyczne |
| `e2b-dev/E2B` | Sandbox do bezpiecznego wykonywania kodu generowanego przez agenta |

## 4. Głos i telefonia (5)

Spedycja to branża telefoniczna. Kierowca nie wypełni formularza, ale zadzwoni.

| Repo | Po co |
|---|---|
| `livekit/agents` | **Agent głosowy czasu rzeczywistego.** Kierowca dzwoni, podaje numer kontenera, system aktualizuje status |
| `pipecat-ai/pipecat` | Framework pipeline'ów głosowych, prostszy start |
| `openai/whisper` | Transkrypcja — nagrania rozmów z klientami jako źródło danych |
| `SYSTRAN/faster-whisper` | 4× szybszy, ta sama jakość. Dobra polszczyzna |
| `rhasspy/piper` | Synteza mowy offline, obsługuje polski |

## 5. Modele lokalne i kontrola kosztu (8)

| Repo | Po co |
|---|---|
| `ollama/ollama` | Modele lokalnie jednym poleceniem. Do zadań, których nie chcesz wysyłać na zewnątrz |
| `ggml-org/llama.cpp` | Inferencja na CPU — klasyfikacja maili nie potrzebuje GPU |
| `vllm-project/vllm` | Serwowanie z wysoką przepustowością, gdy przetwarzasz archiwum tysięcy cenników |
| `huggingface/text-generation-inference` | Alternatywa produkcyjna |
| `huggingface/transformers` | Baza wszystkiego |
| `unslothai/unsloth` | **Fine-tuning na twoich cennikach.** Po roku masz zbiór, którego nikt inny nie ma — mały dotrenowany model będzie tańszy i celniejszy niż ogólny |
| `axolotl-ai-cloud/axolotl` | Fine-tuning z konfiguracji YAML |
| `ggml-org/whisper.cpp` | Transkrypcja lokalnie |

## 6. RAG, pamięć, wiedza firmowa (10)

| Repo | Po co |
|---|---|
| `qdrant/qdrant` | Baza wektorowa — jeśli wyrośniesz z pgvectora |
| `chroma-core/chroma` | Najprostsza do prototypu |
| `weaviate/weaviate` | Hybrydowe wyszukiwanie: wektory + filtry |
| `infiniflow/ragflow` | RAG z naciskiem na dokumenty o złożonym układzie |
| `deepset-ai/haystack` | Dojrzały framework RAG |
| `microsoft/graphrag` | RAG po grafie powiązań — kto z kim, na jakiej relacji, po jakiej stawce |
| `mem0ai/mem0` | Pamięć długoterminowa agenta — preferencje klientów, historia negocjacji |
| `getzep/zep` | Alternatywa z pamięcią czasową |
| `Mintplex-Labs/anything-llm` | Gotowy interfejs do bazy wiedzy firmowej |
| `FlagOpen/FlagEmbedding` | **Embeddingi wielojęzyczne z dobrą polszczyzną.** Kluczowe do mapowania nazw opłat |

## 7. Document AI nowej generacji (7)

Uzupełnienie do Doclinga i Markera — modele wizyjne czytające dokument jak człowiek.

| Repo | Po co |
|---|---|
| `opendatalab/MinerU` | Bardzo dobry na PDF-y z gęstymi tabelami |
| `allenai/olmocr` | OCR oparty na modelu wizyjnym, otwarte wagi |
| `getomni-ai/zerox` | Strona → obraz → model wizyjny → markdown. Prosty i skuteczny na brzydkich skanach |
| `microsoft/table-transformer` | Wykrywanie struktury tabeli: wiersze, kolumny, komórki scalone |
| `huridocs/pdf-document-layout-analysis` | Analiza układu strony przed ekstrakcją |
| `Filimoa/open-parse` | Podział dokumentu z zachowaniem układu wizualnego |
| `docling-project/docling-serve` | Docling jako usługa HTTP — wpinasz w pipeline zamiast importować |

## 8. Zbiór testowy i anotacja (4)

Nie pominiesz tego, jeśli chcesz mierzyć skuteczność ekstrakcji.

| Repo | Po co |
|---|---|
| `HumanSignal/label-studio` | **Anotacja twoich cenników jako zbiór referencyjny.** Bez tego „95% skuteczności" jest liczbą wymyśloną |
| `doccano/doccano` | Lżejsza alternatywa do etykietowania tekstu |
| `iterative/dvc` | Wersjonowanie zbiorów testowych razem z kodem |
| `mlflow/mlflow` | Śledzenie eksperymentów — który prompt, który model, jaki wynik |

## 9. Ewaluacja i niezawodność (7)

| Repo | Po co |
|---|---|
| `confident-ai/deepeval` | Testy jednostkowe dla LLM. Wpinasz w CI — regresja ekstrakcji nie przejdzie do produkcji |
| `Giskard-AI/giskard` | Automatyczne wykrywanie słabych punktów modelu |
| `comet-ml/opik` | Śledzenie i ocena wywołań, open source |
| `traceloop/openllmetry` | OpenTelemetry dla LLM — spójne z resztą twojej obserwowalności |
| `helicone/helicone` | Proxy z logowaniem, cache i limitami kosztów |
| `truera/trulens` | Ewaluacja jakości odpowiedzi |
| `openai/evals` | Framework benchmarków |

## 10. Bezpieczeństwo warstwy AI (4)

| Repo | Po co |
|---|---|
| `protectai/llm-guard` | Filtrowanie wejścia i wyjścia. **Cennik od nieznanego agenta to niezaufane wejście** — może zawierać instrukcje dla modelu |
| `protectai/rebuff` | Wykrywanie prompt injection |
| `NVIDIA/NeMo-Guardrails` | Reguły, czego agent nie może zrobić — np. nie zatwierdza stawki bez człowieka |
| `leondz/garak` | Skaner podatności modelu, testy przeciwnika |

## 11. Interfejs z AI w środku (5)

| Repo | Po co |
|---|---|
| `CopilotKit/CopilotKit` | **Copilot wbudowany w aplikację React.** Użytkownik pisze „oferta dla Jurgi, Gdynia–Szanghaj, 2×40HC", formularz się wypełnia. To jest ta różnica, którą klient zobaczy w pierwszej minucie demo |
| `vercel/ai` | Streaming odpowiedzi i generatywne UI — komponenty budowane przez model |
| `assistant-ui/assistant-ui` | Gotowe komponenty czatu z narzędziami |
| `vercel/next.js` | Jeśli frontend miałby być w Next |
| `e2b-dev/E2B` | Wykonywanie kodu z interfejsu — np. ad-hoc analiza cennika |

## 12. Praca z Cursorem i agentami kodującymi (8)

| Repo | Po co |
|---|---|
| `github/spec-kit` | **Development sterowany specyfikacją.** Twoje pliki spec'a jako źródło prawdy dla agenta zamiast promptowania z pamięci. Przy projekcie tej wielkości to różnica między porządkiem a chaosem |
| `PatrickJS/awesome-cursorrules` | Gotowe `.cursorrules` per stack — wyraźnie poprawia jakość generowania |
| `x1xhlol/system-prompts-and-models-of-ai-tools` | Zebrane prompty systemowe narzędzi AI. Nauka inżynierii promptu na działających przykładach |
| `anthropics/claude-code` | Agent terminalowy do zadań wieloplikowych, których Cursor nie ogarnia |
| `anthropics/anthropic-quickstarts` | Działające szkielety aplikacji z Claude |
| `qodo-ai/pr-agent` | Automatyczny przegląd pull requestów. **Piszesz sam — nie masz kto cię sprawdzić. To jest twój recenzent** |
| `danielmiessler/fabric` | Biblioteka wzorców promptów do zadań powtarzalnych |
| `BuilderIO/micro-agent` | Agent piszący kod pod testy — najpierw test, potem implementacja |

## 13. Optymalizacja — AI, którego spedycja naprawdę potrzebuje (6)

Tu nie chodzi o LLM. Chodzi o algorytmy, które liczą lepiej niż człowiek i dają natychmiastowy zysk.

| Repo | Po co |
|---|---|
| `google/or-tools` | **Konsolidacja drobnicy, wybór wariantu przewozu, przydział zasobów.** Silnik, który powie ci, czy opłaca się doładować kontener |
| `skjolber/3d-bin-container-packing` | Upakowanie kontenera 3D — ile paczek wejdzie do 40HC i jak |
| `jerry800416/3D-bin-packing` | To samo w Pythonie, prostsze |
| `PyVRP/PyVRP` | Trasowanie z ograniczeniami — dowozy i odwozy |
| `TimefoldAI/timefold-solver` | Solver ograniczeń: harmonogramy, przydziały, okna czasowe |
| `coin-or/pulp` | Programowanie liniowe — optymalizacja wyboru dostawcy przy wielu ograniczeniach |

## 14. Prognozowanie (4)

| Repo | Po co |
|---|---|
| `Nixtla/statsforecast` | Prognoza stawek i wolumenów, metody klasyczne, bardzo szybkie |
| `Nixtla/neuralforecast` | Modele głębokie, gdy masz dużo historii |
| `unit8co/darts` | Jednolite API do wielu modeli — dobre do porównań |
| `facebook/prophet` | Sezonowość i trend, znośny bez wiedzy statystycznej |

---

## Kolejność wdrażania warstwy AI

Nie wszystko naraz. W tej kolejności każdy krok jest użyteczny sam z siebie:

**Krok 1 — po fazie 1 (ofertowanie):** `modelcontextprotocol/python-sdk`. Opakuj swoje API w serwer MCP. Kilka dni pracy, a dostajesz asystenta operacyjnego w Claude bez pisania interfejsu.

**Krok 2 — razem z pipeline'em ekstrakcji:** `label-studio` + `deepeval`. Zanim zaczniesz optymalizować skuteczność, musisz umieć ją zmierzyć.

**Krok 3 — po fazie 3 (pieniądze):** `Canner/WrenAI` + `tobymao/sqlglot`. Masz dane o marży — pozwól pytać o nie zdaniami. Sqlglot obowiązkowo: zapytanie od modelu bez walidacji nie idzie do bazy.

**Krok 4 — gdy będziesz miał klientów:** `CopilotKit`. To jest funkcja demonstracyjna. Sprzedaje system w pierwszej minucie pokazu.

**Krok 5 — gdy pipeline będzie stabilny:** `browser-use` do stawek spot z portali linii.

**Krok 6 — po roku danych:** `unsloth`. Dotrenowany mały model na twoich cennikach będzie tańszy i celniejszy od ogólnego. I nikt inny nie ma tego zbioru.

## Dwie rzeczy, których nie odkładaj

**`protectai/llm-guard`** — od pierwszego dnia pipeline'u. Przetwarzasz pliki od nieznanych nadawców i wysyłasz je do modelu. Prompt injection w komórce Excela to nie teoria: wystarczy, że jeden „agent" wpisze w polu uwag instrukcję, a twój ekstraktor zacznie zwracać stawki, których nie ma w cenniku.

**`qodo-ai/pr-agent`** — piszesz ten system sam. Nie ma kto cię sprawdzić. Automatyczny recenzent to jedyna warstwa kontroli, jaką będziesz miał między Cursorem a produkcją.
