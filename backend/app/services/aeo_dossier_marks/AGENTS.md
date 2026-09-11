# BC aeo_dossier_mark (G14)

HITL katalog dossier AEO per tenant. mark_code + dossier_kind aeo|authorised|other + source_ref. Nie party_document. Nie scoring.

## Dozwolone zależności
- `app.models.aeo_dossier_mark`
- `app.repositories.aeo_dossier_marks`
- `app.domain`

## Zakaz
- import innych BC services (party_documents, parties, charges, extraction)
- zapis `party_document` / `party` / `charge` / `extraction_draft`
- zestaw C8 / scoring osoby / amount / bytes / float / kwota
- HTTP
- UPDATE / DELETE wiersza
