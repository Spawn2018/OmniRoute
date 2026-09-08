import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CHAR,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_ROLES_SQL = (
    "roles <@ ARRAY['customer','vendor','agent','carrier',"
    "'shipper','consignee','notify','subcontractor']::text[] AND cardinality(roles) >= 1"
)
_CREDIT_SQL = (
    "(credit_limit IS NULL AND credit_currency IS NULL) OR "
    "(credit_limit IS NOT NULL AND credit_currency IS NOT NULL)"
)


class Party(Base, TimestampMixin):
    __tablename__ = "party"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_party_org_id"),
        ForeignKeyConstraint(
            ["organization_id", "parent_party_id"],
            ["party.organization_id", "party.id"],
            name="fk_party_parent_party",
            ondelete="RESTRICT",
        ),
        CheckConstraint(_ROLES_SQL, name="ck_party_roles"),
        CheckConstraint(_CREDIT_SQL, name="ck_party_credit_pair"),
        CheckConstraint(
            "parent_party_id IS NULL OR parent_party_id <> id",
            name="ck_party_parent_not_self",
        ),
        Index(
            "uq_party_org_country_tax_id",
            "organization_id",
            "country_code",
            "tax_id",
            unique=True,
            postgresql_where=text("tax_id IS NOT NULL"),
        ),
        Index(
            "uq_party_org_vat_eu",
            "organization_id",
            "vat_eu",
            unique=True,
            postgresql_where=text("vat_eu IS NOT NULL"),
        ),
        Index(
            "uq_party_org_eori",
            "organization_id",
            "eori",
            unique=True,
            postgresql_where=text("eori IS NOT NULL"),
        ),
        Index(
            "uq_party_org_duns",
            "organization_id",
            "duns",
            unique=True,
            postgresql_where=text("duns IS NOT NULL"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Katalog główny — tax_id unikalny tylko gdy niepusty.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False, index=True,
    )
    legal_name: Mapped[str] = mapped_column(String(256), nullable=False)
    short_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    tax_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    vat_eu: Mapped[str | None] = mapped_column(String(32), nullable=True)
    eori: Mapped[str | None] = mapped_column(String(32), nullable=True)
    duns: Mapped[str | None] = mapped_column(String(16), nullable=True)
    regon: Mapped[str | None] = mapped_column(String(14), nullable=True)
    krs: Mapped[str | None] = mapped_column(String(10), nullable=True)
    country_code: Mapped[str] = mapped_column(CHAR(2), nullable=False)
    address_line: Mapped[str | None] = mapped_column(String(256), nullable=True)
    city: Mapped[str | None] = mapped_column(String(128), nullable=True)
    postal_code: Mapped[str | None] = mapped_column(String(16), nullable=True)
    roles: Mapped[list[str]] = mapped_column(ARRAY(Text()), nullable=False)
    payment_terms_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    credit_limit: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    credit_currency: Mapped[str | None] = mapped_column(CHAR(3), nullable=True)
    default_currency: Mapped[str | None] = mapped_column(CHAR(3), nullable=True)
    language: Mapped[str | None] = mapped_column(String(16), nullable=True)
    gus_synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    vies_checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_sole_trader: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    parent_party_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
    # URI listy, którą operator już ma — nie live HTTP i nie auto-match.
    sanctions_list_ref: Mapped[str | None] = mapped_column(Text, nullable=True)
    sanctions_checked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
