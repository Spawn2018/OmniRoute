default: check test

# --- codzienne (wymaga backend/frontend w Fazie B) ---
dev:
    @echo "Faza B: docker compose up -d && granian --interface asgi app.main:app --reload"

check:
    @echo "check: uruchom po Fazie B (ruff, mypy, eslint, tsc)"
    @test -d backend && ruff check backend || true
    @test -d backend && mypy backend/app || true

fix:
    @test -d backend && ruff check --fix backend && ruff format backend || true

test:
    @echo "test: uruchom po Fazie B (pytest, vitest)"
    @test -d backend && pytest -x backend/tests || true

arch:
    lint-imports

perf:
    @echo "perf: pytest -m perf (Faza B)"

audit:
    @echo "audit: pip-audit, pnpm audit (Faza B)"

# --- baza ---
migrate:
    alembic upgrade head

migrate-down:
    alembic downgrade -1 && alembic upgrade head

migration name:
    alembic revision --autogenerate -m "{{name}}"

# --- generowanie ---
api-types:
    @echo "api-types: Faza B"

docs:
    @echo "docs: Faza B"

# --- jakość ---
complexity:
    @test -d backend && ruff check --select C901 backend || true

dead:
    @test -d backend && vulture backend/app --min-confidence 80 || true

dup:
    jscpd backend/app frontend/src --min-lines 5 --threshold 3 || true

agent-refs:
    python scripts/quality/check_agent_refs.py

agentlint:
    @echo "agentlint: pip install agentlint && agentlint (opcjonalnie CI)"

# --- pełna bramka ---
gate: check test arch agent-refs
    @echo "gate: rozszerz o perf, migrate-down, docs w Fazie B"

new-module name:
    @echo "new-module {{name}}: generator w Fazie B — patrz skill module-factory"
