"""create commodity_code catalog with RLS

Revision ID: 017_commodity_code_rls
Revises: 016_quotation_port_party
Create Date: 2026-09-01
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "017_commodity_code_rls"
down_revision: str | None = "016_quotation_port_party"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "commodity_code",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=10), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column(
            "aliases",
            postgresql.ARRAY(sa.Text()),
            nullable=False,
            server_default="{}",
        ),
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
            name="fk_commodity_code_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "code", name="uq_commodity_code_org_code"),
        sa.CheckConstraint("code ~ '^[0-9]{4,10}$'", name="ck_commodity_code_digits"),
    )
    op.create_index("ix_commodity_code_organization_id", "commodity_code", ["organization_id"])
    op.create_index(
        "ix_commodity_code_aliases",
        "commodity_code",
        ["aliases"],
        postgresql_using="gin",
    )

    op.execute("ALTER TABLE commodity_code ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE commodity_code FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY commodity_code_tenant_isolation ON commodity_code
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS commodity_code_tenant_isolation ON commodity_code")
    op.drop_index("ix_commodity_code_aliases", table_name="commodity_code")
    op.drop_index("ix_commodity_code_organization_id", table_name="commodity_code")
    op.drop_table("commodity_code")
