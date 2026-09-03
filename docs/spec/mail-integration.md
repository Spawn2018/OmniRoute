# M-32 integracja pocztowa — tablica znanych adresów + inbound_message

**Moduł żywy:** M-32  
**Plaster:** **80.0** (zamknięty) · 78.0 Graph · 66.0 extract · 65.0 resolve · 64.0 tabela · 25.0 tablica adresów  
**Status:** operator zapisuje fixture albo ingest `graph://` / `imap://` + `external_id`, dopina nadawcę, wysyła treść na HITL. Nie live skrzynka. Nie send. Nie blob.

Delta: [80.0](../deltas/archived/80.0-imap-ingest.md) · [78.0](../deltas/archived/78.0-graph-ingest.md) · [66.0](../deltas/archived/66.0-inbound-extract.md) · [65.0](../deltas/archived/65.0-inbound-resolve-email.md) · [64.0](../deltas/archived/64.0-inbound-message.md) · [25.0](../deltas/archived/25.0-mail-integration.md).

## 25.0 tablica odczytu na `/mail`

### Zakres

- Ekran `/mail`: wybór `party` + lista `party_email_domain` i `party_contact.email` + `resolve_email`
- Zero IMAP. Zero SMTP. Zero sekretu skrzynki
- Zero N+1 po całym katalogu

### Poza 25.0

Live IMAP · magazyn sekretów tenanta · Outlook (M-33) · powiadomienia (M-34) · auto-INSERT kontaktu · LLM

## 64.0 inbound_message

### Zakres

- Tabela `inbound_message` per tenant: `source_ref`, `from_address`, `subject`, `body_text`, `status = draft`
- RLS FORCE. OpenFGA `can_manage_inbound_messages` = member
- `GET/POST /inbound-messages`. Zapis tylko z `fixture://` albo `synth://`
- Ten sam `/mail`: lista DataTableShell + formularz fixture

### Poza 64.0

extract z treści (S3) · IMAP · Graph · send · załączniki blob · outbox

## 65.0 resolve_email na wiadomości

### Zakres

- `inbound_message.party_id` nullable, FK tenanta (`organization_id` + `party_id`)
- `POST /inbound-messages/{id}/resolve-email` — istniejący matcher domeny
- `/mail`: przycisk „Dopasuj nadawcę”
- BC inbound nie importuje parties; API składa

### Poza 65.0

extract (S3) · IMAP · Graph · auto przy INSERT · INSERT kontaktu

## 66.0 extract HITL z treści

### Zakres

- `POST /inbound-messages/{id}/extract` — temat + treść → `extract_to_draft`; `source_ref` z wiersza
- Szkic na istniejącej kolejce `/extractions`. Accept zostaje tam. Brak `rate_line` na tym endpoincie
- `/mail`: przycisk „Extract HITL”
- API składa BC; ExtractionService nie importuje inbound

### Poza 66.0

załącznik blob · IMAP · Graph · auto-extract przy INSERT · RFQ (S4)

### HC

- Adresy kontaktów zostają w `party_contact` / `party_email_domain` (SQL).
- Wiadomość nie jest `party`. Lookup nie zapisuje karty.
- LLM nie czyta skrzynki i nie liczy.
- `charge` zostaje prawdą o marży.
- ExtractionService nie importuje inbound_messages

## 78.0 ingest Graph

### Zakres

- `inbound_message.external_id` nullable; unikat `(organization_id, external_id)` gdy niepuste
- CHECK `source_ref` dopuszcza `graph://` obok `fixture://` / `synth://`
- `POST /inbound-messages/ingest-graph` — ten sam `external_id` = ten sam wiersz
- `/mail`: formularz ingest (nie `CatalogCreateForm`). Zwykły POST zostaje `fixture://` | `synth://`
- Serwis nie woła Microsoft Graph i nie trzyma tokenu

### Poza 78.0

live HTTP Graph · sekret tenanta · IMAP (S17) · send (S18) · outbox (S16) · blob

## 80.0 ingest skrzynki

### Zakres

- CHECK `source_ref` dopuszcza `imap://`
- `POST /inbound-messages/ingest-imap` — ten sam `external_id` = ten sam wiersz
- `/mail`: formularz ingest skrzynki. API składa outbox jak przy Graph
- Serwis nie zawiera słowa `imap` i nie woła skrzynki

### Poza 80.0

live IMAP · EmailEngine · sekret · send (S18)
