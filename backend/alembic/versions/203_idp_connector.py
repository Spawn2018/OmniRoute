"""create idp_connector catalog with RLS FORCE

Revision ID: 203_idp_connector
Revises: 202_terminal_slot_connector
Create Date: 2026-09-10

HITL konektor IdP (token auth0) jako dane. Nie live HTTP. Nie sekrety. Nie login.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "203_idp_connector"
down_revision: str | None = "202_terminal_slot_connector"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "idp_connector",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("connector_code", sa.String(length=32), nullable=False),
        sa.Column("provider_code", sa.String(length=16), nullable=False),
        sa.Column("public_domain", sa.String(length=253), nullable=True),
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
            name="fk_idp_connector_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_idp_connector_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "connector_code",
            name="uq_idp_connector_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_idp_connector_org_source_ref",
        ),
        sa.CheckConstraint(
            "connector_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_idp_connector_code",
        ),
        sa.CheckConstraint(
            "provider_code IN ('auth0')",
            name="ck_idp_connector_provider",
        ),
        sa.CheckConstraint(
            "public_domain IS NULL OR public_domain ~ "
            "'^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?"
            "(\\.[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?)+$'",
            name="ck_idp_connector_public_domain",
        ),
    )
    # Lista per tenant: unique prefix albo ten indeks — nie sekwencyjne skanowanie.
    op.create_index(
        "ix_idp_connector_organization_id",
        "idp_connector",
        ["organization_id"],
    )
    op.execute("ALTER TABLE idp_connector ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE idp_connector FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY idp_connector_tenant_isolation ON idp_connector
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS idp_connector_tenant_isolation ON idp_connector")
    op.drop_index("ix_idp_connector_organization_id", table_name="idp_connector")
    op.drop_table("idp_connector")
