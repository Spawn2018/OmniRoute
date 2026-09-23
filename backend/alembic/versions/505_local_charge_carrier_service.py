"""add optional carrier_label and service_label on local_charge leftover P4b

Revision ID: 505_local_charge_carrier_service
Revises: 504_network_print_gate_mark
Create Date: 2026-09-23

Etykiety armator/serwis jako dane HITL. Bez FK party. Bez live HTTP.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "505_local_charge_carrier_service"
down_revision: str | None = "504_network_print_gate_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "local_charge",
        sa.Column("carrier_label", sa.String(length=64), nullable=True),
    )
    op.add_column(
        "local_charge",
        sa.Column("service_label", sa.String(length=64), nullable=True),
    )
    op.create_check_constraint(
        "ck_local_charge_carrier_label",
        "local_charge",
        "carrier_label IS NULL OR char_length(btrim(carrier_label)) BETWEEN 1 AND 64",
    )
    op.create_check_constraint(
        "ck_local_charge_service_label",
        "local_charge",
        "service_label IS NULL OR char_length(btrim(service_label)) BETWEEN 1 AND 64",
    )
    op.drop_constraint(
        "uq_local_charge_org_kind_port_type",
        "local_charge",
        type_="unique",
    )
    op.create_unique_constraint(
        "uq_local_charge_org_kind_port_type_carrier_service",
        "local_charge",
        [
            "organization_id",
            "charge_kind",
            "port_unlocode",
            "iso_size_type",
            "carrier_label",
            "service_label",
        ],
        postgresql_nulls_not_distinct=True,
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_local_charge_org_kind_port_type_carrier_service",
        "local_charge",
        type_="unique",
    )
    op.drop_constraint("ck_local_charge_service_label", "local_charge", type_="check")
    op.drop_constraint("ck_local_charge_carrier_label", "local_charge", type_="check")
    op.drop_column("local_charge", "service_label")
    op.drop_column("local_charge", "carrier_label")
    op.create_unique_constraint(
        "uq_local_charge_org_kind_port_type",
        "local_charge",
        ["organization_id", "charge_kind", "port_unlocode", "iso_size_type"],
    )
