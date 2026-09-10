import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class PurchaseOrder(Base, TimestampMixin):
    __tablename__ = "purchase_order"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_purchase_order_org_id"),
        UniqueConstraint("organization_id", "po_code", name="uq_purchase_order_org_code"),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_purchase_order_org_source_ref",
        ),
        CheckConstraint(
            "po_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_purchase_order_code",
        ),
        CheckConstraint(
            "plant_label IS NULL OR char_length(btrim(plant_label)) BETWEEN 1 AND 128",
            name="ck_purchase_order_plant",
        ),
        Index("ix_purchase_order_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: nagłówek PO tego tenanta — etykieta zakładu, nie FK i nie linia SKU.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    po_code: Mapped[str] = mapped_column(String(32), nullable=False)
    plant_label: Mapped[str | None] = mapped_column(String(128), nullable=True)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
