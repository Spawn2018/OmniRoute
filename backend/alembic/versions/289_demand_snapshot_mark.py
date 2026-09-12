"""create demand_snapshot_mark catalog with RLS FORCE

Revision ID: 271_demand_snapshot_mark
Revises: 276_MQC_mark
Create Date: 2026-09-12

EXP3.13 HITL znacznik MQC jako dane. Nie live giełda. Nie auto-forecast.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "289_demand_snapshot_mark"
down_revision: str | None = "288_tender_decline_reason"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "demand_snapshot_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("snapshot_kind", sa.String(length=16), nullable=False),
        sa.Column("source_ref", sa.String(length=256), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("created_by", PGUUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
            name="fk_demand_snapshot_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_demand_snapshot_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_demand_snapshot_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_demand_snapshot_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_demand_snapshot_mark_code",
        ),
        sa.CheckConstraint(
            "snapshot_kind IN ('forecast', 'booking', 'actual', 'other')",
            name="ck_demand_snapshot_mark_snapshot_kind",
        ),
    )
    op.create_index(
        "ix_demand_snapshot_mark_organization_id",
        "demand_snapshot_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE demand_snapshot_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE demand_snapshot_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY demand_snapshot_mark_tenant_isolation ON demand_snapshot_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS demand_snapshot_mark_tenant_isolation ON demand_snapshot_mark",
    )
    op.drop_index(
        "ix_demand_snapshot_mark_organization_id",
        table_name="demand_snapshot_mark",
    )
    op.drop_table("demand_snapshot_mark")
