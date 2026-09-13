import uuid
from decimal import Decimal

from sqlalchemy import (
    CHAR,
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
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
        CheckConstraint(
            "("
            "(status IN ('in_transit', 'completed') "
            "AND expected_buy_amount IS NOT NULL AND expected_buy_amount > 0 "
            "AND expected_buy_currency ~ '^[A-Z]{3}$') "
            "OR "
            "(status IN ('draft', 'planned', 'cancelled') "
            "AND expected_buy_amount IS NULL AND expected_buy_currency IS NULL)"
            ")",
            name="ck_trip_expected_buy_freeze",
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
        ForeignKeyConstraint(
            ["organization_id", "driver2_id"],
            ["resource.organization_id", "resource.id"],
            name="fk_trip_driver2",
            ondelete="RESTRICT",
        ),
        CheckConstraint(
            "driver2_id IS NULL OR driver_id IS NULL OR driver2_id <> driver_id",
            name="ck_trip_driver2_distinct",
        ),
        CheckConstraint(
            "planned_distance_km IS NULL OR planned_distance_km >= 0",
            name="ck_trip_planned_distance",
        ),
        CheckConstraint(
            "actual_distance_km IS NULL OR actual_distance_km >= 0",
            name="ck_trip_actual_distance",
        ),
        ForeignKeyConstraint(
            ["organization_id", "subcontractor_party_id"],
            ["party.organization_id", "party.id"],
            name="fk_trip_subcontractor_party",
            ondelete="RESTRICT",
        ),
        Index("ix_trip_org_status", "organization_id", "status"),
        UniqueConstraint("organization_id", "id", name="uq_trip_org_id"),
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
    driver2_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    source_ref: Mapped[str] = mapped_column(Text, nullable=False)
    route_label: Mapped[str | None] = mapped_column(String(128), nullable=True)
    planned_distance_km: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    actual_distance_km: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    subcontractor_party_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    expected_buy_amount: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    expected_buy_currency: Mapped[str | None] = mapped_column(CHAR(length=3), nullable=True)
    superseded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("trip.id", ondelete="RESTRICT"),
        nullable=True,
    )
