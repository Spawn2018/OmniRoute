"""allow graph:// ingest with external_id idempotency

Revision ID: 038_inbound_graph_ingest
Revises: 037_operator_decision_lock
Create Date: 2026-09-03

Ingest Graph to ta sama tabela. Nie live HTTP. Nie send.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "038_inbound_graph_ingest"
down_revision: str | None = "037_operator_decision_lock"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "inbound_message",
        sa.Column("external_id", sa.String(length=256), nullable=True),
    )
    op.create_index(
        "uq_inbound_message_org_external",
        "inbound_message",
        ["organization_id", "external_id"],
        unique=True,
        postgresql_where=sa.text("external_id IS NOT NULL"),
    )
    op.drop_constraint(
        "ck_inbound_message_source_fixture",
        "inbound_message",
        type_="check",
    )
    op.create_check_constraint(
        "ck_inbound_message_source_fixture",
        "inbound_message",
        "source_ref ~ '^(fixture|synth|graph)://'",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_inbound_message_source_fixture",
        "inbound_message",
        type_="check",
    )
    op.create_check_constraint(
        "ck_inbound_message_source_fixture",
        "inbound_message",
        "source_ref ~ '^(fixture|synth)://'",
    )
    op.drop_index("uq_inbound_message_org_external", table_name="inbound_message")
    op.drop_column("inbound_message", "external_id")
