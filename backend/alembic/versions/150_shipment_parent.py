"""add optional parent_shipment_id on shipment leftover T4

Revision ID: 150_shipment_parent
Revises: 149_shipment_leg_air_waybill
Create Date: 2026-09-09

Opcjonalny rodzic + rodzaj relacji jako dana. Bez widoku rentowności.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "150_shipment_parent"
down_revision: str | None = "149_shipment_leg_air_waybill"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "shipment",
        sa.Column("parent_shipment_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.add_column(
        "shipment",
        sa.Column("relation_kind", sa.String(length=32), nullable=True),
    )
    op.create_foreign_key(
        "fk_shipment_parent",
        "shipment",
        "shipment",
        ["organization_id", "parent_shipment_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )
    op.create_check_constraint(
        "ck_shipment_parent_pair",
        "shipment",
        "(parent_shipment_id IS NULL AND relation_kind IS NULL) OR "
        "(parent_shipment_id IS NOT NULL AND relation_kind IS NOT NULL AND "
        "relation_kind IN "
        "('drayage', 'oncarriage', 'leg_subcontract', 'other'))",
    )
    op.create_check_constraint(
        "ck_shipment_parent_not_self",
        "shipment",
        "parent_shipment_id IS NULL OR parent_shipment_id <> id",
    )
    op.create_index(
        "ix_shipment_org_parent",
        "shipment",
        ["organization_id", "parent_shipment_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_shipment_org_parent", table_name="shipment")
    op.drop_constraint("ck_shipment_parent_not_self", "shipment", type_="check")
    op.drop_constraint("ck_shipment_parent_pair", "shipment", type_="check")
    op.drop_constraint("fk_shipment_parent", "shipment", type_="foreignkey")
    op.drop_column("shipment", "relation_kind")
    op.drop_column("shipment", "parent_shipment_id")
