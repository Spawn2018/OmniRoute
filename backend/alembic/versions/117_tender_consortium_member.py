"""create tender_consortium_member catalog with RLS FORCE

Revision ID: 117_tender_consortium_member
Revises: 116_tender_win_loss
Create Date: 2026-09-09

Fotel konsorcjum: seat_code + source_ref. Nie extract RFP. Nie TED. Nie kwota.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "117_tender_consortium_member"
down_revision: str | None = "116_tender_win_loss"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "tender_consortium_member",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tender_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("seat_code", sa.String(length=16), nullable=False),
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
            name="fk_tender_consortium_member_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_consortium_member_tender",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_tender_consortium_member_party",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_tender_consortium_member_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "tender_id",
            "party_id",
            name="uq_tender_consortium_member_org_tender_party",
        ),
        sa.CheckConstraint(
            "seat_code IN ('lead', 'member')",
            name="ck_tender_consortium_member_seat",
        ),
    )
    op.create_index(
        "ix_tender_consortium_member_organization_id",
        "tender_consortium_member",
        ["organization_id"],
    )
    op.create_index(
        "ix_tender_consortium_member_org_tender",
        "tender_consortium_member",
        ["organization_id", "tender_id"],
    )
    op.execute("ALTER TABLE tender_consortium_member ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE tender_consortium_member FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY tender_consortium_member_tenant_isolation ON tender_consortium_member
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS tender_consortium_member_tenant_isolation "
        "ON tender_consortium_member"
    )
    op.drop_index(
        "ix_tender_consortium_member_org_tender",
        table_name="tender_consortium_member",
    )
    op.drop_index(
        "ix_tender_consortium_member_organization_id",
        table_name="tender_consortium_member",
    )
    op.drop_table("tender_consortium_member")
