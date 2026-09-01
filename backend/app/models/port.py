import uuid
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.wpi import HARBOR_SIZES, HARBOR_TYPES, SHELTERS, sql_in_list
from app.models.base import Base, TimestampMixin

_HARBOR_SIZE_SQL = f"harbor_size IS NULL OR harbor_size IN ({sql_in_list(HARBOR_SIZES)})"
_HARBOR_TYPE_SQL = f"harbor_type IS NULL OR harbor_type IN ({sql_in_list(HARBOR_TYPES)})"
_SHELTER_SQL = f"shelter IS NULL OR shelter IN ({sql_in_list(SHELTERS)})"


class Port(Base, TimestampMixin):
    __tablename__ = "port"
    __table_args__ = (
        UniqueConstraint("organization_id", "unlocode", name="uq_port_org_unlocode"),
        # Nośnik dla FK złożonego z location i terminal — bez niego port innego tenanta przeszedłby.
        UniqueConstraint("organization_id", "id", name="uq_port_org_id"),
        CheckConstraint(_HARBOR_SIZE_SQL, name="ck_port_harbor_size"),
        CheckConstraint(_HARBOR_TYPE_SQL, name="ck_port_harbor_type"),
        CheckConstraint(_SHELTER_SQL, name="ck_port_shelter"),
        Index(
            "uq_port_org_wpi_number",
            "organization_id",
            "wpi_number",
            unique=True,
            postgresql_where=text("wpi_number IS NOT NULL"),
        ),
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
    wpi_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    harbor_size: Mapped[str | None] = mapped_column(String(16), nullable=True)
    harbor_type: Mapped[str | None] = mapped_column(String(32), nullable=True)
    shelter: Mapped[str | None] = mapped_column(String(16), nullable=True)
    channel_depth_m: Mapped[Decimal | None] = mapped_column(Numeric(6, 1), nullable=True)
    cargo_pier_depth_m: Mapped[Decimal | None] = mapped_column(Numeric(6, 1), nullable=True)
    wpi_source_ref: Mapped[str | None] = mapped_column(String(256), nullable=True)
