import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ExtractionPromptMark(Base, TimestampMixin):
    __tablename__ = "extraction_prompt_mark"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # Prompt jako dana AI3.1 — katalog HITL, nie wiring Instructor.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
    )
    mark_code: Mapped[str] = mapped_column(String(32), nullable=False)
    prompt_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)

    __table_args__ = (
        Index("ix_extraction_prompt_mark_organization_id", "organization_id"),
        CheckConstraint(
            "prompt_kind IN ('extract', 'system', 'other')",
            name="ck_extraction_prompt_mark_kind",
        ),
        CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_extraction_prompt_mark_code",
        ),
        UniqueConstraint("organization_id", "id", name="uq_extraction_prompt_mark_org_id"),
        UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_extraction_prompt_mark_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_extraction_prompt_mark_org_source_ref",
        ),
    )
