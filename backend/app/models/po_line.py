import uuid
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class PoLine(Base, TimestampMixin):
    __tablename__ = "po_line"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "purchase_order_id"],
            ["purchase_order.organization_id", "purchase_order.id"],
            name="fk_po_line_purchase_order",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("organization_id", "id", name="uq_po_line_org_id"),
        UniqueConstraint(
            "organization_id",
            "purchase_order_id",
            "line_code",
            name="uq_po_line_org_header_line",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_po_line_org_source_ref",
        ),
        CheckConstraint(
            "line_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_po_line_code",
        ),
        CheckConstraint("qty >= 0", name="ck_po_line_qty"),
        CheckConstraint(
            "char_length(btrim(sku_code)) BETWEEN 1 AND 64",
            name="ck_po_line_sku",
        ),
        CheckConstraint(
            "char_length(btrim(uom_code)) BETWEEN 1 AND 16",
            name="ck_po_line_uom",
        ),
        CheckConstraint(
            "plant_label IS NULL OR char_length(btrim(plant_label)) BETWEEN 1 AND 128",
            name="ck_po_line_plant",
        ),
        CheckConstraint(
            "batch_label IS NULL OR char_length(btrim(batch_label)) BETWEEN 1 AND 128",
            name="ck_po_line_batch",
        ),
        CheckConstraint(
            "serial_label IS NULL OR char_length(btrim(serial_label)) BETWEEN 1 AND 128",
            name="ck_po_line_serial",
        ),
        CheckConstraint(
            "coo_label IS NULL OR char_length(btrim(coo_label)) BETWEEN 1 AND 128",
            name="ck_po_line_coo",
        ),
        Index("ix_po_line_organization_id", "organization_id"),
        Index("ix_po_line_org_header", "organization_id", "purchase_order_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: linia SKU tego tenanta — qty Decimal, nie float i nie kwota.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    purchase_order_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    line_code: Mapped[str] = mapped_column(String(32), nullable=False)
    sku_code: Mapped[str] = mapped_column(String(64), nullable=False)
    qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    uom_code: Mapped[str] = mapped_column(String(16), nullable=False)
    plant_label: Mapped[str | None] = mapped_column(String(128), nullable=True)
    batch_label: Mapped[str | None] = mapped_column(String(128), nullable=True)
    serial_label: Mapped[str | None] = mapped_column(String(128), nullable=True)
    coo_label: Mapped[str | None] = mapped_column(String(128), nullable=True)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
