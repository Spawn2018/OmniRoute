"""add spot_or_contract on rate_line leftover EXP1

Revision ID: 519_rate_line_spot_contract
Revises: 518_rate_line_allotment
Create Date: 2026-09-24

HITL opcjonalny stance spot|contract|other. Nie matching. Nie float.
Rozszerza trigger niemutowalności o allotment_teu + spot_or_contract.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "519_rate_line_spot_contract"
down_revision: str | None = "518_rate_line_allotment"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_IMMUTABLE_FN = """
CREATE OR REPLACE FUNCTION rate_line_forbid_mutate() RETURNS trigger
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
     OR NEW.allotment_teu IS DISTINCT FROM OLD.allotment_teu
     OR NEW.spot_or_contract IS DISTINCT FROM OLD.spot_or_contract
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

_IMMUTABLE_FN_DOWN = """
CREATE OR REPLACE FUNCTION rate_line_forbid_mutate() RETURNS trigger
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
    op.add_column(
        "rate_line",
        sa.Column("spot_or_contract", sa.Text(), nullable=True),
    )
    op.create_check_constraint(
        "ck_rate_line_spot_or_contract",
        "rate_line",
        "spot_or_contract IS NULL OR spot_or_contract IN ('spot', 'contract', 'other')",
    )
    op.execute(_IMMUTABLE_FN)


def downgrade() -> None:
    op.execute(_IMMUTABLE_FN_DOWN)
    op.drop_constraint("ck_rate_line_spot_or_contract", "rate_line", type_="check")
    op.drop_column("rate_line", "spot_or_contract")
