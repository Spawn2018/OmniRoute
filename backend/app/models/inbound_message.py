import uuid

from sqlalchemy import CheckConstraint, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class InboundMessage(Base, TimestampMixin):
    __tablename__ = "inbound_message"
    __table_args__ = (
        CheckConstraint("status = 'draft'", name="ck_inbound_message_status_draft"),
        CheckConstraint(
            "source_ref ~ '^(fixture|synth)://'",
            name="ck_inbound_message_source_fixture",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    source_ref: Mapped[str] = mapped_column(String(512), nullable=False)
    from_address: Mapped[str] = mapped_column(String(320), nullable=False)
    subject: Mapped[str] = mapped_column(String(512), nullable=False)
    body_text: Mapped[str] = mapped_column(Text(), nullable=False)
    status: Mapped[str] = mapped_column(String(8), nullable=False)
