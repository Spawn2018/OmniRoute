import uuid

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class CarrierProfile(Base, TimestampMixin):
    __tablename__ = "carrier_profile"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_carrier_profile_party",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("organization_id", "party_id", name="uq_carrier_profile_org_party"),
        CheckConstraint(
            "api_adapter IN ('none','maersk','hapag','cma','msc')",
            name="ck_carrier_profile_adapter",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Żywe HTTP armatorskie poza tym plasterem.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False, index=True,
    )
    party_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    scac_code: Mapped[str | None] = mapped_column(String(8), nullable=True)
    is_nvocc: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    rate_source_email: Mapped[str | None] = mapped_column(String(256), nullable=True)
    api_adapter: Mapped[str] = mapped_column(String(16), nullable=False, default="none")
    dcsa_tnt_version: Mapped[str | None] = mapped_column(String(16), nullable=True)
