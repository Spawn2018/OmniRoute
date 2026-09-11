"""create clause_notice catalog with RLS FORCE

Revision ID: 229_clause_notice
Revises: 228_impact_scenario
Create Date: 2026-09-11

CI3 HITL powiadomienie o klauzuli jako dane. Nie 409. Nie auto-kara.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "229_clause_notice"
down_revision: str | None = "228_impact_scenario"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "clause_notice",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("notice_code", sa.String(length=32), nullable=False),
        sa.Column("clause_label", sa.String(length=128), nullable=False),
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
            name="fk_clause_notice_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_clause_notice_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "notice_code",
            name="uq_clause_notice_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_clause_notice_org_source_ref",
        ),
        sa.CheckConstraint(
            "notice_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_clause_notice_code",
        ),
        sa.CheckConstraint(
            "char_length(btrim(clause_label)) BETWEEN 1 AND 128",
            name="ck_clause_notice_clause_label",
        ),
    )
    op.create_index(
        "ix_clause_notice_organization_id",
        "clause_notice",
        ["organization_id"],
    )
    op.execute("ALTER TABLE clause_notice ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE clause_notice FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY clause_notice_tenant_isolation ON clause_notice
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS clause_notice_tenant_isolation ON clause_notice")
    op.drop_index("ix_clause_notice_organization_id", table_name="clause_notice")
    op.drop_table("clause_notice")
