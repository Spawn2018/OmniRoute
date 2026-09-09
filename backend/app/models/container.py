import uuid

from sqlalchemy import ForeignKey, ForeignKeyConstraint, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Container(Base, TimestampMixin):
    __tablename__ = "container"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_container_shipment",
            ondelete="RESTRICT",
        ),
        Index("ix_container_org_type", "organization_id", "iso_size_type"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    container_no: Mapped[str] = mapped_column(String(11), nullable=False)
    iso_size_type: Mapped[str] = mapped_column(String(4), nullable=False)
    shipment_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    source_ref: Mapped[str] = mapped_column(Text, nullable=False)
    seal_no_1: Mapped[str | None] = mapped_column(String(32), nullable=True)
    seal_no_2: Mapped[str | None] = mapped_column(String(32), nullable=True)
    seal_no_3: Mapped[str | None] = mapped_column(String(32), nullable=True)
    vessel_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    voyage_no: Mapped[str | None] = mapped_column(String(32), nullable=True)
    remarks: Mapped[str | None] = mapped_column(String(256), nullable=True)
    cargo_description: Mapped[str | None] = mapped_column(String(256), nullable=True)
    packaging_code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    ref_1: Mapped[str | None] = mapped_column(String(64), nullable=True)
    ref_2: Mapped[str | None] = mapped_column(String(64), nullable=True)
    superseded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("container.id", ondelete="RESTRICT"),
        nullable=True,
    )
