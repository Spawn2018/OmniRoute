"""create war_room_mark catalog with RLS FORCE

Revision ID: 140_war_room_mark
Revises: 139_twin_mark
Create Date: 2026-09-09

HITL rodzaj incydentu sali. Nie drugi czat. Nie scalanie alertów.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "140_war_room_mark"
down_revision: str | None = "139_twin_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "war_room_mark",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("incident_kind", sa.String(length=16), nullable=False),
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
            name="fk_war_room_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_war_room_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_war_room_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "incident_kind IN ("
            "'weather','congestion','labor','carrier','credit','other'"
            ")",
            name="ck_war_room_mark_kind",
        ),
    )
    # Lista per tenant — RLS filtruje organization_id; unique source_ref nie zastępuje tego skanu.
    op.create_index("ix_war_room_mark_organization_id", "war_room_mark", ["organization_id"])
    op.execute("ALTER TABLE war_room_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE war_room_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY war_room_mark_tenant_isolation ON war_room_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS war_room_mark_tenant_isolation ON war_room_mark")
    op.drop_index("ix_war_room_mark_organization_id", table_name="war_room_mark")
    op.drop_table("war_room_mark")
