"""create booking_instruction with RLS FORCE

Revision ID: 088_booking_instruction
Revises: 087_document_dispatch_rule
Create Date: 2026-09-08

Instrukcja bookingu na zleceniu. Nie S21. Nie mail_draft.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "088_booking_instruction"
down_revision: str | None = "087_document_dispatch_rule"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "booking_instruction",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("shipment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("booking_scope", sa.String(length=20), nullable=False),
        sa.Column("target_role", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=12), nullable=False),
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
            name="fk_booking_instruction_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_booking_instruction_shipment",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["superseded_by"],
            ["booking_instruction.id"],
            name="fk_booking_instruction_superseded_by",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "booking_scope IN ('precarriage','ocean','oncarriage','contact_exchange','none')",
            name="ck_booking_instruction_scope",
        ),
        sa.CheckConstraint(
            "target_role IN ('shipper','consignee','origin_agent','dest_agent',"
            "'ocean_carrier','omni_customs','client_customs')",
            name="ck_booking_instruction_role",
        ),
        sa.CheckConstraint(
            "status IN ('suggested','accepted','sent','confirmed','rejected')",
            name="ck_booking_instruction_status",
        ),
    )
    op.create_index(
        "ix_booking_instruction_organization_id",
        "booking_instruction",
        ["organization_id"],
    )
    # GET po zleceniu — RLS + superseded w SQL.
    op.create_index(
        "ix_booking_instruction_org_shipment",
        "booking_instruction",
        ["organization_id", "shipment_id"],
    )
    op.execute("ALTER TABLE booking_instruction ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE booking_instruction FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY booking_instruction_tenant_isolation
        ON booking_instruction
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS booking_instruction_tenant_isolation ON booking_instruction"
    )
    op.drop_index(
        "ix_booking_instruction_org_shipment",
        table_name="booking_instruction",
    )
    op.drop_index(
        "ix_booking_instruction_organization_id",
        table_name="booking_instruction",
    )
    op.drop_table("booking_instruction")
