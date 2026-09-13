"""plan_snapshot FK to shipment trip resource

Revision ID: 357_plan_snap_fk
Revises: 356_prediction_ledger_null
Create Date: 2026-09-13

AI4.0. ON DELETE RESTRICT. Nie CASCADE.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "357_plan_snap_fk"
down_revision: str | None = "356_prediction_ledger_null"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_unique_constraint("uq_trip_org_id", "trip", ["organization_id", "id"])
    op.execute(
        """
        DELETE FROM plan_snapshot ps
        WHERE NOT EXISTS (
            SELECT 1 FROM shipment s
            WHERE s.organization_id = ps.organization_id AND s.id = ps.shipment_id
        )
        OR NOT EXISTS (
            SELECT 1 FROM trip t
            WHERE t.organization_id = ps.organization_id AND t.id = ps.trip_id
        )
        OR NOT EXISTS (
            SELECT 1 FROM resource r
            WHERE r.organization_id = ps.organization_id AND r.id = ps.resource_id
        )
        """
    )
    op.create_foreign_key(
        "fk_plan_snapshot_shipment",
        "plan_snapshot",
        "shipment",
        ["organization_id", "shipment_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "fk_plan_snapshot_trip",
        "plan_snapshot",
        "trip",
        ["organization_id", "trip_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "fk_plan_snapshot_resource",
        "plan_snapshot",
        "resource",
        ["organization_id", "resource_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint("fk_plan_snapshot_resource", "plan_snapshot", type_="foreignkey")
    op.drop_constraint("fk_plan_snapshot_trip", "plan_snapshot", type_="foreignkey")
    op.drop_constraint("fk_plan_snapshot_shipment", "plan_snapshot", type_="foreignkey")
    op.drop_constraint("uq_trip_org_id", "trip", type_="unique")
