import uuid

from sqlalchemy import CheckConstraint, ForeignKey, String, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class CommodityCode(Base, TimestampMixin):
    __tablename__ = "commodity_code"
    __table_args__ = (
        UniqueConstraint("organization_id", "code", name="uq_commodity_code_org_code"),
        CheckConstraint("code ~ '^[0-9]{4,10}$'", name="ck_commodity_code_digits"),
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
    code: Mapped[str] = mapped_column(String(10), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    aliases: Mapped[list[str]] = mapped_column(
        ARRAY(Text()),
        nullable=False,
        server_default=text("'{}'"),
    )
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
