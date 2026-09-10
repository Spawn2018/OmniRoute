import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Stop(Base, TimestampMixin):
    __tablename__ = "stop"
    __table_args__ = (
        CheckConstraint(
            "stop_kind IN ('loading','unloading','customs','ferry','terminal','depot','other')",
            name="ck_stop_kind",
        ),
        CheckConstraint(
            "status IN ('pending','at_stop','completed','failed')",
            name="ck_stop_status",
        ),
        CheckConstraint("sequence_no >= 1", name="ck_stop_sequence"),
        CheckConstraint(
            "time_zone ~ '^[A-Za-z_]+/[A-Za-z0-9_+-]+(/[A-Za-z0-9_+-]+)?$'",
            name="ck_stop_time_zone",
        ),
        CheckConstraint(
            "stop_group_code IS NULL OR stop_group_code ~ '^[A-Za-z0-9_-]{2,32}$'",
            name="ck_stop_group_code",
        ),
        CheckConstraint(
            "weight_kg IS NULL OR weight_kg >= 0",
            name="ck_stop_weight_kg",
        ),
        CheckConstraint(
            "quantity IS NULL OR quantity >= 0",
            name="ck_stop_quantity",
        ),
        ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_stop_shipment",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "location_id"],
            ["location.organization_id", "location.id"],
            name="fk_stop_location",
            ondelete="RESTRICT",
        ),
        Index("ix_stop_org_shipment", "organization_id", "shipment_id"),
        UniqueConstraint(
            "organization_id",
            "shipment_id",
            "id",
            name="uq_stop_org_shipment_id",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    shipment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    location_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    stop_kind: Mapped[str] = mapped_column(String(12), nullable=False)
    sequence_no: Mapped[int] = mapped_column(Integer, nullable=False)
    time_zone: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(12), nullable=False)
    source_ref: Mapped[str] = mapped_column(Text, nullable=False)
    stop_group_code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    notes_for_driver: Mapped[str | None] = mapped_column(String(256), nullable=True)
    weight_kg: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    quantity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    packaging_code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    seal_in: Mapped[str | None] = mapped_column(String(32), nullable=True)
    seal_out: Mapped[str | None] = mapped_column(String(32), nullable=True)
    appointment_ref: Mapped[str | None] = mapped_column(String(32), nullable=True)
    eta_physical: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    eta_legal: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    superseded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("stop.id", ondelete="RESTRICT"),
        nullable=True,
    )
