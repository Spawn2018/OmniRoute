from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.api.deps import set_authz_checker
from app.main import app
from tests.http_auth import bearer_auth_headers

_DENIED = "Brak uprawnienia can_manage_label_parking_marks na organization"

_CALLS = (

    ("GET", "/api/v1/label-parking-marks", None, None),

    (

        "POST",

        "/api/v1/label-parking-marks",

        None,

        {

            "mark_code": "lp_secure_01",

            "parking_kind": "secure",

            "source_ref": "fixture://label-parking-mark/a",

        },

    ),

)





class DenyLabelParkingAuthz:

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

def test_label_parking_mark_endpoints_are_forbidden_without_permission(

    method: str,

    path: str,

    params: dict[str, str] | None,

    json_body: dict[str, object] | None,

) -> None:

    set_authz_checker(DenyLabelParkingAuthz())

    response = TestClient(app).request(

        method,

        path,

        headers=bearer_auth_headers(),

        params=params,

        json=json_body,

    )

    assert response.status_code == 403

    assert response.json()["detail"] == _DENIED





def test_fga_source_declares_label_parking_mark_relation() -> None:

    source = (Path(__file__).resolve().parents[3] / "authz" / "model.fga").read_text(

        encoding="utf-8",

    )

    assert "can_manage_label_parking_marks: member" in source

