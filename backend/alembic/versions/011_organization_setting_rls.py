"""create organization_setting catalog with RLS

Revision ID: 011_organization_setting_rls
Revises: 010_quotation_rls
Create Date: 2026-09-01
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "011_organization_setting_rls"
down_revision: str | None = "010_quotation_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "organization_setting",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("setting_key", sa.String(length=64), nullable=False),
        sa.Column("setting_value", sa.String(length=64), nullable=False),
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
            name="fk_organization_setting_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "setting_key",
            name="uq_organization_setting_org_key",
        ),
    )
    op.create_index(
        "ix_organization_setting_organization_id",
        "organization_setting",
        ["organization_id"],
    )

    op.execute("ALTER TABLE organization_setting ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE organization_setting FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY organization_setting_tenant_isolation ON organization_setting
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS organization_setting_tenant_isolation ON organization_setting"
    )
    op.drop_index("ix_organization_setting_organization_id", table_name="organization_setting")
    op.drop_table("organization_setting")
