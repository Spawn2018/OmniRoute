import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_SNAKE = r"^[a-z][a-z0-9_]{1,31}$"


class DataSource(Base, TimestampMixin):
    __tablename__ = "data_source"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_data_source_org_id"),
        UniqueConstraint(
            "organization_id",
            "source_code",
            name="uq_data_source_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_data_source_org_src",
        ),
        CheckConstraint(
            f"source_code ~ '{_SNAKE}'",
            name="ck_data_source_code",
        ),
        CheckConstraint(
            "char_length(btrim(license_label)) BETWEEN 2 AND 64",
            name="ck_data_source_license",
        ),
        CheckConstraint(
            "char_length(btrim(rights_scope)) BETWEEN 2 AND 128",
            name="ck_data_source_rights",
        ),
        Index("ix_data_source_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: slownik zrodla tego tenanta — wiersz, nie CHECK listy.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    source_code: Mapped[str] = mapped_column(String(32), nullable=False)
    license_label: Mapped[str] = mapped_column(String(64), nullable=False)
    rights_scope: Mapped[str] = mapped_column(String(128), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
    created_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
