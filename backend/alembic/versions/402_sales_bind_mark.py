"""create sales_bind_mark catalog with RLS FORCE

Revision ID: 402_sales_bind_mark
Revises: 401_crm_link_mark
Create Date: 2026-09-15

BR6.1 leftover HITL bind sprzedaży. Nie HubSpot live. Nie FK.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "402_sales_bind_mark"
down_revision: str | None = "401_crm_link_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "sales_bind_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("bind_kind", sa.String(length=32), nullable=False),
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
            name="fk_sales_bind_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_sales_bind_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_sales_bind_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_sales_bind_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_sales_bind_mark_code",
        ),
        sa.CheckConstraint(
            "bind_kind IN ('opportunity', 'party', 'other')",
            name="ck_sales_bind_mark_kind",
        ),
    )
    op.create_index(
        "ix_sales_bind_mark_organization_id",
        "sales_bind_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE sales_bind_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE sales_bind_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY sales_bind_mark_tenant_isolation ON sales_bind_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS sales_bind_mark_tenant_isolation ON sales_bind_mark",
    )
    op.drop_index(
        "ix_sales_bind_mark_organization_id",
        table_name="sales_bind_mark",
    )
    op.drop_table("sales_bind_mark")
