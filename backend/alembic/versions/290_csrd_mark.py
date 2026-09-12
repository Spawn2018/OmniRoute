"""create csrd_mark catalog with RLS FORCE

Revision ID: 271_csrd_mark
Revises: 276_MQC_mark
Create Date: 2026-09-12

EXP3.14 HITL znacznik MQC jako dane. Nie live giełda. Nie CSRD live filing.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "290_csrd_mark"
down_revision: str | None = "289_demand_snapshot_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "csrd_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("report_kind", sa.String(length=16), nullable=False),
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
            name="fk_csrd_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_csrd_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_csrd_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_csrd_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_csrd_mark_code",
        ),
        sa.CheckConstraint(
            "report_kind IN ('csrd', 'esrs', 'assurance', 'other')",
            name="ck_csrd_mark_report_kind",
        ),
    )
    op.create_index(
        "ix_csrd_mark_organization_id",
        "csrd_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE csrd_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE csrd_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY csrd_mark_tenant_isolation ON csrd_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS csrd_mark_tenant_isolation ON csrd_mark",
    )
    op.drop_index(
        "ix_csrd_mark_organization_id",
        table_name="csrd_mark",
    )
    op.drop_table("csrd_mark")
