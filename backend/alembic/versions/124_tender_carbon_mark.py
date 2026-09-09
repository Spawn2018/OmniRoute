"""create tender_carbon_mark catalog with RLS FORCE

Revision ID: 124_tender_carbon_mark
Revises: 123_tender_ted_notice
Create Date: 2026-09-09

HITL CO2 mark: declared/exempt + source_ref. Nie kg. Nie kalkulator.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "124_tender_carbon_mark"
down_revision: str | None = "123_tender_ted_notice"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "tender_carbon_mark",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tender_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=16), nullable=False),
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
            name="fk_tender_carbon_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_carbon_mark_tender",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_tender_carbon_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "tender_id",
            name="uq_tender_carbon_mark_org_tender",
        ),
        sa.CheckConstraint(
            "mark_code IN ('declared', 'exempt')",
            name="ck_tender_carbon_mark_code",
        ),
    )
    op.create_index(
        "ix_tender_carbon_mark_organization_id",
        "tender_carbon_mark",
        ["organization_id"],
    )
    op.create_index(
        "ix_tender_carbon_mark_org_code",
        "tender_carbon_mark",
        ["organization_id", "mark_code"],
    )
    op.execute("ALTER TABLE tender_carbon_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE tender_carbon_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY tender_carbon_mark_tenant_isolation ON tender_carbon_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS tender_carbon_mark_tenant_isolation ON tender_carbon_mark"
    )
    op.drop_index("ix_tender_carbon_mark_org_code", table_name="tender_carbon_mark")
    op.drop_index(
        "ix_tender_carbon_mark_organization_id", table_name="tender_carbon_mark"
    )
    op.drop_table("tender_carbon_mark")
