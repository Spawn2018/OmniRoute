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


class TenderWinLoss(Base, TimestampMixin):
    __tablename__ = "tender_win_loss"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_tender_win_loss_org_id"),
        UniqueConstraint(
            "organization_id",
            "tender_id",
            name="uq_tender_win_loss_org_tender",
        ),
        CheckConstraint(
            "outcome IN ('won', 'lost', 'no_bid')",
            name="ck_tender_win_loss_outcome",
        ),
        CheckConstraint(
            "reason_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_tender_win_loss_reason",
        ),
        ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_win_loss_tender",
            ondelete="RESTRICT",
        ),
        Index("ix_tender_win_loss_org_outcome", "organization_id", "outcome"),
        Index("ix_tender_win_loss_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: werdykt i nagłówek jednego tenanta — CHECK wyniku nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
    )
    tender_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    outcome: Mapped[str] = mapped_column(String(16), nullable=False)
    reason_code: Mapped[str] = mapped_column(String(32), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
