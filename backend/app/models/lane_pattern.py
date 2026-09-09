import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_UNLOCODE = r"^[A-Z]{2}[A-Z0-9]{3}$"


class LanePattern(Base, TimestampMixin):
    __tablename__ = "lane_pattern"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_lane_pattern_org_id"),
        UniqueConstraint(
            "organization_id",
            "origin_unlocode",
            "destination_unlocode",
            name="uq_lane_pattern_org_pair",
        ),
        CheckConstraint(
            "origin_unlocode <> destination_unlocode",
            name="ck_lane_pattern_ends_differ",
        ),
        CheckConstraint(
            f"origin_unlocode ~ '{_UNLOCODE}'",
            name="ck_lane_pattern_origin_unlocode",
        ),
        CheckConstraint(
            f"destination_unlocode ~ '{_UNLOCODE}'",
            name="ck_lane_pattern_dest_unlocode",
        ),
        Index("ix_lane_pattern_org_origin", "organization_id", "origin_unlocode"),
        Index("ix_lane_pattern_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: wzorzec korytarza tego tenanta — CHECK UN/LOCODE nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    origin_unlocode: Mapped[str] = mapped_column(String(5), nullable=False)
    destination_unlocode: Mapped[str] = mapped_column(String(5), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
