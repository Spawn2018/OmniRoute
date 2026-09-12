import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class IntegrationHubMark(Base, TimestampMixin):
    __tablename__ = "integration_hub_mark"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_integration_hub_mark_org_id"),
        UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_integration_hub_mark_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_integration_hub_mark_org_source_ref",
        ),
        CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_integration_hub_mark_code",
        ),
        CheckConstraint(
            "hub_kind IN ('rest', 'soap', 'edi', 'sftp', 'other')",
            name="ck_integration_hub_mark_hub_kind",
        ),
        Index("ix_integration_hub_mark_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: znacznik Integration Hub tego tenanta — katalog HITL, nie live HTTP hubu.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    mark_code: Mapped[str] = mapped_column(String(32), nullable=False)
    hub_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
