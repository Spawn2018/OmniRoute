"""create cod_instruction on shipment with RLS FORCE

Revision ID: 098_cod_instruction
Revises: 097_dock_appointment
Create Date: 2026-09-08

Znacznik pobrania COD na zleceniu. Bez kwoty. Nie Fala F.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "098_cod_instruction"
down_revision: str | None = "097_dock_appointment"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "cod_instruction",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("shipment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("instruction_code", sa.String(length=32), nullable=False),
        sa.Column("collection_status", sa.String(length=16), nullable=False),
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
            name="fk_cod_instruction_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_cod_instruction_shipment",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_cod_instruction_org_id"),
        sa.CheckConstraint(
            "collection_status IN ('noted','advised','collected','refused')",
            name="ck_cod_instruction_status",
        ),
    )
    op.create_index(
        "ix_cod_instruction_organization_id",
        "cod_instruction",
        ["organization_id"],
    )
    op.create_index(
        "ix_cod_instruction_org_shipment",
        "cod_instruction",
        ["organization_id", "shipment_id"],
    )
    op.execute("ALTER TABLE cod_instruction ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE cod_instruction FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY cod_instruction_tenant_isolation ON cod_instruction
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS cod_instruction_tenant_isolation ON cod_instruction")
    op.drop_index("ix_cod_instruction_org_shipment", table_name="cod_instruction")
    op.drop_index("ix_cod_instruction_organization_id", table_name="cod_instruction")
    op.drop_table("cod_instruction")
