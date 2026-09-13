"""create telematics_device catalog with RLS FORCE

Revision ID: 363_telematics_device
Revises: 362_position_event
Create Date: 2026-09-13

BR2.1 HITL katalog urzadzenia. Nie parowanie. Nie poll.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "363_telematics_device"
down_revision: str | None = "362_position_event"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "telematics_device",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("device_code", sa.String(length=32), nullable=False),
        sa.Column("device_kind", sa.String(length=16), nullable=False),
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
            name="fk_telematics_device_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_telematics_device_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "device_code",
            name="uq_telematics_device_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_telematics_device_org_source_ref",
        ),
        sa.CheckConstraint(
            "device_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_telematics_device_code",
        ),
        sa.CheckConstraint(
            "device_kind IN ('tracker', 'fault', 'other')",
            name="ck_telematics_device_kind",
        ),
    )
    op.create_index(
        "ix_telematics_device_organization_id",
        "telematics_device",
        ["organization_id"],
    )
    op.execute("ALTER TABLE telematics_device ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE telematics_device FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY telematics_device_tenant_isolation ON telematics_device
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS telematics_device_tenant_isolation ON telematics_device",
    )
    op.drop_index(
        "ix_telematics_device_organization_id",
        table_name="telematics_device",
    )
    op.drop_table("telematics_device")
