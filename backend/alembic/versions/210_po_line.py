"""create po_line catalog with RLS FORCE

Revision ID: 210_po_line
Revises: 209_purchase_order
Create Date: 2026-09-10

HITL linia zamówienia zakupu jako dane. Nie ASN. Nie shipment. Nie kwota.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "210_po_line"
down_revision: str | None = "209_purchase_order"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "po_line",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("purchase_order_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("line_code", sa.String(length=32), nullable=False),
        sa.Column("sku_code", sa.String(length=64), nullable=False),
        sa.Column("qty", sa.Numeric(14, 4), nullable=False),
        sa.Column("uom_code", sa.String(length=16), nullable=False),
        sa.Column("plant_label", sa.String(length=128), nullable=True),
        sa.Column("batch_label", sa.String(length=128), nullable=True),
        sa.Column("serial_label", sa.String(length=128), nullable=True),
        sa.Column("coo_label", sa.String(length=128), nullable=True),
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
            name="fk_po_line_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "purchase_order_id"],
            ["purchase_order.organization_id", "purchase_order.id"],
            name="fk_po_line_purchase_order",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_po_line_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "purchase_order_id",
            "line_code",
            name="uq_po_line_org_header_line",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_po_line_org_source_ref",
        ),
        sa.CheckConstraint(
            "line_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_po_line_code",
        ),
        sa.CheckConstraint("qty >= 0", name="ck_po_line_qty"),
        sa.CheckConstraint(
            "char_length(btrim(sku_code)) BETWEEN 1 AND 64",
            name="ck_po_line_sku",
        ),
        sa.CheckConstraint(
            "char_length(btrim(uom_code)) BETWEEN 1 AND 16",
            name="ck_po_line_uom",
        ),
        sa.CheckConstraint(
            "plant_label IS NULL OR char_length(btrim(plant_label)) BETWEEN 1 AND 128",
            name="ck_po_line_plant",
        ),
        sa.CheckConstraint(
            "batch_label IS NULL OR char_length(btrim(batch_label)) BETWEEN 1 AND 128",
            name="ck_po_line_batch",
        ),
        sa.CheckConstraint(
            "serial_label IS NULL OR char_length(btrim(serial_label)) BETWEEN 1 AND 128",
            name="ck_po_line_serial",
        ),
        sa.CheckConstraint(
            "coo_label IS NULL OR char_length(btrim(coo_label)) BETWEEN 1 AND 128",
            name="ck_po_line_coo",
        ),
    )
    op.create_index("ix_po_line_organization_id", "po_line", ["organization_id"])
    op.create_index(
        "ix_po_line_org_header",
        "po_line",
        ["organization_id", "purchase_order_id"],
    )
    op.execute("ALTER TABLE po_line ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE po_line FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY po_line_tenant_isolation ON po_line
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS po_line_tenant_isolation ON po_line")
    op.drop_index("ix_po_line_org_header", table_name="po_line")
    op.drop_index("ix_po_line_organization_id", table_name="po_line")
    op.drop_table("po_line")
