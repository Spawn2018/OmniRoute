"""optional stop_group_id on stop leftover T1b bind

Revision ID: 477_stop_group_bind
Revises: 476_stop_group
Create Date: 2026-09-20

Opcjonalny FK grupy punktów na stopie. Unique na stop_group dla złożonego FK.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "477_stop_group_bind"
down_revision: str | None = "476_stop_group"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_stop_group_org_shipment_id",
        "stop_group",
        ["organization_id", "shipment_id", "id"],
    )
    op.add_column(
        "stop",
        sa.Column("stop_group_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_stop_stop_group",
        "stop",
        "stop_group",
        ["organization_id", "shipment_id", "stop_group_id"],
        ["organization_id", "shipment_id", "id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint("fk_stop_stop_group", "stop", type_="foreignkey")
    op.drop_column("stop", "stop_group_id")
    op.drop_constraint("uq_stop_group_org_shipment_id", "stop_group", type_="unique")
