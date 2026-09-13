"""create groupage_dispatcher_mark catalog with RLS FORCE

Revision ID: 368_groupage_disp_mark
Revises: 367_campaign_mark
Create Date: 2026-09-13

BR3.2 HITL katalog dyspozytora drobnicy. Nie silnik hubów. Nie live.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "368_groupage_disp_mark"
down_revision: str | None = "367_campaign_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "groupage_dispatcher_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("dispatcher_kind", sa.String(length=16), nullable=False),
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
            name="fk_groupage_dispatcher_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_groupage_disp_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_groupage_disp_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_groupage_disp_mark_org_src",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_groupage_disp_mark_code",
        ),
        sa.CheckConstraint(
            "dispatcher_kind IN ('line', 'hub', 'cutoff', 'consol', 'other')",
            name="ck_groupage_disp_mark_kind",
        ),
    )
    op.create_index(
        "ix_groupage_dispatcher_mark_organization_id",
        "groupage_dispatcher_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE groupage_dispatcher_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE groupage_dispatcher_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY groupage_dispatcher_mark_tenant_isolation ON groupage_dispatcher_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS groupage_dispatcher_mark_tenant_isolation"
        " ON groupage_dispatcher_mark",
    )
    op.drop_index(
        "ix_groupage_dispatcher_mark_organization_id",
        table_name="groupage_dispatcher_mark",
    )
    op.drop_table("groupage_dispatcher_mark")
