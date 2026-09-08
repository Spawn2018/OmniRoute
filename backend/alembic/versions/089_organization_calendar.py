"""create organization_calendar with RLS FORCE

Revision ID: 089_organization_calendar
Revises: 088_booking_instruction
Create Date: 2026-09-08

Dni robocze i święta per kraj. Nie V5. Nie GPS.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "089_organization_calendar"
down_revision: str | None = "088_booking_instruction"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "organization_calendar",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("country_code", sa.String(length=2), nullable=False),
        sa.Column("calendar_day", sa.Date(), nullable=False),
        sa.Column("day_kind", sa.String(length=8), nullable=False),
        sa.Column("source_ref", sa.Text(), nullable=False),
        sa.Column("superseded_by", postgresql.UUID(as_uuid=True), nullable=True),
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
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
            name="fk_organization_calendar_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["superseded_by"],
            ["organization_calendar.id"],
            name="fk_organization_calendar_superseded_by",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "country_code ~ '^[A-Z]{2}$'",
            name="ck_organization_calendar_country",
        ),
        sa.CheckConstraint(
            "day_kind IN ('holiday', 'working')",
            name="ck_organization_calendar_kind",
        ),
    )
    op.create_index(
        "ix_organization_calendar_organization_id",
        "organization_calendar",
        ["organization_id"],
    )
    # GET listy i is_working_day filtrują RLS + kraj + dzień.
    op.create_index(
        "ix_organization_calendar_org_country_day",
        "organization_calendar",
        ["organization_id", "country_code", "calendar_day"],
    )
    op.execute("ALTER TABLE organization_calendar ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE organization_calendar FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY organization_calendar_tenant_isolation
        ON organization_calendar
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS organization_calendar_tenant_isolation "
        "ON organization_calendar"
    )
    op.drop_index(
        "ix_organization_calendar_org_country_day",
        table_name="organization_calendar",
    )
    op.drop_index(
        "ix_organization_calendar_organization_id",
        table_name="organization_calendar",
    )
    op.drop_table("organization_calendar")
