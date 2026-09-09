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


class TenderAwardReview(Base, TimestampMixin):
    __tablename__ = "tender_award_review"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_tender_award_review_org_id"),
        UniqueConstraint(
            "organization_id",
            "tender_id",
            name="uq_tender_award_review_org_tender",
        ),
        CheckConstraint(
            "review_code IN ('countersign', 'challenge')",
            name="ck_tender_award_review_code",
        ),
        ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_award_review_tender",
            ondelete="RESTRICT",
        ),
        Index("ix_tender_award_review_org_code", "organization_id", "review_code"),
        Index("ix_tender_award_review_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: cztery oczy i nagłówek tego tenanta — CHECK countersign/challenge nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    tender_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    review_code: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
