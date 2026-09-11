from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.sla_clause import parse_sla_clause_row
from app.main import app
from app.models.sla_clause import SlaClause
from tests.http_auth import bearer_auth_headers

_FORBIDDEN = ("shipment_id", "amount", "penalty_ciphertext", "currency")


class PermitSlaClauseAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemorySlaClauseDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.clauses: list[SlaClause] = []
        self.known_contract: UUID | None = None

    async def list_clauses(self) -> list[SlaClause]:
        return list(self.clauses)

    async def persist_sla_clause(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        customer_contract_id: object,
        clause_code: object,
        metric_kind: object,
        threshold_label: object,
        source_ref: object,
    ) -> SlaClause:
        packed = parse_sla_clause_row(
            customer_contract_id=customer_contract_id,
            clause_code=clause_code,
            metric_kind=metric_kind,
            threshold_label=threshold_label,
            source_ref=source_ref,
        )
        if self.known_contract is None or packed[0] != self.known_contract:
            raise ResourceNotFound("nieznana umowa")
        row = SlaClause(
            id=uuid4(),
            organization_id=organization_id,
            customer_contract_id=packed[0],
            clause_code=packed[1],
            metric_kind=packed[2],
            threshold_label=packed[3],
            source_ref=packed[4],
            created_by=user_id,
        )
        self.clauses.append(row)
        return row


@pytest.fixture
def sla_clause_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemorySlaClauseDesk(object())
    desk.known_contract = uuid4()

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr("app.api.sla_clauses.SlaClauseService", lambda _s: desk)
    set_authz_checker(PermitSlaClauseAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(desk: InMemorySlaClauseDesk, **extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "customer_contract_id": str(desk.known_contract),
        "clause_code": "sla_otif_01",
        "metric_kind": "otif",
        "threshold_label": "OTIF >= 95%",
        "source_ref": "fixture://sla-clause/pl-1",
    }
    body.update(extra)
    return body


def test_post_sla_clause_persists_row(sla_clause_http: object) -> None:
    client, desk = sla_clause_http
    response = client.post(
        "/api/v1/sla-clauses",
        headers=bearer_auth_headers(),
        json=_payload(desk),
    )
    assert response.status_code == 201
    body = response.json()
    assert body["clause_code"] == "sla_otif_01"
    assert body["metric_kind"] == "otif"
    assert body["threshold_label"] == "OTIF >= 95%"
    assert len(desk.clauses) == 1


def test_post_sla_clause_rejects_bad_metric(sla_clause_http: object) -> None:
    client, desk = sla_clause_http
    response = client.post(
        "/api/v1/sla-clauses",
        headers=bearer_auth_headers(),
        json=_payload(desk, metric_kind="ebitda"),
    )
    assert response.status_code == 400
    assert "metryka" in response.json()["detail"]


def test_post_sla_clause_rejects_extra_forbid(sla_clause_http: object) -> None:
    client, desk = sla_clause_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/sla-clauses",
            headers=bearer_auth_headers(),
            json=_payload(desk, **{field: "x"}),
        )
        assert response.status_code == 422, field


def test_get_sla_clauses_lists_tenant_rows(sla_clause_http: object) -> None:
    client, desk = sla_clause_http
    client.post(
        "/api/v1/sla-clauses",
        headers=bearer_auth_headers(),
        json=_payload(desk),
    )
    response = client.get("/api/v1/sla-clauses", headers=bearer_auth_headers())
    assert response.status_code == 200
    assert len(response.json()) == 1
