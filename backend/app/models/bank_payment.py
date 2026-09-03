import uuid

from sqlalchemy import ForeignKey, ForeignKeyConstraint, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class BankPayment(Base, TimestampMixin):
    __tablename__ = "bank_payment"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "sales_invoice_id"],
            ["sales_invoice.organization_id", "sales_invoice.id"],
            name="fk_bank_payment_invoice",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "party_bank_account_id"],
            ["party_bank_account.organization_id", "party_bank_account.id"],
            name="fk_bank_payment_account",
            ondelete="RESTRICT",
        ),
        UniqueConstraint(
            "organization_id",
            "sales_invoice_id",
            "party_bank_account_id",
            name="uq_bank_payment_pair",
        ),
        Index("ix_bank_payment_org_invoice", "organization_id", "sales_invoice_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), index=True,
    )
    sales_invoice_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    party_bank_account_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
