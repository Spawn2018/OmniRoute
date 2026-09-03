import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class NetworkMember(Base, TimestampMixin):
    __tablename__ = "network_member"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "network_id",
            "member_code",
            name="uq_network_member_org_network_code",
        ),
        CheckConstraint(
            "member_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_network_member_code_snake",
        ),
        Index("ix_network_member_org_network", "organization_id", "network_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    network_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("network.id", ondelete="RESTRICT"),
        nullable=False,
    )
    member_code: Mapped[str] = mapped_column(String(32), nullable=False)
    legal_name: Mapped[str] = mapped_column(String(128), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
