"""create asn catalog with RLS FORCE

Revision ID: 211_asn
Revises: 210_po_line
Create Date: 2026-09-11

HITL awizo wysyłki jako dane. Nie live EDI. Nie shipment. Nie kwota.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "211_asn"
down_revision: str | None = "210_po_line"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "asn",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("purchase_order_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("asn_code", sa.String(length=32), nullable=False),
        sa.Column("plant_label", sa.String(length=128), nullable=True),
        sa.Column("carrier_label", sa.String(length=128), nullable=True),
        sa.Column("ship_ref_label", sa.String(length=128), nullable=True),
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
            name="fk_asn_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "purchase_order_id"],
            ["purchase_order.organization_id", "purchase_order.id"],
            name="fk_asn_purchase_order",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_asn_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "purchase_order_id",
            "asn_code",
            name="uq_asn_org_header_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_asn_org_source_ref",
        ),
        sa.CheckConstraint(
            "asn_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_asn_code",
        ),
        sa.CheckConstraint(
            "plant_label IS NULL OR char_length(btrim(plant_label)) BETWEEN 1 AND 128",
            name="ck_asn_plant",
        ),
        sa.CheckConstraint(
            "carrier_label IS NULL OR char_length(btrim(carrier_label)) BETWEEN 1 AND 128",
            name="ck_asn_carrier",
        ),
        sa.CheckConstraint(
            "ship_ref_label IS NULL OR char_length(btrim(ship_ref_label)) BETWEEN 1 AND 128",
            name="ck_asn_ship_ref",
        ),
    )
    op.create_index("ix_asn_organization_id", "asn", ["organization_id"])
    op.create_index(
        "ix_asn_org_header",
        "asn",
        ["organization_id", "purchase_order_id"],
    )
    op.execute("ALTER TABLE asn ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE asn FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY asn_tenant_isolation ON asn
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS asn_tenant_isolation ON asn")
    op.drop_index("ix_asn_org_header", table_name="asn")
    op.drop_index("ix_asn_organization_id", table_name="asn")
    op.drop_table("asn")
