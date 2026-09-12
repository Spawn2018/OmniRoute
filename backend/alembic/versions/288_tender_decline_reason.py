"""create tender_decline_reason catalog with RLS FORCE

Revision ID: 271_tender_decline_reason
Revises: 276_MQC_mark
Create Date: 2026-09-12

EXP3.12 HITL znacznik MQC jako dane. Nie live giełda. Nie RFP scrape.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "288_tender_decline_reason"
down_revision: str | None = "287_general_average_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "tender_decline_reason",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("decline_kind", sa.String(length=16), nullable=False),
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
        sa.Column("created_by", PGUUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
            name="fk_tender_decline_reason_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_tender_decline_reason_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_tender_decline_reason_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_tender_decline_reason_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_tender_decline_reason_code",
        ),
        sa.CheckConstraint(
            "decline_kind IN ('decline', 'no_bid', 'withdraw', 'other')",
            name="ck_tender_decline_reason_decline_kind",
        ),
    )
    op.create_index(
        "ix_tender_decline_reason_organization_id",
        "tender_decline_reason",
        ["organization_id"],
    )
    op.execute("ALTER TABLE tender_decline_reason ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE tender_decline_reason FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY tender_decline_reason_tenant_isolation ON tender_decline_reason
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS tender_decline_reason_tenant_isolation ON tender_decline_reason",
    )
    op.drop_index(
        "ix_tender_decline_reason_organization_id",
        table_name="tender_decline_reason",
    )
    op.drop_table("tender_decline_reason")
