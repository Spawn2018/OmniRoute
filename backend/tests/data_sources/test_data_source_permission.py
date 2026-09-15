from pathlib import Path

from app.integrations.openfga.model import authorization_model_request

_ROOT = Path(__file__).resolve().parents[3]


def test_fga_source_declares_data_source_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_data_sources: member" in source


def test_authorization_model_grants_data_sources_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_data_sources"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"
