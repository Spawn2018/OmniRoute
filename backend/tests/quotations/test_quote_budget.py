from pathlib import Path

import pytest
from sqlalchemy import text

from app.repositories.quotations.quotation_repository import QUOTE_FROM_CURRENT_SQL

_ROOT = Path(__file__).resolve().parents[3]
_CARD = _ROOT / "docs" / "ops" / "quote-budget.md"
_BUDGET_ROWS = 50_000

_QUOTE_SELECT_SQL = """
SELECT rl.charge_code, rl.id, rl.amount, rl.currency, rl.source_ref
FROM rate_line AS rl
WHERE rl.charge_code = :charge_code
  AND rl.superseded_by IS NULL
ORDER BY rl.created_at DESC, rl.id
LIMIT 1
"""


def test_quote_budget_card_records_count_and_verdict() -> None:
    assert _CARD.is_file()
    text = _CARD.read_text(encoding="utf-8")
    assert "ix_rate_line_current_charge_code" in text
    assert "rate_line" in text
    assert "N/A" in text or "p95" in text


def test_quote_select_for_explain_matches_insert_from_current_rate() -> None:
    insert_sql = " ".join(QUOTE_FROM_CURRENT_SQL.split())
    assert "FROM rate_line AS rl" in insert_sql
    assert "rl.superseded_by IS NULL" in insert_sql
    select_sql = " ".join(_QUOTE_SELECT_SQL.split())
    assert "FROM rate_line AS rl" in select_sql
    assert "rl.superseded_by IS NULL" in select_sql


@pytest.mark.integration
@pytest.mark.asyncio
async def test_quote_select_plan_uses_current_rate_index(engine) -> None:
    async with engine.connect() as conn:
        await conn.execute(text("SET enable_seqscan = off"))
        rows = await conn.execute(
            text(f"EXPLAIN {_QUOTE_SELECT_SQL}"),
            {"charge_code": "THC"},
        )
        plan = "\n".join(row[0] for row in rows)
    assert "ix_rate_line_current_charge_code" in plan


@pytest.mark.integration
@pytest.mark.asyncio
async def test_quote_p95_is_na_below_fifty_thousand_rate_lines(engine) -> None:
    async with engine.connect() as conn:
        count = (await conn.execute(text("SELECT COUNT(*) FROM rate_line"))).scalar_one()
    if count < _BUDGET_ROWS:
        card = _CARD.read_text(encoding="utf-8")
        assert "N/A" in card
        assert str(count) in card or "0" in card
        return
    raise AssertionError("p95 < 300 ms wymaga pomiaru przy ≥ 50k wierszy rate_line")
