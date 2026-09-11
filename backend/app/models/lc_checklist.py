import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class LcChecklist(Base, TimestampMixin):
    __tablename__ = "lc_checklist"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_lc_checklist_org_id"),
        UniqueConstraint(
            "organization_id",
            "checklist_code",
            name="uq_lc_checklist_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_lc_checklist_org_source_ref",
        ),
        CheckConstraint(
            "checklist_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_lc_checklist_code",
        ),
        CheckConstraint(
            "status_kind IN ('open', 'presented', 'closed', 'other')",
            name="ck_lc_checklist_status_kind",
        ),
        Index("ix_lc_checklist_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: checklista LC tego tenanta — katalog HITL, nie bank due.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    checklist_code: Mapped[str] = mapped_column(String(32), nullable=False)
    status_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
