"""optional branding_ref on document_template

Revision ID: 499_document_template_branding
Revises: 498_network_print_requirement
Create Date: 2026-09-22

D9f branding HITL. Nie PDF. Nie ZPL. Nie bajty.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "499_document_template_branding"
down_revision: str | None = "498_network_print_requirement"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "document_template",
        sa.Column("branding_ref", sa.String(length=64), nullable=True),
    )
    op.create_check_constraint(
        "ck_document_template_branding",
        "document_template",
        "branding_ref IS NULL OR branding_ref ~ '^[a-z0-9][a-z0-9_-]{1,63}$'",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_document_template_branding",
        "document_template",
        type_="check",
    )
    op.drop_column("document_template", "branding_ref")
