import uuid

from sqlalchemy import ForeignKey, ForeignKeyConstraint, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class MoneyCost(Base, TimestampMixin):
    __tablename__ = "money_cost"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "bank_payment_id"],
            ["bank_payment.organization_id", "bank_payment.id"],
            name="fk_money_cost_payment",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "nbp_rate_id"],
            ["nbp_rate.organization_id", "nbp_rate.id"],
            name="fk_money_cost_rate",
            ondelete="RESTRICT",
        ),
        UniqueConstraint(
            "organization_id",
            "bank_payment_id",
            "nbp_rate_id",
            name="uq_money_cost_pair",
        ),
        Index("ix_money_cost_org_payment", "organization_id", "bank_payment_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), index=True,
    )
    bank_payment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    nbp_rate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
