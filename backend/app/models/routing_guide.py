import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class RoutingGuide(Base, TimestampMixin):
    __tablename__ = "routing_guide"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_routing_guide_org_id"),
        UniqueConstraint(
            "organization_id",
            "guide_code",
            name="uq_routing_guide_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_routing_guide_org_source_ref",
        ),
        CheckConstraint(
            "guide_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_routing_guide_code",
        ),
        CheckConstraint(
            "lane_label IS NULL OR char_length(btrim(lane_label)) BETWEEN 1 AND 128",
            name="ck_routing_guide_lane",
        ),
        CheckConstraint(
            "mode_label IS NULL OR char_length(btrim(mode_label)) BETWEEN 1 AND 128",
            name="ck_routing_guide_mode",
        ),
        Index("ix_routing_guide_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: przewodnik CT4 tego tenanta — katalog HITL, nie 409.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    guide_code: Mapped[str] = mapped_column(String(32), nullable=False)
    lane_label: Mapped[str | None] = mapped_column(String(128), nullable=True)
    mode_label: Mapped[str | None] = mapped_column(String(128), nullable=True)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
