"""create carbon_method catalog with RLS FORCE

Revision ID: 130_carbon_method
Revises: 129_cash_discount
Create Date: 2026-09-09

HITL GLEC/GHG method + version + source_ref. Nie kg. Nie kalkulator.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "130_carbon_method"
down_revision: str | None = "129_cash_discount"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "carbon_method",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("method_code", sa.String(length=32), nullable=False),
        sa.Column("method_version", sa.String(length=32), nullable=False),
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
            name="fk_carbon_method_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_carbon_method_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "method_code",
            "method_version",
            name="uq_carbon_method_org_code_version",
        ),
        sa.CheckConstraint(
            "method_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_carbon_method_code",
        ),
        sa.CheckConstraint(
            "method_version ~ '^[a-z0-9][a-z0-9_]{0,31}$'",
            name="ck_carbon_method_version",
        ),
    )
    op.create_index("ix_carbon_method_organization_id", "carbon_method", ["organization_id"])
    op.execute("ALTER TABLE carbon_method ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE carbon_method FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY carbon_method_tenant_isolation ON carbon_method
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS carbon_method_tenant_isolation ON carbon_method")
    op.drop_index("ix_carbon_method_organization_id", table_name="carbon_method")
    op.drop_table("carbon_method")
