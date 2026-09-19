"""add optional container_release_party_id on container leftover T3

Revision ID: 464_container_release
Revises: 463_container_ext_power
Create Date: 2026-09-19

Opcjonalny FK zwolnienia kontenera. Zlozone FK per tenant. Nie live HTTP.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "464_container_release"
down_revision: str | None = "463_container_ext_power"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("container_release_party_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_container_release_party",
        "container",
        "party",
        ["organization_id", "container_release_party_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint("fk_container_release_party", "container", type_="foreignkey")
    op.drop_column("container", "container_release_party_id")
