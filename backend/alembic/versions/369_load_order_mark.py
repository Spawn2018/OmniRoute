"""create load_order_mark catalog with RLS FORCE

Revision ID: 369_load_order_mark
Revises: 368_groupage_disp_mark
Create Date: 2026-09-13

BR3.1 HITL katalog kolejności załadunku. Nie solver. Nie wymiary Decimal.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "369_load_order_mark"
down_revision: str | None = "368_groupage_disp_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "load_order_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("order_kind", sa.String(length=16), nullable=False),
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
            name="fk_load_order_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_load_order_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_load_order_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_load_order_mark_org_src",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_load_order_mark_code",
        ),
        sa.CheckConstraint(
            "order_kind IN ('sequence', 'stack', 'door', 'other')",
            name="ck_load_order_mark_kind",
        ),
    )
    op.create_index(
        "ix_load_order_mark_organization_id",
        "load_order_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE load_order_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE load_order_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY load_order_mark_tenant_isolation ON load_order_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS load_order_mark_tenant_isolation ON load_order_mark",
    )
    op.drop_index(
        "ix_load_order_mark_organization_id",
        table_name="load_order_mark",
    )
    op.drop_table("load_order_mark")
