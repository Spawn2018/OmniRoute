"""create tender_rfp_intake catalog with RLS FORCE

Revision ID: 118_tender_rfp_intake
Revises: 117_tender_consortium_member
Create Date: 2026-09-09

HITL przyjęcie RFP: intake_code + source_ref. Nie zapis z LLM. Nie auto-award.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "118_tender_rfp_intake"
down_revision: str | None = "117_tender_consortium_member"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "tender_rfp_intake",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tender_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("intake_code", sa.String(length=32), nullable=False),
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
            name="fk_tender_rfp_intake_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_rfp_intake_tender",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_tender_rfp_intake_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "tender_id",
            "intake_code",
            name="uq_tender_rfp_intake_org_tender_code",
        ),
        sa.CheckConstraint(
            "intake_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_tender_rfp_intake_code",
        ),
    )
    op.create_index(
        "ix_tender_rfp_intake_organization_id",
        "tender_rfp_intake",
        ["organization_id"],
    )
    op.create_index(
        "ix_tender_rfp_intake_org_tender",
        "tender_rfp_intake",
        ["organization_id", "tender_id"],
    )
    op.execute("ALTER TABLE tender_rfp_intake ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE tender_rfp_intake FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY tender_rfp_intake_tenant_isolation ON tender_rfp_intake
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS tender_rfp_intake_tenant_isolation ON tender_rfp_intake")
    op.drop_index("ix_tender_rfp_intake_org_tender", table_name="tender_rfp_intake")
    op.drop_index("ix_tender_rfp_intake_organization_id", table_name="tender_rfp_intake")
    op.drop_table("tender_rfp_intake")
