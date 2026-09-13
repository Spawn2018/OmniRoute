import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class CircleSimPair(Base):
    __tablename__ = "circle_sim_pair"

    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    left_sim_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    right_sim_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    left_sim_code: Mapped[str] = mapped_column(String(32), nullable=False)
    right_sim_code: Mapped[str] = mapped_column(String(32), nullable=False)
    unload_unlocode: Mapped[str] = mapped_column(String(5), nullable=False)
    load_unlocode: Mapped[str] = mapped_column(String(5), nullable=False)
