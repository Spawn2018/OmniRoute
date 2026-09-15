import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class KpiDefinitionMark(Base, TimestampMixin):
    __tablename__ = "kpi_definition_mark"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "id",
            name="uq_kpi_definition_mark_org_id",
        ),
        UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_kpi_definition_mark_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_kpi_definition_mark_org_src",
        ),
        CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_kpi_definition_mark_code",
        ),
        CheckConstraint(
            "kpi_kind IN ('otd', 'otif', 'custom', 'other')",
            name="ck_kpi_definition_mark_kind",
        ),
        Index("ix_kpi_definition_mark_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: etykieta definicji KPI — HITL, nie wzór KPI.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
    )
    kpi_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    mark_code: Mapped[str] = mapped_column(String(32), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
