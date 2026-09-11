import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class EdiMapMark(Base, TimestampMixin):
    __tablename__ = "edi_map_mark"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_edi_map_mark_org_id"),
        UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_edi_map_mark_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_edi_map_mark_org_source_ref",
        ),
        CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_edi_map_mark_code",
        ),
        CheckConstraint(
            "map_kind IN ('field_map', 'segment', 'other')",
            name="ck_edi_map_mark_map_kind",
        ),
        Index("ix_edi_map_mark_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: mapa pól EDI tego tenanta — katalog HITL, nie silent write.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    mark_code: Mapped[str] = mapped_column(String(32), nullable=False)
    map_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
