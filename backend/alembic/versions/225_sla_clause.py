"""create sla_clause catalog with RLS FORCE

Revision ID: 225_sla_clause
Revises: 224_visibility_connector_vendors
Create Date: 2026-09-11

CI1 HITL klauzula SLA na umowie. Nie extract. Nie kara SQL. Nie ciphertext.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "225_sla_clause"
down_revision: str | None = "224_visibility_connector_vendors"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "sla_clause",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("customer_contract_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("clause_code", sa.String(length=32), nullable=False),
        sa.Column("metric_kind", sa.String(length=16), nullable=False),
        sa.Column("threshold_label", sa.String(length=128), nullable=False),
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
            name="fk_sla_clause_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "customer_contract_id"],
            ["customer_contract.organization_id", "customer_contract.id"],
            name="fk_sla_clause_customer_contract",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_sla_clause_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "clause_code",
            name="uq_sla_clause_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_sla_clause_org_source_ref",
        ),
        sa.CheckConstraint(
            "clause_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_sla_clause_code",
        ),
        sa.CheckConstraint(
            "metric_kind IN ('otif', 'delay', 'damage', 'other')",
            name="ck_sla_clause_metric",
        ),
        sa.CheckConstraint(
            "char_length(btrim(threshold_label)) BETWEEN 1 AND 128",
            name="ck_sla_clause_threshold",
        ),
    )
    op.create_index(
        "ix_sla_clause_organization_id",
        "sla_clause",
        ["organization_id"],
    )
    op.create_index(
        "ix_sla_clause_org_contract",
        "sla_clause",
        ["organization_id", "customer_contract_id"],
    )
    op.execute("ALTER TABLE sla_clause ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE sla_clause FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY sla_clause_tenant_isolation ON sla_clause
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS sla_clause_tenant_isolation ON sla_clause")
    op.drop_index("ix_sla_clause_org_contract", table_name="sla_clause")
    op.drop_index("ix_sla_clause_organization_id", table_name="sla_clause")
    op.drop_table("sla_clause")
