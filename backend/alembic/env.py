"""Generic single-database configuration."""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import settings
from app.models.app_user import AppUser  # noqa: F401
from app.models.base import Base
from app.models.organization import Organization  # noqa: F401
from app.models.charge_code import ChargeCode  # noqa: F401
from app.models.rate_line import RateLine  # noqa: F401
from app.models.charge import Charge  # noqa: F401
from app.models.quotation import Quotation  # noqa: F401
from app.models.organization_setting import OrganizationSetting  # noqa: F401
from app.models.extraction_draft import ExtractionDraft  # noqa: F401
from app.models.table_view import TableView  # noqa: F401
from app.models.port import Port  # noqa: F401

config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url_sync)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
