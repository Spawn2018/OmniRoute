import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Container(Base, TimestampMixin):
    __tablename__ = "container"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_container_shipment",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "carrier_party_id"],
            ["party.organization_id", "party.id"],
            name="fk_container_carrier_party",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "shipment_leg_id"],
            ["shipment_leg.organization_id", "shipment_leg.id"],
            name="fk_container_shipment_leg",
            ondelete="RESTRICT",
        ),
        Index("ix_container_org_type", "organization_id", "iso_size_type"),
        CheckConstraint(
            "quantity IS NULL OR quantity >= 0",
            name="ck_container_quantity",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    container_no: Mapped[str] = mapped_column(String(11), nullable=False)
    iso_size_type: Mapped[str] = mapped_column(String(4), nullable=False)
    shipment_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    source_ref: Mapped[str] = mapped_column(Text, nullable=False)
    seal_no_1: Mapped[str | None] = mapped_column(String(32), nullable=True)
    seal_no_2: Mapped[str | None] = mapped_column(String(32), nullable=True)
    seal_no_3: Mapped[str | None] = mapped_column(String(32), nullable=True)
    vessel_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    voyage_no: Mapped[str | None] = mapped_column(String(32), nullable=True)
    remarks: Mapped[str | None] = mapped_column(String(256), nullable=True)
    cargo_description: Mapped[str | None] = mapped_column(String(256), nullable=True)
    packaging_code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    ref_1: Mapped[str | None] = mapped_column(String(64), nullable=True)
    ref_2: Mapped[str | None] = mapped_column(String(64), nullable=True)
    ref_3: Mapped[str | None] = mapped_column(String(64), nullable=True)
    ref_4: Mapped[str | None] = mapped_column(String(64), nullable=True)
    ref_5: Mapped[str | None] = mapped_column(String(64), nullable=True)
    reefer: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        server_default=text("false"),
        default=False,
    )
    pickup_terminal: Mapped[str | None] = mapped_column(String(32), nullable=True)
    return_terminal: Mapped[str | None] = mapped_column(String(32), nullable=True)
    bl_kind: Mapped[str | None] = mapped_column(String(16), nullable=True)
    free_time_origin_h: Mapped[int | None] = mapped_column(Integer(), nullable=True)
    free_time_dest_h: Mapped[int | None] = mapped_column(Integer(), nullable=True)
    demurrage_free_days: Mapped[int | None] = mapped_column(Integer(), nullable=True)
    detention_free_days: Mapped[int | None] = mapped_column(Integer(), nullable=True)
    mixed_dd_days: Mapped[int | None] = mapped_column(Integer(), nullable=True)
    si_cutoff_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ams_cutoff_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cy_cutoff_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cfs_cutoff_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    vgm_kg: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    tare_kg: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    pin_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    payload_kg: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    teu: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    quantity: Mapped[int | None] = mapped_column(Integer(), nullable=True)
    weight_kg: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    volume_m3: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    pickup_date: Mapped[date | None] = mapped_column(Date(), nullable=True)
    return_date: Mapped[date | None] = mapped_column(Date(), nullable=True)
    gate_in_date: Mapped[date | None] = mapped_column(Date(), nullable=True)
    delivery_date: Mapped[date | None] = mapped_column(Date(), nullable=True)
    unload_date: Mapped[date | None] = mapped_column(Date(), nullable=True)
    temp_min: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    vgm_method: Mapped[str | None] = mapped_column(String(16), nullable=True)
    vgm_cutoff_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_survey_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    booking_no: Mapped[str | None] = mapped_column(String(64), nullable=True)
    carrier_party_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    shipment_leg_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    superseded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("container.id", ondelete="RESTRICT"),
        nullable=True,
    )
