"""create allocation_level open dictionary with RLS FORCE

Revision ID: 408_allocation_level
Revises: 407_cost_category_mark
Create Date: 2026-09-15

AI7.0 HITL allocation_level. Otwarty slownik poziomow. Nie CHECK listy 12.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "408_allocation_level"
down_revision: str | None = "407_cost_category_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"
_SNAKE = r"^[a-z][a-z0-9_]{1,31}$"


def upgrade() -> None:
    op.create_table(
        "allocation_level",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("level_code", sa.String(length=32), nullable=False),
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
            name="fk_allocation_level_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_allocation_level_org_id"),
        sa.UniqueConstraint("organization_id", "level_code", name="uq_allocation_level_org_code"),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_allocation_level_org_source_ref",
        ),
        sa.CheckConstraint(f"level_code ~ '{_SNAKE}'", name="ck_allocation_level_code"),
    )
    op.create_index("ix_allocation_level_organization_id", "allocation_level", ["organization_id"])
    op.execute("ALTER TABLE allocation_level ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE allocation_level FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY allocation_level_tenant_isolation ON allocation_level
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS allocation_level_tenant_isolation ON allocation_level")
    op.drop_index("ix_allocation_level_organization_id", table_name="allocation_level")
    op.drop_table("allocation_level")
