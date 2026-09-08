import uuid
from decimal import Decimal

from sqlalchemy import (
    CHAR,
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class GroupageTariff(Base, TimestampMixin):
    __tablename__ = "groupage_tariff"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "location_id"],
            ["location.organization_id", "location.id"],
            name="fk_groupage_tariff_location",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("organization_id", "id", name="uq_groupage_tariff_org_id"),
        CheckConstraint("amount > 0", name="ck_groupage_tariff_amount_positive"),
        CheckConstraint(
            "chargeable_weight > 0",
            name="ck_groupage_tariff_weight_positive",
        ),
        CheckConstraint("currency ~ '^[A-Z]{3}$'", name="ck_groupage_tariff_currency_iso"),
        Index("ix_groupage_tariff_org_location", "organization_id", "location_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: cennik i strefa jednego tenanta — złożone FK nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    location_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    tariff_code: Mapped[str] = mapped_column(String(32), nullable=False)
    chargeable_weight: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
