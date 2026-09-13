"""create outcome_ledger catalog with RLS FORCE

Revision ID: 343_outcome_ledger
Revises: 342_suggestion_ledger
Create Date: 2026-09-13

AI1.1 HITL outcome_ledger. Nie liczenie błędu przedziału. Nie FK do suggestion_ledger.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "343_outcome_ledger"
down_revision: str | None = "342_suggestion_ledger"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"
_SNAKE = r"^[a-z][a-z0-9_]{1,31}$"


def upgrade() -> None:
    op.create_table(
        "outcome_ledger",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("target_bc", sa.String(length=32), nullable=False),
        sa.Column("entity_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("suggestion_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("outcome_kind", sa.String(length=16), nullable=False),
        sa.Column("actual_value", sa.Numeric(14, 4), nullable=False),
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
            name="fk_outcome_ledger_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_outcome_ledger_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_outcome_ledger_org_source_ref",
        ),
        sa.CheckConstraint(
            "outcome_kind IN ('eta', 'rate', 'route', 'other')",
            name="ck_outcome_ledger_kind",
        ),
        sa.CheckConstraint(
            f"target_bc ~ '{_SNAKE}'",
            name="ck_outcome_ledger_target_bc",
        ),
    )
    op.create_index(
        "ix_outcome_ledger_organization_id",
        "outcome_ledger",
        ["organization_id"],
    )
    op.execute("ALTER TABLE outcome_ledger ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE outcome_ledger FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY outcome_ledger_tenant_isolation ON outcome_ledger
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS outcome_ledger_tenant_isolation ON outcome_ledger",
    )
    op.drop_index(
        "ix_outcome_ledger_organization_id",
        table_name="outcome_ledger",
    )
    op.drop_table("outcome_ledger")
