"""create free_time_clock catalog with RLS FORCE

Revision ID: 136_free_time_clock
Revises: 135_weather_observation
Create Date: 2026-09-09

HITL rodzaj + dni wolne. Nie countdown. Nie charge.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "136_free_time_clock"
down_revision: str | None = "135_weather_observation"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "free_time_clock",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("clock_kind", sa.String(length=12), nullable=False),
        sa.Column("free_days", sa.Integer(), nullable=False),
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
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
            name="fk_free_time_clock_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_free_time_clock_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_free_time_clock_org_source_ref",
        ),
        sa.CheckConstraint(
            "clock_kind IN ('demurrage','detention','mixed','rollover')",
            name="ck_free_time_clock_kind",
        ),
        sa.CheckConstraint("free_days >= 0", name="ck_free_time_clock_days"),
    )
    # Lista per tenant — RLS filtruje organization_id; unique source_ref nie zastępuje tego skanu.
    op.create_index(
        "ix_free_time_clock_organization_id",
        "free_time_clock",
        ["organization_id"],
    )
    op.execute("ALTER TABLE free_time_clock ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE free_time_clock FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY free_time_clock_tenant_isolation ON free_time_clock
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS free_time_clock_tenant_isolation ON free_time_clock")
    op.drop_index("ix_free_time_clock_organization_id", table_name="free_time_clock")
    op.drop_table("free_time_clock")
