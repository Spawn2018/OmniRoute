import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_HOURS = "(median_response_hours IS NULL OR median_response_hours >= 0)"
_WINDOW = "(window_days >= 1 AND window_days <= 365)"


class PartyLaneScorecard(Base, TimestampMixin):
    __tablename__ = "party_lane_scorecard"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "party_id",
            "origin_port_id",
            "destination_port_id",
            "window_days",
            name="uq_party_lane_scorecard_org_party_lane_window",
        ),
        ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_party_lane_scorecard_party",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "origin_port_id"],
            ["port.organization_id", "port.id"],
            name="fk_party_lane_scorecard_origin_port",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "destination_port_id"],
            ["port.organization_id", "port.id"],
            name="fk_party_lane_scorecard_destination_port",
            ondelete="RESTRICT",
        ),
        CheckConstraint("sample_size >= 0", name="ck_party_lane_scorecard_sample_size"),
        CheckConstraint(
            "answered_inquiry_count >= 0",
            name="ck_party_lane_scorecard_answered",
        ),
        CheckConstraint("shipment_count >= 0", name="ck_party_lane_scorecard_shipments"),
        CheckConstraint("cheapest_count >= 0", name="ck_party_lane_scorecard_cheapest"),
        CheckConstraint(_WINDOW, name="ck_party_lane_scorecard_window_days"),
        CheckConstraint(_HOURS, name="ck_party_lane_scorecard_median_hours"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    party_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    origin_port_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    destination_port_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    window_days: Mapped[int] = mapped_column(Integer, nullable=False)
    sample_size: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    answered_inquiry_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=text("0"),
    )
    shipment_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    cheapest_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    median_response_hours: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), nullable=True)
    computed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
