"""create tender_playbook catalog with RLS FORCE

Revision ID: 115_tender_playbook
Revises: 114_tender_matrix_cell
Create Date: 2026-09-09

Playbook: twierdzenie + source_ref. Nie extract RFP. Nie kwota.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "115_tender_playbook"
down_revision: str | None = "114_tender_matrix_cell"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "tender_playbook",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tender_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("claim_code", sa.String(length=32), nullable=False),
        sa.Column("claim_text", sa.String(length=512), nullable=False),
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
            name="fk_tender_playbook_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_playbook_tender",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_tender_playbook_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "tender_id",
            "claim_code",
            name="uq_tender_playbook_org_tender_code",
        ),
        sa.CheckConstraint(
            "char_length(claim_text) >= 1 AND char_length(claim_text) <= 512",
            name="ck_tender_playbook_claim_text",
        ),
        sa.CheckConstraint(
            "claim_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_tender_playbook_code",
        ),
    )
    op.create_index(
        "ix_tender_playbook_organization_id",
        "tender_playbook",
        ["organization_id"],
    )
    op.create_index(
        "ix_tender_playbook_org_tender",
        "tender_playbook",
        ["organization_id", "tender_id"],
    )
    op.execute("ALTER TABLE tender_playbook ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE tender_playbook FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY tender_playbook_tenant_isolation ON tender_playbook
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS tender_playbook_tenant_isolation ON tender_playbook")
    op.drop_index("ix_tender_playbook_org_tender", table_name="tender_playbook")
    op.drop_index("ix_tender_playbook_organization_id", table_name="tender_playbook")
    op.drop_table("tender_playbook")
