"""create high_value_mark catalog with RLS FORCE

Revision ID: 333_high_value_mark
Revises: 332_profit_center_mark
Create Date: 2026-09-12

EXP1 HITL high_value. Nie kolumna shipment. Nie cargo_value.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "333_high_value_mark"
down_revision: str | None = "332_profit_center_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "high_value_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("protocol_kind", sa.String(length=16), nullable=False),
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
            name="fk_high_value_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_high_value_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_high_value_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_high_value_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_high_value_mark_code",
        ),
        sa.CheckConstraint(
            "protocol_kind IN ('high_value', 'protocol', 'other')",
            name="ck_high_value_mark_protocol_kind",
        ),
    )
    op.create_index(
        "ix_high_value_mark_organization_id",
        "high_value_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE high_value_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE high_value_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY high_value_mark_tenant_isolation ON high_value_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS high_value_mark_tenant_isolation ON high_value_mark",
    )
    op.drop_index(
        "ix_high_value_mark_organization_id",
        table_name="high_value_mark",
    )
    op.drop_table("high_value_mark")
