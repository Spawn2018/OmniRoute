import uuid
from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, Numeric, String, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Port(Base, TimestampMixin):
    __tablename__ = "port"
    __table_args__ = (
        UniqueConstraint("organization_id", "unlocode", name="uq_port_org_unlocode"),
        # Nośnik dla FK złożonego z location — bez niego port innego tenanta przeszedłby.
        UniqueConstraint("organization_id", "id", name="uq_port_org_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    unlocode: Mapped[str] = mapped_column(String(5), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    country_code: Mapped[str] = mapped_column(String(2), nullable=False)
    lat: Mapped[Decimal | None] = mapped_column(Numeric(8, 6), nullable=True)
    lng: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
    is_seaport: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )
    function_flags: Mapped[list[str]] = mapped_column(
        ARRAY(Text()),
        nullable=False,
        server_default=text("'{}'"),
    )
    aliases: Mapped[list[str]] = mapped_column(
        ARRAY(Text()),
        nullable=False,
        server_default=text("'{}'"),
    )
    is_official: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true"),
    )
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
