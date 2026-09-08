"""add network_member.party_id leftover O0

Revision ID: 073_network_member_party
Revises: 072_charge_source_ref
Create Date: 2026-09-08

Stare człony zostają NULL. Nowy INSERT wymaga party_id w serwisie.
FK tenanta. Nie ranking.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "073_network_member_party"
down_revision: str | None = "072_charge_source_ref"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "network_member",
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_network_member_party",
        "network_member",
        "party",
        ["organization_id", "party_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )
    op.create_index(
        "ix_network_member_org_party_id",
        "network_member",
        ["organization_id", "party_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_network_member_org_party_id", table_name="network_member")
    op.drop_constraint("fk_network_member_party", "network_member", type_="foreignkey")
    op.drop_column("network_member", "party_id")
