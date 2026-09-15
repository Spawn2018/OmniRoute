"""create shipper_round_mark catalog with RLS FORCE

Revision ID: 398_shipper_round_mark
Revises: 397_sales_lane_volume
Create Date: 2026-09-15

BR6.2 leftover HITL katalog rundy zaladowcy. Nie Alpega.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "398_shipper_round_mark"
down_revision: str | None = "397_sales_lane_volume"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "shipper_round_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("round_kind", sa.String(length=16), nullable=False),
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
            name="fk_shipper_round_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_shipper_round_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_shipper_round_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_shipper_round_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_shipper_round_mark_code",
        ),
        sa.CheckConstraint(
            "round_kind IN ('first', 'second', 'final', 'other')",
            name="ck_shipper_round_mark_kind",
        ),
    )
    op.create_index(
        "ix_shipper_round_mark_organization_id",
        "shipper_round_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE shipper_round_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE shipper_round_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY shipper_round_mark_tenant_isolation ON shipper_round_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS shipper_round_mark_tenant_isolation ON shipper_round_mark",
    )
    op.drop_index(
        "ix_shipper_round_mark_organization_id",
        table_name="shipper_round_mark",
    )
    op.drop_table("shipper_round_mark")
