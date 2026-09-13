"""create route_plan_mark catalog with RLS FORCE

Revision ID: 360_route_plan_mk
Revises: 359_circle_pair
Create Date: 2026-09-13

BR3.0 HITL znacznik planu trasy. Nie Valhalla. Nie km.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "360_route_plan_mk"
down_revision: str | None = "359_circle_pair"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "route_plan_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("plan_kind", sa.String(length=16), nullable=False),
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
            name="fk_route_plan_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_route_plan_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_route_plan_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_route_plan_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_route_plan_mark_code",
        ),
        sa.CheckConstraint(
            "plan_kind IN ('route', 'stop', 'window', 'other')",
            name="ck_route_plan_mark_plan_kind",
        ),
    )
    op.create_index(
        "ix_route_plan_mark_organization_id",
        "route_plan_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE route_plan_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE route_plan_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY route_plan_mark_tenant_isolation ON route_plan_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS route_plan_mark_tenant_isolation ON route_plan_mark",
    )
    op.drop_index(
        "ix_route_plan_mark_organization_id",
        table_name="route_plan_mark",
    )
    op.drop_table("route_plan_mark")
