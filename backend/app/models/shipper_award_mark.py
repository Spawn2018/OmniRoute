import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ShipperAwardMark(Base, TimestampMixin):
    __tablename__ = "shipper_award_mark"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # Award stance BR6.2 — katalog HITL, nie silnik auto-award.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
    )
    mark_code: Mapped[str] = mapped_column(String(32), nullable=False)
    award_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)

    __table_args__ = (
        Index("ix_shipper_award_mark_organization_id", "organization_id"),
        CheckConstraint(
            "award_kind IN ('go', 'hold', 'no_award', 'other')",
            name="ck_shipper_award_mark_kind",
        ),
        CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_shipper_award_mark_code",
        ),
        UniqueConstraint("organization_id", "id", name="uq_shipper_award_mark_org_id"),
        UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_shipper_award_mark_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_shipper_award_mark_org_source_ref",
        ),
    )
