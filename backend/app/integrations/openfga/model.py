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
                    "can_list_users": Userset(
                        computed_userset=ObjectRelation(object="", relation="member"),
                    ),
                    "can_manage_table_views": Userset(
                        computed_userset=ObjectRelation(object="", relation="member"),
                    ),
                },
                metadata=Metadata(
                    relations={
                        "member": RelationMetadata(
                            directly_related_user_types=[RelationReference(type="user")],
                        ),
                    },
                ),
            ),
        ],
    )
