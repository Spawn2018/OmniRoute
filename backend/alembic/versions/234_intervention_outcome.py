"""create intervention_outcome catalog with RLS FORCE

Revision ID: 234_intervention_outcome
Revises: 233_penalty_mark
Create Date: 2026-09-11

CI7 HITL wynik interwencji jako dane. Nie SQL oszczędności. Nie marża.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "234_intervention_outcome"
down_revision: str | None = "233_penalty_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "intervention_outcome",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("outcome_code", sa.String(length=32), nullable=False),
        sa.Column("result_kind", sa.String(length=16), nullable=False),
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
            name="fk_intervention_outcome_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_intervention_outcome_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "outcome_code",
            name="uq_intervention_outcome_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_intervention_outcome_org_source_ref",
        ),
        sa.CheckConstraint(
            "outcome_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_intervention_outcome_code",
        ),
        sa.CheckConstraint(
            "result_kind IN ('contained', 'rerouted', 'claimed', 'other')",
            name="ck_intervention_outcome_result_kind",
        ),
    )
    op.create_index(
        "ix_intervention_outcome_organization_id",
        "intervention_outcome",
        ["organization_id"],
    )
    op.execute("ALTER TABLE intervention_outcome ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE intervention_outcome FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY intervention_outcome_tenant_isolation ON intervention_outcome
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS intervention_outcome_tenant_isolation ON intervention_outcome"
    )
    op.drop_index(
        "ix_intervention_outcome_organization_id",
        table_name="intervention_outcome",
    )
    op.drop_table("intervention_outcome")
