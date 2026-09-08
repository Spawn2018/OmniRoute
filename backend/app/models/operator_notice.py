import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class OperatorNotice(Base, TimestampMixin):
    __tablename__ = "operator_notice"
    __table_args__ = (
        CheckConstraint("kind IN ('manual','no_reply')", name="ck_operator_notice_kind"),
        CheckConstraint("status IN ('unread', 'read')", name="ck_operator_notice_status"),
        CheckConstraint(
            "(status = 'unread' AND read_at IS NULL) OR "
            "(status = 'read' AND read_at IS NOT NULL)",
            name="ck_operator_notice_read_pair",
        ),
        Index("ix_operator_notice_org_created", "organization_id", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    kind: Mapped[str] = mapped_column(String(16), nullable=False)
    body: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[str] = mapped_column(String(8), nullable=False)
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    source_ref: Mapped[str] = mapped_column(String(512), nullable=False)
