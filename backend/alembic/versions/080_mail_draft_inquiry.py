"""allow mail_draft subject_kind carrier_inquiry leftover O4

Revision ID: 080_mail_draft_inquiry
Revises: 079_quotation_incoterm
Create Date: 2026-09-08

Szkic zapytania do agenta. Nie send. Nie O5.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "080_mail_draft_inquiry"
down_revision: str | None = "079_quotation_incoterm"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_NEW = "subject_kind IN ('extraction_draft','carrier_inquiry')"
_OLD = "subject_kind = 'extraction_draft'"


def upgrade() -> None:
    op.drop_constraint("ck_mail_draft_subject_kind", "mail_draft", type_="check")
    op.create_check_constraint("ck_mail_draft_subject_kind", "mail_draft", _NEW)


def downgrade() -> None:
    op.drop_constraint("ck_mail_draft_subject_kind", "mail_draft", type_="check")
    op.create_check_constraint("ck_mail_draft_subject_kind", "mail_draft", _OLD)
