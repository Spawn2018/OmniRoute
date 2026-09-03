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

_KIND_SQL = "invoice_kind IN ('issued', 'noted', 'other')"


class SalesInvoice(Base, TimestampMixin):
    __tablename__ = "sales_invoice"
    __table_args__ = (
        CheckConstraint(_KIND_SQL, name="ck_sales_invoice_kind"),
        ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_sales_invoice_shipment",
            ondelete="RESTRICT",
        ),
        Index("ix_sales_invoice_org_shipment", "organization_id", "shipment_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        index=True,
    )
    shipment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    invoice_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    invoice_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
