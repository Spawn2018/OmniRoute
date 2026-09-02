from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.domain.errors import InvalidInboundMessage, InvalidSourceRef
from app.models.inbound_message import InboundMessage
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
    assert created.party_id is None
    session.add.assert_called_once()


@pytest.mark.asyncio
async def test_attach_party_sets_party_id() -> None:
    row = InboundMessage(
        id=uuid4(),
        organization_id=uuid4(),
        source_ref="fixture://inbound-mail/1",
        from_address="ops@carrier.example",
        subject="RFQ",
        body_text="treść",
        status="draft",
    )
    session = AsyncMock()
    session.get = AsyncMock(return_value=row)
    session.add = MagicMock()
    session.flush = AsyncMock()
    service = InboundMessageService(session)
    party_id = uuid4()
    attached = await service.attach_party(row.id, party_id)
    assert attached.party_id == party_id


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
