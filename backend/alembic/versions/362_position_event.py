"""create position_event catalog with RLS FORCE

Revision ID: 362_position_event
Revises: 361_crm_opportunity
Create Date: 2026-09-13

BR2.0 HITL zdarzenie pozycji. Nie wspolrzedne. Nie poll.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "362_position_event"
down_revision: str | None = "361_crm_opportunity"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "position_event",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("event_code", sa.String(length=32), nullable=False),
        sa.Column("source_kind", sa.String(length=16), nullable=False),
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
            name="fk_position_event_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_position_event_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "event_code",
            name="uq_position_event_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_position_event_org_source_ref",
        ),
        sa.CheckConstraint(
            "event_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_position_event_code",
        ),
        sa.CheckConstraint(
            "source_kind IN ('gps', 'manual', 'other')",
            name="ck_position_event_source_kind",
        ),
    )
    op.create_index(
        "ix_position_event_organization_id",
        "position_event",
        ["organization_id"],
    )
    op.execute("ALTER TABLE position_event ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE position_event FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY position_event_tenant_isolation ON position_event
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS position_event_tenant_isolation ON position_event",
    )
    op.drop_index(
        "ix_position_event_organization_id",
        table_name="position_event",
    )
    op.drop_table("position_event")
