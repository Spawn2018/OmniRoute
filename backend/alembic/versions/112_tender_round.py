"""create tender_round catalog with RLS FORCE

Revision ID: 112_tender_round
Revises: 111_tender_lane
Create Date: 2026-09-09

Runda przetargu. Nie data room. Nie kwota.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "112_tender_round"
down_revision: str | None = "111_tender_lane"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "tender_round",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tender_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("round_no", sa.Integer(), nullable=False),
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
            name="fk_tender_round_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_round_tender",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_tender_round_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "tender_id",
            "round_no",
            name="uq_tender_round_org_tender_no",
        ),
        sa.CheckConstraint("round_no >= 1", name="ck_tender_round_no"),
    )
    op.create_index("ix_tender_round_organization_id", "tender_round", ["organization_id"])
    op.create_index(
        "ix_tender_round_org_tender",
        "tender_round",
        ["organization_id", "tender_id"],
    )
    op.execute("ALTER TABLE tender_round ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE tender_round FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY tender_round_tenant_isolation ON tender_round
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS tender_round_tenant_isolation ON tender_round")
    op.drop_index("ix_tender_round_org_tender", table_name="tender_round")
    op.drop_index("ix_tender_round_organization_id", table_name="tender_round")
    op.drop_table("tender_round")
