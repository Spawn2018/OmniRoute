"""create invoice_match_candidate catalog with RLS FORCE

Revision ID: 435_invoice_match_cand
Revises: 434_rel_doc_requirement
Create Date: 2026-09-17

F10 HITL invoice_match_candidate. Nie live ranking SQL. Nie auto-link.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "435_invoice_match_cand"
down_revision: str | None = "434_rel_doc_requirement"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "invoice_match_candidate",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("candidate_code", sa.String(length=32), nullable=False),
        sa.Column("candidate_kind", sa.String(length=16), nullable=False),
        sa.Column("source_ref", sa.String(length=256), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("created_by", PGUUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
            name="fk_invoice_match_candidate_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_invoice_match_candidate_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "candidate_code",
            name="uq_invoice_match_candidate_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_invoice_match_candidate_org_source_ref",
        ),
        sa.CheckConstraint(
            "candidate_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_invoice_match_candidate_code",
        ),
        sa.CheckConstraint(
            "candidate_kind IN ('proposed', 'held', 'rejected', 'other')",
            name="ck_invoice_match_candidate_candidate_kind",
        ),
    )
    op.create_index(
        "ix_invoice_match_candidate_organization_id",
        "invoice_match_candidate",
        ["organization_id"],
    )
    op.execute("ALTER TABLE invoice_match_candidate ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE invoice_match_candidate FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY invoice_match_candidate_tenant_isolation
        ON invoice_match_candidate
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS invoice_match_candidate_tenant_isolation "
        "ON invoice_match_candidate",
    )
    op.drop_index(
        "ix_invoice_match_candidate_organization_id",
        table_name="invoice_match_candidate",
    )
    op.drop_table("invoice_match_candidate")
