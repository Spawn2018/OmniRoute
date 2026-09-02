from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.domain.errors import InvalidInboundMessage, InvalidSourceRef
from app.services.inbound_messages.inbound_message_service import InboundMessageService


@pytest.mark.asyncio
async def test_create_normalizes_fixture_fields() -> None:
    session = AsyncMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    service = InboundMessageService(session)

    created = await service.create_message(
        organization_id=uuid4(),
        user_id=uuid4(),
        source_ref=" fixture://inbound-mail/42 ",
        from_address="  Ops@Carrier.Example ",
        subject="  RFQ Gdynia  ",
        body_text="  1x40HC  ",
    )

    assert created.source_ref == "fixture://inbound-mail/42"
    assert created.from_address == "ops@carrier.example"
    assert created.subject == "RFQ Gdynia"
    assert created.body_text == "1x40HC"
    assert created.status == "draft"
    session.add.assert_called_once()


@pytest.mark.asyncio
async def test_create_rejects_imap_source() -> None:
    service = InboundMessageService(AsyncMock())
    with pytest.raises(InvalidInboundMessage, match="fixture"):
        await service.create_message(
            organization_id=uuid4(),
            user_id=uuid4(),
            source_ref="imap://inbox",
            from_address="ops@carrier.example",
            subject="RFQ",
            body_text="treść",
        )


@pytest.mark.asyncio
async def test_create_rejects_blank_source() -> None:
    service = InboundMessageService(AsyncMock())
    with pytest.raises(InvalidSourceRef, match="obowiązkowy"):
        await service.create_message(
            organization_id=uuid4(),
            user_id=uuid4(),
            source_ref="  ",
            from_address="ops@carrier.example",
            subject="RFQ",
            body_text="treść",
        )
