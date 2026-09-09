"""create kreptd_licence catalog with RLS FORCE

Revision ID: 126_kreptd_licence
Revises: 125_lane_pattern
Create Date: 2026-09-09

HITL KREPTD licence number on party + source_ref. Nie scrape. Nie Citizen API.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "126_kreptd_licence"
down_revision: str | None = "125_lane_pattern"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "kreptd_licence",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("licence_no", sa.String(length=64), nullable=False),
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
            name="fk_kreptd_licence_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_kreptd_licence_party",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_kreptd_licence_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "party_id",
            name="uq_kreptd_licence_org_party",
        ),
    )
    op.create_index("ix_kreptd_licence_organization_id", "kreptd_licence", ["organization_id"])
    op.create_index(
        "ix_kreptd_licence_org_licence",
        "kreptd_licence",
        ["organization_id", "licence_no"],
    )
    op.execute("ALTER TABLE kreptd_licence ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE kreptd_licence FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY kreptd_licence_tenant_isolation ON kreptd_licence
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS kreptd_licence_tenant_isolation ON kreptd_licence")
    op.drop_index("ix_kreptd_licence_org_licence", table_name="kreptd_licence")
    op.drop_index("ix_kreptd_licence_organization_id", table_name="kreptd_licence")
    op.drop_table("kreptd_licence")
