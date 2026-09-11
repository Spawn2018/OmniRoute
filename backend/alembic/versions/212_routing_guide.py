"""create routing_guide catalog with RLS FORCE

Revision ID: 212_routing_guide
Revises: 211_asn
Create Date: 2026-09-11

HITL przewodnik routingu jako dane. Nie 409. Nie shipment. Nie kwota.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "212_routing_guide"
down_revision: str | None = "211_asn"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "routing_guide",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("guide_code", sa.String(length=32), nullable=False),
        sa.Column("lane_label", sa.String(length=128), nullable=True),
        sa.Column("mode_label", sa.String(length=128), nullable=True),
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
            name="fk_routing_guide_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_routing_guide_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "guide_code",
            name="uq_routing_guide_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_routing_guide_org_source_ref",
        ),
        sa.CheckConstraint(
            "guide_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_routing_guide_code",
        ),
        sa.CheckConstraint(
            "lane_label IS NULL OR char_length(btrim(lane_label)) BETWEEN 1 AND 128",
            name="ck_routing_guide_lane",
        ),
        sa.CheckConstraint(
            "mode_label IS NULL OR char_length(btrim(mode_label)) BETWEEN 1 AND 128",
            name="ck_routing_guide_mode",
        ),
    )
    op.create_index(
        "ix_routing_guide_organization_id",
        "routing_guide",
        ["organization_id"],
    )
    op.execute("ALTER TABLE routing_guide ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE routing_guide FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY routing_guide_tenant_isolation ON routing_guide
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS routing_guide_tenant_isolation ON routing_guide")
    op.drop_index("ix_routing_guide_organization_id", table_name="routing_guide")
    op.drop_table("routing_guide")
