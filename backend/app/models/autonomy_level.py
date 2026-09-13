import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_SNAKE = r"^[a-z][a-z0-9_]{1,31}$"


class AutonomyLevel(Base, TimestampMixin):
    __tablename__ = "autonomy_level"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_autonomy_level_org_id"),
        UniqueConstraint(
            "organization_id",
            "level_code",
            name="uq_autonomy_level_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_autonomy_level_org_source_ref",
        ),
        CheckConstraint(
            f"level_code ~ '{_SNAKE}'",
            name="ck_autonomy_level_code",
        ),
        Index("ix_autonomy_level_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: otwarty poziom autonomii tego tenanta — wiersz, nie CHECK.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    level_code: Mapped[str] = mapped_column(String(32), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
