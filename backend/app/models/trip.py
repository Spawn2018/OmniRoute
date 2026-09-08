import uuid

from sqlalchemy import CheckConstraint, ForeignKey, ForeignKeyConstraint, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Trip(Base, TimestampMixin):
    __tablename__ = "trip"
    __table_args__ = (
        CheckConstraint(
            "status IN ('draft', 'planned', 'in_transit', 'completed', 'cancelled')",
            name="ck_trip_status",
        ),
        ForeignKeyConstraint(
            ["organization_id", "vehicle_id"],
            ["resource.organization_id", "resource.id"],
            name="fk_trip_vehicle",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "trailer_id"],
            ["resource.organization_id", "resource.id"],
            name="fk_trip_trailer",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "driver_id"],
            ["resource.organization_id", "resource.id"],
            name="fk_trip_driver",
            ondelete="RESTRICT",
        ),
        Index("ix_trip_org_status", "organization_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    trip_no: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(12), nullable=False)
    vehicle_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    trailer_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    driver_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    source_ref: Mapped[str] = mapped_column(Text, nullable=False)
    superseded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("trip.id", ondelete="RESTRICT"),
        nullable=True,
    )
