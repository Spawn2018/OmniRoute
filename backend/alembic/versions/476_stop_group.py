"""create stop_group on shipment with RLS FORCE

Revision ID: 476_stop_group
Revises: 475_resource_vehicle_profile
Create Date: 2026-09-20

T1b HITL nagłówek grupy punktów. N grup na shipment. Nie członkostwo stop.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "476_stop_group"
down_revision: str | None = "475_resource_vehicle_profile"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "stop_group",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("shipment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("group_code", sa.String(length=32), nullable=False),
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
            name="fk_stop_group_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_stop_group_shipment",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_stop_group_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "shipment_id",
            "group_code",
            name="uq_stop_group_org_shipment_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_stop_group_org_source",
        ),
        sa.CheckConstraint(
            "group_code ~ '^[A-Za-z0-9_-]{2,32}$'",
            name="ck_stop_group_group_code",
        ),
    )
    op.create_index(
        "ix_stop_group_organization_id",
        "stop_group",
        ["organization_id"],
    )
    op.create_index(
        "ix_stop_group_org_shipment",
        "stop_group",
        ["organization_id", "shipment_id"],
    )
    op.execute("ALTER TABLE stop_group ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE stop_group FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY stop_group_tenant_isolation ON stop_group
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS stop_group_tenant_isolation ON stop_group")
    op.drop_index("ix_stop_group_org_shipment", table_name="stop_group")
    op.drop_index("ix_stop_group_organization_id", table_name="stop_group")
    op.drop_table("stop_group")
