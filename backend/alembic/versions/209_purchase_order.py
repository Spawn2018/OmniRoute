"""create purchase_order header catalog with RLS FORCE

Revision ID: 209_purchase_order
Revises: 208_visibility_connector
Create Date: 2026-09-10

HITL nagłówek zamówienia zakupu jako dane. Nie linia SKU. Nie ASN. Nie shipment.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "209_purchase_order"
down_revision: str | None = "208_visibility_connector"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "purchase_order",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("po_code", sa.String(length=32), nullable=False),
        sa.Column("plant_label", sa.String(length=128), nullable=True),
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
            name="fk_purchase_order_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_purchase_order_org_id"),
        sa.UniqueConstraint("organization_id", "po_code", name="uq_purchase_order_org_code"),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_purchase_order_org_source_ref",
        ),
        sa.CheckConstraint(
            "po_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_purchase_order_code",
        ),
        sa.CheckConstraint(
            "plant_label IS NULL OR char_length(btrim(plant_label)) BETWEEN 1 AND 128",
            name="ck_purchase_order_plant",
        ),
    )
    # Lista per tenant: unique prefix albo ten indeks — nie sekwencyjne skanowanie.
    op.create_index(
        "ix_purchase_order_organization_id",
        "purchase_order",
        ["organization_id"],
    )
    op.execute("ALTER TABLE purchase_order ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE purchase_order FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY purchase_order_tenant_isolation ON purchase_order
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS purchase_order_tenant_isolation ON purchase_order")
    op.drop_index("ix_purchase_order_organization_id", table_name="purchase_order")
    op.drop_table("purchase_order")
