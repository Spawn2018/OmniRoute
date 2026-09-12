import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class OceanAllianceMark(Base, TimestampMixin):
    __tablename__ = "ocean_alliance_mark"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_ocean_alliance_mark_org_id"),
        UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_ocean_alliance_mark_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_ocean_alliance_mark_org_source_ref",
        ),
        CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_ocean_alliance_mark_code",
        ),
        CheckConstraint(
            "ocean_kind IN ('alliance', 'feeder', 'slot', 'other')",
            name="ck_ocean_alliance_mark_ocean_kind",
        ),
        Index("ix_ocean_alliance_mark_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: znacznik ocean alliance tego tenanta — katalog HITL, nie ocean live API.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    mark_code: Mapped[str] = mapped_column(String(32), nullable=False)
    ocean_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
