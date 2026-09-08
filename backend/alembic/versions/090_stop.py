"""create stop with RLS FORCE

Revision ID: 090_stop
Revises: 089_organization_calendar
Create Date: 2026-09-08

Punkt operacyjny na zleceniu. Nie mapa. Nie T2.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "090_stop"
down_revision: str | None = "089_organization_calendar"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "stop",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("shipment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("location_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("stop_kind", sa.String(length=12), nullable=False),
        sa.Column("sequence_no", sa.Integer(), nullable=False),
        sa.Column("time_zone", sa.String(length=64), nullable=False),
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
            name="fk_stop_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_stop_shipment",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "location_id"],
            ["location.organization_id", "location.id"],
            name="fk_stop_location",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["superseded_by"],
            ["stop.id"],
            name="fk_stop_superseded_by",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "stop_kind IN ('loading','unloading','customs','ferry','terminal','depot','other')",
            name="ck_stop_kind",
        ),
        sa.CheckConstraint(
            "status IN ('pending','at_stop','completed','failed')",
            name="ck_stop_status",
        ),
        sa.CheckConstraint("sequence_no >= 1", name="ck_stop_sequence"),
        sa.CheckConstraint(
            "time_zone ~ '^[A-Za-z_]+/[A-Za-z0-9_+-]+(/[A-Za-z0-9_+-]+)?$'",
            name="ck_stop_time_zone",
        ),
    )
    op.create_index("ix_stop_organization_id", "stop", ["organization_id"])
    # GET po zleceniu — RLS + superseded w SQL.
    op.create_index("ix_stop_org_shipment", "stop", ["organization_id", "shipment_id"])
    op.execute("ALTER TABLE stop ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE stop FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY stop_tenant_isolation
        ON stop
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS stop_tenant_isolation ON stop")
    op.drop_index("ix_stop_org_shipment", table_name="stop")
    op.drop_index("ix_stop_organization_id", table_name="stop")
    op.drop_table("stop")
