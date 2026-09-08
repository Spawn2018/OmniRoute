"""create field_carry_forward and document_checklist_rule with RLS FORCE

Revision ID: 084_carry_checklist
Revises: 083_inquiry_no_reply
Create Date: 2026-09-08

Snapshot pól wyceny na zlecenie + reguła checklisty. Nie dispatch. Nie C8.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "084_carry_checklist"
down_revision: str | None = "083_inquiry_no_reply"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "field_carry_forward",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("quotation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("shipment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("field_key", sa.String(length=16), nullable=False),
        sa.Column("field_value", sa.String(length=128), nullable=False),
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
            name="fk_field_carry_forward_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "quotation_id"],
            ["quotation.organization_id", "quotation.id"],
            name="fk_field_carry_forward_quotation",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_field_carry_forward_shipment",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["superseded_by"],
            ["field_carry_forward.id"],
            name="fk_field_carry_forward_superseded_by",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "field_key IN ('incoterm', 'trade_side', 'named_place')",
            name="ck_field_carry_forward_key",
        ),
    )
    op.create_index(
        "ix_field_carry_forward_organization_id",
        "field_carry_forward",
        ["organization_id"],
    )
    op.create_index(
        "ix_field_carry_forward_org_shipment",
        "field_carry_forward",
        ["organization_id", "shipment_id"],
    )
    op.execute("ALTER TABLE field_carry_forward ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE field_carry_forward FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY field_carry_forward_tenant_isolation ON field_carry_forward
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )

    op.create_table(
        "document_checklist_rule",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("incoterm", sa.CHAR(length=3), nullable=False),
        sa.Column("trade_side", sa.String(length=6), nullable=False),
        sa.Column("mode", sa.String(length=8), nullable=False),
        sa.Column("document_kind", sa.String(length=32), nullable=False),
        sa.Column("blocks_dispatch", sa.Boolean(), nullable=False),
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
            name="fk_document_checklist_rule_organization_id",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "incoterm IN ('EXW','FCA','CPT','CIP','DAP','DPU','DDP','FAS','FOB','CFR','CIF')",
            name="ck_document_checklist_rule_incoterm",
        ),
        sa.CheckConstraint(
            "trade_side IN ('import', 'export')",
            name="ck_document_checklist_rule_side",
        ),
        sa.CheckConstraint(
            "mode IN ('ocean', 'road', 'rail', 'air')",
            name="ck_document_checklist_rule_mode",
        ),
        sa.CheckConstraint(
            "document_kind IN ("
            "'commercial_invoice', 'packing_list', 'bill_of_lading', 'export_declaration')",
            name="ck_document_checklist_rule_kind",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "incoterm",
            "trade_side",
            "mode",
            "document_kind",
            name="uq_document_checklist_rule_triple_kind",
        ),
    )
    op.create_index(
        "ix_document_checklist_rule_organization_id",
        "document_checklist_rule",
        ["organization_id"],
    )
    op.create_index(
        "ix_document_checklist_rule_org_triple",
        "document_checklist_rule",
        ["organization_id", "incoterm", "trade_side", "mode"],
    )
    op.execute("ALTER TABLE document_checklist_rule ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE document_checklist_rule FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY document_checklist_rule_tenant_isolation
        ON document_checklist_rule
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS document_checklist_rule_tenant_isolation ON document_checklist_rule"
    )
    op.drop_index(
        "ix_document_checklist_rule_org_triple",
        table_name="document_checklist_rule",
    )
    op.drop_index(
        "ix_document_checklist_rule_organization_id",
        table_name="document_checklist_rule",
    )
    op.drop_table("document_checklist_rule")
    op.execute("DROP POLICY IF EXISTS field_carry_forward_tenant_isolation ON field_carry_forward")
    op.drop_index("ix_field_carry_forward_org_shipment", table_name="field_carry_forward")
    op.drop_index("ix_field_carry_forward_organization_id", table_name="field_carry_forward")
    op.drop_table("field_carry_forward")
