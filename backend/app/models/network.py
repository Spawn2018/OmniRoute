import uuid

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, String, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Network(Base, TimestampMixin):
    __tablename__ = "network"
    __table_args__ = (
        UniqueConstraint("organization_id", "code", name="uq_network_org_code"),
        CheckConstraint("code ~ '^[a-z][a-z0-9_]{1,31}$'", name="ck_network_code_snake"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(32), nullable=False)
    is_global: Mapped[bool] = mapped_column(Boolean(), nullable=False, server_default=text("false"))
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    website: Mapped[str | None] = mapped_column(String(256), nullable=True)
    region_scope: Mapped[str | None] = mapped_column(String(64), nullable=True)
    aliases: Mapped[list[str]] = mapped_column(
        ARRAY(Text()), nullable=False, server_default=text("'{}'"))
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
