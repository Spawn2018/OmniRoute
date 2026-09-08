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


class TenderDataRoom(Base, TimestampMixin):
    __tablename__ = "tender_data_room"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_tender_data_room_org_id"),
        UniqueConstraint(
            "organization_id",
            "tender_id",
            "nda_mark",
            name="uq_tender_data_room_org_tender_nda",
        ),
        CheckConstraint("nda_mark = 'signed'", name="ck_tender_data_room_nda"),
        ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_data_room_tender",
            ondelete="RESTRICT",
        ),
        Index("ix_tender_data_room_org_tender", "organization_id", "tender_id"),
        Index("ix_tender_data_room_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organization.id", ondelete="RESTRICT"),
        type_=UUID(as_uuid=True),
        nullable=False,
    )
    tender_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    nda_mark: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
