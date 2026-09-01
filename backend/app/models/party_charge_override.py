import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import (
    CHAR,
    Date,
    ForeignKey,
    ForeignKeyConstraint,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class PartyChargeOverride(Base, TimestampMixin):
    __tablename__ = "party_charge_override"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_party_charge_override_party",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "charge_code"],
            ["charge_code.organization_id", "charge_code.code"],
            name="fk_party_charge_override_charge_code",
            ondelete="RESTRICT",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Wyjątek nie wchodzi do silnika wyceny w 5.0.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False, index=True,
    )
    party_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    charge_code: Mapped[str] = mapped_column(String(32), nullable=False)
    lane_pattern: Mapped[str | None] = mapped_column(Text, nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    basis: Mapped[str | None] = mapped_column(String(32), nullable=True)
    valid_from: Mapped[date | None] = mapped_column(Date, nullable=True)
    valid_to: Mapped[date | None] = mapped_column(Date, nullable=True)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
