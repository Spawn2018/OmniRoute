import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class RepairPlaybook(Base, TimestampMixin):
    __tablename__ = "repair_playbook"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_repair_playbook_org_id"),
        UniqueConstraint(
            "organization_id",
            "playbook_code",
            name="uq_repair_playbook_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_repair_playbook_org_source_ref",
        ),
        CheckConstraint(
            "playbook_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_repair_playbook_code",
        ),
        CheckConstraint(
            "stance_kind IN ('contain', 'reroute', 'claim', 'other')",
            name="ck_repair_playbook_stance_kind",
        ),
        Index("ix_repair_playbook_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: playbook naprawy tego tenanta — katalog HITL, nie auto-send S11.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    playbook_code: Mapped[str] = mapped_column(String(32), nullable=False)
    stance_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
