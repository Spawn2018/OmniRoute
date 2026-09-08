import uuid
from datetime import time

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    SmallInteger,
    String,
    Text,
    Time,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class GroupageLine(Base, TimestampMixin):
    __tablename__ = "groupage_line"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "origin_location_id"],
            ["location.organization_id", "location.id"],
            name="fk_groupage_line_origin",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "destination_location_id"],
            ["location.organization_id", "location.id"],
            name="fk_groupage_line_destination",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("organization_id", "id", name="uq_groupage_line_org_id"),
        CheckConstraint("transit_days >= 1", name="ck_groupage_line_transit_days"),
        CheckConstraint(
            "cardinality(operating_dows) >= 1",
            name="ck_groupage_line_dows_len",
        ),
        CheckConstraint(
            "operating_dows <@ ARRAY[1,2,3,4,5,6,7]::smallint[]",
            name="ck_groupage_line_dows_iso",
        ),
        CheckConstraint(
            "origin_location_id <> destination_location_id",
            name="ck_groupage_line_distinct_ends",
        ),
        Index("ix_groupage_line_org_code", "organization_id", "line_code"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    line_code: Mapped[str] = mapped_column(String(32), nullable=False)
    origin_location_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    destination_location_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    cutoff_local: Mapped[time] = mapped_column(Time, nullable=False)
    transit_days: Mapped[int] = mapped_column(Integer, nullable=False)
    operating_dows: Mapped[list[int]] = mapped_column(ARRAY(SmallInteger), nullable=False)
    source_ref: Mapped[str] = mapped_column(Text, nullable=False)
    superseded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("groupage_line.id", ondelete="RESTRICT"),
        nullable=True,
    )
