import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ShipmentPackage(Base, TimestampMixin):
    __tablename__ = "shipment_package"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_shipment_package_shipment",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "shipment_id", "stop_id"],
            ["stop.organization_id", "stop.shipment_id", "stop.id"],
            name="fk_shipment_package_stop",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "consignment_id"],
            ["consignment.organization_id", "consignment.id"],
            name="fk_shipment_package_consignment",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("organization_id", "id", name="uq_shipment_package_org_id"),
        CheckConstraint(
            "package_status IN ('noted','at_stop','in_transit','delivered')",
            name="ck_shipment_package_status",
        ),
        Index("ix_shipment_package_org_shipment", "organization_id", "shipment_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: paczka, zlecenie i stop jednego tenanta — trójka FK nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    shipment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    stop_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    consignment_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    package_code: Mapped[str] = mapped_column(String(32), nullable=False)
    package_status: Mapped[str] = mapped_column(String(16), nullable=False)
    scan_token: Mapped[str] = mapped_column(Text, nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
