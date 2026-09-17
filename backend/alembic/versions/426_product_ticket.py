"""create product_ticket with title/body/kind + RLS FORCE

Revision ID: 426_product_ticket
Revises: 425_od_margin_floor
Create Date: 2026-09-17

Plat-HD-flow HITL wpis ticketu produktu. Nie auto-fix. Nie CAPA.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "426_product_ticket"
down_revision: str | None = "425_od_margin_floor"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "product_ticket",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("ticket_code", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("body", sa.String(length=2000), nullable=False),
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
            name="fk_product_ticket_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_product_ticket_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "ticket_code",
            name="uq_product_ticket_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_product_ticket_org_src",
        ),
        sa.CheckConstraint(
            "ticket_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_product_ticket_code",
        ),
        sa.CheckConstraint(
            "char_length(title) BETWEEN 1 AND 200",
            name="ck_product_ticket_title",
        ),
        sa.CheckConstraint(
            "char_length(body) BETWEEN 1 AND 2000",
            name="ck_product_ticket_body",
        ),
        sa.CheckConstraint(
            "ticket_kind IN ('report', 'triage', 'owner_ok', 'other')",
            name="ck_product_ticket_kind",
        ),
    )
    op.create_index(
        "ix_product_ticket_organization_id",
        "product_ticket",
        ["organization_id"],
    )
    op.execute("ALTER TABLE product_ticket ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE product_ticket FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY product_ticket_tenant_isolation
        ON product_ticket
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS product_ticket_tenant_isolation ON product_ticket",
    )
    op.drop_index(
        "ix_product_ticket_organization_id",
        table_name="product_ticket",
    )
    op.drop_table("product_ticket")
