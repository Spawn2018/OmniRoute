import uuid

from sqlalchemy import ForeignKey, ForeignKeyConstraint, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class TenderTedNotice(Base, TimestampMixin):
    __tablename__ = "tender_ted_notice"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_tender_ted_notice_org_id"),
        UniqueConstraint(
            "organization_id",
            "tender_id",
            name="uq_tender_ted_notice_org_tender",
        ),
        ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_ted_notice_tender",
            ondelete="RESTRICT",
        ),
        Index("ix_tender_ted_notice_org_notice", "organization_id", "notice_number"),
        Index("ix_tender_ted_notice_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: numer TED i nagłówek tego tenanta — tekst ogłoszenia nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    tender_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    notice_number: Mapped[str] = mapped_column(String(64), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
