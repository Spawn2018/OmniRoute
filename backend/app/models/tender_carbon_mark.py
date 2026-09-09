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


class TenderCarbonMark(Base, TimestampMixin):
    __tablename__ = "tender_carbon_mark"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_tender_carbon_mark_org_id"),
        UniqueConstraint(
            "organization_id",
            "tender_id",
            name="uq_tender_carbon_mark_org_tender",
        ),
        CheckConstraint(
            "mark_code IN ('declared', 'exempt')",
            name="ck_tender_carbon_mark_code",
        ),
        ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_carbon_mark_tender",
            ondelete="RESTRICT",
        ),
        Index("ix_tender_carbon_mark_org_code", "organization_id", "mark_code"),
        Index("ix_tender_carbon_mark_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: znacznik śladu i nagłówek tego tenanta — CHECK declared/exempt nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    tender_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    mark_code: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
