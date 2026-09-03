import uuid

from sqlalchemy import ForeignKey, ForeignKeyConstraint, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class CashFlow(Base, TimestampMixin):
    __tablename__ = "cash_flow"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "quotation_id"],
            ["quotation.organization_id", "quotation.id"],
            name="fk_cash_flow_quotation",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "bank_payment_id"],
            ["bank_payment.organization_id", "bank_payment.id"],
            name="fk_cash_flow_payment",
            ondelete="RESTRICT",
        ),
        UniqueConstraint(
            "organization_id",
            "quotation_id",
            "bank_payment_id",
            name="uq_cash_flow_pair",
        ),
        Index("ix_cash_flow_org_quotation", "organization_id", "quotation_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), index=True,
    )
    quotation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    bank_payment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
