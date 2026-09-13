import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import BigInteger, Date, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class VersionWindow(Base):
    __tablename__ = "version_window"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )
    model_version: Mapped[str] = mapped_column(String(32), primary_key=True)
    created_on: Mapped[date] = mapped_column(Date, primary_key=True)
    pair_count: Mapped[int] = mapped_column(BigInteger, nullable=False)
    avg_mae: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    avg_crps: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
