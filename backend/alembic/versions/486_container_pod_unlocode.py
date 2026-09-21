"""add optional pod_unlocode on container

Revision ID: 486_container_pod_unlocode
Revises: 485_container_pol_unlocode
Create Date: 2026-09-21

Opcjonalny UN/LOCODE portu wyładunku HITL. Nie FK portu. Nie mapa.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "486_container_pod_unlocode"
down_revision: str | None = "485_container_pol_unlocode"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("pod_unlocode", sa.String(5), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "pod_unlocode")
