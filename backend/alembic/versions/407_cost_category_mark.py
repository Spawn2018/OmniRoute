"""create cost_category_mark catalog with RLS FORCE

Revision ID: 407_cost_category_mark
Revises: 406_allocation_key
Create Date: 2026-09-15

AI7.0 leftover HITL kategoria kosztu PDF §13j. Nie allocation SQL. Nie TCM.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "407_cost_category_mark"
down_revision: str | None = "406_allocation_key"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "cost_category_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("category_kind", sa.String(length=16), nullable=False),
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
            name="fk_cost_category_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_cost_category_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_cost_category_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_cost_category_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_cost_category_mark_code",
        ),
        sa.CheckConstraint(
            "category_kind IN ("
            "'direct', 'shared', 'allocated', 'overhead', 'capital', 'risk', 'other'"
            ")",
            name="ck_cost_category_mark_category_kind",
        ),
    )
    op.create_index(
        "ix_cost_category_mark_organization_id",
        "cost_category_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE cost_category_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE cost_category_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY cost_category_mark_tenant_isolation ON cost_category_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS cost_category_mark_tenant_isolation ON cost_category_mark",
    )
    op.drop_index("ix_cost_category_mark_organization_id", table_name="cost_category_mark")
    op.drop_table("cost_category_mark")
