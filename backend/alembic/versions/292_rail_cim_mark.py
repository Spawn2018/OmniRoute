"""create rail_cim_mark catalog with RLS FORCE

Revision ID: 271_rail_cim_mark
Revises: 276_MQC_mark
Create Date: 2026-09-12

EXP4.2 HITL znacznik MQC jako dane. Nie live giełda. Nie CIM scrape.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "292_rail_cim_mark"
down_revision: str | None = "291_air_ra3_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "rail_cim_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("rail_kind", sa.String(length=16), nullable=False),
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
            name="fk_rail_cim_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_rail_cim_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_rail_cim_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_rail_cim_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_rail_cim_mark_code",
        ),
        sa.CheckConstraint(
            "rail_kind IN ('uic', 'cim', 'smgs', 'other')",
            name="ck_rail_cim_mark_rail_kind",
        ),
    )
    op.create_index(
        "ix_rail_cim_mark_organization_id",
        "rail_cim_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE rail_cim_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE rail_cim_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY rail_cim_mark_tenant_isolation ON rail_cim_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS rail_cim_mark_tenant_isolation ON rail_cim_mark",
    )
    op.drop_index(
        "ix_rail_cim_mark_organization_id",
        table_name="rail_cim_mark",
    )
    op.drop_table("rail_cim_mark")
