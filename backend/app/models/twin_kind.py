import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_SNAKE = r"^[a-z][a-z0-9_]{1,31}$"


class TwinKind(Base, TimestampMixin):
    __tablename__ = "twin_kind"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_twin_kind_org_id"),
        UniqueConstraint(
            "organization_id",
            "kind_code",
            name="uq_twin_kind_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_twin_kind_org_source_ref",
        ),
        CheckConstraint(
            f"kind_code ~ '{_SNAKE}'",
            name="ck_twin_kind_code",
        ),
        Index("ix_twin_kind_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: otwarty rodzaj bliźniaka tego tenanta — wiersz, nie CHECK.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    kind_code: Mapped[str] = mapped_column(String(32), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
