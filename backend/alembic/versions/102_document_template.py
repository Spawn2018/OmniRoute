"""create document_template catalog with RLS FORCE

Revision ID: 102_document_template
Revises: 101_pallet_balance
Create Date: 2026-09-08

Szablon wydruku jako dane. Nie PDF. Nie etykieta sieci. Nie C8.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "102_document_template"
down_revision: str | None = "101_pallet_balance"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "document_template",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("template_kind", sa.String(length=16), nullable=False),
        sa.Column("language", sa.String(length=8), nullable=False),
        sa.Column("layout_ref", sa.String(length=64), nullable=False),
        sa.Column("output_kind", sa.String(length=16), nullable=False),
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
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
            name="fk_document_template_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_document_template_org_id"),
        sa.CheckConstraint(
            "template_kind IN ('own_label','cmr')",
            name="ck_document_template_kind",
        ),
        sa.CheckConstraint(
            "language IN ('pl','en')",
            name="ck_document_template_language",
        ),
        sa.CheckConstraint(
            "output_kind IN ('html_print')",
            name="ck_document_template_output",
        ),
    )
    op.create_index(
        "ix_document_template_organization_id",
        "document_template",
        ["organization_id"],
    )
    op.create_index(
        "ix_document_template_org_kind",
        "document_template",
        ["organization_id", "template_kind"],
    )
    op.execute("ALTER TABLE document_template ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE document_template FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY document_template_tenant_isolation ON document_template
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS document_template_tenant_isolation ON document_template")
    op.drop_index("ix_document_template_org_kind", table_name="document_template")
    op.drop_index("ix_document_template_organization_id", table_name="document_template")
    op.drop_table("document_template")
