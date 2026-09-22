"""widen shipment_document.document_kind with rod

Revision ID: 496_shipment_document_rod
Revises: 495_pallet_balance_epal
Create Date: 2026-09-22

D4b rodzaj dokumentu rod. Nie skan. Nie token pod.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "496_shipment_document_rod"
down_revision: str | None = "495_pallet_balance_epal"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_WIDE = "document_kind IN ('noted', 'attached', 'other', 'rod')"
_NARROW = "document_kind IN ('noted', 'attached', 'other')"


def upgrade() -> None:
    op.drop_constraint("ck_shipment_document_kind", "shipment_document", type_="check")
    op.create_check_constraint("ck_shipment_document_kind", "shipment_document", _WIDE)


def downgrade() -> None:
    # CHECK bez rod nie wstanie, dopóki zostaną takie wiersze.
    op.execute("DELETE FROM shipment_document WHERE document_kind = 'rod'")
    op.drop_constraint("ck_shipment_document_kind", "shipment_document", type_="check")
    op.create_check_constraint("ck_shipment_document_kind", "shipment_document", _NARROW)
