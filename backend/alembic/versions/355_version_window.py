"""version_window view: mean MAE/CRPS per model_version and UTC day

Revision ID: 355_version_window
Revises: 354_version_score
Create Date: 2026-09-13

AI2.1 leftover. Srednie per dzien UTC z created_at. Bez detektora.
Bez przelaczania modelu.
"""
from collections.abc import Sequence

from alembic import op

revision: str = "355_version_window"
down_revision: str | None = "354_version_score"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_VIEW = """
CREATE VIEW version_window
WITH (security_invoker = true) AS
SELECT
  i.organization_id,
  s.model_version,
  (s.created_at AT TIME ZONE 'UTC')::date AS created_on,
  count(*)::bigint AS pair_count,
  round(avg(i.mae), 4) AS avg_mae,
  round(avg(i.crps), 4) AS avg_crps
FROM interval_score i
INNER JOIN suggestion_ledger s
  ON s.organization_id = i.organization_id
 AND s.id = i.suggestion_id
GROUP BY i.organization_id, s.model_version, (s.created_at AT TIME ZONE 'UTC')::date
"""


def upgrade() -> None:
    op.execute(_VIEW)


def downgrade() -> None:
    op.execute("DROP VIEW IF EXISTS version_window")
