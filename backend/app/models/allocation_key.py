import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_SNAKE = r"^[a-z][a-z0-9_]{1,31}$"


class AllocationKey(Base, TimestampMixin):
    __tablename__ = "allocation_key"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_allocation_key_org_id"),
        UniqueConstraint(
            "organization_id",
            "key_code",
            name="uq_allocation_key_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_allocation_key_org_source_ref",
        ),
        CheckConstraint(
            f"key_code ~ '{_SNAKE}'",
            name="ck_allocation_key_code",
        ),
        Index("ix_allocation_key_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: otwarty klucz alokacji tego tenanta — wiersz, nie CHECK 23.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    key_code: Mapped[str] = mapped_column(String(32), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
