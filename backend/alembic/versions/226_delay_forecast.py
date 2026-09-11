"""create delay_forecast catalog with RLS FORCE

Revision ID: 226_delay_forecast
Revises: 225_sla_clause
Create Date: 2026-09-11

CI4 HITL prognoza opóźnienia jako dane. Nie wróżba. Nie GPS.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "226_delay_forecast"
down_revision: str | None = "225_sla_clause"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "delay_forecast",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("forecast_code", sa.String(length=32), nullable=False),
        sa.Column("horizon_hours", sa.Integer(), nullable=False),
        sa.Column("p_late", sa.Numeric(precision=14, scale=4), nullable=False),
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
            name="fk_delay_forecast_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_delay_forecast_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "forecast_code",
            name="uq_delay_forecast_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_delay_forecast_org_source_ref",
        ),
        sa.CheckConstraint(
            "forecast_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_delay_forecast_code",
        ),
        sa.CheckConstraint(
            "horizon_hours BETWEEN 1 AND 168",
            name="ck_delay_forecast_horizon",
        ),
        sa.CheckConstraint(
            "p_late >= 0 AND p_late <= 1",
            name="ck_delay_forecast_p_late",
        ),
    )
    op.create_index(
        "ix_delay_forecast_organization_id",
        "delay_forecast",
        ["organization_id"],
    )
    op.execute("ALTER TABLE delay_forecast ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE delay_forecast FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY delay_forecast_tenant_isolation ON delay_forecast
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS delay_forecast_tenant_isolation ON delay_forecast")
    op.drop_index("ix_delay_forecast_organization_id", table_name="delay_forecast")
    op.drop_table("delay_forecast")
