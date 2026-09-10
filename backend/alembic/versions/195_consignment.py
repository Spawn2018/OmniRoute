"""create consignment on shipment with RLS FORCE

Revision ID: 195_consignment
Revises: 194_trip_subcontractor
Create Date: 2026-09-10

Przesyłka N1 obok zlecenia. N wierszy na shipment. Nie FTL unique. Nie paczka.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "195_consignment"
down_revision: str | None = "194_trip_subcontractor"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "consignment",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("shipment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("consignment_ref", sa.String(length=64), nullable=False),
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
            name="fk_consignment_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_consignment_shipment",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_consignment_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "consignment_ref",
            name="uq_consignment_org_ref",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_consignment_org_source",
        ),
    )
    op.create_index(
        "ix_consignment_organization_id",
        "consignment",
        ["organization_id"],
    )
    op.create_index(
        "ix_consignment_org_shipment",
        "consignment",
        ["organization_id", "shipment_id"],
    )
    op.execute("ALTER TABLE consignment ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE consignment FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY consignment_tenant_isolation ON consignment
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS consignment_tenant_isolation ON consignment")
    op.drop_index("ix_consignment_org_shipment", table_name="consignment")
    op.drop_index("ix_consignment_organization_id", table_name="consignment")
    op.drop_table("consignment")
