"""add optional iso_size_type on local_charge leftover P4b

Revision ID: 148_local_charge_iso
Revises: 147_local_charge_port
Create Date: 2026-09-09

Opcjonalny iso_size_type jako dana. Bez FK container. Bez numeru BIC.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "148_local_charge_iso"
down_revision: str | None = "147_local_charge_port"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "local_charge",
        sa.Column("iso_size_type", sa.String(length=4), nullable=True),
    )
    op.create_check_constraint(
        "ck_local_charge_iso_size_type",
        "local_charge",
        "iso_size_type IS NULL OR iso_size_type ~ '^[0-9]{2}[A-Z][A-Z0-9]$'",
    )
    op.drop_constraint("uq_local_charge_org_kind_port", "local_charge", type_="unique")
    op.create_unique_constraint(
        "uq_local_charge_org_kind_port_type",
        "local_charge",
        ["organization_id", "charge_kind", "port_unlocode", "iso_size_type"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_local_charge_org_kind_port_type",
        "local_charge",
        type_="unique",
    )
    op.drop_constraint("ck_local_charge_iso_size_type", "local_charge", type_="check")
    op.drop_column("local_charge", "iso_size_type")
    op.create_unique_constraint(
        "uq_local_charge_org_kind_port",
        "local_charge",
        ["organization_id", "charge_kind", "port_unlocode"],
    )
