import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class StopGroup(Base, TimestampMixin):
    __tablename__ = "stop_group"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_stop_group_shipment",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("organization_id", "id", name="uq_stop_group_org_id"),
        UniqueConstraint(
            "organization_id",
            "shipment_id",
            "group_code",
            name="uq_stop_group_org_shipment_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_stop_group_org_source",
        ),
        CheckConstraint(
            "group_code ~ '^[A-Za-z0-9_-]{2,32}$'",
            name="ck_stop_group_group_code",
        ),
        Index("ix_stop_group_org_shipment", "organization_id", "shipment_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: grupa i zlecenie jednego tenanta — złożone FK nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    shipment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    group_code: Mapped[str] = mapped_column(String(32), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
