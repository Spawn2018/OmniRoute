import uuid
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Index, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class LaneKm(Base, TimestampMixin):
    __tablename__ = "lane_km"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_lane_km_org_id"),
        UniqueConstraint(
            "organization_id",
            "km_code",
            name="uq_lane_km_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_lane_km_org_source_ref",
        ),
        CheckConstraint(
            "km_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_lane_km_code",
        ),
        CheckConstraint(
            "loaded_km >= 0",
            name="ck_lane_km_loaded",
        ),
        CheckConstraint(
            "empty_km >= 0",
            name="ck_lane_km_empty",
        ),
        CheckConstraint(
            "approach_km >= 0",
            name="ck_lane_km_approach",
        ),
        Index("ix_lane_km_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: km korytarza tego tenanta — trójka Decimal to dane, nie Haversine.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    km_code: Mapped[str] = mapped_column(String(32), nullable=False)
    loaded_km: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    empty_km: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    approach_km: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
