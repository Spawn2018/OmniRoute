"""create tower_impact catalog with RLS FORCE

Revision ID: 138_tower_impact
Revises: 137_telematics_connector
Create Date: 2026-09-09

HITL etap łańcucha + status umowy. Nie silnik EBITDA. Nie scoring osoby.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "138_tower_impact"
down_revision: str | None = "137_telematics_connector"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "tower_impact",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("chain_stage", sa.String(length=16), nullable=False),
        sa.Column("contract_data_status", sa.String(length=16), nullable=False),
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
            name="fk_tower_impact_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_tower_impact_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_tower_impact_org_source_ref",
        ),
        sa.CheckConstraint(
            "chain_stage IN ('stock','production','sales','ebitda')",
            name="ck_tower_impact_stage",
        ),
        sa.CheckConstraint(
            "contract_data_status IN ('missing','recorded')",
            name="ck_tower_impact_pact",
        ),
    )
    # Lista per tenant — RLS filtruje organization_id; unique source_ref nie zastępuje tego skanu.
    op.create_index(
        "ix_tower_impact_organization_id",
        "tower_impact",
        ["organization_id"],
    )
    op.execute("ALTER TABLE tower_impact ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE tower_impact FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY tower_impact_tenant_isolation ON tower_impact
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS tower_impact_tenant_isolation ON tower_impact")
    op.drop_index("ix_tower_impact_organization_id", table_name="tower_impact")
    op.drop_table("tower_impact")
