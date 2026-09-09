"""create memory_edge catalog with RLS FORCE

Revision ID: 141_memory_edge
Revises: 140_war_room_mark
Create Date: 2026-09-09

HITL rodzaj krawędzi pamięci. Nie graf na zdarzeniach. Nie wyszukiwanie.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "141_memory_edge"
down_revision: str | None = "140_war_room_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "memory_edge",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("edge_kind", sa.String(length=16), nullable=False),
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
            name="fk_memory_edge_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_memory_edge_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_memory_edge_org_source_ref",
        ),
        sa.CheckConstraint(
            "edge_kind IN ("
            "'recalls','follows','blocks','cites','other'"
            ")",
            name="ck_memory_edge_kind",
        ),
    )
    # Lista per tenant — RLS filtruje organization_id; unique source_ref nie zastępuje tego skanu.
    op.create_index("ix_memory_edge_organization_id", "memory_edge", ["organization_id"])
    op.execute("ALTER TABLE memory_edge ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE memory_edge FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY memory_edge_tenant_isolation ON memory_edge
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS memory_edge_tenant_isolation ON memory_edge")
    op.drop_index("ix_memory_edge_organization_id", table_name="memory_edge")
    op.drop_table("memory_edge")
