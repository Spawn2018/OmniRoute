"""create data_source catalog with RLS FORCE

Revision ID: 412_data_source
Revises: 411_article50_mark
Create Date: 2026-09-15

AI5.0 HITL slownik zrodel z licencja. Nie live ingest.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "412_data_source"
down_revision: str | None = "411_article50_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "data_source",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("source_code", sa.String(length=32), nullable=False),
        sa.Column("license_label", sa.String(length=64), nullable=False),
        sa.Column("rights_scope", sa.String(length=128), nullable=False),
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
            name="fk_data_source_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_data_source_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_code",
            name="uq_data_source_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_data_source_org_src",
        ),
        sa.CheckConstraint(
            "source_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_data_source_code",
        ),
        sa.CheckConstraint(
            "char_length(btrim(license_label)) BETWEEN 2 AND 64",
            name="ck_data_source_license",
        ),
        sa.CheckConstraint(
            "char_length(btrim(rights_scope)) BETWEEN 2 AND 128",
            name="ck_data_source_rights",
        ),
    )
    op.create_index(
        "ix_data_source_organization_id",
        "data_source",
        ["organization_id"],
    )
    op.execute("ALTER TABLE data_source ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE data_source FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY data_source_tenant_isolation
        ON data_source
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS data_source_tenant_isolation ON data_source",
    )
    op.drop_index(
        "ix_data_source_organization_id",
        table_name="data_source",
    )
    op.drop_table("data_source")
