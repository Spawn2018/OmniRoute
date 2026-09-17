import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class PurchaseInvoice(Base, TimestampMixin):
    __tablename__ = "purchase_invoice"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_purchase_invoice_org_id"),
        UniqueConstraint(
            "organization_id",
            "invoice_ref",
            name="uq_purchase_invoice_org_ref",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_purchase_invoice_org_source_ref",
        ),
        CheckConstraint(
            "char_length(btrim(invoice_ref)) BETWEEN 1 AND 64",
            name="ck_purchase_invoice_ref",
        ),
        CheckConstraint(
            "invoice_kind IN ('noted', 'other')",
            name="ck_purchase_invoice_kind",
        ),
        Index("ix_purchase_invoice_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: FV zakupu HITL — nie ranking i nie allocation.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    invoice_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    invoice_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
