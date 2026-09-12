import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class NamedPlaceMark(Base, TimestampMixin):
    __tablename__ = "named_place_mark"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_named_place_mark_org_id"),
        UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_named_place_mark_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_named_place_mark_org_source_ref",
        ),
        CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_named_place_mark_code",
        ),
        CheckConstraint(
            "terms_version IN ('2020', '2010')",
            name="ck_named_place_mark_terms_version",
        ),
        CheckConstraint(
            "btrim(named_place) <> ''",
            name="ck_named_place_mark_place_nonempty",
        ),
        Index("ix_named_place_mark_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: znacznik miejsca nazwanego tego tenanta — katalog HITL, nie cytat ICC.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    mark_code: Mapped[str] = mapped_column(String(32), nullable=False)
    named_place: Mapped[str] = mapped_column(String(128), nullable=False)
    terms_version: Mapped[str] = mapped_column(String(4), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
