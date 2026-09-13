"""create benefit_ledger catalog with RLS FORCE

Revision ID: 345_benefit_ledger
Revises: 344_counterfactual_run
Create Date: 2026-09-13

AI1.3 HITL benefit_ledger. Nie druga marza. Nie SQL z charge.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "345_benefit_ledger"
down_revision: str | None = "344_counterfactual_run"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"
_SNAKE = r"^[a-z][a-z0-9_]{1,31}$"
_CCY = r"^[A-Z]{3}$"


def upgrade() -> None:
    op.create_table(
        "benefit_ledger",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("benefit_code", sa.String(length=32), nullable=False),
        sa.Column("method_label", sa.String(length=256), nullable=False),
        sa.Column("hours_saved", sa.Numeric(14, 4), nullable=False),
        sa.Column("saved_amount", sa.Numeric(14, 4), nullable=False),
        sa.Column("saved_currency", sa.CHAR(length=3), nullable=False),
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
            name="fk_benefit_ledger_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_benefit_ledger_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "benefit_code",
            name="uq_benefit_ledger_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_benefit_ledger_org_source_ref",
        ),
        sa.CheckConstraint(
            f"benefit_code ~ '{_SNAKE}'",
            name="ck_benefit_ledger_code",
        ),
        sa.CheckConstraint(
            f"saved_currency ~ '{_CCY}'",
            name="ck_benefit_ledger_currency",
        ),
    )
    op.create_index(
        "ix_benefit_ledger_organization_id",
        "benefit_ledger",
        ["organization_id"],
    )
    op.execute("ALTER TABLE benefit_ledger ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE benefit_ledger FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY benefit_ledger_tenant_isolation ON benefit_ledger
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS benefit_ledger_tenant_isolation ON benefit_ledger",
    )
    op.drop_index(
        "ix_benefit_ledger_organization_id",
        table_name="benefit_ledger",
    )
    op.drop_table("benefit_ledger")
