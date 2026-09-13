"""create outcome_kind open dictionary with RLS FORCE

Revision ID: 351_outcome_kind
Revises: 350_twin_mark_kind_fk
Create Date: 2026-09-13

AI1.4 leftover HITL outcome_kind. Otwarty slownik. Nie CHECK listy.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "351_outcome_kind"
down_revision: str | None = "350_twin_mark_kind_fk"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"
_SNAKE = r"^[a-z][a-z0-9_]{1,31}$"


def upgrade() -> None:
    op.create_table(
        "outcome_kind",
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
            name="fk_outcome_kind_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_outcome_kind_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "kind_code",
            name="uq_outcome_kind_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_outcome_kind_org_source_ref",
        ),
        sa.CheckConstraint(f"kind_code ~ '{_SNAKE}'", name="ck_outcome_kind_code"),
    )
    op.create_index("ix_outcome_kind_organization_id", "outcome_kind", ["organization_id"])
    op.execute("ALTER TABLE outcome_kind ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE outcome_kind FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY outcome_kind_tenant_isolation ON outcome_kind
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS outcome_kind_tenant_isolation ON outcome_kind")
    op.drop_index("ix_outcome_kind_organization_id", table_name="outcome_kind")
    op.drop_table("outcome_kind")
