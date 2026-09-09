"""add ADR tunnel and IMDG SG on dangerous_good leftover EXP0.9

Revision ID: 132_dangerous_good_adr
Revises: 131_cargo_claim_cmr
Create Date: 2026-09-09

HITL tunel ADR + grupa SG. LLM nie nadaje klasy. Nie live IMO.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "132_dangerous_good_adr"
down_revision: str | None = "131_cargo_claim_cmr"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SG = ", ".join(["'none'"] + [f"'sg{n}'" for n in range(1, 19)])


def upgrade() -> None:
    op.add_column(
        "dangerous_good",
        sa.Column("adr_tunnel_code", sa.String(length=1), nullable=True),
    )
    op.add_column(
        "dangerous_good",
        sa.Column("segregation_group", sa.String(length=8), nullable=True),
    )
    op.execute(
        """
        UPDATE dangerous_good SET
            adr_tunnel_code = 'A',
            segregation_group = 'none'
        WHERE adr_tunnel_code IS NULL
        """
    )
    op.alter_column("dangerous_good", "adr_tunnel_code", nullable=False)
    op.alter_column("dangerous_good", "segregation_group", nullable=False)
    op.create_check_constraint(
        "ck_dangerous_good_adr_tunnel",
        "dangerous_good",
        "adr_tunnel_code IN ('A', 'B', 'C', 'D', 'E')",
    )
    op.create_check_constraint(
        "ck_dangerous_good_segregation_group",
        "dangerous_good",
        f"segregation_group IN ({_SG})",
    )


def downgrade() -> None:
    op.drop_constraint("ck_dangerous_good_segregation_group", "dangerous_good", type_="check")
    op.drop_constraint("ck_dangerous_good_adr_tunnel", "dangerous_good", type_="check")
    op.drop_column("dangerous_good", "segregation_group")
    op.drop_column("dangerous_good", "adr_tunnel_code")
