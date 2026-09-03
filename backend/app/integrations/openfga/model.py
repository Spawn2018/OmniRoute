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


def _organization_relations() -> dict[str, Userset]:
    return {
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
        "can_manage_operator_decisions": _member(),
        "can_manage_operator_notices": _member(),
        "can_manage_mail_drafts": _member(),
        "can_manage_outbox_events": _member(),
        "can_manage_shipments": _member(),
        "can_manage_tracking": _member(),
        "can_manage_shipment_documents": _member(),
        "can_manage_exceptions": _member(),
        "can_manage_edi_messages": _member(),
        "can_manage_sales_invoices": _member(),
        "can_manage_quote_invoice_settlements": _member(),
        "can_manage_bank_payments": _member(),
        "can_manage_money_costs": _member(),
        "can_manage_fx_differences": _member(),
    }


def _organization_relation_metadata() -> dict[str, RelationMetadata]:
    user_type = [RelationReference(type="user")]
    return {
        "member": RelationMetadata(directly_related_user_types=user_type),
        "reviewer": RelationMetadata(directly_related_user_types=user_type),
    }


def authorization_model_request() -> WriteAuthorizationModelRequest:
    """Model odpowiadający authz/model.fga — źródło prawdy dla write_authorization_model."""
    return WriteAuthorizationModelRequest(
        schema_version="1.1",
        type_definitions=[
            TypeDefinition(type="user"),
            TypeDefinition(
                type="organization",
                relations=_organization_relations(),
                metadata=Metadata(relations=_organization_relation_metadata()),
            ),
        ],
    )
