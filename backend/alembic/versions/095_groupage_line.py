"""create groupage_line catalog with RLS FORCE

Revision ID: 095_groupage_line
Revises: 094_shipment_leg_air_kind
Create Date: 2026-09-08

Katalog linii drobnicy per tenant. Nie WMS. Nie OR hubów.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "095_groupage_line"
down_revision: str | None = "094_shipment_leg_air_kind"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "groupage_line",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("line_code", sa.String(length=32), nullable=False),
        sa.Column("origin_location_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("destination_location_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("cutoff_local", sa.Time(), nullable=False),
        sa.Column("transit_days", sa.Integer(), nullable=False),
        sa.Column("operating_dows", postgresql.ARRAY(sa.SmallInteger()), nullable=False),
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
            name="fk_groupage_line_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "origin_location_id"],
            ["location.organization_id", "location.id"],
            name="fk_groupage_line_origin",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "destination_location_id"],
            ["location.organization_id", "location.id"],
            name="fk_groupage_line_destination",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["superseded_by"],
            ["groupage_line.id"],
            name="fk_groupage_line_superseded_by",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_groupage_line_org_id"),
        sa.CheckConstraint("transit_days >= 1", name="ck_groupage_line_transit_days"),
        sa.CheckConstraint(
            "cardinality(operating_dows) >= 1",
            name="ck_groupage_line_dows_len",
        ),
        sa.CheckConstraint(
            "operating_dows <@ ARRAY[1,2,3,4,5,6,7]::smallint[]",
            name="ck_groupage_line_dows_iso",
        ),
        sa.CheckConstraint(
            "origin_location_id <> destination_location_id",
            name="ck_groupage_line_distinct_ends",
        ),
    )
    op.create_index("ix_groupage_line_organization_id", "groupage_line", ["organization_id"])
    op.create_index(
        "ix_groupage_line_org_code",
        "groupage_line",
        ["organization_id", "line_code"],
    )
    op.execute("ALTER TABLE groupage_line ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE groupage_line FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY groupage_line_tenant_isolation
        ON groupage_line
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS groupage_line_tenant_isolation ON groupage_line")
    op.drop_index("ix_groupage_line_org_code", table_name="groupage_line")
    op.drop_index("ix_groupage_line_organization_id", table_name="groupage_line")
    op.drop_table("groupage_line")
