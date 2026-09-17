# shipment_monitoring_filing (C1)

## Zakres
- Tabela `shipment_monitoring_filing`: organization_id, filing_code, status_kind (`en`|`uss`|`epo`|`other`), source_ref, created_at.
- Append-only. RLS FORCE.
- API GET/POST `/shipment-monitoring-filings`. OpenFGA `can_manage_shipment_monitoring_filings`.
- UI `/shipment-monitoring-filings`.

## Poza
- live PUESC / książka EN+USS+EPO silnik / `postal_epo` / XML SENT / kwota
