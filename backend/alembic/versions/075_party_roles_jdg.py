"""add party JDG, parent and role assignment leftover M10-2

Revision ID: 075_party_roles_jdg
Revises: 074_party_business_ids
Create Date: 2026-09-08

Role zostają na party.roles; assignment to ta sama lista.
JDG nie dostaje limitu na INSERT. Nie trzy tabele.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "075_party_roles_jdg"
down_revision: str | None = "074_party_business_ids"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"
_ROLES = (
    "roles <@ ARRAY['customer','vendor','agent','carrier',"
    "'shipper','consignee','notify','subcontractor']::text[] "
    "AND cardinality(roles) >= 1"
)
_ASSIGN_ROLE = (
    "role IN ('customer','vendor','agent','carrier',"
    "'shipper','consignee','notify','subcontractor')"
)


def upgrade() -> None:
    op.add_column(
        "party",
        sa.Column("is_sole_trader", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "party",
        sa.Column("parent_party_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.drop_constraint("ck_party_roles", "party", type_="check")
    op.create_check_constraint("ck_party_roles", "party", _ROLES)
    op.create_check_constraint(
        "ck_party_parent_not_self",
        "party",
        "parent_party_id IS NULL OR parent_party_id <> id",
    )
    op.create_foreign_key(
        "fk_party_parent_party",
        "party",
        "party",
        ["organization_id", "parent_party_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )
    op.create_table(
        "party_role_assignment",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
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
            name="fk_party_role_assignment_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_party_role_assignment_party",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "party_id",
            "role",
            name="uq_party_role_assignment_org_party_role",
        ),
        sa.CheckConstraint(_ASSIGN_ROLE, name="ck_party_role_assignment_role"),
    )
    op.create_index(
        "ix_party_role_assignment_organization_id",
        "party_role_assignment",
        ["organization_id"],
    )
    op.execute("ALTER TABLE party_role_assignment ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE party_role_assignment FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY party_role_assignment_tenant_isolation ON party_role_assignment
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS party_role_assignment_tenant_isolation "
        "ON party_role_assignment"
    )
    op.drop_index(
        "ix_party_role_assignment_organization_id",
        table_name="party_role_assignment",
    )
    op.drop_table("party_role_assignment")
    op.drop_constraint("fk_party_parent_party", "party", type_="foreignkey")
    op.drop_constraint("ck_party_parent_not_self", "party", type_="check")
    op.drop_constraint("ck_party_roles", "party", type_="check")
    op.create_check_constraint(
        "ck_party_roles",
        "party",
        "roles <@ ARRAY['customer','vendor','agent','carrier',"
        "'shipper','consignee','notify']::text[] AND cardinality(roles) >= 1",
    )
    op.drop_column("party", "parent_party_id")
    op.drop_column("party", "is_sole_trader")
