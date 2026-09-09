import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class CashDiscount(Base, TimestampMixin):
    __tablename__ = "cash_discount"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_cash_discount_org_id"),
        UniqueConstraint(
            "organization_id",
            "sales_invoice_id",
            "discount_kind",
            name="uq_cash_discount_org_invoice_kind",
        ),
        ForeignKeyConstraint(
            ["organization_id", "sales_invoice_id"],
            ["sales_invoice.organization_id", "sales_invoice.id"],
            name="fk_cash_discount_sales_invoice",
            ondelete="RESTRICT",
        ),
        CheckConstraint(
            "discount_kind ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_cash_discount_kind",
        ),
        Index("ix_cash_discount_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: skonto tego tenanta — kind nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    sales_invoice_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    discount_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
