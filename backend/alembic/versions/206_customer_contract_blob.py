"""add nullable opaque blob on customer_contract

Revision ID: 206_customer_contract_blob
Revises: 205_customer_contract
Create Date: 2026-09-10

HITL opaque fixture BYTEA. Nie szyfr. Nie KEK. RLS zostaje z 205.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import BYTEA

revision: str = "206_customer_contract_blob"
down_revision: str | None = "205_customer_contract"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "customer_contract",
        sa.Column("blob_ciphertext", BYTEA(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("customer_contract", "blob_ciphertext")
