import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class TenderDeclineReason(Base, TimestampMixin):
    __tablename__ = "tender_decline_reason"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_tender_decline_reason_org_id"),
        UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_tender_decline_reason_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_tender_decline_reason_org_source_ref",
        ),
        CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_tender_decline_reason_code",
        ),
        CheckConstraint(
            "decline_kind IN ('decline', 'no_bid', 'withdraw', 'other')",
            name="ck_tender_decline_reason_decline_kind",
        ),
        Index("ix_tender_decline_reason_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: znacznik tender decline tego tenanta — katalog HITL, nie decline auto.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    mark_code: Mapped[str] = mapped_column(String(32), nullable=False)
    decline_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
