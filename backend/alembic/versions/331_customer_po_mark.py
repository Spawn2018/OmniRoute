"""create customer_po_mark catalog with RLS FORCE

Revision ID: 331_customer_po_mark
Revises: 330_freight_term_mark
Create Date: 2026-09-12

EXP1 HITL customer_po. Nie purchase_order CT1. Nie kwota.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "331_customer_po_mark"
down_revision: str | None = "330_freight_term_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "customer_po_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("ref_kind", sa.String(length=16), nullable=False),
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
            name="fk_customer_po_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_customer_po_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_customer_po_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_customer_po_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_customer_po_mark_code",
        ),
        sa.CheckConstraint(
            "ref_kind IN ('customer_po', 'release', 'call_off', 'other')",
            name="ck_customer_po_mark_ref_kind",
        ),
    )
    op.create_index(
        "ix_customer_po_mark_organization_id",
        "customer_po_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE customer_po_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE customer_po_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY customer_po_mark_tenant_isolation ON customer_po_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS customer_po_mark_tenant_isolation ON customer_po_mark",
    )
    op.drop_index(
        "ix_customer_po_mark_organization_id",
        table_name="customer_po_mark",
    )
    op.drop_table("customer_po_mark")
