import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class BidDecisionMark(Base, TimestampMixin):
    __tablename__ = "bid_decision_mark"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_bid_decision_mark_org_id"),
        UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_bid_decision_mark_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_bid_decision_mark_org_source_ref",
        ),
        CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_bid_decision_mark_code",
        ),
        CheckConstraint(
            "decision_kind IN ('go', 'no_go', 'hold', 'other')",
            name="ck_bid_decision_mark_decision_kind",
        ),
        Index("ix_bid_decision_mark_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: decyzja go/no_go/hold tego tenanta — katalog HITL, nie kolumna quotation.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    mark_code: Mapped[str] = mapped_column(String(32), nullable=False)
    decision_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
