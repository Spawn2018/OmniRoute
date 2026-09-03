from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.domain.errors import InvalidOrganizationSetting
from app.models.organization_setting import OrganizationSetting
from app.services.extraction import extraction_service as extraction_module
from app.services.organization_settings.organization_setting_service import (
    OrganizationSettingService,
)


def _row(*, key: str = "default_currency", value: str = "EUR") -> OrganizationSetting:
    return OrganizationSetting(
        id=uuid4(),
        organization_id=uuid4(),
        setting_key=key,
        setting_value=value,
    )


@pytest.mark.asyncio
async def test_upsert_stores_default_currency() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    session.add = MagicMock()
    session.flush = AsyncMock()
    service = OrganizationSettingService(session)

    stored = await service.upsert_setting(
        organization_id=uuid4(),
        user_id=uuid4(),
        setting_key=" default_currency ",
        setting_value="eur",
    )

    assert stored.setting_key == "default_currency"
    assert stored.setting_value == "EUR"
    session.add.assert_called_once()


@pytest.mark.asyncio
async def test_upsert_updates_existing_row() -> None:
    existing = _row(value="USD")
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=existing)
    session.flush = AsyncMock()
    service = OrganizationSettingService(session)

    stored = await service.upsert_setting(
        organization_id=existing.organization_id,
        user_id=uuid4(),
        setting_key="default_currency",
        setting_value="PLN",
    )

    assert stored.id == existing.id
    assert stored.setting_value == "PLN"
    session.add.assert_not_called()


@pytest.mark.asyncio
async def test_upsert_rejects_unknown_key() -> None:
    service = OrganizationSettingService(AsyncMock())
    with pytest.raises(InvalidOrganizationSetting, match="allowlist"):
        await service.upsert_setting(
            organization_id=uuid4(),
            user_id=uuid4(),
            setting_key="loose_flag",
            setting_value="yes",
        )


@pytest.mark.asyncio
async def test_upsert_rejects_secret_key() -> None:
    service = OrganizationSettingService(AsyncMock())
    with pytest.raises(InvalidOrganizationSetting, match="sekret"):
        await service.upsert_setting(
            organization_id=uuid4(),
            user_id=uuid4(),
            setting_key="openai_api_key",
            setting_value="sk-test",
        )


@pytest.mark.asyncio
async def test_upsert_rejects_invalid_currency() -> None:
    service = OrganizationSettingService(AsyncMock())
    with pytest.raises(InvalidOrganizationSetting, match="ISO"):
        await service.upsert_setting(
            organization_id=uuid4(),
            user_id=uuid4(),
            setting_key="default_currency",
            setting_value="euro",
        )


@pytest.mark.asyncio
async def test_list_returns_repository_rows() -> None:
    session = AsyncMock()
    row = _row()
    scalars = MagicMock()
    scalars.all.return_value = [row]
    session.scalars = AsyncMock(return_value=scalars)
    service = OrganizationSettingService(session)

    listed = await service.list_settings()
    assert listed == [row]


@pytest.mark.asyncio
async def test_upsert_stores_prefix_and_template() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    session.add = MagicMock()
    session.flush = AsyncMock()
    service = OrganizationSettingService(session)
    prefix = await service.upsert_setting(
        organization_id=uuid4(),
        user_id=uuid4(),
        setting_key="quotation_number_prefix",
        setting_value="or-q",
    )
    assert prefix.setting_key == "quotation_number_prefix"
    assert prefix.setting_value == "OR-Q"
    template = await service.upsert_setting(
        organization_id=uuid4(),
        user_id=uuid4(),
        setting_key="quotation_print_template",
        setting_value="plain",
    )
    assert template.setting_value == "plain"


@pytest.mark.asyncio
async def test_get_setting_returns_none_when_missing() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    found = await OrganizationSettingService(session).get_setting("quotation_number_prefix")
    assert found is None


def test_settings_and_quote_services_stay_apart() -> None:
    root = Path(__file__).resolve().parents[2]
    settings = (
        root / "app" / "services" / "organization_settings" / "organization_setting_service.py"
    ).read_text(encoding="utf-8")
    quotes = (root / "app" / "services" / "quotations" / "quotation_service.py").read_text(
        encoding="utf-8",
    )
    assert "quotations" not in settings
    assert "organization_settings" not in quotes
    assert "quotation_number_prefix" not in quotes


def test_extraction_service_does_not_import_organization_settings() -> None:
    source = Path(extraction_module.__file__).read_text(encoding="utf-8")
    assert "from app.services.organization_settings" not in source
    assert "from app.repositories.organization_settings" not in source
    assert "from app.models.organization_setting" not in source
