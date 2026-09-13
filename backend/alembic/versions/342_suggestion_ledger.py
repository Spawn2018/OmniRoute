"""create suggestion_ledger catalog with RLS FORCE

Revision ID: 342_suggestion_ledger
Revises: 341_quote_validity_mark
Create Date: 2026-09-13

AI1.0 HITL suggestion_ledger. Nie zapis LLM. Nie CRPS liczone.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "342_suggestion_ledger"
down_revision: str | None = "341_quote_validity_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"
_SNAKE = r"^[a-z][a-z0-9_]{1,31}$"


def upgrade() -> None:
    op.create_table(
        "suggestion_ledger",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("target_bc", sa.String(length=32), nullable=False),
        sa.Column("entity_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("suggestion_kind", sa.String(length=16), nullable=False),
        sa.Column("interval_low", sa.Numeric(14, 4), nullable=False),
        sa.Column("interval_high", sa.Numeric(14, 4), nullable=False),
        sa.Column("model_version", sa.String(length=32), nullable=False),
        sa.Column("prompt_version", sa.String(length=32), nullable=False),
        sa.Column("reaction", sa.String(length=16), nullable=False),
        sa.Column("changed_to", sa.String(length=256), nullable=False),
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
            name="fk_suggestion_ledger_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_suggestion_ledger_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_suggestion_ledger_org_source_ref",
        ),
        sa.CheckConstraint(
            "suggestion_kind IN ('eta', 'rate', 'route', 'other')",
            name="ck_suggestion_ledger_kind",
        ),
        sa.CheckConstraint(
            "reaction IN ('accept', 'modify', 'reject')",
            name="ck_suggestion_ledger_reaction",
        ),
        sa.CheckConstraint(
            "interval_high >= interval_low",
            name="ck_suggestion_ledger_interval",
        ),
        sa.CheckConstraint(
            "(reaction IN ('accept', 'reject') AND changed_to = 'none') "
            "OR (reaction = 'modify' AND changed_to <> 'none')",
            name="ck_suggestion_ledger_changed",
        ),
        sa.CheckConstraint(
            f"target_bc ~ '{_SNAKE}'",
            name="ck_suggestion_ledger_target_bc",
        ),
        sa.CheckConstraint(
            f"model_version ~ '{_SNAKE}'",
            name="ck_suggestion_ledger_model",
        ),
        sa.CheckConstraint(
            f"prompt_version ~ '{_SNAKE}'",
            name="ck_suggestion_ledger_prompt",
        ),
    )
    op.create_index(
        "ix_suggestion_ledger_organization_id",
        "suggestion_ledger",
        ["organization_id"],
    )
    op.execute("ALTER TABLE suggestion_ledger ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE suggestion_ledger FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY suggestion_ledger_tenant_isolation ON suggestion_ledger
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS suggestion_ledger_tenant_isolation ON suggestion_ledger",
    )
    op.drop_index(
        "ix_suggestion_ledger_organization_id",
        table_name="suggestion_ledger",
    )
    op.drop_table("suggestion_ledger")
