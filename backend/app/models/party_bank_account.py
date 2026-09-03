import uuid
from datetime import datetime

from sqlalchemy import (
    CHAR,
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class PartyBankAccount(Base, TimestampMixin):
    __tablename__ = "party_bank_account"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_party_bank_account_party",
            ondelete="RESTRICT",
        ),
        CheckConstraint(
            "whitelist_status IN ('pending','listed','not_listed','unavailable')",
            name="ck_party_bank_whitelist",
        ),
        UniqueConstraint("organization_id", "id", name="uq_party_bank_account_org_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Lookup IBAN nie INSERT-uje — ten wiersz jest ręczny.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False, index=True,
    )
    party_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    iban: Mapped[str] = mapped_column(String(34), nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    bank_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    whitelist_status: Mapped[str] = mapped_column(String(16), nullable=False)
    whitelist_checked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
