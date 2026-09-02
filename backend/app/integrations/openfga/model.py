from openfga_sdk import (
    Metadata,
    ObjectRelation,
    RelationMetadata,
    RelationReference,
    TypeDefinition,
    Userset,
    WriteAuthorizationModelRequest,
)


def _member() -> Userset:
    return Userset(computed_userset=ObjectRelation(object="", relation="member"))


def _reviewer() -> Userset:
    return Userset(computed_userset=ObjectRelation(object="", relation="reviewer"))


def authorization_model_request() -> WriteAuthorizationModelRequest:
    """Model odpowiadający authz/model.fga — źródło prawdy dla write_authorization_model."""
    return WriteAuthorizationModelRequest(
        schema_version="1.1",
        type_definitions=[
            TypeDefinition(type="user"),
            TypeDefinition(
                type="organization",
                relations={
                    "member": Userset(this={}),
                    "reviewer": Userset(this={}),
                    "can_list_users": _member(),
                    "can_manage_table_views": _member(),
                    "can_review_extractions": _reviewer(),
                    "can_manage_charge_codes": _member(),
                    "can_manage_rate_lines": _member(),
                    "can_manage_charges": _member(),
                    "can_manage_quotations": _member(),
                    "can_manage_organization_settings": _member(),
                    "can_manage_geography": _member(),
                    "can_manage_parties": _member(),
                    "can_manage_commodity_codes": _member(),
                    "can_manage_nbp_rates": _member(),
                    "can_manage_dangerous_goods": _member(),
                    "can_manage_networks": _member(),
                    "can_manage_inbound_messages": _member(),
                    "can_manage_customer_rfqs": _member(),
                },
                metadata=Metadata(
                    relations={
                        "member": RelationMetadata(
                            directly_related_user_types=[RelationReference(type="user")],
                        ),
                        "reviewer": RelationMetadata(
                            directly_related_user_types=[RelationReference(type="user")],
                        ),
                    },
                ),
            ),
        ],
    )
