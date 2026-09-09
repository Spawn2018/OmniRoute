import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class TenderBidStance(Base, TimestampMixin):
    __tablename__ = "tender_bid_stance"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_tender_bid_stance_org_id"),
        UniqueConstraint(
            "organization_id",
            "tender_id",
            name="uq_tender_bid_stance_org_tender",
        ),
        CheckConstraint(
            "stance_code IN ('bid', 'no_bid')",
            name="ck_tender_bid_stance_code",
        ),
        ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_bid_stance_tender",
            ondelete="RESTRICT",
        ),
        Index("ix_tender_bid_stance_org_stance", "organization_id", "stance_code"),
        Index("ix_tender_bid_stance_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: postawa i nagłówek tego samego tenanta — CHECK bid/no_bid nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    tender_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    stance_code: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
