# Spec: otif_mark (CT3)

**Moduł żywy:** CT3 (`otif_mark` HITL katalog zakresu)

## 280.0 katalog zakresu OTIF

- Tabela `otif_mark` per tenant: `mark_code`, `scope_kind` (`pickup`|`delivery`|`sku`), `source_ref`
- POST INSERT / GET lista; brak UPDATE/DELETE
- Nie OTIF%; nie SQL na stop/SKU; nie kwota; nie FK shipment
