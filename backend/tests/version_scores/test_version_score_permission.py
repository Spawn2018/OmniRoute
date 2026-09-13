from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.api.deps import set_authz_checker
from app.main import app
from tests.http_auth import bearer_auth_headers

_DENIED = "Brak uprawnienia can_manage_version_scores na organization"


class DenyVersionScoreAuthz:
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


def test_version_score_get_is_forbidden_without_permission() -> None:
    set_authz_checker(DenyVersionScoreAuthz())
    response = TestClient(app).get(
        "/api/v1/version-scores",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 403
    assert response.json()["detail"] == _DENIED


def test_fga_source_declares_version_score_relation() -> None:
    source = (Path(__file__).resolve().parents[3] / "authz" / "model.fga").read_text(
        encoding="utf-8",
    )
    assert "can_manage_version_scores: member" in source
