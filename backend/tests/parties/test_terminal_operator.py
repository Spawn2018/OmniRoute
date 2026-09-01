from app.api.terminals import TerminalCreate, TerminalResponse


def test_terminal_create_dto_accepts_operator_party_id() -> None:
    assert "operator_party_id" in TerminalCreate.model_fields
    assert "operator_name" in TerminalCreate.model_fields


def test_terminal_response_dto_exposes_operator_party_id() -> None:
    assert "operator_party_id" in TerminalResponse.model_fields
    assert "operator_name" in TerminalResponse.model_fields
