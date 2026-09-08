"""add quotation incoterm leftover I0/U2

Revision ID: 079_quotation_incoterm
Revises: 078_carrier_inquiry_batch
Create Date: 2026-09-08

Incoterms na wycenie. DAP/DDP bez miejsca blokuje CHECK. Nie cytat ICC.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "079_quotation_incoterm"
down_revision: str | None = "078_carrier_inquiry_batch"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_CODES = "EXW,FCA,CPT,CIP,DAP,DPU,DDP,FAS,FOB,CFR,CIF"
_RULES = (
    f"(incoterm IS NULL AND incoterms_version IS NULL AND trade_side IS NULL "
    f"AND named_place IS NULL) OR "
    f"(incoterm IN ({','.join(repr(code) for code in _CODES.split(','))}) "
    f"AND incoterms_version IN ('2020','2010') "
    f"AND trade_side IN ('import','export') "
    f"AND (incoterm NOT IN ('DAP','DDP') OR "
    f"(named_place IS NOT NULL AND btrim(named_place) <> '')))"
)


def upgrade() -> None:
    op.add_column("quotation", sa.Column("incoterm", sa.CHAR(length=3), nullable=True))
    op.add_column("quotation", sa.Column("incoterms_version", sa.CHAR(length=4), nullable=True))
    op.add_column("quotation", sa.Column("trade_side", sa.String(length=6), nullable=True))
    op.add_column("quotation", sa.Column("named_place", sa.String(length=128), nullable=True))
    op.create_check_constraint("ck_quotation_incoterm", "quotation", _RULES)


def downgrade() -> None:
    op.drop_constraint("ck_quotation_incoterm", "quotation", type_="check")
    op.drop_column("quotation", "named_place")
    op.drop_column("quotation", "trade_side")
    op.drop_column("quotation", "incoterms_version")
    op.drop_column("quotation", "incoterm")
