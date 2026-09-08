"""create tender_matrix_cell catalog with RLS FORCE

Revision ID: 114_tender_matrix_cell
Revises: 113_tender_data_room
Create Date: 2026-09-09

Komórka matrycy: kwota Decimal z P. Nie LLM. Nie druga marża.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "114_tender_matrix_cell"
down_revision: str | None = "113_tender_data_room"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "tender_matrix_cell",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tender_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("cell_code", sa.String(length=32), nullable=False),
        sa.Column("amount", sa.Numeric(14, 4), nullable=False),
        sa.Column("currency", sa.CHAR(length=3), nullable=False),
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
            name="fk_tender_matrix_cell_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_matrix_cell_tender",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_tender_matrix_cell_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "tender_id",
            "cell_code",
            name="uq_tender_matrix_cell_org_tender_code",
        ),
        sa.CheckConstraint("amount > 0", name="ck_tender_matrix_cell_amount"),
        sa.CheckConstraint("currency ~ '^[A-Z]{3}$'", name="ck_tender_matrix_cell_currency"),
        sa.CheckConstraint(
            "cell_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_tender_matrix_cell_code",
        ),
    )
    op.create_index(
        "ix_tender_matrix_cell_organization_id",
        "tender_matrix_cell",
        ["organization_id"],
    )
    op.create_index(
        "ix_tender_matrix_cell_org_tender",
        "tender_matrix_cell",
        ["organization_id", "tender_id"],
    )
    op.execute("ALTER TABLE tender_matrix_cell ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE tender_matrix_cell FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY tender_matrix_cell_tenant_isolation ON tender_matrix_cell
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS tender_matrix_cell_tenant_isolation ON tender_matrix_cell")
    op.drop_index("ix_tender_matrix_cell_org_tender", table_name="tender_matrix_cell")
    op.drop_index("ix_tender_matrix_cell_organization_id", table_name="tender_matrix_cell")
    op.drop_table("tender_matrix_cell")
