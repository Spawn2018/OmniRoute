"""create visibility_connector catalog with RLS FORCE

Revision ID: 208_visibility_connector
Revises: 207_tenant_contract_kek
Create Date: 2026-09-10

HITL konektor widoczności (token p44) jako dane. Nie live HTTP. Nie sekrety. Nie AIS.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "208_visibility_connector"
down_revision: str | None = "207_tenant_contract_kek"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "visibility_connector",
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
            name="fk_visibility_connector_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_visibility_connector_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "connector_code",
            name="uq_visibility_connector_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_visibility_connector_org_source_ref",
        ),
        sa.CheckConstraint(
            "connector_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_visibility_connector_code",
        ),
        sa.CheckConstraint("system_kind IN ('p44')", name="ck_visibility_connector_kind"),
    )
    # Lista per tenant: unique prefix albo ten indeks — nie sekwencyjne skanowanie.
    op.create_index(
        "ix_visibility_connector_organization_id",
        "visibility_connector",
        ["organization_id"],
    )
    op.execute("ALTER TABLE visibility_connector ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE visibility_connector FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY visibility_connector_tenant_isolation ON visibility_connector
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS visibility_connector_tenant_isolation ON visibility_connector"
    )
    op.drop_index("ix_visibility_connector_organization_id", table_name="visibility_connector")
    op.drop_table("visibility_connector")
