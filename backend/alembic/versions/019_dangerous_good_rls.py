"""create dangerous_good catalog with RLS

Revision ID: 019_dangerous_good_rls
Revises: 018_nbp_rate_rls
Create Date: 2026-09-01
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "019_dangerous_good_rls"
down_revision: str | None = "018_nbp_rate_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"
_IMDG = (
    "'1','1.1','1.2','1.3','1.4','1.5','1.6',"
    "'2.1','2.2','2.3','3','4.1','4.2','4.3',"
    "'5.1','5.2','6.1','6.2','7','8','9'"
)


def upgrade() -> None:
    op.create_table(
        "dangerous_good",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("un_number", sa.String(length=4), nullable=False),
        sa.Column("imdg_class", sa.String(length=3), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column(
            "aliases",
            postgresql.ARRAY(sa.Text()),
            nullable=False,
            server_default="{}",
        ),
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
            name="fk_dangerous_good_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "un_number",
            name="uq_dangerous_good_org_un",
        ),
        sa.CheckConstraint("un_number ~ '^[0-9]{4}$'", name="ck_dangerous_good_un_digits"),
        sa.CheckConstraint(f"imdg_class IN ({_IMDG})", name="ck_dangerous_good_imdg_class"),
    )
    op.create_index("ix_dangerous_good_organization_id", "dangerous_good", ["organization_id"])
    op.create_index(
        "ix_dangerous_good_aliases",
        "dangerous_good",
        ["aliases"],
        postgresql_using="gin",
    )

    op.execute("ALTER TABLE dangerous_good ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE dangerous_good FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY dangerous_good_tenant_isolation ON dangerous_good
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS dangerous_good_tenant_isolation ON dangerous_good")
    op.drop_index("ix_dangerous_good_aliases", table_name="dangerous_good")
    op.drop_index("ix_dangerous_good_organization_id", table_name="dangerous_good")
    op.drop_table("dangerous_good")
