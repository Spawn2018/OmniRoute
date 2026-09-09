import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_KIND_SQL = "clock_kind IN ('demurrage','detention','mixed','rollover')"


class FreeTimeClock(Base, TimestampMixin):
    __tablename__ = "free_time_clock"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_free_time_clock_org_id"),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_free_time_clock_org_source_ref",
        ),
        CheckConstraint(_KIND_SQL, name="ck_free_time_clock_kind"),
        CheckConstraint("free_days >= 0", name="ck_free_time_clock_days"),
        Index("ix_free_time_clock_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: zegar D&D tego tenanta — HITL dni, nie countdown.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    clock_kind: Mapped[str] = mapped_column(String(12), nullable=False)
    free_days: Mapped[int] = mapped_column(Integer, nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
