"""create bin_pack_mark catalog with RLS FORCE

Revision ID: 265_bin_pack_mark
Revises: 264_fleet_cost_mark
Create Date: 2026-09-12

EXP2.16 HITL znacznik bin-pack jako dane. Nie solver OR. Nie LLM-VRP.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "265_bin_pack_mark"
down_revision: str | None = "264_fleet_cost_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "bin_pack_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("pack_kind", sa.String(length=16), nullable=False),
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
            name="fk_bin_pack_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_bin_pack_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_bin_pack_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_bin_pack_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_bin_pack_mark_code",
        ),
        sa.CheckConstraint(
            "pack_kind IN ('volume', 'weight', 'mixed', 'other')",
            name="ck_bin_pack_mark_pack_kind",
        ),
    )
    op.create_index(
        "ix_bin_pack_mark_organization_id",
        "bin_pack_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE bin_pack_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE bin_pack_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY bin_pack_mark_tenant_isolation ON bin_pack_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS bin_pack_mark_tenant_isolation ON bin_pack_mark",
    )
    op.drop_index(
        "ix_bin_pack_mark_organization_id",
        table_name="bin_pack_mark",
    )
    op.drop_table("bin_pack_mark")
