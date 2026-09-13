"""create counterfactual_run catalog with RLS FORCE

Revision ID: 344_counterfactual_run
Revises: 343_outcome_ledger
Create Date: 2026-09-13

AI1.2 HITL counterfactual_run. Nie silnik what-if. Nie kwota oszczednosci.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "344_counterfactual_run"
down_revision: str | None = "343_outcome_ledger"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"
_SNAKE = r"^[a-z][a-z0-9_]{1,31}$"


def upgrade() -> None:
    op.create_table(
        "counterfactual_run",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("run_code", sa.String(length=32), nullable=False),
        sa.Column("baseline_label", sa.String(length=256), nullable=False),
        sa.Column("levers_label", sa.String(length=256), nullable=False),
        sa.Column("result_label", sa.String(length=256), nullable=False),
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
            name="fk_counterfactual_run_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_counterfactual_run_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "run_code",
            name="uq_counterfactual_run_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_counterfactual_run_org_source_ref",
        ),
        sa.CheckConstraint(
            f"run_code ~ '{_SNAKE}'",
            name="ck_counterfactual_run_code",
        ),
    )
    op.create_index(
        "ix_counterfactual_run_organization_id",
        "counterfactual_run",
        ["organization_id"],
    )
    op.execute("ALTER TABLE counterfactual_run ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE counterfactual_run FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY counterfactual_run_tenant_isolation ON counterfactual_run
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS counterfactual_run_tenant_isolation ON counterfactual_run",
    )
    op.drop_index(
        "ix_counterfactual_run_organization_id",
        table_name="counterfactual_run",
    )
    op.drop_table("counterfactual_run")
