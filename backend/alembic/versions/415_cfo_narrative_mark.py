"""create cfo_narrative_mark catalog with RLS FORCE

Revision ID: 415_cfo_narrative_mark
Revises: 414_model_feature_mark
Create Date: 2026-09-15

AI7.1 HITL katalog etykiety narracji CFO. Nie silnik narracji. Nie druga marza.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "415_cfo_narrative_mark"
down_revision: str | None = "414_model_feature_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "cfo_narrative_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("narrative_kind", sa.String(length=16), nullable=False),
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
            name="fk_cfo_narrative_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_cfo_narrative_mark_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_cfo_narrative_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_cfo_narrative_mark_org_src",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_cfo_narrative_mark_code",
        ),
        sa.CheckConstraint(
            "narrative_kind IN ('anomaly', 'story', 'summary', 'other')",
            name="ck_cfo_narrative_mark_kind",
        ),
    )
    op.create_index(
        "ix_cfo_narrative_mark_organization_id",
        "cfo_narrative_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE cfo_narrative_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE cfo_narrative_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY cfo_narrative_mark_tenant_isolation
        ON cfo_narrative_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS cfo_narrative_mark_tenant_isolation ON cfo_narrative_mark",
    )
    op.drop_index(
        "ix_cfo_narrative_mark_organization_id",
        table_name="cfo_narrative_mark",
    )
    op.drop_table("cfo_narrative_mark")
