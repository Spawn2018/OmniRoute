"""create rate_line buy-side immutable with RLS

Revision ID: 008_rate_line_rls
Revises: 007_charge_code_rls
Create Date: 2026-09-01
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "008_rate_line_rls"
down_revision: str | None = "007_charge_code_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"

_IMMUTABLE_FN = """
CREATE FUNCTION rate_line_forbid_mutate() RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF TG_OP = 'DELETE' THEN
    RAISE EXCEPTION 'rate_line niemutowalny';
  END IF;
  IF NEW.organization_id IS DISTINCT FROM OLD.organization_id
     OR NEW.charge_code IS DISTINCT FROM OLD.charge_code
     OR NEW.amount IS DISTINCT FROM OLD.amount
     OR NEW.currency IS DISTINCT FROM OLD.currency
     OR NEW.source_ref IS DISTINCT FROM OLD.source_ref
     OR NEW.created_by IS DISTINCT FROM OLD.created_by
     OR NEW.id IS DISTINCT FROM OLD.id
  THEN
    RAISE EXCEPTION 'rate_line niemutowalny';
  END IF;
  IF OLD.superseded_by IS NOT NULL
     AND NEW.superseded_by IS DISTINCT FROM OLD.superseded_by
  THEN
    RAISE EXCEPTION 'rate_line już zastąpiony';
  END IF;
  RETURN NEW;
END;
$$;
"""


def upgrade() -> None:
    op.create_table(
        "rate_line",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("charge_code", sa.String(length=32), nullable=False),
        sa.Column("amount", sa.Numeric(14, 4), nullable=False),
        sa.Column("currency", sa.CHAR(length=3), nullable=False),
        sa.Column("source_ref", sa.String(length=512), nullable=False),
        sa.Column("superseded_by", postgresql.UUID(as_uuid=True), nullable=True),
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
            name="fk_rate_line_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["superseded_by"],
            ["rate_line.id"],
            name="fk_rate_line_superseded_by",
            ondelete="RESTRICT",
        ),
    )
    op.create_index("ix_rate_line_organization_id", "rate_line", ["organization_id"])

    op.execute("ALTER TABLE rate_line ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE rate_line FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY rate_line_tenant_isolation ON rate_line
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )
    op.execute(_IMMUTABLE_FN)
    op.execute(
        """
        CREATE TRIGGER rate_line_forbid_mutate
        BEFORE UPDATE OR DELETE ON rate_line
        FOR EACH ROW EXECUTE FUNCTION rate_line_forbid_mutate()
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS rate_line_forbid_mutate ON rate_line")
    op.execute("DROP FUNCTION IF EXISTS rate_line_forbid_mutate()")
    op.execute("DROP POLICY IF EXISTS rate_line_tenant_isolation ON rate_line")
    op.drop_index("ix_rate_line_organization_id", table_name="rate_line")
    op.drop_table("rate_line")
