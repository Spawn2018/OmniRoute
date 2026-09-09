"""create lane_pattern catalog with RLS FORCE

Revision ID: 125_lane_pattern
Revises: 124_tender_carbon_mark
Create Date: 2026-09-09

HITL corridor pattern: UN/LOCODE pair + source_ref. Nie km. Nie nakładanie.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "125_lane_pattern"
down_revision: str | None = "124_tender_carbon_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "lane_pattern",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
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
            name="fk_lane_pattern_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_lane_pattern_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "origin_unlocode",
            "destination_unlocode",
            name="uq_lane_pattern_org_pair",
        ),
        sa.CheckConstraint(
            "origin_unlocode <> destination_unlocode",
            name="ck_lane_pattern_ends_differ",
        ),
        sa.CheckConstraint(
            r"origin_unlocode ~ '^[A-Z]{2}[A-Z0-9]{3}$'",
            name="ck_lane_pattern_origin_unlocode",
        ),
        sa.CheckConstraint(
            r"destination_unlocode ~ '^[A-Z]{2}[A-Z0-9]{3}$'",
            name="ck_lane_pattern_dest_unlocode",
        ),
    )
    op.create_index("ix_lane_pattern_organization_id", "lane_pattern", ["organization_id"])
    op.create_index(
        "ix_lane_pattern_org_origin",
        "lane_pattern",
        ["organization_id", "origin_unlocode"],
    )
    op.execute("ALTER TABLE lane_pattern ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE lane_pattern FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY lane_pattern_tenant_isolation ON lane_pattern
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS lane_pattern_tenant_isolation ON lane_pattern")
    op.drop_index("ix_lane_pattern_org_origin", table_name="lane_pattern")
    op.drop_index("ix_lane_pattern_organization_id", table_name="lane_pattern")
    op.drop_table("lane_pattern")
