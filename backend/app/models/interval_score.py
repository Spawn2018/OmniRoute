import uuid
from decimal import Decimal

from sqlalchemy import Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class IntervalScore(Base):
    __tablename__ = "interval_score"

    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    outcome_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    suggestion_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    interval_low: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    interval_high: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    actual_value: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    mae: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    crps: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
