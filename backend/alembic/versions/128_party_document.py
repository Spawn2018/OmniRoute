"""create party_document catalog with RLS FORCE

Revision ID: 128_party_document
Revises: 127_monitoring_scheme
Create Date: 2026-09-09

HITL party document kind on party + source_ref. Nie 409 na shipment. Nie extract.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "128_party_document"
down_revision: str | None = "127_monitoring_scheme"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "party_document",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("document_kind", sa.String(length=32), nullable=False),
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
            name="fk_party_document_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_party_document_party",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_party_document_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "party_id",
            "document_kind",
            name="uq_party_document_org_party_kind",
        ),
        sa.CheckConstraint(
            "document_kind ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_party_document_kind",
        ),
    )
    op.create_index("ix_party_document_organization_id", "party_document", ["organization_id"])
    op.execute("ALTER TABLE party_document ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE party_document FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY party_document_tenant_isolation ON party_document
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS party_document_tenant_isolation ON party_document")
    op.drop_index("ix_party_document_organization_id", table_name="party_document")
    op.drop_table("party_document")
