from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.api.deps import set_authz_checker
from app.main import app
from tests.http_auth import bearer_auth_headers

_DENIED = "Brak uprawnienia can_manage_counterfactual_runs na organization"

_CALLS = (
    ("GET", "/api/v1/counterfactual-runs", None, None),
    ("GET", "/api/v1/what-if-replays", None, None),
    (
        "POST",
        "/api/v1/counterfactual-runs",
        None,
        {
            "run_code": "fuel_spike",
            "plan_snapshot_id": "00000000-0000-0000-0000-000000000001",
            "baseline_label": "plan z wczoraj",
            "levers_label": "paliwo w gore",
            "result_label": "eta plus dwie godziny",
            "source_ref": "fixture://counterfactual-run/a",
        },
    ),
)


class DenyCounterfactualAuthz:
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
def test_counterfactual_run_endpoints_are_forbidden_without_permission(
    method: str,
    path: str,
    params: dict[str, str] | None,
    json_body: dict[str, object] | None,
) -> None:
    set_authz_checker(DenyCounterfactualAuthz())
    response = TestClient(app).request(
        method,
        path,
        headers=bearer_auth_headers(),
        params=params,
        json=json_body,
    )
    assert response.status_code == 403
    assert response.json()["detail"] == _DENIED


def test_fga_source_declares_counterfactual_run_relation() -> None:
    source = (Path(__file__).resolve().parents[3] / "authz" / "model.fga").read_text(
        encoding="utf-8",
    )
    assert "can_manage_counterfactual_runs: member" in source
