"""create party_lane_scorecard snapshot with RLS leftover O5

Revision ID: 081_party_lane_scorecard
Revises: 080_mail_draft_inquiry
Create Date: 2026-09-08

Snapshot per lane. Nie scoring osoby. Nie refresh SQL z innych BC.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "081_party_lane_scorecard"
down_revision: str | None = "080_mail_draft_inquiry"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "party_lane_scorecard",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("origin_port_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("destination_port_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("window_days", sa.Integer(), nullable=False),
        sa.Column("sample_size", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column(
            "answered_inquiry_count",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column("shipment_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("cheapest_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("median_response_hours", sa.Numeric(12, 4), nullable=True),
        sa.Column(
            "computed_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
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
            name="fk_party_lane_scorecard_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_party_lane_scorecard_party",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "origin_port_id"],
            ["port.organization_id", "port.id"],
            name="fk_party_lane_scorecard_origin_port",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "destination_port_id"],
            ["port.organization_id", "port.id"],
            name="fk_party_lane_scorecard_destination_port",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "party_id",
            "origin_port_id",
            "destination_port_id",
            "window_days",
            name="uq_party_lane_scorecard_org_party_lane_window",
        ),
        sa.CheckConstraint("sample_size >= 0", name="ck_party_lane_scorecard_sample_size"),
        sa.CheckConstraint(
            "answered_inquiry_count >= 0",
            name="ck_party_lane_scorecard_answered",
        ),
        sa.CheckConstraint("shipment_count >= 0", name="ck_party_lane_scorecard_shipments"),
        sa.CheckConstraint("cheapest_count >= 0", name="ck_party_lane_scorecard_cheapest"),
        sa.CheckConstraint(
            "window_days >= 1 AND window_days <= 365",
            name="ck_party_lane_scorecard_window_days",
        ),
        sa.CheckConstraint(
            "median_response_hours IS NULL OR median_response_hours >= 0",
            name="ck_party_lane_scorecard_median_hours",
        ),
    )
    op.create_index(
        "ix_party_lane_scorecard_organization_id",
        "party_lane_scorecard",
        ["organization_id"],
    )
    op.execute("ALTER TABLE party_lane_scorecard ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE party_lane_scorecard FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY party_lane_scorecard_tenant_isolation ON party_lane_scorecard
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS party_lane_scorecard_tenant_isolation ON party_lane_scorecard"
    )
    op.drop_index("ix_party_lane_scorecard_organization_id", table_name="party_lane_scorecard")
    op.drop_table("party_lane_scorecard")
