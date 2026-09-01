"""create channel_quote catalog with RLS

Revision ID: 024_channel_quote_rls
Revises: 023_port_surcharge_rls
Create Date: 2026-09-02
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "024_channel_quote_rls"
down_revision: str | None = "023_port_surcharge_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "channel_quote",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("amount", sa.Numeric(14, 4), nullable=False),
        sa.Column("currency", sa.CHAR(length=3), nullable=False),
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("origin_port_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("destination_port_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("quote_date", sa.Date(), nullable=False),
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
            name="fk_channel_quote_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_channel_quote_party",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "origin_port_id"],
            ["port.organization_id", "port.id"],
            name="fk_channel_quote_origin_port",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "destination_port_id"],
            ["port.organization_id", "port.id"],
            name="fk_channel_quote_destination_port",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "party_id",
            "origin_port_id",
            "destination_port_id",
            "quote_date",
            name="uq_channel_quote_org_lane_day",
        ),
        sa.CheckConstraint("currency ~ '^[A-Z]{3}$'", name="ck_channel_quote_currency_iso"),
        sa.CheckConstraint("amount > 0", name="ck_channel_quote_amount_positive"),
    )
    op.create_index("ix_channel_quote_organization_id", "channel_quote", ["organization_id"])

    op.execute("ALTER TABLE channel_quote ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE channel_quote FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY channel_quote_tenant_isolation ON channel_quote
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS channel_quote_tenant_isolation ON channel_quote")
    op.drop_index("ix_channel_quote_organization_id", table_name="channel_quote")
    op.drop_table("channel_quote")
