"""create edi_message on shipment with RLS FORCE

Revision ID: 053_edi_message_rls
Revises: 052_operational_exception_rls
Create Date: 2026-09-03

Komunikat na zleceniu. Nie parser. Nie live siec.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "053_edi_message_rls"
down_revision: str | None = "052_operational_exception_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "edi_message",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("shipment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("message_kind", sa.String(length=16), nullable=False),
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
            name="fk_edi_message_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_edi_message_shipment",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "message_kind IN ('noted', 'outbound', 'other')",
            name="ck_edi_message_kind",
        ),
    )
    op.create_index(
        "ix_edi_message_organization_id",
        "edi_message",
        ["organization_id"],
    )
    op.create_index(
        "ix_edi_message_org_shipment",
        "edi_message",
        ["organization_id", "shipment_id"],
    )
    op.execute("ALTER TABLE edi_message ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE edi_message FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY edi_message_tenant_isolation ON edi_message
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS edi_message_tenant_isolation ON edi_message")
    op.drop_index("ix_edi_message_org_shipment", table_name="edi_message")
    op.drop_index("ix_edi_message_organization_id", table_name="edi_message")
    op.drop_table("edi_message")
