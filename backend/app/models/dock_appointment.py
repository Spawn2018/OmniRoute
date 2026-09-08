import uuid
from datetime import date, time

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
    Time,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class DockAppointment(Base, TimestampMixin):
    __tablename__ = "dock_appointment"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_dock_appointment_shipment",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "shipment_id", "stop_id"],
            ["stop.organization_id", "stop.shipment_id", "stop.id"],
            name="fk_dock_appointment_stop",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("organization_id", "id", name="uq_dock_appointment_org_id"),
        CheckConstraint(
            "appointment_status IN ('noted','advised','at_dock','released')",
            name="ck_dock_appointment_status",
        ),
        CheckConstraint(
            "window_end_local > window_start_local",
            name="ck_dock_appointment_window",
        ),
        Index("ix_dock_appointment_org_stop", "organization_id", "stop_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: awizacja, zlecenie i stop jednego tenanta — trójka FK nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    shipment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    stop_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    appointment_code: Mapped[str] = mapped_column(String(32), nullable=False)
    appointment_status: Mapped[str] = mapped_column(String(16), nullable=False)
    window_date: Mapped[date] = mapped_column(Date, nullable=False)
    window_start_local: Mapped[time] = mapped_column(Time, nullable=False)
    window_end_local: Mapped[time] = mapped_column(Time, nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
