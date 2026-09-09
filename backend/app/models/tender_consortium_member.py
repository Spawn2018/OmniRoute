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


class TenderConsortiumMember(Base, TimestampMixin):
    __tablename__ = "tender_consortium_member"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_tender_consortium_member_org_id"),
        UniqueConstraint(
            "organization_id",
            "tender_id",
            "party_id",
            name="uq_tender_consortium_member_org_tender_party",
        ),
        CheckConstraint(
            "seat_code IN ('lead', 'member')",
            name="ck_tender_consortium_member_seat",
        ),
        ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_consortium_member_tender",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_tender_consortium_member_party",
            ondelete="RESTRICT",
        ),
        Index("ix_tender_consortium_member_org_tender", "organization_id", "tender_id"),
        Index("ix_tender_consortium_member_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: fotel i nagłówek jednego tenanta — CHECK fotela nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
    )
    tender_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    party_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    seat_code: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
