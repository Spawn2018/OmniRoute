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


class PalletLedger(Base, TimestampMixin):
    __tablename__ = "pallet_ledger"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_pallet_ledger_party",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("organization_id", "id", name="uq_pallet_ledger_org_id"),
        UniqueConstraint(
            "organization_id",
            "movement_code",
            name="uq_pallet_ledger_org_code",
        ),
        CheckConstraint(
            "pallet_kind IN ('chep','lpr','epal')",
            name="ck_pallet_ledger_kind",
        ),
        CheckConstraint(
            "movement_code ~ '^[a-z][a-z0-9_]{0,63}$'",
            name="ck_pallet_ledger_code",
        ),
        Index("ix_pallet_ledger_org_party", "organization_id", "party_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: ruch palet i kontrahent jednego tenanta — złożone FK nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    party_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    movement_code: Mapped[str] = mapped_column(String(64), nullable=False)
    pallet_kind: Mapped[str] = mapped_column(String(8), nullable=False)
    delta_count: Mapped[int] = mapped_column(Integer, nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
