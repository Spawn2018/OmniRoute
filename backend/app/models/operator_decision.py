import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class OperatorDecision(Base, TimestampMixin):
    __tablename__ = "operator_decision"
    __table_args__ = (
        CheckConstraint(
            "subject_kind = 'inbound_message'",
            name="ck_operator_decision_subject_kind",
        ),
        CheckConstraint(
            "status IN ('pending', 'accepted', 'changed', 'rejected')",
            name="ck_operator_decision_status",
        ),
        Index(
            "uq_operator_decision_pending",
            "organization_id",
            "subject_kind",
            "subject_id",
            unique=True,
            postgresql_where=text("status = 'pending'"),
        ),
        Index("ix_operator_decision_org_created", "organization_id", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    subject_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    subject_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    decided_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    source_ref: Mapped[str] = mapped_column(String(512), nullable=False)
