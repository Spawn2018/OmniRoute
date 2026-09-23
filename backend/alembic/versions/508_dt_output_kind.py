"""expand document_template output_kind allowlist

Revision ID: 508_dt_output_kind
Revises: 507_local_charge_warning_mark
Create Date: 2026-09-23

D9f rest: intended pdf|zpl HITL. Nie silnik bajtów.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "508_dt_output_kind"
down_revision: str | None = "507_local_charge_warning_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint(
        "ck_document_template_output",
        "document_template",
        type_="check",
    )
    op.create_check_constraint(
        "ck_document_template_output",
        "document_template",
        "output_kind IN ('html_print','pdf','zpl')",
    )


def downgrade() -> None:
    op.execute(
        "UPDATE document_template SET output_kind = 'html_print' "
        "WHERE output_kind IN ('pdf','zpl')"
    )
    op.drop_constraint(
        "ck_document_template_output",
        "document_template",
        type_="check",
    )
    op.create_check_constraint(
        "ck_document_template_output",
        "document_template",
        "output_kind IN ('html_print')",
    )
