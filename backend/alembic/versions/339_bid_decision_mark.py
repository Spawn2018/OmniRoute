"""create bid_decision_mark catalog with RLS FORCE

Revision ID: 339_bid_decision_mark
Revises: 338_spot_contract_mark
Create Date: 2026-09-13

EXP1 HITL bid_decision_mark. Nie kolumna na quotation. Nie auto-award.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "339_bid_decision_mark"
down_revision: str | None = "338_spot_contract_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "bid_decision_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("decision_kind", sa.String(length=16), nullable=False),
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
            name="fk_bid_decision_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_bid_decision_mark_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_bid_decision_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_bid_decision_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_bid_decision_mark_code",
        ),
        sa.CheckConstraint(
            "decision_kind IN ('go', 'no_go', 'hold', 'other')",
            name="ck_bid_decision_mark_decision_kind",
        ),
    )
    op.create_index(
        "ix_bid_decision_mark_organization_id",
        "bid_decision_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE bid_decision_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE bid_decision_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY bid_decision_mark_tenant_isolation ON bid_decision_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS bid_decision_mark_tenant_isolation ON bid_decision_mark",
    )
    op.drop_index(
        "ix_bid_decision_mark_organization_id",
        table_name="bid_decision_mark",
    )
    op.drop_table("bid_decision_mark")
