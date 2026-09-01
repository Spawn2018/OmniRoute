from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import NotAPostalZone, PostalRangeOverlap, UnknownPostalZone
from app.main import app
from app.models.location import Location, LocationZoneMember
from tests.http_auth import bearer_auth_headers


class AllowAllAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class StubLocationService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.zones: list[Location] = []
        self.members: list[LocationZoneMember] = []

    async def list_locations(
        self,
        *,
        kind: str | None = None,
        search: str | None = None,
    ) -> list[Location]:
        rows = [row for row in self.zones if kind is None or row.kind == kind]
        if search is None:
            return rows
        needle = search.strip().upper()
        return [row for row in rows if needle in row.name.upper()]

    async def create_zone(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        code: str,
        name: str,
    ) -> Location:
        row = Location(
            id=uuid4(),
            organization_id=organization_id,
            kind="postal_zone",
            name=name.strip(),
            code=code.strip().upper().replace(" ", "_"),
            source_ref="tenant:manual",
            created_by=user_id,
        )
        self.zones.append(row)
        return row

    async def add_zone_member(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        zone_id: UUID,
        country_code: str,
        postal_from: str,
        postal_to: str,
    ) -> LocationZoneMember:
        if not any(row.id == zone_id for row in self.zones):
            raise NotAPostalZone(f"lokalizacja {zone_id} nie jest strefą pocztową")
        lower = postal_from.replace("-", "").replace(" ", "").upper()
        upper = postal_to.replace("-", "").replace(" ", "").upper()
        if any(
            row.zone_location_id == zone_id and row.postal_from == lower for row in self.members
        ):
            raise PostalRangeOverlap(f"zakres {lower}-{upper} nachodzi na istniejący w strefie")
        row = LocationZoneMember(
            id=uuid4(),
            organization_id=organization_id,
            zone_location_id=zone_id,
            country_code=country_code.upper(),
            postal_from=lower,
            postal_to=upper,
            source_ref="tenant:manual",
            created_by=user_id,
        )
        self.members.append(row)
        return row

    async def list_zone_members(self, zone_id: UUID) -> list[LocationZoneMember]:
        return [row for row in self.members if row.zone_location_id == zone_id]

    async def resolve_postal(self, *, country_code: str, postal_code: str) -> Location:
        code = postal_code.replace("-", "").replace(" ", "").upper()
        for member in self.members:
            if member.country_code != country_code.upper():
                continue
            if len(member.postal_from) != len(code):
                continue
            if member.postal_from <= code <= member.postal_to:
                return next(row for row in self.zones if row.id == member.zone_location_id)
        raise UnknownPostalZone(f"kod {code} ({country_code.upper()}) nie trafia w żadną strefę")


@pytest.fixture
def locations_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubLocationService(object())

    def _factory(session: object) -> StubLocationService:
        return stub

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.locations.LocationService", _factory)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _create_zone(client: TestClient, headers: dict[str, str]) -> str:
    created = client.post(
        "/api/v1/locations",
        headers=headers,
        json={"code": "trojmiasto", "name": " Trójmiasto "},
    )
    assert created.status_code == 201
    body = created.json()
    assert body["kind"] == "postal_zone"
    assert body["code"] == "TROJMIASTO"
    assert body["name"] == "Trójmiasto"
    assert body["source_ref"] == "tenant:manual"
    return str(body["id"])


def test_http_creates_zone_and_lists_it(locations_client: TestClient) -> None:
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    zone_id = _create_zone(locations_client, headers)

    listed = locations_client.get(
        "/api/v1/locations",
        headers=headers,
        params={"kind": "postal_zone"},
    )
    assert listed.status_code == 200
    assert [row["id"] for row in listed.json()] == [zone_id]
    assert listed.json()[0]["organization_id"] == str(org_id)


def test_http_adds_a_range_and_resolves_a_postal_code(locations_client: TestClient) -> None:
    headers = bearer_auth_headers()
    zone_id = _create_zone(locations_client, headers)

    added = locations_client.post(
        f"/api/v1/locations/{zone_id}/members",
        headers=headers,
        json={"country_code": "pl", "postal_from": "81-000", "postal_to": "81-999"},
    )
    assert added.status_code == 201
    assert added.json()["postal_from"] == "81000"

    members = locations_client.get(f"/api/v1/locations/{zone_id}/members", headers=headers)
    assert members.status_code == 200
    assert [row["postal_to"] for row in members.json()] == ["81999"]

    resolved = locations_client.get(
        "/api/v1/locations/resolve",
        headers=headers,
        params={"country_code": "PL", "postal_code": "81-198"},
    )
    assert resolved.status_code == 200
    assert resolved.json()["id"] == zone_id


def test_http_resolve_rejects_a_code_outside_every_range(locations_client: TestClient) -> None:
    headers = bearer_auth_headers()
    zone_id = _create_zone(locations_client, headers)
    locations_client.post(
        f"/api/v1/locations/{zone_id}/members",
        headers=headers,
        json={"country_code": "PL", "postal_from": "81000", "postal_to": "81999"},
    )

    response = locations_client.get(
        "/api/v1/locations/resolve",
        headers=headers,
        params={"country_code": "PL", "postal_code": "00-950"},
    )
    assert response.status_code == 400
    assert "nie trafia" in response.json()["detail"]


def test_http_overlapping_range_comes_back_as_a_domain_refusal(
    locations_client: TestClient,
) -> None:
    headers = bearer_auth_headers()
    zone_id = _create_zone(locations_client, headers)
    locations_client.post(
        f"/api/v1/locations/{zone_id}/members",
        headers=headers,
        json={"country_code": "PL", "postal_from": "81000", "postal_to": "81999"},
    )

    conflicting = locations_client.post(
        f"/api/v1/locations/{zone_id}/members",
        headers=headers,
        json={"country_code": "PL", "postal_from": "81-000", "postal_to": "81-999"},
    )
    assert conflicting.status_code == 400
    assert "nachodzi" in conflicting.json()["detail"]


def test_http_range_on_unknown_zone_is_refused(locations_client: TestClient) -> None:
    response = locations_client.post(
        f"/api/v1/locations/{uuid4()}/members",
        headers=bearer_auth_headers(),
        json={"country_code": "PL", "postal_from": "81000", "postal_to": "81999"},
    )
    assert response.status_code == 400
    assert "strefą pocztową" in response.json()["detail"]
