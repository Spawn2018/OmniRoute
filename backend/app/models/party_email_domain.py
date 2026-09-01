import uuid

from sqlalchemy import ForeignKey, ForeignKeyConstraint, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class PartyEmailDomain(Base, TimestampMixin):
    __tablename__ = "party_email_domain"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_party_email_domain_party",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("organization_id", "domain", name="uq_party_email_domain_org_domain"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Unikalność domeny jest per tenant, nie per party.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False, index=True,
    )
    party_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    domain: Mapped[str] = mapped_column(String(256), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
