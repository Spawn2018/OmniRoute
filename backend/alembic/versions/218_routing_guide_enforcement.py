"""create routing_guide_enforcement catalog with RLS FORCE

Revision ID: 218_routing_guide_enforcement
Revises: 217_collaboration_mark
Create Date: 2026-09-11

HITL tryb egzekucji przewodnika jako dane. Nie HTTP 409 na shipment.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "218_routing_guide_enforcement"
down_revision: str | None = "217_collaboration_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "routing_guide_enforcement",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("enforcement_kind", sa.String(length=16), nullable=False),
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
            name="fk_routing_guide_enforcement_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_routing_guide_enforcement_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_routing_guide_enforcement_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_routing_guide_enforcement_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_routing_guide_enforcement_code",
        ),
        sa.CheckConstraint(
            "enforcement_kind IN ('record_only', 'block_409')",
            name="ck_routing_guide_enforcement_kind",
        ),
    )
    op.create_index(
        "ix_routing_guide_enforcement_organization_id",
        "routing_guide_enforcement",
        ["organization_id"],
    )
    op.execute("ALTER TABLE routing_guide_enforcement ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE routing_guide_enforcement FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY routing_guide_enforcement_tenant_isolation
        ON routing_guide_enforcement
        FOR ALL
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS routing_guide_enforcement_tenant_isolation "
        "ON routing_guide_enforcement"
    )
    op.drop_index(
        "ix_routing_guide_enforcement_organization_id",
        table_name="routing_guide_enforcement",
    )
    op.drop_table("routing_guide_enforcement")
