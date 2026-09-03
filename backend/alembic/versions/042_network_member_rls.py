"""create network_member catalog with RLS FORCE

Revision ID: 042_network_member_rls
Revises: 041_mail_draft_sent
Create Date: 2026-09-03

Ręczny katalog agenta w sieci tenanta. Nie scraping.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "042_network_member_rls"
down_revision: str | None = "041_mail_draft_sent"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "network_member",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("network_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("member_code", sa.String(length=32), nullable=False),
        sa.Column("legal_name", sa.String(length=128), nullable=False),
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
            name="fk_network_member_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["network_id"],
            ["network.id"],
            name="fk_network_member_network_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "network_id",
            "member_code",
            name="uq_network_member_org_network_code",
        ),
        sa.CheckConstraint(
            "member_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_network_member_code_snake",
        ),
    )
    op.create_index("ix_network_member_organization_id", "network_member", ["organization_id"])
    op.create_index(
        "ix_network_member_org_network",
        "network_member",
        ["organization_id", "network_id"],
    )
    op.execute("ALTER TABLE network_member ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE network_member FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY network_member_tenant_isolation ON network_member
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS network_member_tenant_isolation ON network_member")
    op.drop_index("ix_network_member_org_network", table_name="network_member")
    op.drop_index("ix_network_member_organization_id", table_name="network_member")
    op.drop_table("network_member")
