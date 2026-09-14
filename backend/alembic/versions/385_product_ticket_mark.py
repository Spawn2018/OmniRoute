"""create product_ticket_mark catalog with RLS FORCE

Revision ID: 385_product_ticket_mark
Revises: 384_line_impact_layer_mark
Create Date: 2026-09-14

Plat-HD HITL katalog ticketu produktu. Nie CAPA. Nie auto-naprawa.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "385_product_ticket_mark"
down_revision: str | None = "384_line_impact_layer_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "product_ticket_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("ticket_kind", sa.String(length=16), nullable=False),
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
            name="fk_product_ticket_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_product_ticket_mark_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_product_ticket_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_product_ticket_mark_org_src",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_product_ticket_mark_code",
        ),
        sa.CheckConstraint(
            "ticket_kind IN ('report', 'triage', 'owner_ok', 'other')",
            name="ck_product_ticket_mark_kind",
        ),
    )
    op.create_index(
        "ix_product_ticket_mark_organization_id",
        "product_ticket_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE product_ticket_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE product_ticket_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY product_ticket_mark_tenant_isolation
        ON product_ticket_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS product_ticket_mark_tenant_isolation ON product_ticket_mark",
    )
    op.drop_index(
        "ix_product_ticket_mark_organization_id",
        table_name="product_ticket_mark",
    )
    op.drop_table("product_ticket_mark")
