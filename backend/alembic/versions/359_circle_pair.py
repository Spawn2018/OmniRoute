"""circle_sim complementary pair view

Revision ID: 359_circle_pair
Revises: 358_cf_run_snap
Create Date: 2026-09-13

AI4.2. Para unload↔load w SQL. Nie generator 500k. Nie km.
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "359_circle_pair"
down_revision: str | None = "358_cf_run_snap"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_VIEW = """
CREATE VIEW circle_sim_pair
WITH (security_invoker = true) AS
SELECT
  a.organization_id,
  a.id AS left_sim_id,
  b.id AS right_sim_id,
  a.sim_code AS left_sim_code,
  b.sim_code AS right_sim_code,
  a.unload_unlocode,
  a.load_unlocode
FROM circle_sim a
INNER JOIN circle_sim b
  ON b.organization_id = a.organization_id
 AND b.load_unlocode = a.unload_unlocode
 AND b.unload_unlocode = a.load_unlocode
 AND a.id < b.id
"""


def upgrade() -> None:
    op.execute(sa.text(_VIEW))


def downgrade() -> None:
    op.execute(sa.text("DROP VIEW circle_sim_pair"))
