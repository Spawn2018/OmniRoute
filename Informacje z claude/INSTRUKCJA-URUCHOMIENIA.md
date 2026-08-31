# Instrukcja uruchomienia — krok po kroku

Od pustego komputera do pierwszego zielonego plastra. Wykonuj po kolei.
Czas: około trzech dni roboczych.

---

# DZIEŃ 0 · KONTA I WNIOSKI

Zacznij od tego, co ma czas oczekiwania.

## 0.1 Wnioski z czasem oczekiwania (zrób pierwsze)

```
□ GUS BIR — wniosek o klucz do API REGON
    → regon.stat.gov.pl, zakładka API, formularz wniosku
    → czas: kilka dni roboczych
    → obejście na teraz: bigzbig/regonapi ma sandbox bez klucza

□ KSeF — środowisko testowe
    → ksef-test.mf.gov.pl, rejestracja podmiotu testowego

□ Portale deweloperskie armatorów (rejestracja samoobsługowa):
    → Hapag-Lloyd: api.hlag.com — zacznij od nich, mają API pokrycia
    → Maersk: developer.maersk.com
    → CMA CGM: api-portal.cma-cgm.com
```

## 0.2 Konta darmowe

```
□ GitHub — repozytorium prywatne
□ Cloudflare — domena, DNS, Tunnel
□ Oracle Cloud — REGION FRANKFURT (wybór nieodwracalny!)
    → instancja Ampere A1: 2 OCPU, 12 GB RAM, 200 GB
□ Neon — Postgres z gałęziowaniem per PR
□ Sentry, PostHog, Langfuse Cloud, Better Stack
□ Anthropic Console — klucz API do ekstrakcji
```

**Uwaga do Oracle:** region domowy przypisuje się raz i nie da się zmienić.
Frankfurt: dane w UE, dobra dostępność sprzętu Ampere.

## 0.3 Dwie rozmowy

```
□ H&H Logistics — konflikt interesów. Przed pierwszą umową, nie po.
□ Oszacowanie rynku na kartce — ile firm spełnia profil klienta
```

---

# DZIEŃ 1 · MASZYNA I REPOZYTORIUM

## 1.1 Narzędzia systemowe

```bash
# macOS
brew install just uv node pnpm docker trufflehog trivy k6 postgresql@16
brew install --cask cursor docker

# lub Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
npm i -g pnpm
# just, docker, trufflehog, trivy, k6 wg dokumentacji dystrybucji
```

## 1.2 Szkielet projektu

```bash
git clone https://github.com/fastapi/full-stack-fastapi-template spedycja
cd spedycja
rm -rf .git && git init
uv sync --all-extras
cd frontend && pnpm install && cd ..
```

## 1.3 Narzędzia deweloperskie

```bash
uv add --dev ruff mypy pytest pytest-cov pytest-asyncio hypothesis \
             testcontainers schemathesis import-linter vulture radon \
             sqlfluff py-spy memray granian

npm i -g jscpd knip @size-limit/preset-app
```

## 1.4 Struktura katalogów

```bash
mkdir -p \
  .cursor/{rules,skills,subagents,hooks,commands,plans} \
  docs/{spec,deltas/{open,archived},adr,state,_source} \
  backend/app/{api,services,repositories,models,domain,workflows,integrations} \
  frontend/src/{features,components/ui,lib,api} \
  scripts/quality tests/{patterns,perf}

echo "docs/_source/" > .cursorignore
echo "frontend/src/api/" >> .cursorignore
```

## 1.5 Pliki konfiguracyjne

Skopiuj z dokumentów, które już masz:

```
AGENTS.md                     ← z AGENTS-v2.md
justfile                      ← z KIT-KONFIGURACYJNY.md, sekcja 4
.importlinter                 ← z KIT, sekcja 3
.cursor/rules/*.mdc           ← z KIT, sekcja 2 (8 plików)
.cursor/hooks/*.py            ← z ZESTAW-WYKONAWCZY, część 3 (3 pliki)
.cursor/commands/*.md         ← z ZESTAW-WYKONAWCZY, część 1 (6 plików)
.cursor/skills/*/SKILL.md     ← z ZESTAW-WYKONAWCZY, część 2 (6 plików)
.cursor/subagents/*.md        ← z CURSOR-PELNE-WYKORZYSTANIE, sekcja 1.2
.cursor/settings.json         ← z ZESTAW-WYKONAWCZY, część 4
scripts/quality/*.py          ← z ZESTAW-WYKONAWCZY, część 5 (3 skrypty)
tests/patterns/*.py           ← z ZESTAW-WYKONAWCZY, część 6
.github/workflows/ci.yml      ← z KIT, sekcja 5
.github/pull_request_template.md ← z KIT, sekcja 6
```

```bash
chmod +x .cursor/hooks/*.py scripts/quality/*.py
```

## 1.6 Docker Compose

`docker-compose.yml`:

```yaml
services:
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_PASSWORD: dev
      POSTGRES_DB: spedycja
    ports: ["5432:5432"]
    volumes: ["pgdata:/var/lib/postgresql/data"]
    command: >
      postgres -c shared_preload_libraries=pg_stat_statements
               -c pg_stat_statements.track=all
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: dev
      MINIO_ROOT_PASSWORD: devdevdev
    ports: ["9000:9000", "9001:9001"]
  mailpit:
    image: axllent/mailpit
    ports: ["1025:1025", "8025:8025"]
  temporal:
    image: temporalio/auto-setup:latest
    environment:
      DB: postgres12
      POSTGRES_SEEDS: postgres
      POSTGRES_USER: postgres
      POSTGRES_PWD: dev
    ports: ["7233:7233"]
    depends_on: [postgres]
volumes: { pgdata: }
```

```bash
docker compose up -d
docker compose ps        # wszystko healthy?
```

## 1.7 Weryfikacja dnia pierwszego

```bash
just check    # przechodzi na pustym repo
just test     # przechodzi (brak testów to nie błąd)
just arch     # import-linter nie zgłasza naruszeń
```

```bash
git add -A && git commit -m "chore: szkielet projektu i konfiguracja"
git remote add origin <twoje-repo>
git push -u origin main
```

---

# DZIEŃ 2 · CURSOR

## 2.1 Instalacja i logowanie

```
1. Otwórz Cursor, zaloguj się
2. Otwórz katalog projektu
3. Settings → Rules → sprawdź, czy widzi AGENTS.md i .cursor/rules/
```

## 2.2 Serwery MCP

`.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "postgres": {
      "command": "uvx",
      "args": ["mcp-server-postgres",
               "postgresql://postgres:dev@localhost:5432/spedycja"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp"]
    }
  }
}
```

**Weryfikacja:** w czacie zapytaj *„jakie tabele są w bazie"*. Jeśli agent
odpowie bez czytania plików — MCP Postgres działa.

## 2.3 Hooki — test działania

```
1. Settings → Hooks → sprawdź, czy widzi trzy pliki
2. Poproś agenta: "utwórz plik test_hook.py z funkcją,
   która ma nieużywaną zmienną i except Exception"
3. Oczekiwany efekt: agent dostaje błąd z ruff i sam poprawia
4. Usuń plik testowy
```

Jeśli hook nie zadziałał: sprawdź `chmod +x`, ścieżkę w `settings.json`
i czy `ruff` jest w PATH widocznym dla Cursora.

## 2.4 Subagenty i tryby

```
1. Settings → Subagents → sprawdź, czy widzi sześć plików
2. W czacie napisz "/" — powinny pojawić się komendy własne
3. Test trybu: wybierz skill `nowy-plaster`, Opt+Enter → przypina jako tryb
```

## 2.5 Auto-review

```
Settings → Auto-review → włącz
Sprawdź, czy widzi allowlist z .cursor/settings.json
Test: poproś o "just check" — powinno wykonać się bez pytania o zgodę
Test: poproś o "git push" — powinno zapytać
```

## 2.6 Automatyzacje

```
1. cursor.com/automations/new
2. Utwórz „Strażnik bramki": wyzwalacz = PR otwarty/zmieniony,
   zadanie = uruchom `just gate`, skomentuj wynik
3. Utwórz „Raport jakości": wyzwalacz = cron piątek 16:00,
   zadanie = uruchom skrypty z scripts/quality/, opublikuj raport
4. WAŻNE: przy automatyzacjach dotykających ekstrakcji (M-20)
   wyłącz pamięci
5. Włącz BugBot na repozytorium
```

## 2.7 Model

```
Settings → Models
  Domyślny: Auto (nie zużywa puli kredytów)
  Do planowania i refaktoryzacji: model czołowy
  Subagenty: Composer
```

---

# DZIEŃ 3 · DOKUMENTACJA I PIERWSZY PLASTER

## 3.1 Materiał źródłowy

```bash
cp ~/Downloads/SPEC-master.md ~/Downloads/ANEKS-*.md \
   ~/Downloads/REJESTR-MODULOW-I-PLAN-v2.md docs/_source/
```

## 3.2 Kompilacja specyfikacji

**Użyj Claude Code, nie Cursora** — to zadanie przez całe repo.

```bash
claude
```

Wklej polecenie z `ZESTAW-WYKONAWCZY.md`, część 7.2. Rób **partiami po 5–8
modułów**, nie całość naraz.

Po każdej partii:

```bash
wc -l docs/spec/*.md | sort -rn | head      # żaden > 400 linii
grep -c "DO USTALENIA" docs/spec/*.md        # przejrzyj każdą pozycję
```

Weź trzy reguły biznesowe z losowego pliku i sprawdź w źródle, czy liczby się
zgadzają. Jeśli choć jedna nie — powtórz partię.

## 3.3 Dokumenty własne

Napisz sam, ze szkieletów w `ZESTAW-WYKONAWCZY.md`, część 8:

```
□ docs/GLOSSARY.md       — rejestr nazw, zapobiega dryfowi nazewnictwa
□ docs/ARCHITECTURE.md   — mapa dla agenta, żeby nie przeszukiwał repo
□ docs/MODULES.md        — skopiuj rejestr M-01…M-77
□ docs/adr/0001-rezygnacja-z-event-sourcingu.md
```

ADR-001 jest ważny: to świadoma decyzja z audytu, że zamiast pełnego event
sourcingu masz outbox plus audit log plus niemutowalne stawki.

## 3.4 Słownik opłat

Wypełnij `backend/app/seeds/charge_codes.yaml` — około 60 kodów w pięciu
grupach, aliasy w czterech językach. To jest praca na wieczór, z twojej wiedzy
branżowej, i zwraca się natychmiast w skuteczności mapowania.

## 3.5 Pierwszy plaster

```bash
/delta 0.3
```

Uzupełnij `docs/deltas/open/0.3.md`. Sprawdź listę gotowości
(`ZESTAW-WYKONAWCZY.md`, część 10).

```bash
git worktree add ../work-0.3 -b plaster/0.3
cd ../work-0.3
```

W Cursorze:

```
[przypnij tryb nowy-plaster: wybierz z / i Opt+Enter]

/goal Plaster 0.3 przechodzi `just gate` i spełnia kryteria
      z docs/deltas/open/0.3.md

/plaster
```

Dalej wg przykładu przerobionego w `ZESTAW-WYKONAWCZY.md`, część 12.

---

# LISTA KONTROLNA GOTOWOŚCI

Zanim uznasz konfigurację za skończoną:

```
INFRASTRUKTURA
□ docker compose ps — wszystkie usługi healthy
□ just check / test / arch — zielone na pustym repo
□ CI na GitHubie przechodzi
□ Neon podłączony, gałąź per PR działa

CURSOR
□ MCP Postgres odpowiada na pytanie o tabele
□ Context7 działa (zapytaj o aktualne API SQLAlchemy 2.0)
□ Hook po edycji zwraca błędy ruff do agenta
□ Hook przed commitem blokuje przy duplikacji
□ Komendy własne widoczne pod "/"
□ Subagenty widoczne w ustawieniach
□ Auto-review: `just check` bez pytania, `git push` z pytaniem
□ Automatyzacja „strażnik bramki" reaguje na PR
□ Pamięci wyłączone w automatyzacjach dotykających M-20

DOKUMENTACJA
□ docs/spec/ — 71+ plików, żaden powyżej 400 linii
□ GLOSSARY.md, ARCHITECTURE.md, MODULES.md napisane
□ ADR-001 zapisany
□ CURRENT.md wypełniony na plaster 0.3
□ docs/_source/ w .cursorignore

DANE
□ charge_codes.yaml — 60 kodów z aliasami
□ porty z improper-un-locodes zaseedowane
□ klucz GUS złożony (albo sandbox działa)
```

---

# CO ROBIĆ, GDY COŚ NIE DZIAŁA

| Objaw | Przyczyna | Naprawa |
|---|---|---|
| Hook nie uruchamia się | brak `chmod +x` albo zły shebang | `chmod +x .cursor/hooks/*.py` |
| Hook działa, agent ignoruje | zły format wyjścia | musi być JSON z kluczem `followup_message` |
| MCP Postgres nie widzi bazy | kontener nie wystartował | `docker compose ps`, sprawdź port 5432 |
| Agent czyta całe repo | brak `.cursorignore` albo reguły kontekstu | sprawdź `context.mdc` z `alwaysApply` |
| Oracle: „out of host capacity" | brak sprzętu Ampere w regionie | powtarzaj co kilka godzin, Frankfurt zwykle działa |
| `import-linter` nie znajduje pakietu | zły `root_package` | musi być `app`, nie `backend.app` |
| Testcontainers nie startuje | Docker bez uprawnień | dodaj użytkownika do grupy docker |

---

# PIERWSZY TYDZIEŃ — CO POWINNO POWSTAĆ

| Dzień | Efekt |
|---|---|
| 0 | konta założone, wnioski złożone, rozmowa z HHL odbyta |
| 1 | repozytorium z pełną konfiguracją, CI zielone |
| 2 | Cursor skonfigurowany, hooki i subagenty przetestowane |
| 3 | `docs/spec/` skompilowana, GLOSSARY i ARCHITECTURE napisane |
| 4 | plaster 0.3: wielodostępność z RLS i testem izolacji |
| 5 | plastry 0.4–0.5: audit log, outbox, idempotencja |

Po piątym dniu masz fundament, którego nie da się dorobić później, i pętlę,
którą powtarzasz sto dwa razy.
