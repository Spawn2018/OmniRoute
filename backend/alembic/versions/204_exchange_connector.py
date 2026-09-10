"""create exchange_connector catalog with RLS FORCE

Revision ID: 204_exchange_connector
Revises: 203_idp_connector
Create Date: 2026-09-10

HITL konektor giełdy (token trans_eu) jako dane. Nie live HTTP. Nie sekrety. Nie SPA.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "204_exchange_connector"
down_revision: str | None = "203_idp_connector"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "exchange_connector",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("connector_code", sa.String(length=32), nullable=False),
        sa.Column("system_kind", sa.String(length=16), nullable=False),
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
        sa.Column("created_by", PGUUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
            name="fk_exchange_connector_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_exchange_connector_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "connector_code",
            name="uq_exchange_connector_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_exchange_connector_org_source_ref",
        ),
        sa.CheckConstraint(
            "connector_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_exchange_connector_code",
        ),
        sa.CheckConstraint(
            "system_kind IN ('trans_eu')",
            name="ck_exchange_connector_kind",
        ),
    )
    # Lista per tenant: unique prefix albo ten indeks — nie sekwencyjne skanowanie.
    op.create_index(
        "ix_exchange_connector_organization_id",
        "exchange_connector",
        ["organization_id"],
    )
    op.execute("ALTER TABLE exchange_connector ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE exchange_connector FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY exchange_connector_tenant_isolation ON exchange_connector
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS exchange_connector_tenant_isolation ON exchange_connector")
    op.drop_index("ix_exchange_connector_organization_id", table_name="exchange_connector")
    op.drop_table("exchange_connector")
