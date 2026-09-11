"""create lc_checklist catalog with RLS FORCE

Revision ID: 236_lc_checklist
Revises: 235_crm_lead
Create Date: 2026-09-11

G3 HITL checklista LC jako dane. Nie bank. Nie due.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "236_lc_checklist"
down_revision: str | None = "235_crm_lead"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "lc_checklist",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("checklist_code", sa.String(length=32), nullable=False),
        sa.Column("status_kind", sa.String(length=16), nullable=False),
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
            name="fk_lc_checklist_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_lc_checklist_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "checklist_code",
            name="uq_lc_checklist_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_lc_checklist_org_source_ref",
        ),
        sa.CheckConstraint(
            "checklist_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_lc_checklist_code",
        ),
        sa.CheckConstraint(
            "status_kind IN ('open', 'presented', 'closed', 'other')",
            name="ck_lc_checklist_status_kind",
        ),
    )
    op.create_index(
        "ix_lc_checklist_organization_id",
        "lc_checklist",
        ["organization_id"],
    )
    op.execute("ALTER TABLE lc_checklist ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE lc_checklist FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY lc_checklist_tenant_isolation ON lc_checklist
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS lc_checklist_tenant_isolation ON lc_checklist")
    op.drop_index("ix_lc_checklist_organization_id", table_name="lc_checklist")
    op.drop_table("lc_checklist")
