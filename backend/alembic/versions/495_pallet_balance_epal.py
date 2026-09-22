"""widen pallet_balance.pallet_kind with epal

Revision ID: 495_pallet_balance_epal
Revises: 494_ocean_bill_number_pool
Create Date: 2026-09-22

D7d trzeci rodzaj salda. Nie giełda. Nie ledger ujemny.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "495_pallet_balance_epal"
down_revision: str | None = "494_ocean_bill_number_pool"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_WIDE = "pallet_kind IN ('chep','lpr','epal')"
_NARROW = "pallet_kind IN ('chep','lpr')"


def upgrade() -> None:
    op.drop_constraint("ck_pallet_balance_kind", "pallet_balance", type_="check")
    op.create_check_constraint("ck_pallet_balance_kind", "pallet_balance", _WIDE)


def downgrade() -> None:
    # CHECK z powrotem do chep|lpr nie wstanie, dopóki zostaną wiersze epal.
    op.execute("DELETE FROM pallet_balance WHERE pallet_kind = 'epal'")
    op.drop_constraint("ck_pallet_balance_kind", "pallet_balance", type_="check")
    op.create_check_constraint("ck_pallet_balance_kind", "pallet_balance", _NARROW)
