"""create lez_mark catalog with RLS FORCE

Revision ID: 300_lez_mark
Revises: 299_tacho_office_mark
Create Date: 2026-09-12

EXP4.11 HITL znacznik LEZ/zakazy jako dane. Nie LEZ live. Nie mapa.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "300_lez_mark"
down_revision: str | None = "299_tacho_office_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "lez_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("lez_kind", sa.String(length=16), nullable=False),
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
            name="fk_lez_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_lez_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_lez_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_lez_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_lez_mark_code",
        ),
        sa.CheckConstraint(
            "lez_kind IN ('lez', 'ban', 'zone', 'other')",
            name="ck_lez_mark_lez_kind",
        ),
    )
    op.create_index(
        "ix_lez_mark_organization_id",
        "lez_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE lez_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE lez_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY lez_mark_tenant_isolation ON lez_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS lez_mark_tenant_isolation ON lez_mark",
    )
    op.drop_index(
        "ix_lez_mark_organization_id",
        table_name="lez_mark",
    )
    op.drop_table("lez_mark")
