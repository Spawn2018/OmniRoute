import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class TaskTemplate(Base, TimestampMixin):
    __tablename__ = "task_template"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_task_template_org_id"),
        UniqueConstraint(
            "organization_id",
            "template_code",
            name="uq_task_template_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_task_template_org_source_ref",
        ),
        CheckConstraint(
            "template_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_task_template_code",
        ),
        CheckConstraint(
            "char_length(applies_when) BETWEEN 1 AND 512",
            name="ck_task_template_when",
        ),
        Index("ix_task_template_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: szablon zadania tego tenanta — HITL dane, nie worker.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    template_code: Mapped[str] = mapped_column(String(32), nullable=False)
    applies_when: Mapped[str] = mapped_column(String(512), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
