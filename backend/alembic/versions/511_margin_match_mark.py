"""create margin_match_mark catalog with RLS FORCE

Revision ID: 511_margin_match_mark
Revises: 510_trip_variance_mark
Create Date: 2026-09-23

Leftover N6 HITL stance dopasowania podłogi marży. Nie matching SQL lane. Nie auto charge.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "511_margin_match_mark"
down_revision: str | None = "510_trip_variance_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "margin_match_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("match_kind", sa.String(length=32), nullable=False),
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
            name="fk_margin_match_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id", "id", name="uq_margin_match_mark_org_id"
        ),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_margin_match_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_margin_match_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_margin_match_mark_code",
        ),
        sa.CheckConstraint(
            "match_kind IN ('match', 'hold', 'waive', 'other')",
            name="ck_margin_match_mark_kind",
        ),
    )
    op.create_index(
        "ix_margin_match_mark_organization_id",
        "margin_match_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE margin_match_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE margin_match_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY margin_match_mark_tenant_isolation
        ON margin_match_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS margin_match_mark_tenant_isolation "
        "ON margin_match_mark",
    )
    op.drop_index(
        "ix_margin_match_mark_organization_id",
        table_name="margin_match_mark",
    )
    op.drop_table("margin_match_mark")
