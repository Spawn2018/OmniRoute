"""SQL charge_sell_in_pln: sell × NBP mid, not Python

Revision ID: 492_charge_sell_in_pln
Revises: 491_task
Create Date: 2026-09-22

T7d. PLN bez kursu. Brak wiersza NBP = NULL (API 400 kurs).
Nie kolumna marży. Nie fx_rate_day w tym SELECT.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "492_charge_sell_in_pln"
down_revision: str | None = "491_task"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_FN = """
CREATE FUNCTION charge_sell_in_pln(p_charge_id uuid, p_on_date date)
RETURNS numeric
LANGUAGE sql
STABLE
AS $$
  SELECT round(
    CASE
      WHEN c.sell_currency = 'PLN' THEN c.sell_amount
      WHEN r.mid IS NULL THEN NULL
      ELSE c.sell_amount * r.mid
    END,
    4
  )
  FROM charge c
  LEFT JOIN nbp_rate r
    ON r.organization_id = c.organization_id
   AND r.currency = c.sell_currency
   AND r.rate_date = p_on_date
  WHERE c.id = p_charge_id
$$
"""


def upgrade() -> None:
    op.execute(_FN)


def downgrade() -> None:
    op.execute("DROP FUNCTION IF EXISTS charge_sell_in_pln(uuid, date)")
