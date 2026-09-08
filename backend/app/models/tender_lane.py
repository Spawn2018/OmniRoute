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

_UNLOCODE = r"^[A-Z]{2}[A-Z0-9]{3}$"


class TenderLane(Base, TimestampMixin):
    __tablename__ = "tender_lane"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_tender_lane_org_id"),
        UniqueConstraint(
            "organization_id",
            "tender_lot_id",
            "origin_unlocode",
            "destination_unlocode",
            name="uq_tender_lane_org_lot_pair",
        ),
        CheckConstraint(
            "origin_unlocode <> destination_unlocode",
            name="ck_tender_lane_ends_differ",
        ),
        CheckConstraint(
            f"origin_unlocode ~ '{_UNLOCODE}'",
            name="ck_tender_lane_origin_unlocode",
        ),
        CheckConstraint(
            f"destination_unlocode ~ '{_UNLOCODE}'",
            name="ck_tender_lane_dest_unlocode",
        ),
        ForeignKeyConstraint(
            ["organization_id", "tender_lot_id"],
            ["tender_lot.organization_id", "tender_lot.id"],
            name="fk_tender_lane_lot",
            ondelete="RESTRICT",
        ),
        Index("ix_tender_lane_org_lot", "organization_id", "tender_lot_id"),
        Index("ix_tender_lane_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organization.id", ondelete="RESTRICT"),
        type_=UUID(as_uuid=True),
        nullable=False,
    )
    tender_lot_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    origin_unlocode: Mapped[str] = mapped_column(String(5), nullable=False)
    destination_unlocode: Mapped[str] = mapped_column(String(5), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
