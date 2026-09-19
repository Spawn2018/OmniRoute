import uuid
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Resource(Base, TimestampMixin):
    __tablename__ = "resource"
    __table_args__ = (
        CheckConstraint(
            "resource_kind IN ('vehicle', 'driver', 'trailer')",
            name="ck_resource_kind",
        ),
        UniqueConstraint("organization_id", "id", name="uq_resource_org_id"),
        Index("ix_resource_org_kind", "organization_id", "resource_kind"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    resource_kind: Mapped[str] = mapped_column(String(8), nullable=False)
    display_name: Mapped[str] = mapped_column(String(64), nullable=False)
    registration_no: Mapped[str | None] = mapped_column(String(32), nullable=True)
    inventory_no: Mapped[str | None] = mapped_column(String(32), nullable=True)
    adr_certified: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    capacity_kg: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    capacity_ldm: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    capacity_m3: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    source_ref: Mapped[str] = mapped_column(Text, nullable=False)
    superseded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("resource.id", ondelete="RESTRICT"),
        nullable=True,
    )
