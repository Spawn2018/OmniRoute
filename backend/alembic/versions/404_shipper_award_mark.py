"""create shipper_award_mark catalog with RLS FORCE

Revision ID: 404_shipper_award_mark
Revises: 403_shipper_bind_mark
Create Date: 2026-09-15

BR6.2 leftover HITL award załadowcy. Nie Alpega live. Nie auto-award SQL.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "404_shipper_award_mark"
down_revision: str | None = "403_shipper_bind_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "shipper_award_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("award_kind", sa.String(length=32), nullable=False),
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
            name="fk_shipper_award_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_shipper_award_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_shipper_award_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_shipper_award_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_shipper_award_mark_code",
        ),
        sa.CheckConstraint(
            "award_kind IN ('go', 'hold', 'no_award', 'other')",
            name="ck_shipper_award_mark_kind",
        ),
    )
    op.create_index(
        "ix_shipper_award_mark_organization_id",
        "shipper_award_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE shipper_award_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE shipper_award_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY shipper_award_mark_tenant_isolation ON shipper_award_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS shipper_award_mark_tenant_isolation ON shipper_award_mark",
    )
    op.drop_index(
        "ix_shipper_award_mark_organization_id",
        table_name="shipper_award_mark",
    )
    op.drop_table("shipper_award_mark")
