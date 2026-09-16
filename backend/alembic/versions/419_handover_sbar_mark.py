"""create handover_sbar_mark catalog with RLS FORCE

Revision ID: 419_handover_sbar_mark
Revises: 418_shipment_clone_mark
Create Date: 2026-09-16

N11 HITL przekazanie zmiany SBAR. Nie drugi czat. Nie auto SBAR.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "419_handover_sbar_mark"
down_revision: str | None = "418_shipment_clone_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "handover_sbar_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("sbar_kind", sa.String(length=16), nullable=False),
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
            name="fk_handover_sbar_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_handover_sbar_mark_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_handover_sbar_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_handover_sbar_mark_org_src",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_handover_sbar_mark_code",
        ),
        sa.CheckConstraint(
            "sbar_kind IN ("
            "'situation', 'background', 'assessment', 'recommendation', 'other'"
            ")",
            name="ck_handover_sbar_mark_kind",
        ),
    )
    op.create_index(
        "ix_handover_sbar_mark_organization_id",
        "handover_sbar_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE handover_sbar_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE handover_sbar_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY handover_sbar_mark_tenant_isolation
        ON handover_sbar_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS handover_sbar_mark_tenant_isolation ON handover_sbar_mark",
    )
    op.drop_index(
        "ix_handover_sbar_mark_organization_id",
        table_name="handover_sbar_mark",
    )
    op.drop_table("handover_sbar_mark")
