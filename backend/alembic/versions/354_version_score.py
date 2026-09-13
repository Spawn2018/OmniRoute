"""version_score view: mean MAE/CRPS per model_version

Revision ID: 354_version_score
Revises: 353_interval_score
Create Date: 2026-09-13

AI2.1. Postgres liczy srednie. Bez przelaczania modelu. Bez osi czasu.
"""
from collections.abc import Sequence

from alembic import op

revision: str = "354_version_score"
down_revision: str | None = "353_interval_score"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_VIEW = """
CREATE VIEW version_score
WITH (security_invoker = true) AS
SELECT
  i.organization_id,
  s.model_version,
  count(*)::bigint AS pair_count,
  round(avg(i.mae), 4) AS avg_mae,
  round(avg(i.crps), 4) AS avg_crps
FROM interval_score i
INNER JOIN suggestion_ledger s
  ON s.organization_id = i.organization_id
 AND s.id = i.suggestion_id
GROUP BY i.organization_id, s.model_version
"""


def upgrade() -> None:
    op.execute(_VIEW)


def downgrade() -> None:
    op.execute("DROP VIEW IF EXISTS version_score")
