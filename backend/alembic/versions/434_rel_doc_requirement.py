"""create relation_document_requirement catalog with RLS FORCE

Revision ID: 434_rel_doc_requirement
Revises: 433_shipment_monitoring_filing
Create Date: 2026-09-17

C8 HITL relation_document_requirement. Nie live 409 na shipment. Nie blocks_create.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "434_rel_doc_requirement"
down_revision: str | None = "433_shipment_monitoring_filing"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "relation_document_requirement",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("requirement_code", sa.String(length=32), nullable=False),
        sa.Column("relation_kind", sa.String(length=16), nullable=False),
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
            name="fk_relation_document_requirement_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_relation_document_requirement_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "requirement_code",
            name="uq_relation_document_requirement_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_relation_document_requirement_org_source_ref",
        ),
        sa.CheckConstraint(
            "requirement_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_relation_document_requirement_code",
        ),
        sa.CheckConstraint(
            "relation_kind IN ('domestic', 'international', 'waste', 'other')",
            name="ck_relation_document_requirement_relation_kind",
        ),
    )
    op.create_index(
        "ix_relation_document_requirement_organization_id",
        "relation_document_requirement",
        ["organization_id"],
    )
    op.execute("ALTER TABLE relation_document_requirement ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE relation_document_requirement FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY relation_document_requirement_tenant_isolation
        ON relation_document_requirement
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS relation_document_requirement_tenant_isolation "
        "ON relation_document_requirement",
    )
    op.drop_index(
        "ix_relation_document_requirement_organization_id",
        table_name="relation_document_requirement",
    )
    op.drop_table("relation_document_requirement")
