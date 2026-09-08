"""create tender_data_room catalog with RLS FORCE

Revision ID: 113_tender_data_room
Revises: 112_tender_round
Create Date: 2026-09-09

Pokój danych + NDA. Nie extract. Nie kwota.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "113_tender_data_room"
down_revision: str | None = "112_tender_round"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "tender_data_room",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tender_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("nda_mark", sa.String(length=16), nullable=False),
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
            name="fk_tender_data_room_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_data_room_tender",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_tender_data_room_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "tender_id",
            "nda_mark",
            name="uq_tender_data_room_org_tender_nda",
        ),
        sa.CheckConstraint("nda_mark = 'signed'", name="ck_tender_data_room_nda"),
    )
    op.create_index(
        "ix_tender_data_room_organization_id",
        "tender_data_room",
        ["organization_id"],
    )
    op.create_index(
        "ix_tender_data_room_org_tender",
        "tender_data_room",
        ["organization_id", "tender_id"],
    )
    op.execute("ALTER TABLE tender_data_room ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE tender_data_room FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY tender_data_room_tenant_isolation ON tender_data_room
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS tender_data_room_tenant_isolation ON tender_data_room")
    op.drop_index("ix_tender_data_room_org_tender", table_name="tender_data_room")
    op.drop_index("ix_tender_data_room_organization_id", table_name="tender_data_room")
    op.drop_table("tender_data_room")
