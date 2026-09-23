import uuid
from decimal import Decimal

from sqlalchemy import (
    CHAR,
    CheckConstraint,
    ForeignKey,
    Index,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class LocalCharge(Base, TimestampMixin):
    __tablename__ = "local_charge"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_local_charge_org_id"),
        CheckConstraint(
            "charge_kind IN ('thc', 'isps', 'seal', 'amendment')",
            name="ck_local_charge_kind",
        ),
        CheckConstraint("amount > 0", name="ck_local_charge_amount_positive"),
        CheckConstraint("currency ~ '^[A-Z]{3}$'", name="ck_local_charge_currency_iso"),
        CheckConstraint(
            "port_unlocode IS NULL OR port_unlocode ~ '^[A-Z]{2}[A-Z0-9]{3}$'",
            name="ck_local_charge_port_unlocode",
        ),
        UniqueConstraint(
            "organization_id",
            "charge_kind",
            "port_unlocode",
            "iso_size_type",
            "carrier_label",
            "service_label",
            name="uq_local_charge_org_kind_port_type_carrier_service",
            postgresql_nulls_not_distinct=True,
        ),
        CheckConstraint(
            "iso_size_type IS NULL OR iso_size_type ~ '^[0-9]{2}[A-Z][A-Z0-9]$'",
            name="ck_local_charge_iso_size_type",
        ),
        CheckConstraint(
            "carrier_label IS NULL OR char_length(btrim(carrier_label)) BETWEEN 1 AND 64",
            name="ck_local_charge_carrier_label",
        ),
        CheckConstraint(
            "service_label IS NULL OR char_length(btrim(service_label)) BETWEEN 1 AND 64",
            name="ck_local_charge_service_label",
        ),
        Index("ix_local_charge_org_kind", "organization_id", "charge_kind"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: dopłata lokalna jednego tenanta — CHECK kind nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    charge_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    port_unlocode: Mapped[str | None] = mapped_column(String(5), nullable=True)
    iso_size_type: Mapped[str | None] = mapped_column(String(4), nullable=True)
    carrier_label: Mapped[str | None] = mapped_column(String(64), nullable=True)
    service_label: Mapped[str | None] = mapped_column(String(64), nullable=True)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
