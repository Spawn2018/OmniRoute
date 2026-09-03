import uuid

from sqlalchemy import ForeignKey, ForeignKeyConstraint, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class CollectiveInvoice(Base, TimestampMixin):
    __tablename__ = "collective_invoice"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "sales_invoice_id"],
            ["sales_invoice.organization_id", "sales_invoice.id"],
            name="fk_collective_invoice_invoice",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_collective_invoice_shipment",
            ondelete="RESTRICT",
        ),
        UniqueConstraint(
            "organization_id",
            "sales_invoice_id",
            "shipment_id",
            name="uq_collective_invoice_pair",
        ),
        Index("ix_collective_invoice_org_invoice", "organization_id", "sales_invoice_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), index=True,
    )
    sales_invoice_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    shipment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
