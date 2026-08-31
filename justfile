default: gate

agent-refs:
    python scripts/quality/check_agent_refs.py

gate: agent-refs check test-unit arch
    @echo "gate: agent-refs + check + test-unit + arch OK"

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
    pytest backend/tests -m "not integration" -q || true
    pytest backend/tests -m integration -q

test-unit:
    pytest backend/tests -m "not integration" -q

test-integration:
    pytest backend/tests -m integration -q

arch:
    lint-imports

perf:
    @echo "perf: pytest -m perf (Faza B+)"

audit:
    @echo "audit: pip-audit (Faza B+)"

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
    @echo "api-types: Faza B+ (openapi-ts)"

docs:
    @echo "docs: Faza B+"

complexity:
    ruff check --select C901 backend

dead:
    @echo "dead: vulture (Faza B+)"

dup:
    @echo "dup: jscpd (Faza B+)"

agentlint:
    @echo "agentlint: Faza D"

new-module name:
    @echo "new-module {{name}}: patrz skill module-factory"
