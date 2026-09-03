"""create shipment_leg with RLS FORCE

Revision ID: 065_shipment_leg_rls
Revises: 064_gdpr_request_rls
Create Date: 2026-09-03

Odcinek drogowy na zleceniu. Nie mapa. Nie GPS. Nie kwota.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "065_shipment_leg_rls"
down_revision: str | None = "064_gdpr_request_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "shipment_leg",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("shipment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("origin_location_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("destination_location_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("leg_kind", sa.String(length=16), nullable=False),
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
            name="fk_shipment_leg_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_shipment_leg_shipment",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "origin_location_id"],
            ["location.organization_id", "location.id"],
            name="fk_shipment_leg_origin",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "destination_location_id"],
            ["location.organization_id", "location.id"],
            name="fk_shipment_leg_destination",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint("leg_kind = 'road'", name="ck_shipment_leg_kind"),
        sa.CheckConstraint(
            "origin_location_id <> destination_location_id",
            name="ck_shipment_leg_distinct_ends",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "shipment_id",
            "leg_kind",
            name="uq_shipment_leg_org_kind",
        ),
    )
    op.create_index(
        "ix_shipment_leg_organization_id",
        "shipment_leg",
        ["organization_id"],
    )
    op.create_index(
        "ix_shipment_leg_org_shipment",
        "shipment_leg",
        ["organization_id", "shipment_id"],
    )
    op.execute("ALTER TABLE shipment_leg ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE shipment_leg FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY shipment_leg_tenant_isolation
        ON shipment_leg
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS shipment_leg_tenant_isolation ON shipment_leg")
    op.drop_index("ix_shipment_leg_org_shipment", table_name="shipment_leg")
    op.drop_index("ix_shipment_leg_organization_id", table_name="shipment_leg")
    op.drop_table("shipment_leg")
