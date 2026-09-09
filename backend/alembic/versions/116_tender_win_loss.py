"""create tender_win_loss catalog with RLS FORCE

Revision ID: 116_tender_win_loss
Revises: 115_tender_playbook
Create Date: 2026-09-09

Win/loss: wynik + source_ref. Nie extract RFP. Nie kwota. Nie mutacja tender.status.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "116_tender_win_loss"
down_revision: str | None = "115_tender_playbook"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "tender_win_loss",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tender_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("outcome", sa.String(length=16), nullable=False),
        sa.Column("reason_code", sa.String(length=32), nullable=False),
        sa.Column("source_ref", sa.String(length=256), nullable=False),
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
            name="fk_tender_win_loss_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_win_loss_tender",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_tender_win_loss_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "tender_id",
            name="uq_tender_win_loss_org_tender",
        ),
        sa.CheckConstraint(
            "outcome IN ('won', 'lost', 'no_bid')",
            name="ck_tender_win_loss_outcome",
        ),
        sa.CheckConstraint(
            "reason_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_tender_win_loss_reason",
        ),
    )
    op.create_index(
        "ix_tender_win_loss_organization_id",
        "tender_win_loss",
        ["organization_id"],
    )
    op.create_index(
        "ix_tender_win_loss_org_outcome",
        "tender_win_loss",
        ["organization_id", "outcome"],
    )
    op.execute("ALTER TABLE tender_win_loss ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE tender_win_loss FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY tender_win_loss_tenant_isolation ON tender_win_loss
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS tender_win_loss_tenant_isolation ON tender_win_loss")
    op.drop_index("ix_tender_win_loss_org_outcome", table_name="tender_win_loss")
    op.drop_index("ix_tender_win_loss_organization_id", table_name="tender_win_loss")
    op.drop_table("tender_win_loss")
