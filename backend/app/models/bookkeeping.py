import uuid

from sqlalchemy import ForeignKey, ForeignKeyConstraint, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Bookkeeping(Base, TimestampMixin):
    __tablename__ = "bookkeeping"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "charge_id"],
            ["charge.organization_id", "charge.id"],
            name="fk_bookkeeping_charge",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "sales_invoice_id"],
            ["sales_invoice.organization_id", "sales_invoice.id"],
            name="fk_bookkeeping_invoice",
            ondelete="RESTRICT",
        ),
        UniqueConstraint(
            "organization_id",
            "charge_id",
            "sales_invoice_id",
            name="uq_bookkeeping_pair",
        ),
        Index("ix_bookkeeping_org_charge", "organization_id", "charge_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), index=True,
    )
    charge_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    sales_invoice_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
