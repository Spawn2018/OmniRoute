"""create invoice_match_mark catalog with RLS FORCE

Revision ID: 430_invoice_match_mark
Revises: 429_purchase_invoice
Create Date: 2026-09-17

F10 leftover HITL invoice_match_mark. Nie ranking SQL. Nie allocation.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "430_invoice_match_mark"
down_revision: str | None = "429_purchase_invoice"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "invoice_match_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("match_kind", sa.String(length=16), nullable=False),
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
            name="fk_invoice_match_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_invoice_match_mark_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_invoice_match_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_invoice_match_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_invoice_match_mark_code",
        ),
        sa.CheckConstraint(
            "match_kind IN ('candidate', 'rank', 'allocate', 'other')",
            name="ck_invoice_match_mark_match_kind",
        ),
    )
    op.create_index(
        "ix_invoice_match_mark_organization_id",
        "invoice_match_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE invoice_match_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE invoice_match_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY invoice_match_mark_tenant_isolation ON invoice_match_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS invoice_match_mark_tenant_isolation ON invoice_match_mark",
    )
    op.drop_index(
        "ix_invoice_match_mark_organization_id",
        table_name="invoice_match_mark",
    )
    op.drop_table("invoice_match_mark")
