"""create three_way_mark catalog with RLS FORCE

Revision ID: 320_three_way_mark
Revises: 319_line_impact_mark
Create Date: 2026-09-12

EXP3.3c HITL znacznik 3-way (buyer/seller/carrier). Nie tuple per strona. Nie kwota.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "320_three_way_mark"
down_revision: str | None = "319_line_impact_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "three_way_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("way_kind", sa.String(length=16), nullable=False),
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
            name="fk_three_way_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_three_way_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_three_way_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_three_way_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_three_way_mark_code",
        ),
        sa.CheckConstraint(
            "way_kind IN ('buyer', 'seller', 'carrier', 'other')",
            name="ck_three_way_mark_way_kind",
        ),
    )
    op.create_index(
        "ix_three_way_mark_organization_id",
        "three_way_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE three_way_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE three_way_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY three_way_mark_tenant_isolation ON three_way_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS three_way_mark_tenant_isolation ON three_way_mark",
    )
    op.drop_index(
        "ix_three_way_mark_organization_id",
        table_name="three_way_mark",
    )
    op.drop_table("three_way_mark")
