"""create party catalog and terminal.operator_party_id with RLS

Revision ID: 015_party_rls
Revises: 014_terminal_rls
Create Date: 2026-09-01

Indeks uq_party_org_country_tax_id jest częściowy (tax_id IS NOT NULL) —
resolve idzie po (organization_id, country_code, tax_id), nie po luźnej nazwie.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "015_party_rls"
down_revision: str | None = "014_terminal_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"
_ROLES = (
    "roles <@ ARRAY['customer','vendor','agent','carrier',"
    "'shipper','consignee','notify']::text[] AND cardinality(roles) >= 1"
)
_CREDIT = (
    "(credit_limit IS NULL AND credit_currency IS NULL) OR "
    "(credit_limit IS NOT NULL AND credit_currency IS NOT NULL)"
)
_WHITELIST = "whitelist_status IN ('pending','listed','not_listed','unavailable')"
_ADAPTER = "api_adapter IN ('none','maersk','hapag','cma','msc')"
_TABLES = (
    "party",
    "party_contact",
    "party_bank_account",
    "party_email_domain",
    "party_charge_override",
    "carrier_profile",
)


def _timestamps() -> list[sa.Column]:
    return [
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
    ]


def _org_fk(name: str) -> sa.ForeignKeyConstraint:
    return sa.ForeignKeyConstraint(
        ["organization_id"],
        ["organization.id"],
        name=name,
        ondelete="RESTRICT",
    )


def _party_fk(name: str) -> sa.ForeignKeyConstraint:
    return sa.ForeignKeyConstraint(
        ["organization_id", "party_id"],
        ["party.organization_id", "party.id"],
        name=name,
        ondelete="RESTRICT",
    )


def _rls(table: str, policy: str) -> None:
    op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
    op.execute(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY {policy} ON {table}
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def upgrade() -> None:
    op.create_table(
        "party",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("legal_name", sa.String(length=256), nullable=False),
        sa.Column("short_name", sa.String(length=64), nullable=True),
        sa.Column("tax_id", sa.String(length=32), nullable=True),
        sa.Column("vat_eu", sa.String(length=32), nullable=True),
        sa.Column("regon", sa.String(length=14), nullable=True),
        sa.Column("krs", sa.String(length=10), nullable=True),
        sa.Column("country_code", sa.CHAR(length=2), nullable=False),
        sa.Column("address_line", sa.String(length=256), nullable=True),
        sa.Column("city", sa.String(length=128), nullable=True),
        sa.Column("postal_code", sa.String(length=16), nullable=True),
        sa.Column(
            "roles",
            postgresql.ARRAY(sa.Text()),
            nullable=False,
        ),
        sa.Column("payment_terms_days", sa.Integer(), nullable=True),
        sa.Column("credit_limit", sa.Numeric(precision=14, scale=4), nullable=True),
        sa.Column("credit_currency", sa.CHAR(length=3), nullable=True),
        sa.Column("default_currency", sa.CHAR(length=3), nullable=True),
        sa.Column("language", sa.String(length=16), nullable=True),
        sa.Column("gus_synced_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("vies_checked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("source_ref", sa.String(length=256), nullable=False),
        *_timestamps(),
        _org_fk("fk_party_organization_id"),
        sa.UniqueConstraint("organization_id", "id", name="uq_party_org_id"),
        sa.CheckConstraint(_ROLES, name="ck_party_roles"),
        sa.CheckConstraint(_CREDIT, name="ck_party_credit_pair"),
    )
    op.create_index("ix_party_organization_id", "party", ["organization_id"])
    op.execute(
        "CREATE UNIQUE INDEX uq_party_org_country_tax_id "
        "ON party (organization_id, country_code, tax_id) WHERE tax_id IS NOT NULL"
    )
    _rls("party", "party_tenant_isolation")

    op.create_table(
        "party_contact",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("email", sa.String(length=256), nullable=True),
        sa.Column("phone", sa.String(length=64), nullable=True),
        sa.Column("position", sa.String(length=128), nullable=True),
        sa.Column("is_primary", sa.Boolean(), nullable=False, server_default=sa.false()),
        *_timestamps(),
        _org_fk("fk_party_contact_organization_id"),
        _party_fk("fk_party_contact_party"),
    )
    op.create_index("ix_party_contact_organization_id", "party_contact", ["organization_id"])
    _rls("party_contact", "party_contact_tenant_isolation")

    op.create_table(
        "party_bank_account",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("iban", sa.String(length=34), nullable=False),
        sa.Column("currency", sa.CHAR(length=3), nullable=False),
        sa.Column("bank_name", sa.String(length=128), nullable=True),
        sa.Column("whitelist_status", sa.String(length=16), nullable=False),
        sa.Column("whitelist_checked_at", sa.DateTime(timezone=True), nullable=True),
        *_timestamps(),
        _org_fk("fk_party_bank_account_organization_id"),
        _party_fk("fk_party_bank_account_party"),
        sa.CheckConstraint(_WHITELIST, name="ck_party_bank_whitelist"),
    )
    op.create_index(
        "ix_party_bank_account_organization_id",
        "party_bank_account",
        ["organization_id"],
    )
    _rls("party_bank_account", "party_bank_account_tenant_isolation")

    op.create_table(
        "party_email_domain",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("domain", sa.String(length=256), nullable=False),
        sa.Column("source_ref", sa.String(length=256), nullable=False),
        *_timestamps(),
        _org_fk("fk_party_email_domain_organization_id"),
        _party_fk("fk_party_email_domain_party"),
        sa.UniqueConstraint("organization_id", "domain", name="uq_party_email_domain_org_domain"),
    )
    op.create_index(
        "ix_party_email_domain_organization_id",
        "party_email_domain",
        ["organization_id"],
    )
    _rls("party_email_domain", "party_email_domain_tenant_isolation")

    op.create_table(
        "party_charge_override",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("charge_code", sa.String(length=32), nullable=False),
        sa.Column("lane_pattern", sa.Text(), nullable=True),
        sa.Column("amount", sa.Numeric(precision=14, scale=4), nullable=False),
        sa.Column("currency", sa.CHAR(length=3), nullable=False),
        sa.Column("basis", sa.String(length=32), nullable=True),
        sa.Column("valid_from", sa.Date(), nullable=True),
        sa.Column("valid_to", sa.Date(), nullable=True),
        sa.Column("source_ref", sa.String(length=256), nullable=False),
        *_timestamps(),
        _org_fk("fk_party_charge_override_organization_id"),
        _party_fk("fk_party_charge_override_party"),
        sa.ForeignKeyConstraint(
            ["organization_id", "charge_code"],
            ["charge_code.organization_id", "charge_code.code"],
            name="fk_party_charge_override_charge_code",
            ondelete="RESTRICT",
        ),
    )
    op.create_index(
        "ix_party_charge_override_organization_id",
        "party_charge_override",
        ["organization_id"],
    )
    _rls("party_charge_override", "party_charge_override_tenant_isolation")

    op.create_table(
        "carrier_profile",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("scac_code", sa.String(length=8), nullable=True),
        sa.Column("is_nvocc", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("rate_source_email", sa.String(length=256), nullable=True),
        sa.Column("api_adapter", sa.String(length=16), nullable=False, server_default="none"),
        sa.Column("dcsa_tnt_version", sa.String(length=16), nullable=True),
        *_timestamps(),
        _org_fk("fk_carrier_profile_organization_id"),
        _party_fk("fk_carrier_profile_party"),
        sa.UniqueConstraint("organization_id", "party_id", name="uq_carrier_profile_org_party"),
        sa.CheckConstraint(_ADAPTER, name="ck_carrier_profile_adapter"),
    )
    op.create_index("ix_carrier_profile_organization_id", "carrier_profile", ["organization_id"])
    _rls("carrier_profile", "carrier_profile_tenant_isolation")

    op.add_column(
        "terminal",
        sa.Column("operator_party_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_terminal_operator_party",
        "terminal",
        "party",
        ["organization_id", "operator_party_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint("fk_terminal_operator_party", "terminal", type_="foreignkey")
    op.drop_column("terminal", "operator_party_id")

    for table in reversed(_TABLES):
        op.execute(f"DROP POLICY IF EXISTS {table}_tenant_isolation ON {table}")
        op.execute(f"DROP INDEX IF EXISTS ix_{table}_organization_id")
        op.drop_table(table)

    op.execute("DROP INDEX IF EXISTS uq_party_org_country_tax_id")
