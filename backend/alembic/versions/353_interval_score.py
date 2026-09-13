"""interval_score view: MAE and uniform CRPS from ledger join

Revision ID: 353_interval_score
Revises: 352_outcome_ledger_kind_fk
Create Date: 2026-09-13

AI2.0. Postgres liczy. Python nie. Nie ledger predykcji.
MAE = abs(actual - srodek [low, high]).
CRPS = E|X-y| - w/6 dla X ~ Uniform[low, high]; low=high => abs(actual-low).
"""
from collections.abc import Sequence

from alembic import op

revision: str = "353_interval_score"
down_revision: str | None = "352_outcome_ledger_kind_fk"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_MAE = """
CREATE FUNCTION interval_mae(low numeric, high numeric, actual numeric)
RETURNS numeric
LANGUAGE sql
IMMUTABLE
STRICT
AS $$
  SELECT round(
    abs(actual - (least(low, high) + greatest(low, high)) / 2::numeric),
    4
  )
$$
"""

_CRPS = """
CREATE FUNCTION interval_crps(low numeric, high numeric, actual numeric)
RETURNS numeric
LANGUAGE sql
IMMUTABLE
STRICT
AS $$
  SELECT round(
    CASE
      WHEN least(low, high) = greatest(low, high) THEN abs(actual - low)
      ELSE
        (
          CASE
            WHEN actual < least(low, high) THEN
              (least(low, high) + greatest(low, high)) / 2::numeric - actual
            WHEN actual > greatest(low, high) THEN
              actual - (least(low, high) + greatest(low, high)) / 2::numeric
            ELSE
              (
                (actual - least(low, high)) * (actual - least(low, high))
                + (greatest(low, high) - actual) * (greatest(low, high) - actual)
              ) / (2::numeric * (greatest(low, high) - least(low, high)))
          END
        ) - (greatest(low, high) - least(low, high)) / 6::numeric
    END,
    4
  )
$$
"""

_VIEW = """
CREATE VIEW interval_score
WITH (security_invoker = true) AS
SELECT
  o.organization_id,
  o.id AS outcome_id,
  s.id AS suggestion_id,
  o.entity_id,
  s.interval_low,
  s.interval_high,
  o.actual_value,
  interval_mae(s.interval_low, s.interval_high, o.actual_value) AS mae,
  interval_crps(s.interval_low, s.interval_high, o.actual_value) AS crps
FROM outcome_ledger o
INNER JOIN suggestion_ledger s
  ON s.organization_id = o.organization_id
 AND s.id = o.suggestion_id
"""


def upgrade() -> None:
    op.execute(_MAE)
    op.execute(_CRPS)
    op.execute(_VIEW)


def downgrade() -> None:
    op.execute("DROP VIEW IF EXISTS interval_score")
    op.execute("DROP FUNCTION IF EXISTS interval_crps(numeric, numeric, numeric)")
    op.execute("DROP FUNCTION IF EXISTS interval_mae(numeric, numeric, numeric)")
