import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ErruMark(Base, TimestampMixin):
    __tablename__ = "erru_mark"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_erru_mark_org_id"),
        UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_erru_mark_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_erru_mark_org_source_ref",
        ),
        CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_erru_mark_code",
        ),
        CheckConstraint(
            "check_kind IN ('to_verify', 'clear', 'hit', 'other')",
            name="ck_erru_mark_check_kind",
        ),
        Index("ix_erru_mark_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: znacznik sprawdzenia ERRU tego tenanta — katalog HITL, nie live ERRU.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    mark_code: Mapped[str] = mapped_column(String(32), nullable=False)
    check_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
