"""create wms_flow_mark catalog with RLS FORCE

Revision ID: 379_wms_flow_mark
Revises: 378_exchange_connector_kinds
Create Date: 2026-09-14

BR1.0 HITL katalog przepływu WMS. Nie live Manhattan / SAP EWM.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "379_wms_flow_mark"
down_revision: str | None = "378_exchange_connector_kinds"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "wms_flow_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("flow_kind", sa.String(length=16), nullable=False),
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
            name="fk_wms_flow_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_wms_flow_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_wms_flow_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_wms_flow_mark_org_src",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_wms_flow_mark_code",
        ),
        sa.CheckConstraint(
            "flow_kind IN ('receipt', 'location', 'pick', 'ship', 'count', 'other')",
            name="ck_wms_flow_mark_kind",
        ),
    )
    op.create_index(
        "ix_wms_flow_mark_organization_id",
        "wms_flow_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE wms_flow_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE wms_flow_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY wms_flow_mark_tenant_isolation ON wms_flow_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS wms_flow_mark_tenant_isolation ON wms_flow_mark",
    )
    op.drop_index(
        "ix_wms_flow_mark_organization_id",
        table_name="wms_flow_mark",
    )
    op.drop_table("wms_flow_mark")
