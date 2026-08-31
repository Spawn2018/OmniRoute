default: gate

# --- bootstrap (działa bez Fazy B) ---
# Pełne check/test/arch dopiero gdy istnieje pyproject.toml + narzędzia.

agent-refs:
    python scripts/quality/check_agent_refs.py

# Bramka CI: do Fazy B tylko to, co da się uruchomić bez ruff/mypy/pytest.
gate: agent-refs
    @echo "gate (bootstrap): agent-refs OK"
    @echo "Po Fazie B: gate rozszerzy się o check + test + arch + perf"

# --- Faza B+ (wymaga pyproject.toml / package.json) ---
dev:
    @echo "Faza B: docker compose up -d && granian --interface asgi app.main:app --reload"

check:
    @if [ ! -f pyproject.toml ]; then echo "check: pominięte (brak pyproject.toml — Faza B)"; exit 0; fi
    ruff check backend
    mypy backend/app

fix:
    @if [ ! -f pyproject.toml ]; then echo "fix: pominięte — Faza B"; exit 0; fi
    ruff check --fix backend
    ruff format backend

test:
    @if [ ! -f pyproject.toml ]; then echo "test: pominięte — Faza B"; exit 0; fi
    pytest -x backend/tests

arch:
    @if [ ! -f pyproject.toml ]; then echo "arch: pominięte — Faza B"; exit 0; fi
    lint-imports

perf:
    @echo "perf: pytest -m perf (Faza B)"

audit:
    @echo "audit: pip-audit, pnpm audit (Faza B)"

migrate:
    @if [ ! -f pyproject.toml ]; then echo "migrate: pominięte — Faza B"; exit 0; fi
    alembic upgrade head

migrate-down:
    @if [ ! -f pyproject.toml ]; then echo "migrate-down: pominięte — Faza B"; exit 0; fi
    alembic downgrade -1 && alembic upgrade head

migration name:
    alembic revision --autogenerate -m "{{name}}"

api-types:
    @echo "api-types: Faza B"

docs:
    @echo "docs: Faza B"

complexity:
    @if [ ! -f pyproject.toml ]; then echo "complexity: pominięte — Faza B"; exit 0; fi
    ruff check --select C901 backend

dead:
    @if [ ! -f pyproject.toml ]; then echo "dead: pominięte — Faza B"; exit 0; fi
    vulture backend/app --min-confidence 80

dup:
    @if [ ! -f pyproject.toml ]; then echo "dup: pominięte — Faza B"; exit 0; fi
    jscpd backend/app frontend/src --min-lines 5 --threshold 3

agentlint:
    @echo "agentlint: opcjonalnie w CI po Fazie B (pip install agentlint)"

new-module name:
    @echo "new-module {{name}}: generator w Fazie B — patrz skill module-factory"
