"""create allocation_key open dictionary with RLS FORCE

Revision ID: 406_allocation_key
Revises: 405_extraction_prompt_mark
Create Date: 2026-09-15

AI7.0 HITL allocation_key. Otwarty slownik kluczy. Nie CHECK listy 23.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "406_allocation_key"
down_revision: str | None = "405_extraction_prompt_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"
_SNAKE = r"^[a-z][a-z0-9_]{1,31}$"


def upgrade() -> None:
    op.create_table(
        "allocation_key",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("key_code", sa.String(length=32), nullable=False),
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
            name="fk_allocation_key_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_allocation_key_org_id"),
        sa.UniqueConstraint("organization_id", "key_code", name="uq_allocation_key_org_code"),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_allocation_key_org_source_ref",
        ),
        sa.CheckConstraint(f"key_code ~ '{_SNAKE}'", name="ck_allocation_key_code"),
    )
    op.create_index("ix_allocation_key_organization_id", "allocation_key", ["organization_id"])
    op.execute("ALTER TABLE allocation_key ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE allocation_key FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY allocation_key_tenant_isolation ON allocation_key
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS allocation_key_tenant_isolation ON allocation_key")
    op.drop_index("ix_allocation_key_organization_id", table_name="allocation_key")
    op.drop_table("allocation_key")
