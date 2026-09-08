"""add party eori/duns and unique business tokens leftover M10-1

Revision ID: 074_party_business_ids
Revises: 073_network_member_party
Create Date: 2026-09-08

Stare wiersze zostają bez numeru. Nowy INSERT wymaga ID w serwisie.
Nie backfill. Nie M10-2.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "074_party_business_ids"
down_revision: str | None = "073_network_member_party"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("party", sa.Column("eori", sa.String(length=32), nullable=True))
    op.add_column("party", sa.Column("duns", sa.String(length=16), nullable=True))
    op.execute(
        "CREATE UNIQUE INDEX uq_party_org_vat_eu "
        "ON party (organization_id, vat_eu) WHERE vat_eu IS NOT NULL"
    )
    op.execute(
        "CREATE UNIQUE INDEX uq_party_org_eori "
        "ON party (organization_id, eori) WHERE eori IS NOT NULL"
    )
    op.execute(
        "CREATE UNIQUE INDEX uq_party_org_duns "
        "ON party (organization_id, duns) WHERE duns IS NOT NULL"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS uq_party_org_duns")
    op.execute("DROP INDEX IF EXISTS uq_party_org_eori")
    op.execute("DROP INDEX IF EXISTS uq_party_org_vat_eu")
    op.drop_column("party", "duns")
    op.drop_column("party", "eori")
