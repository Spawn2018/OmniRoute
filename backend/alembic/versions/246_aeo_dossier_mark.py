"""create aeo_dossier_mark catalog with RLS FORCE

Revision ID: 246_aeo_dossier_mark
Revises: 245_edi_map_mark
Create Date: 2026-09-11

G14 HITL dossier AEO jako dane. Nie party_document. Nie kwota.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "246_aeo_dossier_mark"
down_revision: str | None = "245_edi_map_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "aeo_dossier_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("dossier_kind", sa.String(length=16), nullable=False),
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
            name="fk_aeo_dossier_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_aeo_dossier_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_aeo_dossier_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_aeo_dossier_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_aeo_dossier_mark_code",
        ),
        sa.CheckConstraint(
            "dossier_kind IN ('aeo', 'authorised', 'other')",
            name="ck_aeo_dossier_mark_dossier_kind",
        ),
    )
    op.create_index(
        "ix_aeo_dossier_mark_organization_id",
        "aeo_dossier_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE aeo_dossier_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE aeo_dossier_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY aeo_dossier_mark_tenant_isolation ON aeo_dossier_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS aeo_dossier_mark_tenant_isolation ON aeo_dossier_mark",
    )
    op.drop_index("ix_aeo_dossier_mark_organization_id", table_name="aeo_dossier_mark")
    op.drop_table("aeo_dossier_mark")
