"""create telematics_connector catalog with RLS FORCE

Revision ID: 137_telematics_connector
Revises: 136_free_time_clock
Create Date: 2026-09-09

HITL reżim + dostawca. Nie poll. Nie sekrety.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "137_telematics_connector"
down_revision: str | None = "136_free_time_clock"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "telematics_connector",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("observation_kind", sa.String(length=16), nullable=False),
        sa.Column("provider_code", sa.String(length=16), nullable=False),
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
            name="fk_telematics_connector_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_telematics_connector_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_telematics_connector_org_source_ref",
        ),
        sa.CheckConstraint(
            "observation_kind IN ('omni_telematic','external_api')",
            name="ck_telematics_connector_kind",
        ),
        sa.CheckConstraint(
            "provider_code IN ('gbox','ikol','flotis','wialon','other')",
            name="ck_telematics_connector_provider",
        ),
    )
    # Lista per tenant — RLS filtruje organization_id; unique source_ref nie zastępuje tego skanu.
    op.create_index(
        "ix_telematics_connector_organization_id",
        "telematics_connector",
        ["organization_id"],
    )
    op.execute("ALTER TABLE telematics_connector ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE telematics_connector FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY telematics_connector_tenant_isolation ON telematics_connector
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS telematics_connector_tenant_isolation ON telematics_connector"
    )
    op.drop_index("ix_telematics_connector_organization_id", table_name="telematics_connector")
    op.drop_table("telematics_connector")
