"""counterfactual_run FK to plan_snapshot + replay view

Revision ID: 358_cf_run_snap
Revises: 357_plan_snap_fk
Create Date: 2026-09-13

AI4.1. ON DELETE RESTRICT. Nie CASCADE. Nie solver.
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "358_cf_run_snap"
down_revision: str | None = "357_plan_snap_fk"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_VIEW = """
CREATE VIEW what_if_replay
WITH (security_invoker = true) AS
SELECT
  r.organization_id,
  r.id AS run_id,
  r.run_code,
  r.baseline_label,
  r.levers_label,
  r.result_label,
  r.source_ref,
  s.id AS plan_snapshot_id,
  s.snapshot_code,
  s.shipment_id,
  s.trip_id,
  s.resource_id
FROM counterfactual_run r
INNER JOIN plan_snapshot s
  ON s.organization_id = r.organization_id
 AND s.id = r.plan_snapshot_id
"""


def upgrade() -> None:
    op.execute(sa.text("DELETE FROM counterfactual_run"))
    op.add_column(
        "counterfactual_run",
        sa.Column("plan_snapshot_id", postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.create_foreign_key(
        "fk_counterfactual_run_snapshot",
        "counterfactual_run",
        "plan_snapshot",
        ["organization_id", "plan_snapshot_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )
    op.execute(sa.text(_VIEW))


def downgrade() -> None:
    op.execute(sa.text("DROP VIEW what_if_replay"))
    op.drop_constraint(
        "fk_counterfactual_run_snapshot",
        "counterfactual_run",
        type_="foreignkey",
    )
    op.drop_column("counterfactual_run", "plan_snapshot_id")
