# BC shipment_monitoring_filing (C1)

HITL katalog stancji zgloszenia SENT/BDO per tenant. filing_code +
status_kind open|filed|closed|other + source_ref. Nie live PUESC. Nie XML.

## Dozwolone zależności
- pp.models.shipment_monitoring_filing
- pp.repositories.shipment_monitoring_filings
- pp.domain

## Zakaz
- import innych BC services (monitoring_schemes, shipments, charges, extraction)
- zapis monitoring_scheme / shipment / charge / extraction_draft
- live PUESC / SENT XML / SENT-GEO / geo_required
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
