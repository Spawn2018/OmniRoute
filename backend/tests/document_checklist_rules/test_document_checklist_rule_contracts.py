from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_checklist_service_does_not_import_parents() -> None:
    service = (
        _SERVICES / "document_checklist_rules" / "document_checklist_rule_service.py"
    ).read_text(encoding="utf-8")
    assert "app.services.shipments" not in service
    assert "app.services.shipment_documents" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_document_checklist_rules_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.document_checklist_rules" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.document_checklist_rules" in forbidden
    assert "app.models.document_checklist_rule" in forbidden


def test_generated_api_types_include_document_checklist_rule() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "DocumentChecklistRuleResponse" in source
    assert "DocumentChecklistRuleCreate" in source
