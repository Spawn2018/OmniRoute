"""create port_surcharge catalog with RLS

Revision ID: 023_port_surcharge_rls
Revises: 022_customer_sop_rls
Create Date: 2026-09-02
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "023_port_surcharge_rls"
down_revision: str | None = "022_customer_sop_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "port_surcharge",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("amount", sa.Numeric(14, 4), nullable=False),
        sa.Column("currency", sa.CHAR(length=3), nullable=False),
        sa.Column("port_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=128), nullable=False),
        sa.Column("applies_when", sa.String(length=512), nullable=False),
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
            name="fk_port_surcharge_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "port_id"],
            ["port.organization_id", "port.id"],
            name="fk_port_surcharge_port",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "port_id",
            "code",
            name="uq_port_surcharge_org_port_code",
        ),
        sa.CheckConstraint("code ~ '^[a-z][a-z0-9_]{1,31}$'", name="ck_port_surcharge_code_snake"),
        sa.CheckConstraint("currency ~ '^[A-Z]{3}$'", name="ck_port_surcharge_currency_iso"),
        sa.CheckConstraint("amount > 0", name="ck_port_surcharge_amount_positive"),
        sa.CheckConstraint("char_length(title) >= 1", name="ck_port_surcharge_title_len"),
        sa.CheckConstraint("char_length(applies_when) >= 1", name="ck_port_surcharge_when_len"),
    )
    op.create_index("ix_port_surcharge_organization_id", "port_surcharge", ["organization_id"])

    op.execute("ALTER TABLE port_surcharge ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE port_surcharge FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY port_surcharge_tenant_isolation ON port_surcharge
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS port_surcharge_tenant_isolation ON port_surcharge")
    op.drop_index("ix_port_surcharge_organization_id", table_name="port_surcharge")
    op.drop_table("port_surcharge")
