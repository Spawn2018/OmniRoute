from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.api.deps import set_authz_checker
from app.main import app
from tests.http_auth import bearer_auth_headers

_DENIED = "Brak uprawnienia can_manage_benefit_ledgers na organization"

_CALLS = (
    ("GET", "/api/v1/benefit-ledgers", None, None),
    (
        "POST",
        "/api/v1/benefit-ledgers",
        None,
        {
            "benefit_code": "dock_save",
            "method_label": "porownanie z wczorajszym charge",
            "hours_saved": "2.5",
            "saved_amount": "150",
            "saved_currency": "EUR",
            "source_ref": "fixture://benefit-ledger/a",
        },
    ),
)


class DenyBenefitLedgerAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return False


@pytest.fixture(autouse=True)
def _reset_authz() -> object:
    set_authz_checker(None)
    yield
    set_authz_checker(None)


@pytest.mark.parametrize(("method", "path", "params", "json_body"), _CALLS)
def test_benefit_ledger_endpoints_are_forbidden_without_permission(
    method: str,
    path: str,
    params: dict[str, str] | None,
    json_body: dict[str, object] | None,
) -> None:
    set_authz_checker(DenyBenefitLedgerAuthz())
    response = TestClient(app).request(
        method,
        path,
        headers=bearer_auth_headers(),
        params=params,
        json=json_body,
    )
    assert response.status_code == 403
    assert response.json()["detail"] == _DENIED


def test_fga_source_declares_benefit_ledger_relation() -> None:
    source = (Path(__file__).resolve().parents[3] / "authz" / "model.fga").read_text(
        encoding="utf-8",
    )
    assert "can_manage_benefit_ledgers: member" in source
