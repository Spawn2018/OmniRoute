"""create abandoned_rto_mark catalog with RLS FORCE

Revision ID: 271_abandoned_rto_mark
Revises: 276_MQC_mark
Create Date: 2026-09-12

EXP3.10 HITL znacznik MQC jako dane. Nie live giełda. Nie RTO scrape.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "286_abandoned_rto_mark"
down_revision: str | None = "285_switch_bl_loi_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "abandoned_rto_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("fate_kind", sa.String(length=16), nullable=False),
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
            name="fk_abandoned_rto_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_abandoned_rto_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_abandoned_rto_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_abandoned_rto_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_abandoned_rto_mark_code",
        ),
        sa.CheckConstraint(
            "fate_kind IN ('abandoned', 'rto', 'return', 'other')",
            name="ck_abandoned_rto_mark_fate_kind",
        ),
    )
    op.create_index(
        "ix_abandoned_rto_mark_organization_id",
        "abandoned_rto_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE abandoned_rto_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE abandoned_rto_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY abandoned_rto_mark_tenant_isolation ON abandoned_rto_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS abandoned_rto_mark_tenant_isolation ON abandoned_rto_mark",
    )
    op.drop_index(
        "ix_abandoned_rto_mark_organization_id",
        table_name="abandoned_rto_mark",
    )
    op.drop_table("abandoned_rto_mark")
