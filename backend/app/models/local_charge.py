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
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
