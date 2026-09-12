from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.api.deps import set_authz_checker
from app.main import app
from tests.http_auth import bearer_auth_headers

_DENIED = "Brak uprawnienia can_manage_mail_accept_marks na organization"

_CALLS = (

    ("GET", "/api/v1/mail-accept-marks", None, None),

    (

        "POST",

        "/api/v1/mail-accept-marks",

        None,

        {

            "mark_code": "mac_mailto_01",

            "accept_kind": "mailto",

            "source_ref": "fixture://mail-accept-mark/a",

        },

    ),

)

class DenyTermsAiAuthz:

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

def test_mail_accept_mark_endpoints_are_forbidden_without_permission(

    method: str,

    path: str,

    params: dict[str, str] | None,

    json_body: dict[str, object] | None,

) -> None:

    set_authz_checker(DenyTermsAiAuthz())

    response = TestClient(app).request(

        method,

        path,

        headers=bearer_auth_headers(),

        params=params,

        json=json_body,

    )

    assert response.status_code == 403

    assert response.json()["detail"] == _DENIED

def test_fga_source_declares_mail_accept_mark_relation() -> None:

    source = (Path(__file__).resolve().parents[3] / "authz" / "model.fga").read_text(

        encoding="utf-8",

    )

    assert "can_manage_mail_accept_marks: member" in source

