"""create resource_document catalog with RLS FORCE

Revision ID: 468_resource_document
Revises: 467_resource_capacity_m3
Create Date: 2026-09-19

HITL waznosc dokumentu floty. Nie dokument kontrahenta. Nie 409 na trip.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "468_resource_document"
down_revision: str | None = "467_resource_capacity_m3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "resource_document",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("resource_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("document_kind", sa.String(length=16), nullable=False),
        sa.Column("valid_until", sa.Date(), nullable=False),
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
            name="fk_resource_document_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "resource_id"],
            ["resource.organization_id", "resource.id"],
            name="fk_resource_document_resource",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_resource_document_org_id",
        ),
        sa.CheckConstraint(
            "document_kind IN ('licence', 'insurance', 'other')",
            name="ck_resource_document_kind",
        ),
    )
    op.create_index(
        "ix_resource_document_organization_id",
        "resource_document",
        ["organization_id"],
    )
    op.execute("ALTER TABLE resource_document ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE resource_document FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY resource_document_tenant_isolation
        ON resource_document
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS resource_document_tenant_isolation ON resource_document"
    )
    op.drop_index(
        "ix_resource_document_organization_id",
        table_name="resource_document",
    )
    op.drop_table("resource_document")
