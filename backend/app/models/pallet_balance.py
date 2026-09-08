import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class PalletBalance(Base, TimestampMixin):
    __tablename__ = "pallet_balance"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_pallet_balance_party",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("organization_id", "id", name="uq_pallet_balance_org_id"),
        CheckConstraint(
            "pallet_kind IN ('chep','lpr')",
            name="ck_pallet_balance_kind",
        ),
        CheckConstraint("unit_count >= 0", name="ck_pallet_balance_count"),
        Index("ix_pallet_balance_org_party", "organization_id", "party_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: saldo palet i kontrahent jednego tenanta — złożone FK nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    party_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    pallet_kind: Mapped[str] = mapped_column(String(8), nullable=False)
    unit_count: Mapped[int] = mapped_column(Integer, nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
