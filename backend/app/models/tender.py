import uuid
from datetime import date

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Tender(Base, TimestampMixin):
    __tablename__ = "tender"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_tender_org_id"),
        CheckConstraint("side IN ('sell', 'buy')", name="ck_tender_side"),
        CheckConstraint(
            "kind IN ('open', 'restricted', 'sealed', 'e_auction')",
            name="ck_tender_kind",
        ),
        CheckConstraint(
            "status IN ('draft', 'open', 'awarded', 'lost', 'no_bid')",
            name="ck_tender_status",
        ),
        ForeignKeyConstraint(
            ["organization_id", "buyer_party_id"],
            ["party.organization_id", "party.id"],
            name="fk_tender_buyer_party",
            ondelete="RESTRICT",
        ),
        Index("ix_tender_org_status", "organization_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    side: Mapped[str] = mapped_column(String(8), nullable=False)
    kind: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    buyer_party_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    deadline_at: Mapped[date] = mapped_column(Date, nullable=False)
    incoterm: Mapped[str] = mapped_column(String(3), nullable=False)
    trade_side: Mapped[str] = mapped_column(String(8), nullable=False)
    named_place: Mapped[str] = mapped_column(String(256), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
