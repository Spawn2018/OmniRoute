"""create shipment_monitoring_filing catalog with RLS FORCE

Revision ID: 433_shipment_monitoring_filing
Revises: 432_postal_dispatch_mark
Create Date: 2026-09-17

C1 HITL shipment_monitoring_filing. Nie live PUESC. Nie XML SENT.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "433_shipment_monitoring_filing"
down_revision: str | None = "432_postal_dispatch_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "shipment_monitoring_filing",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("filing_code", sa.String(length=32), nullable=False),
        sa.Column("status_kind", sa.String(length=16), nullable=False),
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
            name="fk_shipment_monitoring_filing_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_shipment_monitoring_filing_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "filing_code",
            name="uq_shipment_monitoring_filing_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_shipment_monitoring_filing_org_source_ref",
        ),
        sa.CheckConstraint(
            "filing_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_shipment_monitoring_filing_code",
        ),
        sa.CheckConstraint(
            "status_kind IN ('open', 'filed', 'closed', 'other')",
            name="ck_shipment_monitoring_filing_status_kind",
        ),
    )
    op.create_index(
        "ix_shipment_monitoring_filing_organization_id",
        "shipment_monitoring_filing",
        ["organization_id"],
    )
    op.execute("ALTER TABLE shipment_monitoring_filing ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE shipment_monitoring_filing FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY shipment_monitoring_filing_tenant_isolation ON shipment_monitoring_filing
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS shipment_monitoring_filing_tenant_isolation "
        "ON shipment_monitoring_filing",
    )
    op.drop_index(
        "ix_shipment_monitoring_filing_organization_id",
        table_name="shipment_monitoring_filing",
    )
    op.drop_table("shipment_monitoring_filing")
