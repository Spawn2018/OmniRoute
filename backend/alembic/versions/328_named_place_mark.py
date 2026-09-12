"""create named_place_mark catalog with RLS FORCE

Revision ID: 328_named_place_mark
Revises: 327_dual_ledger_mark
Create Date: 2026-09-12

EXP0.6 HITL named_place+wersja. Nie cytat reguł. Nie mutacja quotation.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "328_named_place_mark"
down_revision: str | None = "327_dual_ledger_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "named_place_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("named_place", sa.String(length=128), nullable=False),
        sa.Column("terms_version", sa.String(length=4), nullable=False),
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
            name="fk_named_place_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_named_place_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_named_place_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_named_place_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_named_place_mark_code",
        ),
        sa.CheckConstraint(
            "terms_version IN ('2020', '2010')",
            name="ck_named_place_mark_terms_version",
        ),
        sa.CheckConstraint(
            "btrim(named_place) <> ''",
            name="ck_named_place_mark_place_nonempty",
        ),
    )
    op.create_index(
        "ix_named_place_mark_organization_id",
        "named_place_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE named_place_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE named_place_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY named_place_mark_tenant_isolation ON named_place_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS named_place_mark_tenant_isolation ON named_place_mark",
    )
    op.drop_index(
        "ix_named_place_mark_organization_id",
        table_name="named_place_mark",
    )
    op.drop_table("named_place_mark")
