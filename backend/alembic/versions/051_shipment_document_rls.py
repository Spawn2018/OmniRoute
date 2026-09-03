"""create shipment_document on shipment with RLS FORCE

Revision ID: 051_shipment_document_rls
Revises: 050_tracking_event_rls
Create Date: 2026-09-03

Dokument na zleceniu. Nie bajty pliku. Nie numer listu.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "051_shipment_document_rls"
down_revision: str | None = "050_tracking_event_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "shipment_document",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("shipment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("document_kind", sa.String(length=16), nullable=False),
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
            name="fk_shipment_document_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_shipment_document_shipment",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "document_kind IN ('noted', 'attached', 'other')",
            name="ck_shipment_document_kind",
        ),
    )
    op.create_index(
        "ix_shipment_document_organization_id",
        "shipment_document",
        ["organization_id"],
    )
    op.create_index(
        "ix_shipment_document_org_shipment",
        "shipment_document",
        ["organization_id", "shipment_id"],
    )
    op.execute("ALTER TABLE shipment_document ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE shipment_document FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY shipment_document_tenant_isolation ON shipment_document
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS shipment_document_tenant_isolation ON shipment_document")
    op.drop_index("ix_shipment_document_org_shipment", table_name="shipment_document")
    op.drop_index("ix_shipment_document_organization_id", table_name="shipment_document")
    op.drop_table("shipment_document")
