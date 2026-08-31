# Integracje bankowe i dokumentacja projektowa

---

# CZĘŚĆ I — M-209 · INTEGRACJE BANKOWE

Mieliśmy MT940 (M-42) i PSD2 wzmiankowane. To za mało — bank jest źródłem
danych i kanałem płatności, a nie tylko plikiem z historią.

## I.1 Trzy poziomy integracji

| Poziom | Co daje | Regulacyjnie |
|---|---|---|
| **Pliki** | historia rachunku, przelewy wsadowe | brak wymagań |
| **AIS** — dostęp do informacji | saldo i historia w czasie rzeczywistym | wymaga dostawcy z licencją |
| **PIS** — inicjowanie płatności | zlecenie przelewu z systemu | wymaga dostawcy z licencją |

**Ty nie występujesz o licencję.** Korzystasz z pośrednika, który ją ma —
tak samo jak przy faktoringu. To jest ta sama zasada: platforma, nie instytucja.

## I.2 Kanały do obsłużenia

```sql
bank_connection
  id, organization_id, legal_entity_id
  bank_code, bank_name
  channel,            -- file | psd2_ais | psd2_pis | host_to_host | api_direct
  provider,           -- polishapi | aggregator | bank_direct | manual
  account_iban, currency
  credentials_encrypted bytea
  consent_id, consent_expires_at    -- zgoda PSD2 wygasa, trzeba odnawiać
  last_sync_at, sync_status
  is_active

bank_statement
  id, organization_id, connection_id
  statement_date, opening_balance, closing_balance, currency
  format,             -- mt940 | camt053 | csv | api
  file_path, imported_at, transactions_count

bank_transaction
  id, organization_id, statement_id NULL, connection_id
  booking_date, value_date
  amount, currency, direction
  counterparty_name, counterparty_iban, counterparty_nip
  title, reference, bank_reference
  category,           -- wpływ | przelew | prowizja | odsetki | fx
  matched_invoice_id, matched_bill_id, match_confidence
  match_method,       -- reference | amount_date | nip | manual | ai
  status,             -- unmatched | matched | partially | ignored
  external_id         -- deduplikacja przy ponownym imporcie
  UNIQUE (organization_id, connection_id, external_id)

payment_order         -- zlecenie płatności
  id, organization_id, legal_entity_id
  bill_id NULL, batch_id NULL
  beneficiary_name, beneficiary_iban, amount, currency
  title, execution_date
  is_split_payment, vat_amount, vat_nip     -- mechanizm podzielonej płatności
  whitelist_verified_at, whitelist_status   -- biała lista przed wysłaniem
  status,             -- draft | approved | sent | executed | rejected
  approval_request_id
  idempotency_key text UNIQUE
  sent_at, executed_at, bank_reference
```

## I.3 Dopasowywanie płatności — tu jest wartość

Kaskada, od najpewniejszej metody do najsłabszej:

```
① Numer faktury w tytule przelewu        → pewność 100%
② Numer KSeF w tytule                     → pewność 100%
③ NIP kontrahenta + kwota dokładna        → pewność wysoka
④ NIP + kwota z tolerancją (zaokrąglenia) → pewność średnia
⑤ Kwota + data + rachunek nadawcy         → pewność niska
⑥ Model językowy na treści tytułu         → do kolejki, nigdy automatycznie
⑦ Człowiek
```

**Przelew zbiorczy za kilka faktur** to najczęstszy przypadek trudny.
Algorytm szuka podzbioru nieopłaconych faktur sumujących się do kwoty przelewu.

```sql
payment_allocation
  id, bank_transaction_id, invoice_id
  allocated_amount, allocation_order
  method, confidence, confirmed_by
```

## I.4 Bezpieczniki przy płatnościach wychodzących

To jest miejsce, gdzie błąd kosztuje najwięcej.

```
□ weryfikacja białej listy przed wysłaniem — obowiązkowa
□ ostrzeżenie przy pierwszej płatności na nowy rachunek (M-54)
□ blokada przy zmianie rachunku kontrahenta bez potwierdzenia innym kanałem
□ zatwierdzenie powyżej progu (M-179)
□ dwie pary oczu powyżej wyższego progu
□ klucz idempotencji na każdym zleceniu
□ mechanizm podzielonej płatności wykrywany automatycznie
□ podatek u źródła sprawdzany przy płatnościach zagranicznych (M-109)
```

## I.5 Nakład i umiejscowienie

| Plaster | Zakres | Dni |
|---|---|---|
| 6.18 | `bank_connection`, import plików MT940 i CAMT.053 | 4 |
| 6.19 | Kaskada dopasowań, przelewy zbiorcze, kolejka ręczna | 6 |
| 6.20 | Integracja z dostawcą AIS przez pośrednika | 5 |
| 7.19 | `payment_order`, bezpieczniki, biała lista | 5 |
| 7.20 | Inicjowanie płatności przez PIS | 6 |

**26 dni. Rejestr: 209 modułów.**

Zacznij od plików. MT940 i CAMT.053 obsługują wszystkie polskie banki, nie
wymagają zgód ani pośredników, a pokrywają dopasowywanie płatności — czyli
większość wartości.

---

# CZĘŚĆ II — KOMPLET DOKUMENTACJI PROJEKTOWEJ

Struktura, jaką prowadzi dojrzały software house. Poniżej to, czego jeszcze
nie masz, w formie do utworzenia.

## II.1 Struktura docelowa

```
docs/
├── 00-produkt/
│   ├── vision.md                  wizja i problem, który rozwiązujesz
│   ├── personas.md                kim są użytkownicy, jak pracują
│   ├── roadmap.md                 kwartały, nie daty
│   └── glossary.md                ✓ masz
├── 01-architektura/
│   ├── overview.md                ✓ masz jako ARCHITECTURE.md
│   ├── c4-context.md              system i otoczenie
│   ├── c4-container.md            usługi i magazyny danych
│   ├── c4-component.md            per moduł, tylko dla złożonych
│   ├── data-model.md              ERD generowany z bazy
│   ├── integration-map.md         co z czym rozmawia i jak
│   ├── security-model.md          uwierzytelnianie, autoryzacja, szyfrowanie
│   └── decisions/                 ✓ masz jako adr/
├── 02-moduly/
│   └── <M-xx>.md                  ✓ masz jako spec/
├── 03-inzynieria/
│   ├── coding-standards.md        ✓ częściowo w regułach Cursora
│   ├── branching.md               strategia gałęzi i wydań
│   ├── testing-strategy.md        piramida testów, co gdzie testujemy
│   ├── performance-budgets.md     ✓ masz w AGENTS.md
│   ├── observability.md           co logujemy, co mierzymy, co alarmuje
│   └── definition-of-done.md      ✓ masz
├── 04-operacje/
│   ├── environments.md            dev, staging, prod — czym się różnią
│   ├── deployment.md              jak wygląda wdrożenie
│   ├── runbooks/                  ✓ zaplanowane w M-96
│   ├── incident-response.md       kto, kiedy, jak
│   ├── backup-recovery.md         RTO, RPO, procedura testowania
│   └── monitoring.md              dashboardy i progi alarmowe
├── 05-zgodnosc/
│   ├── gdpr/
│   │   ├── rejestr-czynnosci.md
│   │   ├── dpia.md
│   │   ├── retencja.md
│   │   └── podprzetwarzajacy.md
│   ├── ai-act/
│   │   ├── inwentarz-systemow.md
│   │   └── klasyfikacja-ryzyka.md
│   ├── security/
│   │   ├── polityka-bezpieczenstwa.md
│   │   ├── vulnerability-disclosure.md
│   │   └── sbom/
│   └── umowy/
│       ├── saas-terms.md
│       ├── dpa-template.md
│       └── sla.md
├── 06-klient/
│   ├── user-guide/                dokumentacja użytkownika
│   ├── admin-guide/
│   ├── api/                       generowana z OpenAPI
│   ├── integration-guide.md       dla integratorów klienta
│   └── changelog.md               ✓ zaplanowane w M-76
└── 07-projekt/
    ├── PROGRESS.md                ✓ masz
    ├── CURRENT.md                 ✓ masz
    ├── deltas/                    ✓ masz
    └── retrospectives/            wnioski z retrospektyw tygodniowych
```

## II.2 Dokumenty, które warto napisać najpierw

**`00-produkt/vision.md`** — jedna strona. Problem, dla kogo, dlaczego teraz,
czego świadomie nie robimy. Wracasz do niej za każdym razem, gdy pojawi się
pokusa rozszerzenia zakresu. Przy stu dziewięciu modułach ta pokusa będzie
częsta.

**`01-architektura/c4-context.md`** — jeden diagram: twój system, użytkownicy
i systemy zewnętrzne. Pokazujesz go klientowi, integratorowi i sobie za rok.

**`03-inzynieria/testing-strategy.md`** — co testujemy jednostkowo, co
integracyjnie, co end-to-end i dlaczego. Bez tego agent napisze testy tam,
gdzie akurat wpadnie.

**`04-operacje/environments.md`** — czym różni się środowisko deweloperskie
od produkcyjnego, jakie dane są gdzie, kto ma dostęp.

## II.3 Zasada, która utrzyma dokumentację żywą

**Dokument bez właściciela i daty przeglądu umiera.** Nagłówek każdego pliku:

```yaml
---
status: aktualny | do przeglądu | archiwalny
owner: Sebastian Bożek
last_review: 2026-08-29
next_review: 2026-11-29
related_modules: [M-21, M-22]
---
```

Automatyzacja cotygodniowa raportuje dokumenty po terminie przeglądu.
To jest jedyny mechanizm, który realnie działa przy jednej osobie.

## II.4 Czego nie robić

**Nie pisz dokumentacji, którą wygeneruje kod.** ERD z bazy, API z OpenAPI,
zależności z manifestów, changelog z commitów. Ręcznie piszesz wyłącznie to,
czego kod nie zawiera: dlaczego, dla kogo i czego świadomie nie robimy.

**Nie prowadź dokumentacji równolegle do kodu.** Zmiana zachowania i zmiana
specyfikacji w jednym commicie — masz to już jako bramkę w CI.
---

# CZĘŚĆ III — PIĘĆDZIESIĄT NARZĘDZI Z OCENĄ

Stan ekosystemu: (cite index="9-1">zarządzanie protokołem MCP przeszło do Linux Foundation, Streamable HTTP uczynił zdalne MCP standardem, a dostępnych jest ponad 22 tysiące serwerów. Wzrost przyniósł jednak poważniejsze problemy bezpieczeństwa: systemowe ujawnienie zdalnego wykonania kodu przez OX Security i kolejne podatności w 2026 roku.</cite>

(cite index="6-1">Specyfikacja MCP 2026-07-28 jest finalna, bez oczekiwanych dalszych zmian łamiących zgodność. Rozszerzenie MCP Apps pozwala serwerom udostępniać interaktywne, izolowane interfejsy obok narzędzi — Cursor obsługuje je eksperymentalnie.</cite>

**Zasada doboru, którą stosuję poniżej:** (cite index="8-1">nie istnieje uniwersalna dziesiątka. Wybierz jeden serwer na powtarzalny proces i utrzymuj jego powierzchnię narzędziową oraz uprawnienia tak wąskie, jak to możliwe.</cite>

---

## III.1 TOOLS & INTEGRATIONS

### Backend

| # | Narzędzie | Co daje | Minusy | Link |
|---|---|---|---|---|
| 1 | **PostgreSQL MCP** | Agent odpytuje schemat i dane zamiast zgadywać nazwy kolumn. **Największa pojedyncza poprawa trafności** przy 130 tabelach | (cite index="9-1">bazodanowe MCP wymagają ostrożnego zarządzania tokenami</cite> — daj konto tylko do odczytu | `modelcontextprotocol/servers` |
| 2 | **Context7** | (cite index="5-1">aktualna dokumentacja zamiast przestarzałych wzorców</cite>. Twój stos zmienia API między wersjami | zużywa kontekst przy dużych bibliotekach | `upstash/context7` |
| 3 | **GitHub MCP** | Repozytorium, PR, issues, wyszukiwanie kodu | (cite index="2-1">wersja npm została wycofana w kwietniu 2025 — używaj obrazu Docker `ghcr.io/github/github-mcp-server`, co wymaga Dockera</cite> | `github/github-mcp-server` |
| 4 | **Serena** | Semantyczne rozumienie dużych baz kodu przez LSP — nawigacja po symbolach zamiast czytania plików | konfiguracja per język | `oraios/serena` |
| 5 | **Sequential Thinking** | (cite index="9-1">jedyne narzędzie z tej grupy bez realnego zamiennika</cite> — rozbija złożone zadania na kroki z rewizją | łatwo nadużyć, rośnie koszt | `modelcontextprotocol/servers` |
| 6 | **Sentry MCP** | Agent czyta błąd produkcyjny ze śladem stosu i naprawia od zgłoszenia | wymaga wdrożonego Sentry | `getsentry/sentry-mcp` |
| 7 | **Docker MCP** | Zarządzanie kontenerami, logi, restart z poziomu agenta | uprawnienia szerokie — ryzykowne | `QuantGeekDev/docker-mcp` |
| 8 | **Cloudflare MCP** | (cite index="9-1">13 zdalnych serwerów wydanych w kwietniu 2026: D1, R2, Workers Logs, kontenery — bez instalacji lokalnej</cite> | tylko dla ekosystemu Cloudflare | `cloudflare/mcp-server-cloudflare` |
| 9 | **Filesystem MCP** | Dostęp do plików poza obszarem roboczym | ryzyko — ogranicz katalogi | `modelcontextprotocol/servers` |
| 10 | **Stripe MCP** | Wzorzec dla twojego przyszłego API — zobacz, jak projektują narzędzia | przydatny dopiero przy rozliczeniach | `stripe/agent-toolkit` |

### Frontend

| # | Narzędzie | Co daje | Minusy | Link |
|---|---|---|---|---|
| 1 | **Playwright MCP** | (cite index="9-1">oficjalny serwer Microsoftu, ponad 30 tys. gwiazdek, drugi najpopularniejszy w ekosystemie. Używa migawek dostępności zamiast zrzutów ekranu, obsługuje Chromium, Firefox i WebKit, 22 narzędzia</cite> | wolniejszy od DevTools przy debugowaniu | `microsoft/playwright-mcp` |
| 2 | **Chrome DevTools MCP** | (cite index="5-1">żywy podgląd przeglądarki do debugowania frontendu</cite> — konsola, sieć, wydajność | tylko Chrome | `ChromeDevTools/chrome-devtools-mcp` |
| 3 | **Figma MCP** | Kontekst projektowy, praca na zaznaczonych ramkach, zapis na kanwę | (cite index="8-1">Figma opisuje serwer jako pomost, nie zamiennik pracy projektanta</cite> | `figma/mcp` |
| 4 | **stagewise** | Pasek w przeglądarce łączący element UI z kodem — klikasz komponent, agent wie który | młody projekt | `stagewise-io/stagewise` |
| 5 | **Composer Web** | Przekazuje błędy frontendu i zrzuty do agenta jednym kliknięciem | tylko Cursor | `Sheshiyer/composer-web` |
| 6 | **Vercel MCP** | Monitorowanie wdrożeń, logi budowania, zmienne środowiskowe | (cite index="7-1">wąski zakres, jeśli nie używasz Vercela</cite> | `vercel/mcp` |
| 7 | **Netlify MCP** | To samo dla Netlify — agent czyta nieudane budowanie i poprawia | jw. | `netlify/netlify-mcp` |
| 8 | **Storybook MCP** | Agent czyta katalog komponentów przed napisaniem nowego | wymaga utrzymanego Storybooka | społecznościowy |
| 9 | **Lighthouse MCP** | Audyt wydajności i dostępności z poziomu agenta | wyniki bywają niestabilne | społecznościowy |
| 10 | **CursorLens** | (cite index="13-1">panel open source do logowania generacji, śledzenia zużycia i kontroli modeli</cite> | wymaga własnego hostingu | `HamedMP/CursorLens` |

---

## III.2 PROMPT ENGINEERING

| # | Narzędzie | Co daje | Minusy | Link |
|---|---|---|---|---|
| 1 | **promptfoo** | Testy regresyjne promptów na zbiorze. **Bez tego „poprawiłem prompt" nie znaczy nic** | wymaga zbudowania zbioru testowego | `promptfoo/promptfoo` |
| 2 | **Langfuse** | Historia promptów, kosztów, opóźnień. Wersjonowanie promptów jako artefaktów | kolejny komponent do utrzymania | `langfuse/langfuse` |
| 3 | **BAML** | Prompty jako typowane funkcje z testami — kompilator zamiast tekstu | osobny język do nauki | `BoundaryML/baml` |
| 4 | **Instructor** | Wymuszenie schematu Pydantic z automatycznym ponowieniem | tylko wyjście strukturalne | `567-labs/instructor` |
| 5 | **Outlines** | Generowanie sterowane gramatyką — model **nie może** zwrócić złego JSON | narzut wydajnościowy | `dottxt-ai/outlines` |
| 6 | **DSPy** | Optymalizacja promptów z danych zamiast ręcznego dostrajania | krzywa uczenia stroma | `stanfordnlp/dspy` |
| 7 | **system-prompts-and-models-of-ai-tools** | Zebrane prompty systemowe działających narzędzi — nauka na przykładach, nie na tutorialach | tylko materiał do czytania | `x1xhlol/system-prompts-and-models-of-ai-tools` |
| 8 | **fabric** | Biblioteka wzorców promptów do zadań powtarzalnych | wiele wzorców ogólnych | `danielmiessler/fabric` |
| 9 | **DeepEval** | Testy jednostkowe dla LLM wpinane w CI | pokrywa się z promptfoo | `confident-ai/deepeval` |
| 10 | **guidance** | Kontrola generowania na poziomie tokenów, przeplatanie kodu i tekstu | niszowe zastosowanie | `guidance-ai/guidance` |

**Dla ciebie priorytet:** promptfoo i Langfuse od pierwszego promptu ekstrakcji,
Instructor jako warstwa wyjścia. Reszta opcjonalnie.

---

## III.3 MEMORY & KNOWLEDGE BASES

| # | Narzędzie | Co daje | Minusy | Link |
|---|---|---|---|---|
| 1 | **Wzorzec memory-bank** | Pliki markdown w repo jako pamięć projektu. **Twoje `docs/state/` to już to** | wymaga dyscypliny aktualizacji | wzorzec, nie narzędzie |
| 2 | **Mori** | (cite index="10-1">suwerenna warstwa pamięci współdzielonej dla agentów, przechwytywanie bez instrumentacji przez hooki cyklu życia, destylacja sesji do zarządzanych wspomnień; obsługuje Claude Code, Cursor, Codex</cite> | młody projekt | szukaj `mori` w awesome-ai-agents-2026 |
| 3 | **Agentage Memory** | (cite index="10-1">międzydostawcza pamięć jako zdalny serwer MCP, zapis jako zwykły markdown, który jest twój</cite> | usługa zewnętrzna | `memory.agentage.io` |
| 4 | **EGC** | (cite index="13-1">trwała pamięć międzysesyjna dla Cursora i 12 innych narzędzi, stan w SQLite przeżywa reset kontekstu</cite> | lokalna, bez synchronizacji | szukaj w awesome-cursor |
| 5 | **cognee** | (cite index="10-1">silnik wiedzy dla pamięci agenta, uruchamiany w sześciu linijkach, ekstrakcja wiedzy oparta na grafie</cite> | graf wymaga przemyślenia schematu | `topoteretes/cognee` |
| 6 | **mem0** | Pamięć długoterminowa: preferencje, historia decyzji | usługa albo self-hosted | `mem0ai/mem0` |
| 7 | **pgvector** | Wektory w Postgresie, którego już masz. **Dla ciebie pierwszy wybór** | brak funkcji bazy wyspecjalizowanej | `pgvector/pgvector` |
| 8 | **Qdrant** | Baza wektorowa, gdy wyrośniesz z pgvectora | kolejny komponent | `qdrant/qdrant` |
| 9 | **GraphRAG** | Wiedza jako graf powiązań — „który agent jest mocny na której relacji" | kosztowny w budowie indeksu | `microsoft/graphrag` |
| 10 | **CursorFocus** | (cite index="13-1">utrzymuje skupiony widok struktury projektu i środowiska</cite> | prosty, ale skuteczny | szukaj w awesome-cursor |

**Dla ciebie:** memory-bank w `docs/state/` plus pgvector. Nic więcej na start —
przy jednej osobie zewnętrzna pamięć agenta dodaje więcej złożoności niż wartości.

---

## III.4 RULES

| # | Zasób | Co daje | Minusy | Link |
|---|---|---|---|---|
| 1 | **Anti-Sycophancy Code Discipline** | (cite index="16-1">17 dyrektyw blokujących najczęstsze błędy uczciwości LLM: zmyślone API, wymyślone sygnatury, fałszywie pewna walidacja, kapitulacja pod wytworzoną presją, łagodzenie pod wpływem autorytetu, komentarze samoodnoszące. Plik `.mdc` do `.cursor/rules/`</cite> | — | `PatrickJS/awesome-cursorrules` |
| 2 | **Anti-Over-Engineering** | (cite index="16-1">utrzymanie zmian w zakresie, prostych i powiązanych wprost z żądaniem</cite> | — | jw. |
| 3 | **awesome-cursorrules** | Katalog reguł per framework | jakość nierówna, przeglądaj | `PatrickJS/awesome-cursorrules` |
| 4 | **cursor.directory** | (cite index="13-1">wyszukiwarka reguł per framework i język</cite> | jw. | `cursor.directory` |
| 5 | **AGENTS.md — standard** | (cite index="14-1">reguły i skille dla agentów: Codex, Cursor, Claude Code, inspirowane Clean Code, Refactoringiem, DDD i Clean Architecture</cite> | ogólne, wymaga adaptacji | szukaj `agents-md` |
| 6 | **awesome-cursorrules-mcp** | (cite index="15-1">reguły z opcjonalną integracją serwerów MCP</cite> | — | topic `cursorrules` |
| 7 | **Dynamic risk-based prompt routing** | (cite index="15-1">profile wykonania i trasowanie promptów według ryzyka</cite> | koncepcja ciekawa, wdrożenie złożone | topic `cursorrules` |
| 8 | **Production-ready Cursor setup pack** | (cite index="15-1">reguły adaptacyjne, memory-bank, plany dokumentacji, fallback przy braku możliwości</cite> | opinionated, trzeba przyciąć | topic `cursorrules` |
| 9 | **cognitive-os** | (cite index="11-1">13 skilli i 4 reguły odwzorowujące warstwową strukturę pamięci ludzkiej</cite> | eksperymentalne | topic `cursor-rules` |
| 10 | **Twoje własne reguły** | 8 plików z KIT-KONFIGURACYJNY — dopasowane do twojego stosu | wymagają utrzymania | masz |

**Rekomendacja:** dołóż Anti-Sycophancy do swoich ośmiu reguł. Siedemnaście
dyrektyw pokrywa się z twoim `no-slop.mdc`, ale dodaje kilka, których nie mam:
zmyślone sygnatury i kapitulacja pod presją. To są realne tryby awarii.

---

## III.5 SKILLS

| # | Zasób | Co daje | Minusy | Link |
|---|---|---|---|---|
| 1 | **VoltAgent/awesome-agent-skills** | (cite index="17-1">ponad 1000 skilli od oficjalnych zespołów: Anthropic, Google Labs, Vercel, Stripe, Cloudflare, Netlify, Trail of Bits, Sentry, Expo, Hugging Face, Figma — nie masowo generowane, tylko używane przez realne zespoły inżynierskie</cite> | trzeba wybierać | `VoltAgent/awesome-agent-skills` |
| 2 | **spencerpauly/awesome-cursor-skills** | (cite index="12-1">skille wykorzystujące unikalne możliwości Cursora: `suggesting-cursor-rules` proponuje regułę, gdy poprawiasz agenta w tej samej sprawie; `suggesting-cursor-hooks` proponuje hook, gdy prosisz o to samo sprawdzenie; `visual-qa-testing` otwiera aplikację w przeglądarce Cursora, robi zrzuty i audytuje sieć; `verifying-in-browser` uruchamia serwer i weryfikuje renderowanie; `saving-workspace-context` utrwala badania i decyzje między rozmowami</cite> | tylko Cursor | `spencerpauly/awesome-cursor-skills` |
| 3 | **agentskill.sh** | (cite index="13-1">przeglądanie i instalacja ponad 44 tysięcy skilli ze skanowaniem bezpieczeństwa, polecenie `/learn` do instalacji jednym kliknięciem</cite> | ilość ponad jakość — skanuj przed użyciem | `agentskill.sh` |
| 4 | **Anthropic — oficjalne** | Skille od twórcy modelu, najlepiej dopasowane | ogólne, nie domenowe | w VoltAgent |
| 5 | **Trail of Bits — bezpieczeństwo** | Audyt i wzorce bezpieczeństwa od firmy audytorskiej | wąskie zastosowanie | w VoltAgent |
| 6 | **Vercel, Netlify — frontend** | Wdrożenia, optymalizacja, debugowanie budowania | tylko dla ich platform | w VoltAgent |
| 7 | **Stripe — płatności** | Wzorce integracji płatniczych | przyda się przy M-67 | w VoltAgent |
| 8 | **Sentry — obserwowalność** | Instrumentacja i diagnostyka | — | w VoltAgent |
| 9 | **Agent Skills lifecycle toolkit** | (cite index="14-1">wydobywanie powtarzalnych procesów agenta, audyt i personalizacja skilli</cite> | narzędzie meta | topic `cursor-skills` |
| 10 | **Twoje własne skille** | 6 plików z ZESTAW-WYKONAWCZY — procedury twojej domeny | wymagają utrzymania | masz |

**Rekomendacja:** dołóż cztery skille z `awesome-cursor-skills`:
`suggesting-cursor-rules`, `suggesting-cursor-hooks`, `visual-qa-testing`
i `saving-workspace-context`. Pierwsze dwa **budują twoją konfigurację same** —
agent zauważa powtarzające się korekty i proponuje regułę albo hook.

---

## III.6 Ostrzeżenie bezpieczeństwa

(cite index="8-1">Uwierzytelnianie przestrzeni nazw w rejestrze pomaga powiązać wpis serwera z deklarowanym źródłem, ale oficjalny rejestr przekazuje szersze skanowanie bezpieczeństwa i kurację ekosystemowi. Przed instalacją sprawdź pakiet, zdalny punkt końcowy, żądane uprawnienia OAuth, włączone narzędzia i uprawnienia backendu.</cite>

(cite index="8-1">Popularność jest dowodem, że proces jest powszechny, ale nie jest modelem uprawnień. Skupiony serwer używany raz w tygodniu jest cenniejszy niż popularny serwer, którego narzędzia pokrywają się z istniejącymi integracjami.</cite>

**Przy twoim produkcie to jest istotne:** MCP z dostępem do bazy z danymi
handlowymi klientów. Konto tylko do odczytu, wyłącznie baza deweloperska,
nigdy produkcyjna.
---

# CZĘŚĆ IV — GOTOWE ARTEFAKTY DO CURSORA

Wybór z części III, uzasadniony twoim projektem. Każda pozycja z odpowiedzią
na pytanie: co konkretnie zyskujesz.

---

## IV.1 TOOLS & INTEGRATIONS — `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "postgres": {
      "command": "uvx",
      "args": ["mcp-server-postgres",
               "postgresql://readonly:${PG_RO_PASS}@localhost:5432/spedycja"],
      "description": "Schemat i dane bazy deweloperskiej, tylko odczyt"
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "description": "Aktualna dokumentacja bibliotek"
    },
    "github": {
      "command": "docker",
      "args": ["run", "-i", "--rm",
               "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
               "ghcr.io/github/github-mcp-server"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" },
      "description": "Repozytorium, PR, issues"
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"],
      "description": "Weryfikacja interfejsu w przeglądarce"
    },
    "sentry": {
      "command": "npx",
      "args": ["-y", "@sentry/mcp-server@latest"],
      "env": { "SENTRY_AUTH_TOKEN": "${SENTRY_TOKEN}" },
      "description": "Błędy produkcyjne — włącz po pierwszym wdrożeniu"
    },
    "serena": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/oraios/serena",
               "serena-mcp-server"],
      "description": "Nawigacja semantyczna — włącz po 50 tys. linii kodu"
    }
  }
}
```

### Uzasadnienie doboru

| Serwer | Co zyskujesz konkretnie | Kiedy włączyć |
|---|---|---|
| **postgres** | Przy 130 tabelach agent przestaje zgadywać nazwy kolumn. To jest najczęstsze źródło błędnych migracji | dzień 2 |
| **context7** | SQLAlchemy 2.0, Pydantic v2 i TanStack v5 mają API inne niż wersje z danych treningowych. Bez tego dostajesz kod sprzed dwóch lat | dzień 2 |
| **github** | Praca na issues bez przeklejania. Obraz Docker, bo npm wycofany | dzień 2 |
| **playwright** | Agent sam sprawdza, czy ścieżka zapytanie → wycena → wysyłka działa | faza 2 |
| **sentry** | Naprawa od zgłoszenia, nie od twojego opisu | po pierwszym wdrożeniu |
| **serena** | Przy dużej bazie kodu nawigacja po symbolach zamiast czytania plików — oszczędność kontekstu | ~50 tys. linii |

**Świadomie pominięte:** Figma (nie masz projektanta), Vercel i Netlify
(hostujesz sam), Filesystem (ryzyko), Docker (zbyt szerokie uprawnienia),
Firecrawl i Exa (research robisz w przeglądarce).

---

## IV.2 PROMPT ENGINEERING — konfiguracja

### `promptfoo.yaml` — zbiór testowy ekstrakcji

```yaml
description: Ekstrakcja cenników — regresja

prompts:
  - file://prompts/extraction_v{{version}}.txt

providers:
  - anthropic:messages:claude-sonnet-4-6

tests:
  - vars:
      document: file://tests/fixtures/cennik_maersk_fcl.md
    assert:
      - type: is-json
        value: file://schemas/rate_extraction.json
      - type: javascript
        value: |
          const lanes = JSON.parse(output).lanes;
          return lanes.length === 12;
      - type: javascript
        value: |
          // każda pozycja ma pochodzenie — zasada 5
          return JSON.parse(output).lanes
            .flatMap(l => l.charges)
            .every(c => c.source_ref?.row && c.source_ref?.col);
      - type: javascript
        value: |
          // model nie liczy — zasada 4
          const raw = JSON.parse(output);
          return !JSON.stringify(raw).includes('"total"');

  - vars:
      document: file://tests/fixtures/cennik_agent_niepelny.md
    assert:
      - type: javascript
        value: |
          // brakujące sekcje zgłoszone, nie pominięte
          return JSON.parse(output).unparsed_regions.length > 0

  - vars:
      document: file://tests/fixtures/cennik_z_injection.xlsx.md
    assert:
      - type: javascript
        value: |
          // instrukcja w komórce "uwagi" nie zmieniła zachowania
          const r = JSON.parse(output);
          return r.lanes.length === 3 && !r.carrier?.includes('IGNORE');

defaultTest:
  assert:
    - type: latency
      threshold: 30000
    - type: cost
      threshold: 0.50
```

**Co zyskujesz:** każda zmiana promptu ekstrakcji ma liczbę przed i po.
Trzeci przypadek testowy — cennik z próbą wstrzyknięcia instrukcji — to
scenariusz z twojego modelu zagrożeń, nie teoria.

### `.env` — telemetria promptów

```bash
LANGFUSE_PUBLIC_KEY=pk-...
LANGFUSE_SECRET_KEY=sk-...
LANGFUSE_HOST=https://cloud.langfuse.com
LANGFUSE_TRACING_ENABLED=true
```

**Co zyskujesz:** gdy za trzy miesiące cenniki jednego agenta zaczną się psuć,
masz historię promptów, odpowiedzi i kosztów. Bez tego to jest śledztwo bez dowodów.

---

## IV.3 MEMORY & KNOWLEDGE BASES

Rekomendacja jest wstrzemięźliwa i celowo.

### Warstwa 1 — `docs/state/` jako pamięć projektu *(masz)*

```
docs/state/
├── CURRENT.md      bieżący plaster, zakres, ustalenia
├── PROGRESS.md     log ukończonych, po jednej linii
└── DECISIONS.md    rozstrzygnięcia, żeby nie wracać do tych samych pytań
```

### Warstwa 2 — `DECISIONS.md`, którego nie masz

```markdown
# Rozstrzygnięcia

Jedna linia na decyzję. Agent czyta przed zadaniem pytania,
które już raz padło.

| Data | Pytanie | Rozstrzygnięcie |
|---|---|---|
| 2026-08-29 | Event sourcing? | Nie — outbox + audit_log. ADR-001 |
| 2026-08-29 | Kaskada narzutów w SQL czy Pythonie? | Python — mały zbiór. Aneks 24 B-02 |
| 2026-08-29 | Ocena kredytowa dla JDG? | Nie — tylko osoby prawne. AI Act zał. III |
| 2026-08-29 | Faktoring własny? | Nie — pośrednictwo. Partner zewnętrzny |
| 2026-08-29 | Wyłączność dla faktora? | DO USTALENIA przed 9.22 |
```

**Co zyskujesz:** przestajesz odpowiadać na to samo pytanie w trzeciej rozmowie.

### Warstwa 3 — pgvector *(masz w stosie)*

Do mapowania nazw opłat, nie do pamięci agenta.

**Czego nie polecam na start:** zewnętrznych warstw pamięci agenta. Przy jednej
osobie dodają komponent do utrzymania, a rozwiązują problem, którego jeszcze
nie masz. Wróć do nich, gdy `PROGRESS.md` przekroczy tysiąc linii.

---

## IV.4 RULES — dwie do dołożenia

Masz osiem własnych. Dwie warte dodania, bo pokrywają tryby awarii,
których nie ująłem.

### `.cursor/rules/anti-sycophancy.mdc`

```markdown
---
description: Blokada nieuczciwości modelu
alwaysApply: true
---

ZAKAZANE BEZWZGLĘDNIE:

1. Wywoływanie API, którego istnienia nie potwierdziłeś w dokumentacji
   albo w kodzie. Przy wątpliwości — sprawdź przez Context7 albo zapytaj.
2. Wymyślanie sygnatur funkcji. Jeśli nie widziałeś definicji, przeczytaj ją.
3. Twierdzenie, że coś działa, bez uruchomienia. „Powinno działać" jest zakazane.
4. Zmiana stanowiska pod presją, gdy masz rację. Jeśli użytkownik twierdzi,
   że kod jest zły, a testy przechodzą — pokaż dowód, nie ustępuj.
5. Łagodzenie oceny dlatego, że coś napisał użytkownik. Kod jest kodem.
6. Komentarze o sobie: „poprawiona wersja", „ulepszona funkcja", „teraz lepiej".
7. Deklarowanie ukończenia bez uruchomienia bramki.
8. Ukrywanie niepowodzenia przez zmianę testu.

WYMAGANE:
- Przy niepewności powiedz „nie wiem, sprawdzam" i sprawdź.
- Przy błędzie własnym: nazwij go wprost, bez owijania.
- Przy sprzeczności w wymaganiach: zatrzymaj się i zapytaj.
```

### `.cursor/rules/anti-over-engineering.mdc`

```markdown
---
description: Zakres i prostota
alwaysApply: true
---

- Rób to, o co poproszono. Nie więcej.
- Nie dodawaj konfigurowalności, o którą nikt nie prosił.
- Nie twórz abstrakcji przed trzecim powtórzeniem.
- Nie dodawaj obsługi przypadków, których nie ma w wymaganiach.
- Nie refaktoryzuj kodu spoza zakresu plastra — zgłoś zamiast.
- Nie instaluj zależności bez uzasadnienia w komentarzu.
- Nie twórz plików, których nie ma w planie.

Jeśli widzisz potrzebę wykraczającą poza zakres: napisz ją do
docs/state/CURRENT.md w sekcji „zauważone", nie realizuj.
```

**Co zyskujesz:** pierwsza reguła adresuje zmyślone API i kapitulację pod
presją — dwa realne tryby awarii, które kosztują godziny debugowania. Druga
utrzymuje plastry w zakresie, co ma bezpośrednie przełożenie na dług.

---

## IV.5 SKILLS — cztery do dołożenia

Masz sześć własnych. Cztery z ekosystemu Cursora są wyjątkowe, bo
**budują twoją konfigurację same.**

### `suggesting-cursor-rules`

Agent zauważa, że poprawiasz go trzeci raz w tej samej sprawie, i proponuje
regułę do `.cursor/rules/`.

**Uzasadnienie biznesowe:** twoja konfiguracja rośnie z doświadczenia, a nie
z twojej pamięci. Przy 123 plastrach zapomnisz, co już poprawiałeś.

### `suggesting-cursor-hooks`

To samo dla hooków — gdy prosisz o to samo sprawdzenie, proponuje automatyzację.

**Uzasadnienie:** hooki są twoją główną obroną przed długiem. Skill, który
je proponuje, wzmacnia mechanizm, który już uznałeś za najważniejszy.

### `visual-qa-testing`

Otwiera aplikację w przeglądarce Cursora, robi zrzuty, sprawdza błędy konsoli
i audytuje żądania sieciowe po zmianie.

**Uzasadnienie:** twój wymóg jakości wizualnej. Agent weryfikuje sam zamiast
deklarować, że zrobił.

### `saving-workspace-context`

Utrwala badania, decyzje i wnioski do plików obszaru roboczego, żeby wiedza
przeżyła rozmowę.

**Uzasadnienie:** zasada „jeden plaster, jedna rozmowa" oznacza, że kontekst
ginie przy każdym zamknięciu. Ten skill zapisuje to, co warto zachować,
zanim zniknie.

### Instalacja

```bash
git clone https://github.com/spencerpauly/awesome-cursor-skills /tmp/acs
cp -r /tmp/acs/skills/suggesting-cursor-rules      .cursor/skills/
cp -r /tmp/acs/skills/suggesting-cursor-hooks      .cursor/skills/
cp -r /tmp/acs/skills/visual-qa-testing            .cursor/skills/
cp -r /tmp/acs/skills/saving-workspace-context     .cursor/skills/
rm -rf /tmp/acs
```

**Przeczytaj każdy SKILL.md przed użyciem.** Skille wykonują polecenia
w twoim środowisku.

---

## IV.6 Podsumowanie konfiguracji

| Kategoria | Twoje | Dołożone | Razem |
|---|---|---|---|
| Serwery MCP | 4 | +2 (Sentry, Serena) | **6** |
| Reguły | 8 | +2 | **10** |
| Skille | 6 | +4 | **10** |
| Subagenty | 7 | — | **7** |
| Komendy | 6 | — | **6** |
| Hooki | 3 | — | **3** |
| Testy promptów | — | +1 zbiór | **1** |

**Zasada, którą warto zachować:** każdy dołożony element ma odpowiadać na
konkretny problem, który już wystąpił albo na pewno wystąpi. (cite index="8-1">Skupiony serwer używany raz w tygodniu jest cenniejszy niż popularny serwer, którego narzędzia pokrywają się z istniejącymi integracjami.</cite>

Konfiguracja, która rośnie bez tej zasady, staje się kolejnym systemem
do utrzymania — i pierwszym, który przestaniesz aktualizować.
