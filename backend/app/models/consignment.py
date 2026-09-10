import uuid

from sqlalchemy import ForeignKey, ForeignKeyConstraint, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Consignment(Base, TimestampMixin):
    __tablename__ = "consignment"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_consignment_shipment",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("organization_id", "id", name="uq_consignment_org_id"),
        UniqueConstraint(
            "organization_id",
            "consignment_ref",
            name="uq_consignment_org_ref",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_consignment_org_source",
        ),
        Index("ix_consignment_org_shipment", "organization_id", "shipment_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: przesyłka i zlecenie jednego tenanta — złożone FK nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    shipment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    consignment_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
