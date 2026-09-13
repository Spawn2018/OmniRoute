import uuid

from sqlalchemy import ForeignKey, ForeignKeyConstraint, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class TwinMark(Base, TimestampMixin):
    __tablename__ = "twin_mark"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_twin_mark_org_id"),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_twin_mark_org_source_ref",
        ),
        ForeignKeyConstraint(
            ["organization_id", "twin_kind"],
            ["twin_kind.organization_id", "twin_kind.kind_code"],
            name="fk_twin_mark_kind",
            ondelete="RESTRICT",
        ),
        Index("ix_twin_mark_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: znacznik bliźniaka tego tenanta — HITL rodzaj, nie fizyka.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    twin_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
