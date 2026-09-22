"""create pallet_synchro_mark catalog with RLS FORCE

Revision ID: 502_pallet_synchro_mark
Revises: 501_pallet_ledger
Create Date: 2026-09-22

D7c leftover HITL synchro salda↔ledger. Nie auto-UPDATE. Nie giełda.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "502_pallet_synchro_mark"
down_revision: str | None = "501_pallet_ledger"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "pallet_synchro_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("synchro_kind", sa.String(length=32), nullable=False),
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
            name="fk_pallet_synchro_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_pallet_synchro_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_pallet_synchro_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_pallet_synchro_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_pallet_synchro_mark_code",
        ),
        sa.CheckConstraint(
            "synchro_kind IN ('aligned', 'drift', 'held', 'other')",
            name="ck_pallet_synchro_mark_kind",
        ),
    )
    op.create_index(
        "ix_pallet_synchro_mark_organization_id",
        "pallet_synchro_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE pallet_synchro_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE pallet_synchro_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY pallet_synchro_mark_tenant_isolation ON pallet_synchro_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS pallet_synchro_mark_tenant_isolation ON pallet_synchro_mark",
    )
    op.drop_index(
        "ix_pallet_synchro_mark_organization_id",
        table_name="pallet_synchro_mark",
    )
    op.drop_table("pallet_synchro_mark")
