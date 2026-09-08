import uuid

from sqlalchemy import CheckConstraint, ForeignKey, ForeignKeyConstraint, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class BookingInstruction(Base, TimestampMixin):
    __tablename__ = "booking_instruction"
    __table_args__ = (
        CheckConstraint(
            "booking_scope IN ('precarriage','ocean','oncarriage','contact_exchange','none')",
            name="ck_booking_instruction_scope",
        ),
        CheckConstraint(
            "target_role IN ('shipper','consignee','origin_agent','dest_agent',"
            "'ocean_carrier','omni_customs','client_customs')",
            name="ck_booking_instruction_role",
        ),
        CheckConstraint(
            "status IN ('suggested','accepted','sent','confirmed','rejected')",
            name="ck_booking_instruction_status",
        ),
        ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_booking_instruction_shipment",
            ondelete="RESTRICT",
        ),
        Index("ix_booking_instruction_org_shipment", "organization_id", "shipment_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    superseded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("booking_instruction.id", ondelete="RESTRICT"),
        nullable=True,
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    shipment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    booking_scope: Mapped[str] = mapped_column(String(20), nullable=False)
    target_role: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(12), nullable=False)
    source_ref: Mapped[str] = mapped_column(Text, nullable=False)
