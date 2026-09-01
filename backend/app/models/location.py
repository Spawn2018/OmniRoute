import uuid
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_KIND_SHAPE = """
CASE kind
  WHEN 'unlocode' THEN port_id IS NOT NULL
    AND city IS NULL AND address_line IS NULL AND postal_code IS NULL
  WHEN 'postal_zone' THEN code IS NOT NULL AND port_id IS NULL
  WHEN 'address' THEN country_code IS NOT NULL
    AND city IS NOT NULL AND address_line IS NOT NULL AND port_id IS NULL
END
"""


class Location(Base, TimestampMixin):
    __tablename__ = "location"
    __table_args__ = (
        # Kolumna złożona, żeby baza odrzuciła wskazanie portu innego tenanta.
        ForeignKeyConstraint(
            ["organization_id", "port_id"],
            ["port.organization_id", "port.id"],
            name="fk_location_port",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("organization_id", "id", name="uq_location_org_id"),
        CheckConstraint(
            "kind IN ('unlocode', 'postal_zone', 'address')",
            name="ck_location_kind",
        ),
        CheckConstraint(_KIND_SHAPE, name="ck_location_kind_shape"),
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
    kind: Mapped[str] = mapped_column(String(16), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    port_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    country_code: Mapped[str | None] = mapped_column(String(2), nullable=True)
    city: Mapped[str | None] = mapped_column(String(128), nullable=True)
    address_line: Mapped[str | None] = mapped_column(String(256), nullable=True)
    postal_code: Mapped[str | None] = mapped_column(String(16), nullable=True)
    lat: Mapped[Decimal | None] = mapped_column(Numeric(8, 6), nullable=True)
    lng: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)


class LocationZoneMember(Base, TimestampMixin):
    """Zakres kodów pocztowych w strefie taryfowej tenanta.

    Kolumna `postal_span` i wykluczanie nakładek żyją wyłącznie w bazie
    (migracja 013): typ `postal_range` z kolacją "C" nie ma odpowiednika w ORM,
    a zapytania i tak liczy Postgres.
    """

    __tablename__ = "location_zone_member"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "zone_location_id"],
            ["location.organization_id", "location.id"],
            name="fk_location_zone_member_zone",
            ondelete="RESTRICT",
        ),
        CheckConstraint(
            "length(postal_from) = length(postal_to)",
            name="ck_location_zone_member_equal_length",
        ),
        CheckConstraint(
            'postal_from COLLATE "C" <= postal_to COLLATE "C"',
            name="ck_location_zone_member_ordered",
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
    zone_location_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
    )
    country_code: Mapped[str] = mapped_column(String(2), nullable=False)
    postal_from: Mapped[str] = mapped_column(Text, nullable=False)
    postal_to: Mapped[str] = mapped_column(Text, nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
