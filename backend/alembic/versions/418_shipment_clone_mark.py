"""create shipment_clone_mark catalog with RLS FORCE

Revision ID: 418_shipment_clone_mark
Revises: 417_margin_floor
Create Date: 2026-09-16

N9 HITL intencja klonu zlecenia. Nie drugi SoR. Nie auto-copy.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "418_shipment_clone_mark"
down_revision: str | None = "417_margin_floor"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "shipment_clone_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("clone_kind", sa.String(length=16), nullable=False),
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
            name="fk_shipment_clone_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_shipment_clone_mark_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_shipment_clone_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_shipment_clone_mark_org_src",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_shipment_clone_mark_code",
        ),
        sa.CheckConstraint(
            "clone_kind IN ('last_similar', 'manual_pick', 'other')",
            name="ck_shipment_clone_mark_kind",
        ),
    )
    op.create_index(
        "ix_shipment_clone_mark_organization_id",
        "shipment_clone_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE shipment_clone_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE shipment_clone_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY shipment_clone_mark_tenant_isolation
        ON shipment_clone_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS shipment_clone_mark_tenant_isolation ON shipment_clone_mark",
    )
    op.drop_index(
        "ix_shipment_clone_mark_organization_id",
        table_name="shipment_clone_mark",
    )
    op.drop_table("shipment_clone_mark")
