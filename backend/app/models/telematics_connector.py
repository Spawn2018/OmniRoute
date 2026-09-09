import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_KIND_SQL = "observation_kind IN ('omni_telematic','external_api')"
_PROVIDER_SQL = "provider_code IN ('gbox','ikol','flotis','wialon','other')"


class TelematicsConnector(Base, TimestampMixin):
    __tablename__ = "telematics_connector"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_telematics_connector_org_id"),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_telematics_connector_org_source_ref",
        ),
        CheckConstraint(_KIND_SQL, name="ck_telematics_connector_kind"),
        CheckConstraint(_PROVIDER_SQL, name="ck_telematics_connector_provider"),
        Index("ix_telematics_connector_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: konektor GPS tego tenanta — HITL reżim, nie poll.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    observation_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    provider_code: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
