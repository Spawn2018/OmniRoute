"""create customer_sop catalog with RLS

Revision ID: 022_customer_sop_rls
Revises: 021_party_scorecard_rls
Create Date: 2026-09-02
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "022_customer_sop_rls"
down_revision: str | None = "021_party_scorecard_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "customer_sop",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(length=8), nullable=False, server_default=sa.text("'draft'")),
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=128), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
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
            name="fk_customer_sop_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_customer_sop_party",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "party_id",
            "code",
            name="uq_customer_sop_org_party_code",
        ),
        sa.CheckConstraint("code ~ '^[a-z][a-z0-9_]{1,31}$'", name="ck_customer_sop_code_snake"),
        sa.CheckConstraint("status IN ('draft', 'approved')", name="ck_customer_sop_status"),
        sa.CheckConstraint("char_length(body) >= 1", name="ck_customer_sop_body_len"),
        sa.CheckConstraint(
            "(status = 'draft' AND approved_at IS NULL) OR "
            "(status = 'approved' AND approved_at IS NOT NULL)",
            name="ck_customer_sop_approved_pair",
        ),
    )
    op.create_index("ix_customer_sop_organization_id", "customer_sop", ["organization_id"])

    op.execute("ALTER TABLE customer_sop ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE customer_sop FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY customer_sop_tenant_isolation ON customer_sop
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS customer_sop_tenant_isolation ON customer_sop")
    op.drop_index("ix_customer_sop_organization_id", table_name="customer_sop")
    op.drop_table("customer_sop")
