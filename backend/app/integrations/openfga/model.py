from openfga_sdk import (
    Metadata,
    ObjectRelation,
    RelationMetadata,
    RelationReference,
    TypeDefinition,
    Userset,
    WriteAuthorizationModelRequest,
)


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
                    "can_list_users": Userset(
                        computed_userset=ObjectRelation(object="", relation="member"),
                    ),
                    "can_manage_table_views": Userset(
                        computed_userset=ObjectRelation(object="", relation="member"),
                    ),
                    "can_review_extractions": Userset(
                        computed_userset=ObjectRelation(object="", relation="reviewer"),
                    ),
                    "can_manage_charge_codes": Userset(
                        computed_userset=ObjectRelation(object="", relation="member"),
                    ),
                    "can_manage_rate_lines": Userset(
                        computed_userset=ObjectRelation(object="", relation="member"),
                    ),
                    "can_manage_charges": Userset(
                        computed_userset=ObjectRelation(object="", relation="member"),
                    ),
                    "can_manage_quotations": Userset(
                        computed_userset=ObjectRelation(object="", relation="member"),
                    ),
                    "can_manage_organization_settings": Userset(
                        computed_userset=ObjectRelation(object="", relation="member"),
                    ),
                    "can_manage_geography": Userset(
                        computed_userset=ObjectRelation(object="", relation="member"),
                    ),
                    "can_manage_parties": Userset(
                        computed_userset=ObjectRelation(object="", relation="member"),
                    ),
                    "can_manage_commodity_codes": Userset(
                        computed_userset=ObjectRelation(object="", relation="member"),
                    ),
                    "can_manage_nbp_rates": Userset(
                        computed_userset=ObjectRelation(object="", relation="member"),
                    ),
                    "can_manage_dangerous_goods": Userset(
                        computed_userset=ObjectRelation(object="", relation="member"),
                    ),
                    "can_manage_networks": Userset(
                        computed_userset=ObjectRelation(object="", relation="member"),
                    ),
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
