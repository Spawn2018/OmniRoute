import uuid

from sqlalchemy import ForeignKey, ForeignKeyConstraint, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class FxDifference(Base, TimestampMixin):
    __tablename__ = "fx_difference"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "quotation_id"],
            ["quotation.organization_id", "quotation.id"],
            name="fk_fx_difference_quotation",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "nbp_rate_id"],
            ["nbp_rate.organization_id", "nbp_rate.id"],
            name="fk_fx_difference_rate",
            ondelete="RESTRICT",
        ),
        UniqueConstraint(
            "organization_id",
            "quotation_id",
            "nbp_rate_id",
            name="uq_fx_difference_pair",
        ),
        Index("ix_fx_difference_org_quotation", "organization_id", "quotation_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), index=True,
    )
    quotation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    nbp_rate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
