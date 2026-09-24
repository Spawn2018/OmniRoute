"""add fuel_index_id on rate_line leftover EXP1

Revision ID: 522_rate_line_fuel_index_id
Revises: 521_charge_code_source_ref
Create Date: 2026-09-24

Opcjonalny FK katalogu fuel_index. Pin index_id zostaje. Nie float. Nie mnożenie FSC.
Rozszerza trigger niemutowalności o fuel_index_id.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "522_rate_line_fuel_index_id"
down_revision: str | None = "521_charge_code_source_ref"
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
     OR NEW.index_id IS DISTINCT FROM OLD.index_id
     OR NEW.fuel_index_id IS DISTINCT FROM OLD.fuel_index_id
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
     OR NEW.allotment_teu IS DISTINCT FROM OLD.allotment_teu
     OR NEW.spot_or_contract IS DISTINCT FROM OLD.spot_or_contract
     OR NEW.index_id IS DISTINCT FROM OLD.index_id
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
        sa.Column("fuel_index_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_rate_line_fuel_index",
        "rate_line",
        "fuel_index",
        ["organization_id", "fuel_index_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )
    op.execute(_IMMUTABLE_FN)


def downgrade() -> None:
    op.execute(_IMMUTABLE_FN_DOWN)
    op.drop_constraint("fk_rate_line_fuel_index", "rate_line", type_="foreignkey")
    op.drop_column("rate_line", "fuel_index_id")
