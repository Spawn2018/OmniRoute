import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class PositionEvent(Base, TimestampMixin):
    __tablename__ = "position_event"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_position_event_org_id"),
        UniqueConstraint(
            "organization_id",
            "event_code",
            name="uq_position_event_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_position_event_org_source_ref",
        ),
        CheckConstraint(
            "event_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_position_event_code",
        ),
        CheckConstraint(
            "source_kind IN ('gps', 'manual', 'other')",
            name="ck_position_event_source_kind",
        ),
        Index("ix_position_event_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: zdarzenie pozycji tego tenanta — katalog HITL, nie live GPS.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    event_code: Mapped[str] = mapped_column(String(32), nullable=False)
    source_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
