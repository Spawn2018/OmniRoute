default: gate

agent-refs:
    python scripts/quality/check_agent_refs.py

gate:
    python scripts/quality/run_gate.py

# Lokalny `just gate` zbiera code-gate i meta-gate (E2) — nie przerywa po pierwszym.
# CI i tak ma dwa joby. Rozdział jobów w CI wynika z audytu runów #79-#88.

code-gate: check test-unit arch frontend-typecheck frontend-test dup perf frontend-e2e
    @echo "code-gate: check + test-unit + arch + frontend + dup + perf + e2e OK"

meta-gate: docs-check agent-refs agentlint craft-check craft-style quality-floor
    @echo "meta-gate: docs-check + agent-refs + agentlint + craft-check + craft-style + quality-floor OK"

hooks:
    git config core.hooksPath scripts/githooks
    -chmod +x scripts/githooks/pre-push scripts/githooks/pre-commit
    @echo "core.hooksPath = $(git config --get core.hooksPath)"
    @echo "pre-commit: czyste drzewo poza indeksem + agentlint gdy ruszasz kontrakt"
    @echo "pre-push odpala 'just gate'. Furtka awaryjna: git push --no-verify"

dev:
    docker compose up -d db
    @echo "API: cd backend && granian --interface asgi app.main:app --reload --host 0.0.0.0 --port 8000"

check:
    ruff check backend
    mypy backend/app

fix:
    ruff check --fix backend
    ruff format backend

test:
    pytest backend/tests -m "not integration" -q
    pytest backend/tests -m integration -q

# --cov-report=: bez tabeli per-plik w terminalu (megabajty na fail zawieszają PowerShell / Cursor).
# Próg 80% zostaje (--cov-fail-under). Pełny raport lokalnie: just test-unit-cov
test-unit:
    pytest backend/tests -m "not integration" -q --cov=app --cov-report= --cov-fail-under=80

test-unit-cov:
    pytest backend/tests -m "not integration" -q --cov=app --cov-report=term-missing:skip-covered --cov-fail-under=80

test-integration:
    pytest backend/tests -m integration -q

arch:
    lint-imports

perf:
    cd frontend && pnpm build
    python scripts/quality/check_initial_js_size.py frontend/dist

audit:
    python -m pip_audit --skip-editable --progress-spinner off .

migrate:
    cd backend && alembic upgrade head

migrate-down:
    cd backend && alembic downgrade -1 && alembic upgrade head

migration name:
    cd backend && alembic revision --autogenerate -m "{{name}}"

db-up:
    docker compose up -d db

db-test-init:
    docker compose exec -T db psql -U omniroute -d postgres -c "CREATE DATABASE omniroute_test;" || true

api-types:
    python scripts/export_openapi.py
    cd frontend && pnpm exec openapi-ts

frontend-dev:
    cd frontend && pnpm dev

frontend-build:
    cd frontend && pnpm install && pnpm typecheck && pnpm build

frontend-typecheck:
    cd frontend && pnpm typecheck

frontend-test:
    cd frontend && pnpm test

frontend-e2e:
    cd frontend && pnpm exec playwright test

docs:
    python scripts/quality/sync_os_status.py

docs-check:
    python scripts/quality/sync_os_status.py --check

complexity:
    ruff check --select C901 backend

dead:
    @echo "dead: stub, nie DoD (vulture)"

dup:
    cd frontend && pnpm exec jscpd ../backend/app ../frontend/src --min-lines 5 --threshold 3 --ignore "**/api/**,**/routeTree.gen.ts,**/node_modules/**"

agentlint:
    python scripts/quality/agentlint.py

craft-check:
    python scripts/quality/craft_close.py --check

craft-close:
    python scripts/quality/craft_close.py --write

craft-style:
    python scripts/quality/craft_style.py

quality-floor:
    python scripts/quality/quality_floor.py --check

promptfoo:
    pytest backend/tests/extraction/test_promptfoo_fixtures.py -q

new-module name:
    @echo "new-module {{name}}: stub, nie DoD — skill module-factory"
