import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import (
    CHAR,
    CheckConstraint,
    Date,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class CarrierInquiry(Base, TimestampMixin):
    __tablename__ = "carrier_inquiry"
    __table_args__ = (
        CheckConstraint(
            "status IN ('draft','queued','sent','answered','declined')",
            name="ck_carrier_inquiry_status",
        ),
        CheckConstraint(
            "(status = 'answered' AND quoted_amount IS NOT NULL "
            "AND quoted_currency IS NOT NULL) OR "
            "(status <> 'answered' AND quoted_amount IS NULL "
            "AND quoted_currency IS NULL AND quoted_transit_days IS NULL)",
            name="ck_carrier_inquiry_answered_quote",
        ),
        CheckConstraint(
            "quoted_transit_days IS NULL OR quoted_transit_days >= 1",
            name="ck_carrier_inquiry_transit",
        ),
        ForeignKeyConstraint(
            ["organization_id", "network_member_id"],
            ["network_member.organization_id", "network_member.id"],
            name="fk_carrier_inquiry_network_member",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "origin_port_id"],
            ["port.organization_id", "port.id"],
            name="fk_carrier_inquiry_origin_port",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "destination_port_id"],
            ["port.organization_id", "port.id"],
            name="fk_carrier_inquiry_destination_port",
            ondelete="RESTRICT",
        ),
        Index("ix_carrier_inquiry_org_member", "organization_id", "network_member_id"),
        Index("ix_carrier_inquiry_org_created", "organization_id", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    network_member_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
    status: Mapped[str] = mapped_column(String(8), nullable=False)
    origin_port_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    destination_port_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    quoted_amount: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    quoted_currency: Mapped[str | None] = mapped_column(CHAR(3), nullable=True)
    quoted_transit_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    no_reply_after: Mapped[date | None] = mapped_column(Date, nullable=True)
