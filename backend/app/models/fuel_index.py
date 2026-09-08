import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    Index,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class FuelIndex(Base, TimestampMixin):
    __tablename__ = "fuel_index"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_fuel_index_org_id"),
        UniqueConstraint(
            "organization_id",
            "index_kind",
            "published_on",
            name="uq_fuel_index_org_kind_day",
        ),
        CheckConstraint("index_kind IN ('fsc', 'baf', 'caf')", name="ck_fuel_index_kind"),
        CheckConstraint("index_value > 0", name="ck_fuel_index_value_positive"),
        Index("ix_fuel_index_org_kind", "organization_id", "index_kind"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: indeks paliwowy jednego tenanta — CHECK kind nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    index_kind: Mapped[str] = mapped_column(String(8), nullable=False)
    published_on: Mapped[date] = mapped_column(Date, nullable=False)
    index_value: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
