"""create sap_connector catalog with RLS FORCE

Revision ID: 214_sap_connector
Revises: 213_otif_mark
Create Date: 2026-09-11

HITL konektor SAP/Oracle jako dane. Nie live SOAP. Nie sekrety. Nie SQL do SAP.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "214_sap_connector"
down_revision: str | None = "213_otif_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "sap_connector",
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
            name="fk_sap_connector_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_sap_connector_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "connector_code",
            name="uq_sap_connector_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_sap_connector_org_source_ref",
        ),
        sa.CheckConstraint(
            "connector_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_sap_connector_code",
        ),
        sa.CheckConstraint(
            "system_kind IN ('sap', 'oracle')",
            name="ck_sap_connector_kind",
        ),
    )
    op.create_index(
        "ix_sap_connector_organization_id",
        "sap_connector",
        ["organization_id"],
    )
    op.execute("ALTER TABLE sap_connector ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE sap_connector FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY sap_connector_tenant_isolation ON sap_connector
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS sap_connector_tenant_isolation ON sap_connector")
    op.drop_index("ix_sap_connector_organization_id", table_name="sap_connector")
    op.drop_table("sap_connector")
