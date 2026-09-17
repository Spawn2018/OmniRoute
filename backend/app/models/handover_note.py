import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class HandoverNote(Base, TimestampMixin):
    __tablename__ = "handover_note"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "id",
            name="uq_handover_note_org_id",
        ),
        UniqueConstraint(
            "organization_id",
            "note_code",
            name="uq_handover_note_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_handover_note_org_src",
        ),
        CheckConstraint(
            "note_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_handover_note_code",
        ),
        CheckConstraint(
            "char_length(situation) BETWEEN 1 AND 2000",
            name="ck_handover_note_situation",
        ),
        CheckConstraint(
            "char_length(background) BETWEEN 1 AND 2000",
            name="ck_handover_note_background",
        ),
        CheckConstraint(
            "char_length(assessment) BETWEEN 1 AND 2000",
            name="ck_handover_note_assessment",
        ),
        CheckConstraint(
            "char_length(recommendation) BETWEEN 1 AND 2000",
            name="ck_handover_note_recommendation",
        ),
        Index("ix_handover_note_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: wpis przekazania S/B/A/R — HITL, nie auto z T6.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
    )
    note_code: Mapped[str] = mapped_column(String(32), nullable=False)
    situation: Mapped[str] = mapped_column(String(2000), nullable=False)
    background: Mapped[str] = mapped_column(String(2000), nullable=False)
    assessment: Mapped[str] = mapped_column(String(2000), nullable=False)
    recommendation: Mapped[str] = mapped_column(String(2000), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
