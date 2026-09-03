import uuid

from sqlalchemy import ForeignKey, ForeignKeyConstraint, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class QuoteInvoiceSettlement(Base, TimestampMixin):
    __tablename__ = "quote_invoice_settlement"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "quotation_id"],
            ["quotation.organization_id", "quotation.id"],
            name="fk_quote_invoice_settlement_quotation",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "sales_invoice_id"],
            ["sales_invoice.organization_id", "sales_invoice.id"],
            name="fk_quote_invoice_settlement_invoice",
            ondelete="RESTRICT",
        ),
        UniqueConstraint(
            "organization_id",
            "quotation_id",
            "sales_invoice_id",
            name="uq_quote_invoice_settlement_pair",
        ),
        Index(
            "ix_quote_invoice_settlement_org_quotation",
            "organization_id",
            "quotation_id",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), index=True,
    )
    quotation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    sales_invoice_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
