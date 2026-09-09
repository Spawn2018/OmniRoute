"""daterange exclusion on charge_template leftover P2c

Revision ID: 146_charge_template_span
Revises: 145_rate_card_match
Create Date: 2026-09-09

Nakładanie okien ważności liczy Postgres. Nie T-SQL. Nie parser w Pythonie.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "146_charge_template_span"
down_revision: str | None = "145_rate_card_match"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Inclusive [] — 30 czerwca i 1 lipca nie nachodzą. btree_gist już z 013.
    op.execute(
        "ALTER TABLE charge_template ADD COLUMN validity_span daterange "
        "GENERATED ALWAYS AS (daterange(valid_from, valid_until, '[]')) STORED NOT NULL"
    )
    op.drop_constraint(
        "uq_charge_template_org_code_member",
        "charge_template",
        type_="unique",
    )
    op.execute(
        """
        ALTER TABLE charge_template ADD CONSTRAINT ex_charge_template_no_overlap
        EXCLUDE USING gist (
          organization_id WITH =,
          template_code WITH =,
          charge_code WITH =,
          validity_span WITH &&
        )
        """
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE charge_template DROP CONSTRAINT IF EXISTS ex_charge_template_no_overlap"
    )
    op.execute("ALTER TABLE charge_template DROP COLUMN IF EXISTS validity_span")
    op.create_unique_constraint(
        "uq_charge_template_org_code_member",
        "charge_template",
        ["organization_id", "template_code", "charge_code"],
    )
