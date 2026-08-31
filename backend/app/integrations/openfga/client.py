from typing import Protocol
from uuid import UUID

from openfga_sdk import ClientConfiguration, CreateStoreRequest, OpenFgaClient
from openfga_sdk.client.models import ClientCheckRequest, ClientTuple, ClientWriteRequest

from app.core.config import settings
from app.integrations.openfga.model import authorization_model_request


class AuthzChecker(Protocol):
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        ...


class OpenFgaAuthz:
    def __init__(self, client: OpenFgaClient) -> None:
        self._client = client

    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        response = await self._client.check(
            ClientCheckRequest(
                user=f"user:{user_id}",
                relation=relation,
                object=f"{object_type}:{object_id}",
            ),
        )
        return bool(response.allowed)

    async def write_member(self, *, user_id: UUID, organization_id: UUID) -> None:
        await self._client.write(
            ClientWriteRequest(
                writes=[
                    ClientTuple(
                        user=f"user:{user_id}",
                        relation="member",
                        object=f"organization:{organization_id}",
                    ),
                ],
            ),
        )


async def build_openfga_client() -> OpenFgaClient:
    configuration = ClientConfiguration(
        api_url=settings.openfga_api_url,
        store_id=settings.openfga_store_id or None,
        authorization_model_id=settings.openfga_model_id or None,
    )
    return OpenFgaClient(configuration)


async def bootstrap_store(client: OpenFgaClient, store_name: str = "omniroute") -> tuple[str, str]:
    """Tworzy store + model — używane w testach i lokalnym setupie."""
    store = await client.create_store(CreateStoreRequest(name=store_name))
    store_id = store.id
    assert store_id is not None
    client.set_store_id(store_id)
    model = await client.write_authorization_model(authorization_model_request())
    model_id = model.authorization_model_id
    assert model_id is not None
    client.set_authorization_model_id(model_id)
    return store_id, model_id
