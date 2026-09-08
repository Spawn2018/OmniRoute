"""create tender_lane catalog with RLS FORCE

Revision ID: 111_tender_lane
Revises: 110_tender_lot
Create Date: 2026-09-09

Korytarz partii przetargu. Nie runda. Nie kwota.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "111_tender_lane"
down_revision: str | None = "110_tender_lot"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "tender_lane",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tender_lot_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("origin_unlocode", sa.String(length=5), nullable=False),
        sa.Column("destination_unlocode", sa.String(length=5), nullable=False),
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
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
            name="fk_tender_lane_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "tender_lot_id"],
            ["tender_lot.organization_id", "tender_lot.id"],
            name="fk_tender_lane_lot",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_tender_lane_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "tender_lot_id",
            "origin_unlocode",
            "destination_unlocode",
            name="uq_tender_lane_org_lot_pair",
        ),
        sa.CheckConstraint(
            "origin_unlocode <> destination_unlocode",
            name="ck_tender_lane_ends_differ",
        ),
        sa.CheckConstraint(
            r"origin_unlocode ~ '^[A-Z]{2}[A-Z0-9]{3}$'",
            name="ck_tender_lane_origin_unlocode",
        ),
        sa.CheckConstraint(
            r"destination_unlocode ~ '^[A-Z]{2}[A-Z0-9]{3}$'",
            name="ck_tender_lane_dest_unlocode",
        ),
    )
    op.create_index("ix_tender_lane_organization_id", "tender_lane", ["organization_id"])
    op.create_index(
        "ix_tender_lane_org_lot",
        "tender_lane",
        ["organization_id", "tender_lot_id"],
    )
    op.execute("ALTER TABLE tender_lane ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE tender_lane FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY tender_lane_tenant_isolation ON tender_lane
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS tender_lane_tenant_isolation ON tender_lane")
    op.drop_index("ix_tender_lane_org_lot", table_name="tender_lane")
    op.drop_index("ix_tender_lane_organization_id", table_name="tender_lane")
    op.drop_table("tender_lane")
