"""create po_plant_mark catalog with RLS FORCE

Revision ID: 323_po_plant_mark
Revises: 322_demo_sim_mark
Create Date: 2026-09-12

EXP3.0b HITL znacznik plant/batch/SKU na PO. Nie live EDI. Nie auto shipment.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "323_po_plant_mark"
down_revision: str | None = "322_demo_sim_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "po_plant_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("plant_kind", sa.String(length=16), nullable=False),
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
            name="fk_po_plant_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_po_plant_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_po_plant_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_po_plant_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_po_plant_mark_code",
        ),
        sa.CheckConstraint(
            "plant_kind IN ('plant', 'batch', 'sku', 'other')",
            name="ck_po_plant_mark_plant_kind",
        ),
    )
    op.create_index(
        "ix_po_plant_mark_organization_id",
        "po_plant_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE po_plant_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE po_plant_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY po_plant_mark_tenant_isolation ON po_plant_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS po_plant_mark_tenant_isolation ON po_plant_mark",
    )
    op.drop_index(
        "ix_po_plant_mark_organization_id",
        table_name="po_plant_mark",
    )
    op.drop_table("po_plant_mark")
