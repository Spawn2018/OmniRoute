import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class IdpConnector(Base, TimestampMixin):
    __tablename__ = "idp_connector"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_idp_connector_org_id"),
        UniqueConstraint(
            "organization_id",
            "connector_code",
            name="uq_idp_connector_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_idp_connector_org_source_ref",
        ),
        CheckConstraint(
            "connector_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_idp_connector_code",
        ),
        CheckConstraint(
            "provider_code IN ('auth0')",
            name="ck_idp_connector_provider",
        ),
        Index("ix_idp_connector_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: fixture Auth0 tego tenanta — domena to tekst, nie live issuer.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    connector_code: Mapped[str] = mapped_column(String(32), nullable=False)
    provider_code: Mapped[str] = mapped_column(String(16), nullable=False)
    public_domain: Mapped[str | None] = mapped_column(String(253), nullable=True)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
