"""create dock_appointment on stop with RLS FORCE

Revision ID: 097_dock_appointment
Revises: 096_shipment_package
Create Date: 2026-09-08

Awizacja doku na stop magazynu. Okno TIME. Nie WMS.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "097_dock_appointment"
down_revision: str | None = "096_shipment_package"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "dock_appointment",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("shipment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("stop_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("appointment_code", sa.String(length=32), nullable=False),
        sa.Column("appointment_status", sa.String(length=16), nullable=False),
        sa.Column("window_date", sa.Date(), nullable=False),
        sa.Column("window_start_local", sa.Time(), nullable=False),
        sa.Column("window_end_local", sa.Time(), nullable=False),
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
            name="fk_dock_appointment_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_dock_appointment_shipment",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "shipment_id", "stop_id"],
            ["stop.organization_id", "stop.shipment_id", "stop.id"],
            name="fk_dock_appointment_stop",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_dock_appointment_org_id"),
        sa.CheckConstraint(
            "appointment_status IN ('noted','advised','at_dock','released')",
            name="ck_dock_appointment_status",
        ),
        sa.CheckConstraint(
            "window_end_local > window_start_local",
            name="ck_dock_appointment_window",
        ),
    )
    op.create_index(
        "ix_dock_appointment_organization_id",
        "dock_appointment",
        ["organization_id"],
    )
    op.create_index(
        "ix_dock_appointment_org_stop",
        "dock_appointment",
        ["organization_id", "stop_id"],
    )
    op.execute("ALTER TABLE dock_appointment ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE dock_appointment FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY dock_appointment_tenant_isolation ON dock_appointment
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS dock_appointment_tenant_isolation ON dock_appointment")
    op.drop_index("ix_dock_appointment_org_stop", table_name="dock_appointment")
    op.drop_index("ix_dock_appointment_organization_id", table_name="dock_appointment")
    op.drop_table("dock_appointment")
