"""create operational_exception on shipment with RLS FORCE

Revision ID: 052_operational_exception_rls
Revises: 051_shipment_document_rls
Create Date: 2026-09-03

Wyjatek na zleceniu. Nie mapa. Nie czas przybycia liczony.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "052_operational_exception_rls"
down_revision: str | None = "051_shipment_document_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "operational_exception",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("shipment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("exception_kind", sa.String(length=16), nullable=False),
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
            name="fk_operational_exception_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_operational_exception_shipment",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "exception_kind IN ('noted', 'blocked', 'other')",
            name="ck_operational_exception_kind",
        ),
    )
    op.create_index(
        "ix_operational_exception_organization_id",
        "operational_exception",
        ["organization_id"],
    )
    op.create_index(
        "ix_operational_exception_org_shipment",
        "operational_exception",
        ["organization_id", "shipment_id"],
    )
    op.execute("ALTER TABLE operational_exception ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE operational_exception FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY operational_exception_tenant_isolation ON operational_exception
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS operational_exception_tenant_isolation ON operational_exception"
    )
    op.drop_index("ix_operational_exception_org_shipment", table_name="operational_exception")
    op.drop_index("ix_operational_exception_organization_id", table_name="operational_exception")
    op.drop_table("operational_exception")
