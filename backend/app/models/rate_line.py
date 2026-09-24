import uuid
from decimal import Decimal

from sqlalchemy import CHAR, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class RateLine(Base, TimestampMixin):
    __tablename__ = "rate_line"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    charge_code: Mapped[str] = mapped_column(String(32), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    allotment_teu: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    spot_or_contract: Mapped[str | None] = mapped_column(String(16), nullable=True)
    index_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    source_ref: Mapped[str] = mapped_column(String(512), nullable=False)
    superseded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("rate_line.id", ondelete="RESTRICT"),
        nullable=True,
    )
