import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class GdprRequest(Base, TimestampMixin):
    __tablename__ = "gdpr_request"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "app_user_id"],
            ["app_user.organization_id", "app_user.id"],
            name="fk_gdpr_request_app_user",
            ondelete="RESTRICT",
        ),
        CheckConstraint(
            "request_kind IN ('access', 'erasure')",
            name="ck_gdpr_request_kind",
        ),
        CheckConstraint(
            "status IN ('open', 'fulfilled')",
            name="ck_gdpr_request_status",
        ),
        Index(
            "uq_gdpr_request_open",
            "organization_id",
            "app_user_id",
            "request_kind",
            unique=True,
            postgresql_where=text("status = 'open'"),
        ),
        Index("ix_gdpr_request_org_user", "organization_id", "app_user_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), index=True,
    )
    app_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    request_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
