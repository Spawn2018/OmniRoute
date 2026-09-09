import uuid

from sqlalchemy import ForeignKey, ForeignKeyConstraint, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class KreptdLicence(Base, TimestampMixin):
    __tablename__ = "kreptd_licence"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_kreptd_licence_org_id"),
        UniqueConstraint(
            "organization_id",
            "party_id",
            name="uq_kreptd_licence_org_party",
        ),
        ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_kreptd_licence_party",
            ondelete="RESTRICT",
        ),
        Index("ix_kreptd_licence_org_licence", "organization_id", "licence_no"),
        Index("ix_kreptd_licence_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: numer KREPTD i kontrahent tego tenanta — tekst licencji nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    party_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    licence_no: Mapped[str] = mapped_column(String(64), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
