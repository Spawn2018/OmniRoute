import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class LocalChargeBindMark(Base, TimestampMixin):
    __tablename__ = "local_charge_bind_mark"
    __table_args__ = (
        CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_local_charge_bind_mark_code",
        ),
        CheckConstraint(
            "bind_kind IN ('charge', 'quote', 'other')",
            name="ck_local_charge_bind_mark_kind",
        ),
        UniqueConstraint(
            "organization_id", "id", name="uq_local_charge_bind_mark_org_id"
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_local_charge_bind_mark_org_source_ref",
        ),
        UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_local_charge_bind_mark_org_code",
        ),
        Index("ix_local_charge_bind_mark_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: HITL stance wiązania dopłaty lokalnej — nie FK UUID / matching SQL.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    mark_code: Mapped[str] = mapped_column(String(32), nullable=False)
    bind_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
