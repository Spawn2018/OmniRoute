import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class PlanSnapshot(Base, TimestampMixin):
    __tablename__ = "plan_snapshot"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_plan_snapshot_org_id"),
        UniqueConstraint(
            "organization_id",
            "snapshot_code",
            name="uq_plan_snapshot_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_plan_snapshot_org_source_ref",
        ),
        CheckConstraint(
            "snapshot_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_plan_snapshot_code",
        ),
        CheckConstraint(
            "char_length(author_label) BETWEEN 1 AND 64",
            name="ck_plan_snapshot_author",
        ),
        Index("ix_plan_snapshot_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: migawka planu tego tenanta — UUID trójki to dane, nie FK.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    snapshot_code: Mapped[str] = mapped_column(String(32), nullable=False)
    shipment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    trip_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    resource_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    author_label: Mapped[str] = mapped_column(String(64), nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
