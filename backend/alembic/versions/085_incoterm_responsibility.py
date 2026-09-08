"""create incoterm_responsibility catalog with RLS FORCE

Revision ID: 085_incoterm_responsibility
Revises: 084_carry_checklist
Create Date: 2026-09-08

Macierz obowiązków per tenant. Dane Omni, nie cytat ICC. Nie I2.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "085_incoterm_responsibility"
down_revision: str | None = "084_carry_checklist"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "incoterm_responsibility",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("incoterm", sa.CHAR(length=3), nullable=False),
        sa.Column("trade_side", sa.String(length=6), nullable=False),
        sa.Column("export_clearance_role", sa.String(length=16), nullable=False),
        sa.Column("import_clearance_role", sa.String(length=16), nullable=False),
        sa.Column("main_carriage_booker", sa.String(length=8), nullable=False),
        sa.Column("booking_scope", postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column("source_ref", sa.String(length=256), nullable=False),
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
            name="fk_incoterm_responsibility_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["superseded_by"],
            ["incoterm_responsibility.id"],
            name="fk_incoterm_responsibility_superseded_by",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "incoterm IN ('EXW','FCA','CPT','CIP','DAP','DPU','DDP','FAS','FOB','CFR','CIF')",
            name="ck_incoterm_responsibility_incoterm",
        ),
        sa.CheckConstraint(
            "trade_side IN ('import', 'export')",
            name="ck_incoterm_responsibility_side",
        ),
        sa.CheckConstraint(
            "export_clearance_role IN ("
            "'seller','buyer','omni_customs','origin_agent','client_customs')",
            name="ck_incoterm_responsibility_export_role",
        ),
        sa.CheckConstraint(
            "import_clearance_role IN ("
            "'seller','buyer','omni_customs','origin_agent','client_customs')",
            name="ck_incoterm_responsibility_import_role",
        ),
        sa.CheckConstraint(
            "main_carriage_booker IN ('seller', 'buyer')",
            name="ck_incoterm_responsibility_booker",
        ),
        sa.CheckConstraint(
            "booking_scope <@ ARRAY['precarriage','ocean','oncarriage',"
            "'contact_exchange','none']::text[] AND cardinality(booking_scope) >= 1",
            name="ck_incoterm_responsibility_scope",
        ),
    )
    op.create_index(
        "ix_incoterm_responsibility_organization_id",
        "incoterm_responsibility",
        ["organization_id"],
    )
    op.create_index(
        "ix_incoterm_responsibility_org_pair",
        "incoterm_responsibility",
        ["organization_id", "incoterm", "trade_side"],
    )
    op.execute("ALTER TABLE incoterm_responsibility ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE incoterm_responsibility FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY incoterm_responsibility_tenant_isolation
        ON incoterm_responsibility
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS incoterm_responsibility_tenant_isolation "
        "ON incoterm_responsibility"
    )
    op.drop_index("ix_incoterm_responsibility_org_pair", table_name="incoterm_responsibility")
    op.drop_index(
        "ix_incoterm_responsibility_organization_id",
        table_name="incoterm_responsibility",
    )
    op.drop_table("incoterm_responsibility")
