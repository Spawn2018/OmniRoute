import uuid

from sqlalchemy import ForeignKey, ForeignKeyConstraint, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class CostToServe(Base, TimestampMixin):
    __tablename__ = "cost_to_serve"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "customer_sop_id"],
            ["customer_sop.organization_id", "customer_sop.id"],
            name="fk_cost_to_serve_sop",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "quotation_id"],
            ["quotation.organization_id", "quotation.id"],
            name="fk_cost_to_serve_quotation",
            ondelete="RESTRICT",
        ),
        UniqueConstraint(
            "organization_id",
            "customer_sop_id",
            "quotation_id",
            name="uq_cost_to_serve_pair",
        ),
        Index("ix_cost_to_serve_org_sop", "organization_id", "customer_sop_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), index=True,
    )
    customer_sop_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    quotation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
