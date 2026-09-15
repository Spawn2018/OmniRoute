import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class CrmLinkMark(Base, TimestampMixin):
    __tablename__ = "crm_link_mark"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_crm_link_mark_org_id"),
        UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_crm_link_mark_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_crm_link_mark_org_source_ref",
        ),
        Index("ix_crm_link_mark_organization_id", "organization_id"),
        CheckConstraint(
            "link_kind IN ('lead', 'party', 'other')",
            name="ck_crm_link_mark_kind",
        ),
        CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_crm_link_mark_code",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: link CRM tego tenanta — katalog HITL, nie FK UUID.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    mark_code: Mapped[str] = mapped_column(String(32), nullable=False)
    link_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
