"""create tender_lot catalog with RLS FORCE

Revision ID: 110_tender_lot
Revises: 109_tender
Create Date: 2026-09-08

Partia przetargu. Nie korytarz. Nie kwota.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "110_tender_lot"
down_revision: str | None = "109_tender"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "tender_lot",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tender_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("lot_code", sa.String(length=32), nullable=False),
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
            name="fk_tender_lot_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_lot_tender",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_tender_lot_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "tender_id",
            "lot_code",
            name="uq_tender_lot_org_tender_code",
        ),
        sa.CheckConstraint("char_length(btrim(lot_code)) > 0", name="ck_tender_lot_code"),
    )
    op.create_index("ix_tender_lot_organization_id", "tender_lot", ["organization_id"])
    op.create_index(
        "ix_tender_lot_org_tender",
        "tender_lot",
        ["organization_id", "tender_id"],
    )
    op.execute("ALTER TABLE tender_lot ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE tender_lot FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY tender_lot_tenant_isolation ON tender_lot
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS tender_lot_tenant_isolation ON tender_lot")
    op.drop_index("ix_tender_lot_org_tender", table_name="tender_lot")
    op.drop_index("ix_tender_lot_organization_id", table_name="tender_lot")
    op.drop_table("tender_lot")
