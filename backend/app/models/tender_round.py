import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class TenderRound(Base, TimestampMixin):
    __tablename__ = "tender_round"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_tender_round_org_id"),
        UniqueConstraint(
            "organization_id",
            "tender_id",
            "round_no",
            name="uq_tender_round_org_tender_no",
        ),
        CheckConstraint("round_no >= 1", name="ck_tender_round_no"),
        ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_round_tender",
            ondelete="RESTRICT",
        ),
        Index("ix_tender_round_org_tender", "organization_id", "tender_id"),
        Index("ix_tender_round_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organization.id", ondelete="RESTRICT"),
        type_=UUID(as_uuid=True),
        nullable=False,
    )
    tender_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    round_no: Mapped[int] = mapped_column(Integer, nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
