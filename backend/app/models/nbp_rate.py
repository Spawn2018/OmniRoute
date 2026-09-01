import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import CHAR, CheckConstraint, Date, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class NbpRate(Base, TimestampMixin):
    __tablename__ = "nbp_rate"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "currency",
            "rate_date",
            name="uq_nbp_rate_org_currency_date",
        ),
        CheckConstraint(
            "currency ~ '^[A-Z]{3}$' AND currency <> 'PLN'",
            name="ck_nbp_rate_currency_iso",
        ),
        CheckConstraint("mid > 0", name="ck_nbp_rate_mid_positive"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        index=True,
        nullable=False,
    )
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    rate_date: Mapped[date] = mapped_column(Date, nullable=False)
    mid: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
