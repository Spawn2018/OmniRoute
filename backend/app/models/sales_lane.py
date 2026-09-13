import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class SalesLane(Base, TimestampMixin):
    __tablename__ = "sales_lane"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_sales_lane_org_id"),
        UniqueConstraint(
            "organization_id",
            "lane_code",
            name="uq_sales_lane_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_sales_lane_org_source_ref",
        ),
        CheckConstraint(
            "lane_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_sales_lane_code",
        ),
        CheckConstraint(
            "lane_kind IN ('repeat', 'spot', 'other')",
            name="ck_sales_lane_kind",
        ),
        Index("ix_sales_lane_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: korytarz sprzedazy tego tenanta — katalog HITL, nie para UN/LOCODE.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    lane_code: Mapped[str] = mapped_column(String(32), nullable=False)
    lane_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
