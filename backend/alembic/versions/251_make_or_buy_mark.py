"""create make_or_buy_mark catalog with RLS FORCE

Revision ID: 251_make_or_buy_mark
Revises: 250_working_capital_mark
Create Date: 2026-09-11

EXP2.2 HITL poll rejestru jako dane. Nie silnik kosztu. Nie auto notice.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "251_make_or_buy_mark"
down_revision: str | None = "250_working_capital_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "make_or_buy_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("buy_kind", sa.String(length=16), nullable=False),
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
            name="fk_make_or_buy_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_make_or_buy_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_make_or_buy_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_make_or_buy_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_make_or_buy_mark_code",
        ),
        sa.CheckConstraint(
            "buy_kind IN ('make', 'buy', 'hybrid', 'other')",
            name="ck_make_or_buy_mark_buy_kind",
        ),
    )
    op.create_index(
        "ix_make_or_buy_mark_organization_id",
        "make_or_buy_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE make_or_buy_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE make_or_buy_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY make_or_buy_mark_tenant_isolation ON make_or_buy_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS make_or_buy_mark_tenant_isolation ON make_or_buy_mark",
    )
    op.drop_index("ix_make_or_buy_mark_organization_id", table_name="make_or_buy_mark")
    op.drop_table("make_or_buy_mark")
