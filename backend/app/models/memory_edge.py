import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_KIND_SQL = (
    "edge_kind IN ("
    "'recalls','follows','blocks','cites','other'"
    ")"
)


class MemoryEdge(Base, TimestampMixin):
    __tablename__ = "memory_edge"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_memory_edge_org_id"),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_memory_edge_org_source_ref",
        ),
        CheckConstraint(_KIND_SQL, name="ck_memory_edge_kind"),
        Index("ix_memory_edge_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: znacznik krawędzi tego tenanta — HITL rodzaj, nie graf na zdarzeniach.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    edge_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
