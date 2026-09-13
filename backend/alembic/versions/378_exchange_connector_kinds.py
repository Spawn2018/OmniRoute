"""expand exchange_connector system_kind CHECK for P0 boards

Revision ID: 378_exchange_connector_kinds
Revises: 377_po_financing_mark
Create Date: 2026-09-14

BR5.2 rozszerza allowlistę kind na katalogu 271.0. Nie live HTTP. Nie sekrety.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "378_exchange_connector_kinds"
down_revision: str | None = "377_po_financing_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_NEW_KINDS = "trans_eu', 'timocom', 'teleroute', 'transporeon', 'other"
_OLD_KINDS = "trans_eu"


def upgrade() -> None:
    op.drop_constraint("ck_exchange_connector_kind", "exchange_connector", type_="check")
    op.create_check_constraint(
        "ck_exchange_connector_kind",
        "exchange_connector",
        f"system_kind IN ('{_NEW_KINDS}')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_exchange_connector_kind", "exchange_connector", type_="check")
    op.create_check_constraint(
        "ck_exchange_connector_kind",
        "exchange_connector",
        f"system_kind IN ('{_OLD_KINDS}')",
    )
