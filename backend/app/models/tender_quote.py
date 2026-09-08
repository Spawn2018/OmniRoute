import uuid
from datetime import date

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class TenderQuote(Base, TimestampMixin):
    __tablename__ = "tender_quote"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_tender_quote_org_id"),
        CheckConstraint("order_limit > 0", name="ck_tender_quote_order_limit"),
        ForeignKeyConstraint(
            ["organization_id", "quotation_id"],
            ["quotation.organization_id", "quotation.id"],
            name="fk_tender_quote_quotation",
            ondelete="RESTRICT",
        ),
        Index("ix_tender_quote_org_quotation", "organization_id", "quotation_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    quotation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    valid_until: Mapped[date] = mapped_column(Date, nullable=False)
    order_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
