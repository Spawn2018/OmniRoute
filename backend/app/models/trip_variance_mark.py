import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class TripVarianceMark(Base, TimestampMixin):
    __tablename__ = "trip_variance_mark"
    __table_args__ = (
        CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_trip_variance_mark_code",
        ),
        CheckConstraint(
            "variance_kind IN ('expected', 'actual', 'gap', 'other')",
            name="ck_trip_variance_mark_kind",
        ),
        UniqueConstraint(
            "organization_id", "id", name="uq_trip_variance_mark_org_id"
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_trip_variance_mark_org_source_ref",
        ),
        UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_trip_variance_mark_org_code",
        ),
        Index("ix_trip_variance_mark_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: stance wariancji przejazdu zmiany — HITL, nie SQL na charge / druga marża.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    mark_code: Mapped[str] = mapped_column(String(32), nullable=False)
    variance_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
