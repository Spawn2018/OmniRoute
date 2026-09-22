from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import InvalidPalletLedger, PalletLedgerConflict, ResourceNotFound
from app.domain.pallet_ledger import (
    require_delta_count,
    require_ledger_pallet_kind,
    require_movement_code,
)
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.pallet_ledger import PalletLedger
from app.models.party import Party
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]


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


class StubPartyService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: Party | None = None

    async def get_party(self, party_id: UUID) -> Party:
        if self.row is None or self.row.id != party_id:
            raise ResourceNotFound("nieznany kontrahent")
        return self.row


class StubLedgerService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[PalletLedger] = []

    async def list_movements(self) -> list[PalletLedger]:
        return list(self.rows)

    async def record_movement(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: object,
        movement_code: object,
        pallet_kind: object,
        delta_count: object,
        source_ref: object,
    ) -> PalletLedger:
        code = require_movement_code(movement_code)
        if any(row.movement_code == code for row in self.rows):
            raise PalletLedgerConflict("ten kod ruchu palet już istnieje")
        if type(source_ref) is not str or source_ref.strip() == "":
            raise InvalidPalletLedger("wskazanie zapisu ruchu palet")
        row = PalletLedger(
            id=uuid4(),
            organization_id=organization_id,
            party_id=party_id,  # type: ignore[arg-type]
            movement_code=code,
            pallet_kind=require_ledger_pallet_kind(pallet_kind),
            delta_count=require_delta_count(delta_count),
            source_ref=source_ref.strip(),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    parties = StubPartyService(object())
    ledgers = StubLedgerService(object())
    counterpart = Party(
        id=uuid4(),
        organization_id=uuid4(),
        legal_name="Agent",
        country_code="PL",
        roles=["agent"],
        source_ref="tenant:manual",
        is_active=True,
        created_by=uuid4(),
    )
    parties.row = counterpart

    def _parties(_session: object) -> StubPartyService:
        return parties

    def _ledgers(_session: object) -> StubLedgerService:
        return ledgers

    monkeypatch.setattr("app.api.pallet_ledgers.PartyService", _parties)
    monkeypatch.setattr("app.api.pallet_ledgers.PalletLedgerService", _ledgers)

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), counterpart, ledgers
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_migration_501_creates_pallet_ledger_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/501_pallet_ledger.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "501_pallet_ledger"' in source
    assert 'down_revision: str | None = "500_shipment_fx_anchor_dates"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "pallet_ledger_tenant_isolation" in source
    assert "fk_pallet_ledger_party" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source


def test_pallet_ledger_service_does_not_import_parents() -> None:
    service = (
        _ROOT / "backend/app/services/pallet_ledgers/pallet_ledger_service.py"
    ).read_text(encoding="utf-8")
    for banned in (
        "pallet_balances",
        "charges",
        "shipments",
        "parties",
        "httpx",
        "float(",
    ):
        assert banned not in service


def test_importlinter_lists_pallet_ledgers_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.pallet_ledgers" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.pallet_ledgers" in forbidden
    assert "app.models.pallet_ledger" in forbidden


def test_fga_source_declares_pallet_ledger_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_pallet_ledgers: member" in source


def test_generated_api_types_include_pallet_ledger() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "PalletLedgerResponse" in source
    assert "PalletLedgerCreate" in source


def test_authorization_model_grants_pallet_ledgers_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_pallet_ledgers"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


def test_domain_delta_count_allows_negative() -> None:
    assert require_delta_count(-3) == -3
    assert require_delta_count(0) == 0
    with pytest.raises(InvalidPalletLedger, match="sztuk"):
        require_delta_count(1.5)
    with pytest.raises(InvalidPalletLedger, match="rodzaj"):
        require_ledger_pallet_kind("euro")


def test_http_create_and_list_pallet_ledger(catalog_client: object) -> None:
    client, counterpart, ledgers = catalog_client
    created = client.post(
        "/api/v1/pallet-ledgers",
        headers=bearer_auth_headers(),
        json={
            "party_id": str(counterpart.id),
            "movement_code": "issue_chep_01",
            "pallet_kind": "chep",
            "delta_count": -2,
            "source_ref": "fixture://pallet-ledger/a",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["delta_count"] == -2
    assert body["pallet_kind"] == "chep"
    assert len(ledgers.rows) == 1

    listed = client.get("/api/v1/pallet-ledgers", headers=bearer_auth_headers())
    assert listed.status_code == 200
    assert len(listed.json()) == 1


def test_http_rejects_unknown_kind_and_float(catalog_client: object) -> None:
    client, counterpart, _ledgers = catalog_client
    bad_kind = client.post(
        "/api/v1/pallet-ledgers",
        headers=bearer_auth_headers(),
        json={
            "party_id": str(counterpart.id),
            "movement_code": "bad_kind",
            "pallet_kind": "euro",
            "delta_count": 1,
            "source_ref": "fixture://pallet-ledger/b",
        },
    )
    assert bad_kind.status_code == 400
    assert "rodzaj" in bad_kind.json()["detail"]


def test_http_duplicate_code_returns_409(catalog_client: object) -> None:
    client, counterpart, _ledgers = catalog_client
    payload = {
        "party_id": str(counterpart.id),
        "movement_code": "dup_move",
        "pallet_kind": "lpr",
        "delta_count": 1,
        "source_ref": "fixture://pallet-ledger/c",
    }
    first = client.post(
        "/api/v1/pallet-ledgers",
        headers=bearer_auth_headers(),
        json=payload,
    )
    assert first.status_code == 201
    second = client.post(
        "/api/v1/pallet-ledgers",
        headers=bearer_auth_headers(),
        json={**payload, "source_ref": "fixture://pallet-ledger/d"},
    )
    assert second.status_code == 409
