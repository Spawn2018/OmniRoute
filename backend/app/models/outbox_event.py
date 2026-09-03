import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class OutboxEvent(Base, TimestampMixin):
    __tablename__ = "outbox_event"
    __table_args__ = (
        CheckConstraint(
            "event_kind = 'inbound_message_saved'",
            name="ck_outbox_event_kind",
        ),
        CheckConstraint("status = 'pending'", name="ck_outbox_event_status"),
        UniqueConstraint(
            "organization_id",
            "event_kind",
            "subject_id",
            name="uq_outbox_event_org_kind_subject",
        ),
        Index("ix_outbox_event_org_created", "organization_id", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    event_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    subject_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    status: Mapped[str] = mapped_column(String(8), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(512), nullable=False)
