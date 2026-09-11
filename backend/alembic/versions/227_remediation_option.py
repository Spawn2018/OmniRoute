"""create remediation_option catalog with RLS FORCE

Revision ID: 227_remediation_option
Revises: 226_delay_forecast
Create Date: 2026-09-11

CI6 HITL opcja naprawy jako dane. Nie kwota. Nie S11 silnik.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "227_remediation_option"
down_revision: str | None = "226_delay_forecast"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "remediation_option",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("option_code", sa.String(length=32), nullable=False),
        sa.Column("option_kind", sa.String(length=16), nullable=False),
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
            name="fk_remediation_option_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_remediation_option_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "option_code",
            name="uq_remediation_option_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_remediation_option_org_source_ref",
        ),
        sa.CheckConstraint(
            "option_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_remediation_option_code",
        ),
        sa.CheckConstraint(
            "option_kind IN ('rebook', 'wait', 'claim', 'other')",
            name="ck_remediation_option_kind",
        ),
    )
    op.create_index(
        "ix_remediation_option_organization_id",
        "remediation_option",
        ["organization_id"],
    )
    op.execute("ALTER TABLE remediation_option ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE remediation_option FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY remediation_option_tenant_isolation ON remediation_option
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS remediation_option_tenant_isolation ON remediation_option"
    )
    op.drop_index(
        "ix_remediation_option_organization_id",
        table_name="remediation_option",
    )
    op.drop_table("remediation_option")
