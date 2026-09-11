"""create ncts_draft catalog with RLS FORCE

Revision ID: 237_ncts_draft
Revises: 236_lc_checklist
Create Date: 2026-09-11

G4 HITL szkic NCTS jako dane. Nie PUESC. Nie kwota.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "237_ncts_draft"
down_revision: str | None = "236_lc_checklist"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "ncts_draft",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("draft_code", sa.String(length=32), nullable=False),
        sa.Column("transit_kind", sa.String(length=16), nullable=False),
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
            name="fk_ncts_draft_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_ncts_draft_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "draft_code",
            name="uq_ncts_draft_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_ncts_draft_org_source_ref",
        ),
        sa.CheckConstraint(
            "draft_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_ncts_draft_code",
        ),
        sa.CheckConstraint(
            "transit_kind IN ('t1', 't2', 'other')",
            name="ck_ncts_draft_transit_kind",
        ),
    )
    op.create_index(
        "ix_ncts_draft_organization_id",
        "ncts_draft",
        ["organization_id"],
    )
    op.execute("ALTER TABLE ncts_draft ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE ncts_draft FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY ncts_draft_tenant_isolation ON ncts_draft
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS ncts_draft_tenant_isolation ON ncts_draft")
    op.drop_index("ix_ncts_draft_organization_id", table_name="ncts_draft")
    op.drop_table("ncts_draft")
