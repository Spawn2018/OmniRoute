"""create chassis_mark catalog with RLS FORCE

Revision ID: 318_chassis_mark
Revises: 317_ocean_feeder_mark
Create Date: 2026-09-12

EXP4.5b HITL znacznik chassis/trailer. Nie live chassis pool. Nie TEU. Nie yard.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "318_chassis_mark"
down_revision: str | None = "317_ocean_feeder_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "chassis_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("chassis_kind", sa.String(length=16), nullable=False),
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
            name="fk_chassis_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_chassis_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_chassis_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_chassis_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_chassis_mark_code",
        ),
        sa.CheckConstraint(
            "chassis_kind IN ('chassis', 'trailer', 'other')",
            name="ck_chassis_mark_chassis_kind",
        ),
    )
    op.create_index(
        "ix_chassis_mark_organization_id",
        "chassis_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE chassis_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE chassis_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY chassis_mark_tenant_isolation ON chassis_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS chassis_mark_tenant_isolation ON chassis_mark",
    )
    op.drop_index(
        "ix_chassis_mark_organization_id",
        table_name="chassis_mark",
    )
    op.drop_table("chassis_mark")
