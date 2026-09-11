"""create impact_scenario catalog with RLS FORCE

Revision ID: 228_impact_scenario
Revises: 227_remediation_option
Create Date: 2026-09-11

CI6 HITL scenariusz skutku jako dane. Nie EBITDA SQL. Nie silnik.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "228_impact_scenario"
down_revision: str | None = "227_remediation_option"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "impact_scenario",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("scenario_code", sa.String(length=32), nullable=False),
        sa.Column("chain_label", sa.String(length=64), nullable=False),
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
            name="fk_impact_scenario_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_impact_scenario_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "scenario_code",
            name="uq_impact_scenario_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_impact_scenario_org_source_ref",
        ),
        sa.CheckConstraint(
            "scenario_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_impact_scenario_code",
        ),
        sa.CheckConstraint(
            "char_length(btrim(chain_label)) BETWEEN 1 AND 64",
            name="ck_impact_scenario_chain_label",
        ),
    )
    op.create_index(
        "ix_impact_scenario_organization_id",
        "impact_scenario",
        ["organization_id"],
    )
    op.execute("ALTER TABLE impact_scenario ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE impact_scenario FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY impact_scenario_tenant_isolation ON impact_scenario
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS impact_scenario_tenant_isolation ON impact_scenario")
    op.drop_index("ix_impact_scenario_organization_id", table_name="impact_scenario")
    op.drop_table("impact_scenario")
