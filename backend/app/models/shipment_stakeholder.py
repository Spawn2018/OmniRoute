import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ShipmentStakeholder(Base, TimestampMixin):
    __tablename__ = "shipment_stakeholder"
    __table_args__ = (
        CheckConstraint(
            "role IN ('shipper','consignee','origin_agent','dest_agent',"
            "'ocean_carrier','omni_customs','client_customs')",
            name="ck_shipment_stakeholder_role",
        ),
        ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_shipment_stakeholder_shipment",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_shipment_stakeholder_party",
            ondelete="RESTRICT",
        ),
        Index("ix_shipment_stakeholder_org_shipment", "organization_id", "shipment_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: strona należy do tenanta zlecenia — złożone FK nie zastępują current_org.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    shipment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    party_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    role: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
    superseded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("shipment_stakeholder.id", ondelete="RESTRICT"),
        nullable=True,
    )
