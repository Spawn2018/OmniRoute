import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Task(Base, TimestampMixin):
    __tablename__ = "task"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "id",
            name="uq_task_org_id",
        ),
        UniqueConstraint(
            "organization_id",
            "task_code",
            name="uq_task_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_task_org_src",
        ),
        CheckConstraint(
            "task_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_task_code",
        ),
        CheckConstraint(
            "template_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_task_template_code",
        ),
        CheckConstraint(
            "status_kind IN ('open', 'done', 'skipped', 'other')",
            name="ck_task_status_kind",
        ),
        Index("ix_task_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: wpis zadania HITL — nie matching SQL / FK kontekstu.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
    )
    task_code: Mapped[str] = mapped_column(String(32), nullable=False)
    template_code: Mapped[str] = mapped_column(String(32), nullable=False)
    status_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
