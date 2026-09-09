"""create weather_observation catalog with RLS FORCE

Revision ID: 135_weather_observation
Revises: 134_stop_eta
Create Date: 2026-09-09

HITL warunek + UN/LOCODE + czas. Nie feed HTTP. Nie ETA.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "135_weather_observation"
down_revision: str | None = "134_stop_eta"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "weather_observation",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("condition_code", sa.String(length=8), nullable=False),
        sa.Column("station_unlocode", sa.String(length=5), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("provider_code", sa.String(length=8), nullable=False),
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
            name="fk_weather_observation_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_weather_observation_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_weather_observation_org_source_ref",
        ),
        sa.CheckConstraint(
            "condition_code IN ('clear','rain','snow','wind','fog','ice','other')",
            name="ck_weather_observation_condition",
        ),
        sa.CheckConstraint(
            "station_unlocode ~ '^[A-Z]{2}[A-Z0-9]{3}$'",
            name="ck_weather_observation_station",
        ),
        sa.CheckConstraint("provider_code = 'hitl'", name="ck_weather_observation_provider"),
    )
    # Lista per tenant — RLS filtruje organization_id; unique source_ref nie zastępuje tego skanu.
    op.create_index(
        "ix_weather_observation_organization_id",
        "weather_observation",
        ["organization_id"],
    )
    op.execute("ALTER TABLE weather_observation ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE weather_observation FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY weather_observation_tenant_isolation ON weather_observation
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS weather_observation_tenant_isolation ON weather_observation")
    op.drop_index("ix_weather_observation_organization_id", table_name="weather_observation")
    op.drop_table("weather_observation")
