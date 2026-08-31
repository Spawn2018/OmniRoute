default: gate

agent-refs:
    python scripts/quality/check_agent_refs.py

gate: agent-refs agentlint check test-unit arch frontend-typecheck frontend-test dup
    @echo "gate: agent-refs + agentlint + check + test-unit + arch + frontend + dup OK"

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

test-unit:
    pytest backend/tests -m "not integration" -q --cov=app --cov-fail-under=80

test-integration:
    pytest backend/tests -m integration -q

arch:
    lint-imports

perf:
    @echo "perf: stub, nie DoD (k6 / budżety p95)"

audit:
    @echo "audit: stub, nie DoD (pip-audit)"

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

docs:
    @echo "docs: stub, nie DoD"

complexity:
    ruff check --select C901 backend

dead:
    @echo "dead: stub, nie DoD (vulture)"

dup:
    cd frontend && pnpm exec jscpd ../backend/app ../frontend/src --min-lines 5 --threshold 3 --ignore "**/api/**,**/routeTree.gen.ts,**/node_modules/**"

agentlint:
    python scripts/quality/agentlint.py

promptfoo:
    pytest backend/tests/extraction/test_promptfoo_fixtures.py -q

new-module name:
    @echo "new-module {{name}}: stub, nie DoD — skill module-factory"
