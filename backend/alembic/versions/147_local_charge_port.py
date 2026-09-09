"""add optional port_unlocode on local_charge leftover P4b

Revision ID: 147_local_charge_port
Revises: 146_charge_template_span
Create Date: 2026-09-09

Opcjonalny UN/LOCODE jako dana. Bez FK geography. Bez warning braków.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "147_local_charge_port"
down_revision: str | None = "146_charge_template_span"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "local_charge",
        sa.Column("port_unlocode", sa.String(length=5), nullable=True),
    )
    op.create_check_constraint(
        "ck_local_charge_port_unlocode",
        "local_charge",
        "port_unlocode IS NULL OR port_unlocode ~ '^[A-Z]{2}[A-Z0-9]{3}$'",
    )
    op.create_unique_constraint(
        "uq_local_charge_org_kind_port",
        "local_charge",
        ["organization_id", "charge_kind", "port_unlocode"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_local_charge_org_kind_port", "local_charge", type_="unique")
    op.drop_constraint("ck_local_charge_port_unlocode", "local_charge", type_="check")
    op.drop_column("local_charge", "port_unlocode")
