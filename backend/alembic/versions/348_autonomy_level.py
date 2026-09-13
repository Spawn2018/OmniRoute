"""create autonomy_level open dictionary with RLS FORCE

Revision ID: 348_autonomy_level
Revises: 347_twin_kind
Create Date: 2026-09-13

AI1.4 leftover HITL autonomy_level. Otwarty slownik. Nie CHECK listy.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "348_autonomy_level"
down_revision: str | None = "347_twin_kind"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"
_SNAKE = r"^[a-z][a-z0-9_]{1,31}$"


def upgrade() -> None:
    op.create_table(
        "autonomy_level",
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
            name="fk_autonomy_level_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_autonomy_level_org_id"),
        sa.UniqueConstraint("organization_id", "level_code", name="uq_autonomy_level_org_code"),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_autonomy_level_org_source_ref",
        ),
        sa.CheckConstraint(f"level_code ~ '{_SNAKE}'", name="ck_autonomy_level_code"),
    )
    op.create_index("ix_autonomy_level_organization_id", "autonomy_level", ["organization_id"])
    op.execute("ALTER TABLE autonomy_level ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE autonomy_level FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY autonomy_level_tenant_isolation ON autonomy_level
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS autonomy_level_tenant_isolation ON autonomy_level")
    op.drop_index("ix_autonomy_level_organization_id", table_name="autonomy_level")
    op.drop_table("autonomy_level")
