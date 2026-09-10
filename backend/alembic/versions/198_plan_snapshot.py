"""create plan_snapshot catalog with RLS FORCE

Revision ID: 198_plan_snapshot
Revises: 197_outbox_task_template_kind
Create Date: 2026-09-10

HITL wersja planu jako dane. Nie silnik. Nie kółka. UUID bez FK.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "198_plan_snapshot"
down_revision: str | None = "197_outbox_task_template_kind"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "plan_snapshot",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("snapshot_code", sa.String(length=32), nullable=False),
        sa.Column("shipment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("trip_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("resource_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("author_label", sa.String(length=64), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
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
            name="fk_plan_snapshot_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_plan_snapshot_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "snapshot_code",
            name="uq_plan_snapshot_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_plan_snapshot_org_source_ref",
        ),
        sa.CheckConstraint(
            "snapshot_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_plan_snapshot_code",
        ),
        sa.CheckConstraint(
            "char_length(author_label) BETWEEN 1 AND 64",
            name="ck_plan_snapshot_author",
        ),
    )
    op.create_index(
        "ix_plan_snapshot_organization_id",
        "plan_snapshot",
        ["organization_id"],
    )
    op.execute("ALTER TABLE plan_snapshot ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE plan_snapshot FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY plan_snapshot_tenant_isolation ON plan_snapshot
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS plan_snapshot_tenant_isolation ON plan_snapshot")
    op.drop_index("ix_plan_snapshot_organization_id", table_name="plan_snapshot")
    op.drop_table("plan_snapshot")
