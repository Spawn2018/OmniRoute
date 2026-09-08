import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_EVENT_SQL = "event_kind IN ('inquiry_queued','inquiry_sent','quote_recorded')"
_SUBJECT_SQL = "subject_kind IN ('carrier_inquiry','quotation','channel_quote')"


class EntityEvent(Base, TimestampMixin):
    __tablename__ = "entity_event"
    __table_args__ = (
        CheckConstraint(_EVENT_SQL, name="ck_entity_event_kind"),
        CheckConstraint(_SUBJECT_SQL, name="ck_entity_event_subject_kind"),
        Index("ix_entity_event_org_occurred", "organization_id", "occurred_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    subject_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    subject_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    event_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    source_ref: Mapped[str] = mapped_column(String(512), nullable=False)
