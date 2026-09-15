import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ComplianceProgramMark(Base, TimestampMixin):
    __tablename__ = "compliance_program_mark"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "id",
            name="uq_compliance_program_mark_org_id",
        ),
        UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_compliance_program_mark_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_compliance_program_mark_org_src",
        ),
        CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_compliance_program_mark_code",
        ),
        CheckConstraint(
            "program_kind IN ('draft', 'review', 'signed', 'exempt', 'other')",
            name="ck_compliance_program_mark_kind",
        ),
        Index("ix_compliance_program_mark_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: stancja programu zgodnosci — HITL, nie bajty PDF / nie U-art50 przebudowa.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
    )
    program_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    mark_code: Mapped[str] = mapped_column(String(32), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
