"""create operator_decision rail with RLS FORCE

Revision ID: 034_operator_decision_rls
Revises: 033_customer_sop_blocks_auto
Create Date: 2026-09-03

Szyna Akceptuj/Odrzuć per tenant. Bez FK do inbound — subject_id to UUID.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "034_operator_decision_rls"
down_revision: str | None = "033_customer_sop_blocks_auto"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "operator_decision",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("subject_kind", sa.String(length=32), nullable=False),
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("source_ref", sa.String(length=512), nullable=False),
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
            name="fk_operator_decision_organization_id",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "subject_kind = 'inbound_message'",
            name="ck_operator_decision_subject_kind",
        ),
        sa.CheckConstraint(
            "status IN ('pending', 'accepted', 'changed', 'rejected')",
            name="ck_operator_decision_status",
        ),
    )
    op.create_index(
        "ix_operator_decision_organization_id",
        "operator_decision",
        ["organization_id"],
    )
    op.create_index(
        "ix_operator_decision_org_created",
        "operator_decision",
        ["organization_id", "created_at"],
    )
    op.create_index(
        "uq_operator_decision_pending",
        "operator_decision",
        ["organization_id", "subject_kind", "subject_id"],
        unique=True,
        postgresql_where=sa.text("status = 'pending'"),
    )
    op.execute("ALTER TABLE operator_decision ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE operator_decision FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY operator_decision_tenant_isolation ON operator_decision
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS operator_decision_tenant_isolation ON operator_decision")
    op.drop_index("uq_operator_decision_pending", table_name="operator_decision")
    op.drop_index("ix_operator_decision_org_created", table_name="operator_decision")
    op.drop_index("ix_operator_decision_organization_id", table_name="operator_decision")
    op.drop_table("operator_decision")
