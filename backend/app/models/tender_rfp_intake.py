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


class TenderRfpIntake(Base, TimestampMixin):
    __tablename__ = "tender_rfp_intake"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_tender_rfp_intake_org_id"),
        UniqueConstraint(
            "organization_id",
            "tender_id",
            "intake_code",
            name="uq_tender_rfp_intake_org_tender_code",
        ),
        CheckConstraint(
            "intake_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_tender_rfp_intake_code",
        ),
        ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_rfp_intake_tender",
            ondelete="RESTRICT",
        ),
        Index("ix_tender_rfp_intake_org_tender", "organization_id", "tender_id"),
        Index("ix_tender_rfp_intake_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: przyjęcie i nagłówek jednego tenanta — CHECK kodu nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
    )
    tender_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    intake_code: Mapped[str] = mapped_column(String(32), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
