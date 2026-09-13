"""create suggestion_kind open dictionary with RLS FORCE

Revision ID: 346_suggestion_kind
Revises: 345_benefit_ledger
Create Date: 2026-09-13

AI1.4 HITL suggestion_kind. Otwarty slownik. Nie CHECK listy. Nie ledger.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "346_suggestion_kind"
down_revision: str | None = "345_benefit_ledger"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"
_SNAKE = r"^[a-z][a-z0-9_]{1,31}$"


def upgrade() -> None:
    op.create_table(
        "suggestion_kind",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("kind_code", sa.String(length=32), nullable=False),
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
            name="fk_suggestion_kind_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_suggestion_kind_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "kind_code",
            name="uq_suggestion_kind_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_suggestion_kind_org_source_ref",
        ),
        sa.CheckConstraint(
            f"kind_code ~ '{_SNAKE}'",
            name="ck_suggestion_kind_code",
        ),
    )
    op.create_index(
        "ix_suggestion_kind_organization_id",
        "suggestion_kind",
        ["organization_id"],
    )
    op.execute("ALTER TABLE suggestion_kind ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE suggestion_kind FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY suggestion_kind_tenant_isolation ON suggestion_kind
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS suggestion_kind_tenant_isolation ON suggestion_kind",
    )
    op.drop_index(
        "ix_suggestion_kind_organization_id",
        table_name="suggestion_kind",
    )
    op.drop_table("suggestion_kind")
