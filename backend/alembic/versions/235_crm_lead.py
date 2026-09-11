"""create crm_lead catalog with RLS FORCE

Revision ID: 235_crm_lead
Revises: 234_intervention_outcome
Create Date: 2026-09-11

G1 HITL lead CRM jako dane. Nie szansa. Nie cold-send.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "235_crm_lead"
down_revision: str | None = "234_intervention_outcome"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "crm_lead",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("lead_code", sa.String(length=32), nullable=False),
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
            name="fk_crm_lead_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_crm_lead_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "lead_code",
            name="uq_crm_lead_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_crm_lead_org_source_ref",
        ),
        sa.CheckConstraint(
            "lead_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_crm_lead_code",
        ),
        sa.CheckConstraint(
            "stage_kind IN ('new', 'qualified', 'disqualified', 'other')",
            name="ck_crm_lead_stage_kind",
        ),
    )
    op.create_index(
        "ix_crm_lead_organization_id",
        "crm_lead",
        ["organization_id"],
    )
    op.execute("ALTER TABLE crm_lead ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE crm_lead FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY crm_lead_tenant_isolation ON crm_lead
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS crm_lead_tenant_isolation ON crm_lead")
    op.drop_index("ix_crm_lead_organization_id", table_name="crm_lead")
    op.drop_table("crm_lead")
