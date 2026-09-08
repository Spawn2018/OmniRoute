"""create document_dispatch_rule catalog with RLS FORCE

Revision ID: 087_document_dispatch_rule
Revises: 086_shipment_stakeholder
Create Date: 2026-09-08

Adresat dokumentów per tenant. Nie send. Nie I4.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "087_document_dispatch_rule"
down_revision: str | None = "086_shipment_stakeholder"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "document_dispatch_rule",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("incoterm", sa.CHAR(length=3), nullable=False),
        sa.Column("trade_side", sa.String(length=8), nullable=False),
        sa.Column("document_kind", sa.String(length=24), nullable=False),
        sa.Column("recipient_role", sa.String(length=20), nullable=False),
        sa.Column("source_ref", sa.Text(), nullable=False),
        sa.Column("superseded_by", postgresql.UUID(as_uuid=True), nullable=True),
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
            name="fk_document_dispatch_rule_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["superseded_by"],
            ["document_dispatch_rule.id"],
            name="fk_document_dispatch_rule_superseded_by",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "incoterm IN ('EXW','FCA','CPT','CIP','DAP','DPU','DDP','FAS','FOB','CFR','CIF')",
            name="ck_document_dispatch_rule_incoterm",
        ),
        sa.CheckConstraint(
            "trade_side IN ('import', 'export')",
            name="ck_document_dispatch_rule_side",
        ),
        sa.CheckConstraint(
            "document_kind IN ("
            "'commercial_invoice', 'packing_list', 'bill_of_lading', 'export_declaration')",
            name="ck_document_dispatch_rule_kind",
        ),
        sa.CheckConstraint(
            "recipient_role IN ("
            "'shipper','consignee','origin_agent','dest_agent',"
            "'ocean_carrier','omni_customs','client_customs')",
            name="ck_document_dispatch_rule_role",
        ),
    )
    op.create_index(
        "ix_document_dispatch_rule_organization_id",
        "document_dispatch_rule",
        ["organization_id"],
    )
    # GET po parze/trójce filtruje RLS + superseded w SQL.
    op.create_index(
        "ix_document_dispatch_rule_org_triple",
        "document_dispatch_rule",
        ["organization_id", "incoterm", "trade_side", "document_kind"],
    )
    op.execute("ALTER TABLE document_dispatch_rule ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE document_dispatch_rule FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY document_dispatch_rule_tenant_isolation
        ON document_dispatch_rule
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS document_dispatch_rule_tenant_isolation "
        "ON document_dispatch_rule"
    )
    op.drop_index(
        "ix_document_dispatch_rule_org_triple",
        table_name="document_dispatch_rule",
    )
    op.drop_index(
        "ix_document_dispatch_rule_organization_id",
        table_name="document_dispatch_rule",
    )
    op.drop_table("document_dispatch_rule")
