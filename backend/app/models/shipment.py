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


class Shipment(Base, TimestampMixin):
    __tablename__ = "shipment"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "quotation_id",
            name="uq_shipment_org_quotation",
        ),
        CheckConstraint("status = 'draft'", name="ck_shipment_status_draft"),
        ForeignKeyConstraint(
            ["organization_id", "quotation_id"],
            ["quotation.organization_id", "quotation.id"],
            name="fk_shipment_quotation",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_shipment_party",
            ondelete="RESTRICT",
        ),
        Index("ix_shipment_org_party", "organization_id", "party_id"),
        Index("ix_shipment_org_created", "organization_id", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    quotation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    party_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
    status: Mapped[str] = mapped_column(String(8), nullable=False)
