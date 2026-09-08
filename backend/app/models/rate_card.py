import uuid
from decimal import Decimal

from sqlalchemy import CHAR, CheckConstraint, ForeignKey, Index, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class RateCard(Base, TimestampMixin):
    __tablename__ = "rate_card"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_rate_card_org_id"),
        CheckConstraint("amount > 0", name="ck_rate_card_amount_positive"),
        CheckConstraint("currency ~ '^[A-Z]{3}$'", name="ck_rate_card_currency_iso"),
        CheckConstraint("char_length(applies_when) >= 1", name="ck_rate_card_when_len"),
        CheckConstraint("card_code ~ '^[a-z][a-z0-9_]{1,31}$'", name="ck_rate_card_code_snake"),
        Index("ix_rate_card_org_code", "organization_id", "card_code"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: karta stawek jednego tenanta — CHECK kodu nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    card_code: Mapped[str] = mapped_column(String(32), nullable=False)
    applies_when: Mapped[str] = mapped_column(String(512), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
