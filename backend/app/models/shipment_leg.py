import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ShipmentLeg(Base, TimestampMixin):
    __tablename__ = "shipment_leg"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_shipment_leg_shipment",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "origin_location_id"],
            ["location.organization_id", "location.id"],
            name="fk_shipment_leg_origin",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "destination_location_id"],
            ["location.organization_id", "location.id"],
            name="fk_shipment_leg_destination",
            ondelete="RESTRICT",
        ),
        CheckConstraint(
            "leg_kind IN ('road', 'rail', 'china_rail', 'ocean_lcl', 'air')",
            name="ck_shipment_leg_kind",
        ),
        CheckConstraint(
            "origin_location_id <> destination_location_id",
            name="ck_shipment_leg_distinct_ends",
        ),
        UniqueConstraint(
            "organization_id",
            "shipment_id",
            "leg_kind",
            name="uq_shipment_leg_org_kind",
        ),
        Index("ix_shipment_leg_org_shipment", "organization_id", "shipment_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: odcinek należy do tenanta zlecenia — złożone FK nie zastępują current_org.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), index=True,
    )
    shipment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    origin_location_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    destination_location_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    leg_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
