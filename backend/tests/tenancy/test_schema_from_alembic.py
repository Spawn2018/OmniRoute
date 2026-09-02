from pathlib import Path

import pytest
from sqlalchemy import text

_ROOT = Path(__file__).resolve().parents[3]
_CONFTEST = _ROOT / "backend" / "tests" / "conftest.py"
_ALEMBIC_ENV = _ROOT / "backend" / "alembic" / "env.py"


def test_engine_fixture_upgrades_test_schema_through_alembic() -> None:
    source = _CONFTEST.read_text(encoding="utf-8")
    assert "Base.metadata.create_all" not in source
    assert "_apply_postal_zone_ddl" not in source
    assert "async def _apply_rls_policies" not in source
    assert "command.upgrade" in source


def test_alembic_env_honours_test_database_url_override() -> None:
    source = _ALEMBIC_ENV.read_text(encoding="utf-8")
    assert "ALEMBIC_DATABASE_URL" in source


@pytest.mark.integration
@pytest.mark.asyncio
async def test_test_schema_revision_matches_alembic_head(engine) -> None:
    from alembic.config import Config
    from alembic.script import ScriptDirectory

    cfg = Config(str(_ROOT / "backend" / "alembic.ini"))
    cfg.set_main_option("script_location", str(_ROOT / "backend" / "alembic"))
    head = ScriptDirectory.from_config(cfg).get_current_head()
    async with engine.connect() as conn:
        current = (
            await conn.execute(text("SELECT version_num FROM alembic_version"))
        ).scalar_one()
    assert current == head


@pytest.mark.integration
@pytest.mark.asyncio
async def test_current_rate_index_exists_on_test_schema(engine) -> None:
    async with engine.connect() as conn:
        name = (
            await conn.execute(
                text(
                    "SELECT indexname FROM pg_indexes "
                    "WHERE tablename = 'rate_line' "
                    "AND indexname = 'ix_rate_line_current_charge_code'"
                )
            )
        ).scalar_one_or_none()
    assert name == "ix_rate_line_current_charge_code"
