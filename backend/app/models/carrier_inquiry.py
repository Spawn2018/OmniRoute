import uuid

from sqlalchemy import CheckConstraint, ForeignKey, ForeignKeyConstraint, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class CarrierInquiry(Base, TimestampMixin):
    __tablename__ = "carrier_inquiry"
    __table_args__ = (
        CheckConstraint("status = 'draft'", name="ck_carrier_inquiry_status_draft"),
        ForeignKeyConstraint(
            ["organization_id", "network_member_id"],
            ["network_member.organization_id", "network_member.id"],
            name="fk_carrier_inquiry_network_member",
            ondelete="RESTRICT",
        ),
        Index("ix_carrier_inquiry_org_member", "organization_id", "network_member_id"),
        Index("ix_carrier_inquiry_org_created", "organization_id", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    network_member_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
    status: Mapped[str] = mapped_column(String(8), nullable=False)
