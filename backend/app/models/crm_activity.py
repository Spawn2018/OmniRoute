import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class CrmActivity(Base, TimestampMixin):
    __tablename__ = "crm_activity"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_crm_activity_org_id"),
        UniqueConstraint(
            "organization_id",
            "activity_code",
            name="uq_crm_activity_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_crm_activity_org_source_ref",
        ),
        CheckConstraint(
            "activity_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_crm_activity_code",
        ),
        CheckConstraint(
            "activity_kind IN ('call', 'meeting', 'email', 'note', 'other')",
            name="ck_crm_activity_kind",
        ),
        Index("ix_crm_activity_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: aktywność CRM tego tenanta — katalog HITL, nie pipeline.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    activity_code: Mapped[str] = mapped_column(String(32), nullable=False)
    activity_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
