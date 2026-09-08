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


class TenderPlaybook(Base, TimestampMixin):
    __tablename__ = "tender_playbook"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_tender_playbook_org_id"),
        UniqueConstraint(
            "organization_id",
            "tender_id",
            "claim_code",
            name="uq_tender_playbook_org_tender_code",
        ),
        CheckConstraint(
            "char_length(claim_text) >= 1 AND char_length(claim_text) <= 512",
            name="ck_tender_playbook_claim_text",
        ),
        CheckConstraint(
            "claim_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_tender_playbook_code",
        ),
        ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_playbook_tender",
            ondelete="RESTRICT",
        ),
        Index("ix_tender_playbook_org_tender", "organization_id", "tender_id"),
        Index("ix_tender_playbook_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: teza i nagłówek jednego tenanta — CHECK tekstu nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
    )
    tender_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    claim_code: Mapped[str] = mapped_column(String(32), nullable=False)
    claim_text: Mapped[str] = mapped_column(String(512), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
