"""create carrier_inquiry buy-side record with RLS FORCE

Revision ID: 043_carrier_inquiry_rls
Revises: 042_network_member_rls
Create Date: 2026-09-03

Zapytanie do agenta (network_member). Nie live HTTP. Nie kwota.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "043_carrier_inquiry_rls"
down_revision: str | None = "042_network_member_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_network_member_org_id",
        "network_member",
        ["organization_id", "id"],
    )
    op.create_table(
        "carrier_inquiry",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("network_member_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_ref", sa.String(length=256), nullable=False),
        sa.Column("status", sa.String(length=8), nullable=False),
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
            name="fk_carrier_inquiry_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "network_member_id"],
            ["network_member.organization_id", "network_member.id"],
            name="fk_carrier_inquiry_network_member",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint("status = 'draft'", name="ck_carrier_inquiry_status_draft"),
    )
    op.create_index(
        "ix_carrier_inquiry_organization_id",
        "carrier_inquiry",
        ["organization_id"],
    )
    op.create_index(
        "ix_carrier_inquiry_org_member",
        "carrier_inquiry",
        ["organization_id", "network_member_id"],
    )
    op.create_index(
        "ix_carrier_inquiry_org_created",
        "carrier_inquiry",
        ["organization_id", "created_at"],
    )
    op.execute("ALTER TABLE carrier_inquiry ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE carrier_inquiry FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY carrier_inquiry_tenant_isolation ON carrier_inquiry
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS carrier_inquiry_tenant_isolation ON carrier_inquiry")
    op.drop_index("ix_carrier_inquiry_org_created", table_name="carrier_inquiry")
    op.drop_index("ix_carrier_inquiry_org_member", table_name="carrier_inquiry")
    op.drop_index("ix_carrier_inquiry_organization_id", table_name="carrier_inquiry")
    op.drop_table("carrier_inquiry")
    op.drop_constraint("uq_network_member_org_id", "network_member", type_="unique")
