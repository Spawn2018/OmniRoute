"""add operator_decision.lock_version for optimistic decide

Revision ID: 037_operator_decision_lock
Revises: 036_mail_draft_rls
Create Date: 2026-09-03

Dwa okna, dwa Akceptuj — jeden UPDATE wygrywa.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "037_operator_decision_lock"
down_revision: str | None = "036_mail_draft_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "operator_decision",
        sa.Column(
            "lock_version",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
    )
    op.alter_column("operator_decision", "lock_version", server_default=None)


def downgrade() -> None:
    op.drop_column("operator_decision", "lock_version")
