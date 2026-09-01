"""add POL/POD and party snapshot columns on quotation

Revision ID: 016_quotation_port_party
Revises: 015_party_rls
Create Date: 2026-09-01

Port i kontrahent nie dobierają stawki — UUID z requestu, kwota nadal z rate_line.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "016_quotation_port_party"
down_revision: str | None = "015_party_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_COMPLETE = (
    "(origin_port_id IS NULL AND destination_port_id IS NULL AND party_id IS NULL) OR "
    "(origin_port_id IS NOT NULL AND destination_port_id IS NOT NULL AND party_id IS NOT NULL)"
)


def upgrade() -> None:
    op.add_column(
        "quotation",
        sa.Column("origin_port_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.add_column(
        "quotation",
        sa.Column("destination_port_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.add_column(
        "quotation",
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_quotation_origin_port",
        "quotation",
        "port",
        ["organization_id", "origin_port_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "fk_quotation_destination_port",
        "quotation",
        "port",
        ["organization_id", "destination_port_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "fk_quotation_party",
        "quotation",
        "party",
        ["organization_id", "party_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )
    op.create_check_constraint(
        "ck_quotation_lane_party_complete",
        "quotation",
        _COMPLETE,
    )
    op.create_index("ix_quotation_org_party_id", "quotation", ["organization_id", "party_id"])
    op.create_index(
        "ix_quotation_org_origin_port_id",
        "quotation",
        ["organization_id", "origin_port_id"],
    )
    op.create_index(
        "ix_quotation_org_destination_port_id",
        "quotation",
        ["organization_id", "destination_port_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_quotation_org_destination_port_id", table_name="quotation")
    op.drop_index("ix_quotation_org_origin_port_id", table_name="quotation")
    op.drop_index("ix_quotation_org_party_id", table_name="quotation")
    op.drop_constraint("ck_quotation_lane_party_complete", "quotation", type_="check")
    op.drop_constraint("fk_quotation_party", "quotation", type_="foreignkey")
    op.drop_constraint("fk_quotation_destination_port", "quotation", type_="foreignkey")
    op.drop_constraint("fk_quotation_origin_port", "quotation", type_="foreignkey")
    op.drop_column("quotation", "party_id")
    op.drop_column("quotation", "destination_port_id")
    op.drop_column("quotation", "origin_port_id")
