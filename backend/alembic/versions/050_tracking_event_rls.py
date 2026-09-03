"""create tracking_event on shipment with RLS FORCE

Revision ID: 050_tracking_event_rls
Revises: 049_shipment_rls
Create Date: 2026-09-03

Zdarzenie trackingu na zleceniu. Nie mapa. Nie czas przybycia liczony.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "050_tracking_event_rls"
down_revision: str | None = "049_shipment_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_shipment_org_id",
        "shipment",
        ["organization_id", "id"],
    )
    op.create_table(
        "tracking_event",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("shipment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("event_kind", sa.String(length=16), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
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
            name="fk_tracking_event_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_tracking_event_shipment",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "event_kind IN ('departed', 'arrived', 'noted')",
            name="ck_tracking_event_kind",
        ),
    )
    op.create_index(
        "ix_tracking_event_organization_id",
        "tracking_event",
        ["organization_id"],
    )
    op.create_index(
        "ix_tracking_event_org_shipment",
        "tracking_event",
        ["organization_id", "shipment_id"],
    )
    op.create_index(
        "ix_tracking_event_org_occurred",
        "tracking_event",
        ["organization_id", "occurred_at"],
    )
    op.execute("ALTER TABLE tracking_event ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE tracking_event FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY tracking_event_tenant_isolation ON tracking_event
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS tracking_event_tenant_isolation ON tracking_event")
    op.drop_index("ix_tracking_event_org_occurred", table_name="tracking_event")
    op.drop_index("ix_tracking_event_org_shipment", table_name="tracking_event")
    op.drop_index("ix_tracking_event_organization_id", table_name="tracking_event")
    op.drop_table("tracking_event")
    op.drop_constraint("uq_shipment_org_id", "shipment", type_="unique")
