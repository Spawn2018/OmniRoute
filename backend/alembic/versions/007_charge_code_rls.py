"""create charge_code catalog with RLS

Revision ID: 007_charge_code_rls
Revises: 006_rls_with_check
Create Date: 2026-09-01
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "007_charge_code_rls"
down_revision: str | None = "006_rls_with_check"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "charge_code",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column(
            "aliases",
            postgresql.ARRAY(sa.Text()),
            nullable=False,
            server_default="{}",
        ),
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
            name="fk_charge_code_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "code", name="uq_charge_code_org_code"),
    )
    op.create_index("ix_charge_code_organization_id", "charge_code", ["organization_id"])
    op.create_index(
        "ix_charge_code_aliases",
        "charge_code",
        ["aliases"],
        postgresql_using="gin",
    )

    op.execute("ALTER TABLE charge_code ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE charge_code FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY charge_code_tenant_isolation ON charge_code
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS charge_code_tenant_isolation ON charge_code")
    op.drop_index("ix_charge_code_aliases", table_name="charge_code")
    op.drop_index("ix_charge_code_organization_id", table_name="charge_code")
    op.drop_table("charge_code")
