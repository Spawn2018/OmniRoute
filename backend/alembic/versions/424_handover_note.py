"""create handover_note with S/B/A/R text + RLS FORCE

Revision ID: 424_handover_note
Revises: 423_consignment_stop
Create Date: 2026-09-17

N11 leftover HITL wpis przekazania zmiany. Nie auto SBAR. Nie T6.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "424_handover_note"
down_revision: str | None = "423_consignment_stop"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "handover_note",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("note_code", sa.String(length=32), nullable=False),
        sa.Column("situation", sa.String(length=2000), nullable=False),
        sa.Column("background", sa.String(length=2000), nullable=False),
        sa.Column("assessment", sa.String(length=2000), nullable=False),
        sa.Column("recommendation", sa.String(length=2000), nullable=False),
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
            name="fk_handover_note_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_handover_note_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "note_code",
            name="uq_handover_note_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_handover_note_org_src",
        ),
        sa.CheckConstraint(
            "note_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_handover_note_code",
        ),
        sa.CheckConstraint(
            "char_length(situation) BETWEEN 1 AND 2000",
            name="ck_handover_note_situation",
        ),
        sa.CheckConstraint(
            "char_length(background) BETWEEN 1 AND 2000",
            name="ck_handover_note_background",
        ),
        sa.CheckConstraint(
            "char_length(assessment) BETWEEN 1 AND 2000",
            name="ck_handover_note_assessment",
        ),
        sa.CheckConstraint(
            "char_length(recommendation) BETWEEN 1 AND 2000",
            name="ck_handover_note_recommendation",
        ),
    )
    op.create_index(
        "ix_handover_note_organization_id",
        "handover_note",
        ["organization_id"],
    )
    op.execute("ALTER TABLE handover_note ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE handover_note FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY handover_note_tenant_isolation
        ON handover_note
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS handover_note_tenant_isolation ON handover_note",
    )
    op.drop_index(
        "ix_handover_note_organization_id",
        table_name="handover_note",
    )
    op.drop_table("handover_note")
