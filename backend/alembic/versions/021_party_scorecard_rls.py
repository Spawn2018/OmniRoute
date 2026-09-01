"""create party_scorecard snapshot with RLS

Revision ID: 021_party_scorecard_rls
Revises: 020_network_rls
Create Date: 2026-09-02
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "021_party_scorecard_rls"
down_revision: str | None = "020_network_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "party_scorecard",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("window_days", sa.Integer(), nullable=False, server_default=sa.text("90")),
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sample_size", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("response_rate", sa.Numeric(7, 4), nullable=True),
        sa.Column("median_response_hours", sa.Numeric(12, 4), nullable=True),
        sa.Column("price_position", sa.Numeric(7, 4), nullable=True),
        sa.Column("quote_invoice_match_rate", sa.Numeric(7, 4), nullable=True),
        sa.Column("rollover_count", sa.Integer(), nullable=True),
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
            name="fk_party_scorecard_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_party_scorecard_party",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "party_id", name="uq_party_scorecard_org_party"),
        sa.CheckConstraint(
            "response_rate IS NULL OR (response_rate >= 0 AND response_rate <= 1)",
            name="ck_party_scorecard_response_rate",
        ),
        sa.CheckConstraint(
            "price_position IS NULL OR (price_position >= 0 AND price_position <= 1)",
            name="ck_party_scorecard_price_position",
        ),
        sa.CheckConstraint(
            "quote_invoice_match_rate IS NULL OR "
            "(quote_invoice_match_rate >= 0 AND quote_invoice_match_rate <= 1)",
            name="ck_party_scorecard_quote_invoice_match",
        ),
        sa.CheckConstraint(
            "median_response_hours IS NULL OR median_response_hours >= 0",
            name="ck_party_scorecard_median_hours",
        ),
        sa.CheckConstraint(
            "rollover_count IS NULL OR rollover_count >= 0",
            name="ck_party_scorecard_rollover",
        ),
        sa.CheckConstraint("sample_size >= 0", name="ck_party_scorecard_sample_size"),
        sa.CheckConstraint("window_days > 0", name="ck_party_scorecard_window_days"),
    )
    op.create_index("ix_party_scorecard_organization_id", "party_scorecard", ["organization_id"])

    op.execute("ALTER TABLE party_scorecard ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE party_scorecard FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY party_scorecard_tenant_isolation ON party_scorecard
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS party_scorecard_tenant_isolation ON party_scorecard")
    op.drop_index("ix_party_scorecard_organization_id", table_name="party_scorecard")
    op.drop_table("party_scorecard")
