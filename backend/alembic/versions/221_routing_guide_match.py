"""create routing_guide_match catalog with RLS FORCE

Revision ID: 221_routing_guide_match
Revises: 220_shipment_guide_code
Create Date: 2026-09-11

HITL tryb dopasowania przewodnika jako dane. Nie silnik matching.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "221_routing_guide_match"
down_revision: str | None = "220_shipment_guide_code"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "routing_guide_match",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("match_kind", sa.String(length=32), nullable=False),
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
            name="fk_routing_guide_match_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id", "id", name="uq_routing_guide_match_org_id"
        ),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_routing_guide_match_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_routing_guide_match_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_routing_guide_match_code",
        ),
        sa.CheckConstraint(
            "match_kind IN ('guide_code_only', 'lane_label', 'mode_label')",
            name="ck_routing_guide_match_kind",
        ),
    )
    op.create_index(
        "ix_routing_guide_match_organization_id",
        "routing_guide_match",
        ["organization_id"],
    )
    op.execute("ALTER TABLE routing_guide_match ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE routing_guide_match FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY routing_guide_match_tenant_isolation ON routing_guide_match
        FOR ALL
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS routing_guide_match_tenant_isolation "
        "ON routing_guide_match"
    )
    op.drop_index(
        "ix_routing_guide_match_organization_id",
        table_name="routing_guide_match",
    )
    op.drop_table("routing_guide_match")
