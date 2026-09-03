import uuid
from decimal import Decimal

from sqlalchemy import CHAR, CheckConstraint, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Charge(Base, TimestampMixin):
    __tablename__ = "charge"
    __table_args__ = (
        CheckConstraint("buy_currency = sell_currency", name="charge_same_currency"),
        UniqueConstraint("organization_id", "id", name="uq_charge_org_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False, index=True)
    charge_code: Mapped[str] = mapped_column(String(32), nullable=False)
    buy_amount: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    buy_currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    sell_amount: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    sell_currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    rate_line_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("rate_line.id", ondelete="RESTRICT"), nullable=True
    )
