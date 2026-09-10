"""add optional pod_quality on stop leftover T1 EXP1

Revision ID: 191_stop_pod_quality
Revises: 190_stop_waiting_started
Create Date: 2026-09-10

Opcjonalna jakość POD HITL. Nie kamera. Nie bajty. Nie nowa tabela.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "191_stop_pod_quality"
down_revision: str | None = "190_stop_waiting_started"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "stop",
        sa.Column("pod_quality", sa.String(length=12), nullable=True),
    )
    op.create_check_constraint(
        "ck_stop_pod_quality",
        "stop",
        "pod_quality IS NULL OR pod_quality IN ('ok', 'retake', 'missing')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_stop_pod_quality", "stop", type_="check")
    op.drop_column("stop", "pod_quality")
