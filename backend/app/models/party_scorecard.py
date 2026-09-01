import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_RATE = "(response_rate IS NULL OR (response_rate >= 0 AND response_rate <= 1))"
_PRICE = "(price_position IS NULL OR (price_position >= 0 AND price_position <= 1))"
_MATCH = (
    "(quote_invoice_match_rate IS NULL OR "
    "(quote_invoice_match_rate >= 0 AND quote_invoice_match_rate <= 1))"
)
_HOURS = "(median_response_hours IS NULL OR median_response_hours >= 0)"
_ROLL = "(rollover_count IS NULL OR rollover_count >= 0)"


class PartyScorecard(Base, TimestampMixin):
    __tablename__ = "party_scorecard"
    __table_args__ = (
        UniqueConstraint("organization_id", "party_id", name="uq_party_scorecard_org_party"),
        ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_party_scorecard_party",
            ondelete="RESTRICT",
        ),
        CheckConstraint(_RATE, name="ck_party_scorecard_response_rate"),
        CheckConstraint(_PRICE, name="ck_party_scorecard_price_position"),
        CheckConstraint(_MATCH, name="ck_party_scorecard_quote_invoice_match"),
        CheckConstraint(_HOURS, name="ck_party_scorecard_median_hours"),
        CheckConstraint(_ROLL, name="ck_party_scorecard_rollover"),
        CheckConstraint("sample_size >= 0", name="ck_party_scorecard_sample_size"),
        CheckConstraint("window_days > 0", name="ck_party_scorecard_window_days"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    window_days: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("90"))
    party_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    sample_size: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    response_rate: Mapped[Decimal | None] = mapped_column(Numeric(7, 4), nullable=True)
    median_response_hours: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), nullable=True)
    price_position: Mapped[Decimal | None] = mapped_column(Numeric(7, 4), nullable=True)
    quote_invoice_match_rate: Mapped[Decimal | None] = mapped_column(Numeric(7, 4), nullable=True)
    rollover_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    computed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
