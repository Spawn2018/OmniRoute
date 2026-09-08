"""create shipment_package on shipment with RLS FORCE

Revision ID: 096_shipment_package
Revises: 095_groupage_line
Create Date: 2026-09-08

Paczka na zleceniu. Skan QR Omni + stop trasy. Nie WMS.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "096_shipment_package"
down_revision: str | None = "095_groupage_line"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_stop_org_shipment_id",
        "stop",
        ["organization_id", "shipment_id", "id"],
    )
    op.create_table(
        "shipment_package",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("shipment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("stop_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("package_code", sa.String(length=32), nullable=False),
        sa.Column("package_status", sa.String(length=16), nullable=False),
        sa.Column("scan_token", sa.Text(), nullable=False),
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
            name="fk_shipment_package_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_shipment_package_shipment",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "shipment_id", "stop_id"],
            ["stop.organization_id", "stop.shipment_id", "stop.id"],
            name="fk_shipment_package_stop",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_shipment_package_org_id"),
        sa.CheckConstraint(
            "package_status IN ('noted','at_stop','in_transit','delivered')",
            name="ck_shipment_package_status",
        ),
    )
    op.create_index(
        "ix_shipment_package_organization_id",
        "shipment_package",
        ["organization_id"],
    )
    op.create_index(
        "ix_shipment_package_org_shipment",
        "shipment_package",
        ["organization_id", "shipment_id"],
    )
    op.execute("ALTER TABLE shipment_package ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE shipment_package FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY shipment_package_tenant_isolation ON shipment_package
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS shipment_package_tenant_isolation ON shipment_package")
    op.drop_index("ix_shipment_package_org_shipment", table_name="shipment_package")
    op.drop_index("ix_shipment_package_organization_id", table_name="shipment_package")
    op.drop_table("shipment_package")
    op.drop_constraint("uq_stop_org_shipment_id", "stop", type_="unique")
