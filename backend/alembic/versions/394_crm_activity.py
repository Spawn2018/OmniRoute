"""create crm_activity catalog with RLS FORCE

Revision ID: 394_crm_activity
Revises: 393_compliance_program_mark
Create Date: 2026-09-15

BR6.0 leftover HITL aktywnosc CRM. Nie silnik lejka. Nie FK.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "394_crm_activity"
down_revision: str | None = "393_compliance_program_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "crm_activity",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("activity_code", sa.String(length=32), nullable=False),
        sa.Column("activity_kind", sa.String(length=16), nullable=False),
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
            name="fk_crm_activity_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_crm_activity_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "activity_code",
            name="uq_crm_activity_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_crm_activity_org_source_ref",
        ),
        sa.CheckConstraint(
            "activity_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_crm_activity_code",
        ),
        sa.CheckConstraint(
            "activity_kind IN ('call', 'meeting', 'email', 'note', 'other')",
            name="ck_crm_activity_kind",
        ),
    )
    op.create_index(
        "ix_crm_activity_organization_id",
        "crm_activity",
        ["organization_id"],
    )
    op.execute("ALTER TABLE crm_activity ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE crm_activity FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY crm_activity_tenant_isolation ON crm_activity
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS crm_activity_tenant_isolation ON crm_activity",
    )
    op.drop_index(
        "ix_crm_activity_organization_id",
        table_name="crm_activity",
    )
    op.drop_table("crm_activity")
