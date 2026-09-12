"""create role_view_mark catalog with RLS FORCE

Revision ID: 306_role_view_mark
Revises: 305_mail_accept_mark
Create Date: 2026-09-12

EXP4.17 HITL znacznik widoku roli jako dane. Nie board T6. Nie mapa.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "306_role_view_mark"
down_revision: str | None = "305_mail_accept_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "role_view_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("view_kind", sa.String(length=16), nullable=False),
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
            name="fk_role_view_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_role_view_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_role_view_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_role_view_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_role_view_mark_code",
        ),
        sa.CheckConstraint(
            "view_kind IN ('groupage', 'ftl', 'ocean', 'other')",
            name="ck_role_view_mark_view_kind",
        ),
    )
    op.create_index(
        "ix_role_view_mark_organization_id",
        "role_view_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE role_view_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE role_view_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY role_view_mark_tenant_isolation ON role_view_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS role_view_mark_tenant_isolation ON role_view_mark",
    )
    op.drop_index(
        "ix_role_view_mark_organization_id",
        table_name="role_view_mark",
    )
    op.drop_table("role_view_mark")
