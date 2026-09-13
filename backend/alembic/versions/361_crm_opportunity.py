"""create crm_opportunity catalog with RLS FORCE

Revision ID: 361_crm_opportunity
Revises: 360_route_plan_mk
Create Date: 2026-09-13

BR6.0 HITL okazja CRM. Nie silnik lejka. Nie activity.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "361_crm_opportunity"
down_revision: str | None = "360_route_plan_mk"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "crm_opportunity",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("opportunity_code", sa.String(length=32), nullable=False),
        sa.Column("stage_kind", sa.String(length=16), nullable=False),
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
            name="fk_crm_opportunity_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_crm_opportunity_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "opportunity_code",
            name="uq_crm_opportunity_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_crm_opportunity_org_source_ref",
        ),
        sa.CheckConstraint(
            "opportunity_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_crm_opportunity_code",
        ),
        sa.CheckConstraint(
            "stage_kind IN ('open', 'won', 'lost', 'other')",
            name="ck_crm_opportunity_stage_kind",
        ),
    )
    op.create_index(
        "ix_crm_opportunity_organization_id",
        "crm_opportunity",
        ["organization_id"],
    )
    op.execute("ALTER TABLE crm_opportunity ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE crm_opportunity FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY crm_opportunity_tenant_isolation ON crm_opportunity
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS crm_opportunity_tenant_isolation ON crm_opportunity",
    )
    op.drop_index(
        "ix_crm_opportunity_organization_id",
        table_name="crm_opportunity",
    )
    op.drop_table("crm_opportunity")
