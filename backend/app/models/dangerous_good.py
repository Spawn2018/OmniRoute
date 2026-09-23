import uuid

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, String, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_IMDG = (
    "'1','1.1','1.2','1.3','1.4','1.5','1.6',"
    "'2.1','2.2','2.3','3','4.1','4.2','4.3',"
    "'5.1','5.2','6.1','6.2','7','8','9'"
)


class DangerousGood(Base, TimestampMixin):
    __tablename__ = "dangerous_good"
    __table_args__ = (
        UniqueConstraint("organization_id", "un_number", name="uq_dangerous_good_org_un"),
        UniqueConstraint("organization_id", "id", name="uq_dangerous_good_org_id"),
        CheckConstraint("un_number ~ '^[0-9]{4}$'", name="ck_dangerous_good_un_digits"),
        CheckConstraint(f"imdg_class IN ({_IMDG})", name="ck_dangerous_good_imdg_class"),
        CheckConstraint(
            "adr_tunnel_code IN ('A', 'B', 'C', 'D', 'E')",
            name="ck_dangerous_good_adr_tunnel",
        ),
        CheckConstraint(
            "segregation_group IN ('none','sg1','sg2','sg3','sg4','sg5','sg6',"
            "'sg7','sg8','sg9','sg10','sg11','sg12','sg13','sg14','sg15',"
            "'sg16','sg17','sg18')",
            name="ck_dangerous_good_segregation_group",
        ),
        CheckConstraint(
            "packing_group IN ('I', 'II', 'III')",
            name="ck_dangerous_good_packing_group",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False, index=True)
    un_number: Mapped[str] = mapped_column(String(4), nullable=False)
    imdg_class: Mapped[str] = mapped_column(String(3), nullable=False)
    adr_tunnel_code: Mapped[str] = mapped_column(String(1), nullable=False)
    segregation_group: Mapped[str] = mapped_column(String(8), nullable=False)
    packing_group: Mapped[str] = mapped_column(String(3), nullable=False)
    marine_pollutant: Mapped[bool] = mapped_column(Boolean, nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    aliases: Mapped[list[str]] = mapped_column(
        ARRAY(Text()), nullable=False, server_default=text("'{}'"))
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
