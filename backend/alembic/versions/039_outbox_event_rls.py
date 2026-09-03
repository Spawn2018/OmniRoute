"""create outbox_event with RLS FORCE

Revision ID: 039_outbox_event_rls
Revises: 038_inbound_graph_ingest
Create Date: 2026-09-03

Pierwsze zdarzenie inbound_message_saved. Nie Temporal. Nie konsument.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "039_outbox_event_rls"
down_revision: str | None = "038_inbound_graph_ingest"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "outbox_event",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("event_kind", sa.String(length=32), nullable=False),
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(length=8), nullable=False),
        sa.Column("source_ref", sa.String(length=512), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
            name="fk_outbox_event_organization_id",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "event_kind = 'inbound_message_saved'",
            name="ck_outbox_event_kind",
        ),
        sa.CheckConstraint("status = 'pending'", name="ck_outbox_event_status"),
        sa.UniqueConstraint(
            "organization_id",
            "event_kind",
            "subject_id",
            name="uq_outbox_event_org_kind_subject",
        ),
    )
    op.create_index(
        "ix_outbox_event_organization_id",
        "outbox_event",
        ["organization_id"],
    )
    op.create_index(
        "ix_outbox_event_org_created",
        "outbox_event",
        ["organization_id", "created_at"],
    )
    op.execute("ALTER TABLE outbox_event ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE outbox_event FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY outbox_event_tenant_isolation ON outbox_event
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS outbox_event_tenant_isolation ON outbox_event")
    op.drop_index("ix_outbox_event_org_created", table_name="outbox_event")
    op.drop_index("ix_outbox_event_organization_id", table_name="outbox_event")
    op.drop_table("outbox_event")
